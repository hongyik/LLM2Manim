"""
Code agent: generate Manim code for each step description.
Runs all steps in parallel (simultaneously) since each step only needs its own description.
The final ledger from the step agent is injected into every code generation call
so all scenes use consistent symbols, colors, and object names.
"""
import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    OUTPUT_DIR,
    SYSTEM_PROMPT_CODE_FILE,
    USER_PROMPT_CODE_TEMPLATE_FILE,
    CODE_PATTERNS_FILE,
)
from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm
from .ledger import Ledger


def _load_code_prompts() -> tuple:
    with open(SYSTEM_PROMPT_CODE_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(USER_PROMPT_CODE_TEMPLATE_FILE, "r", encoding="utf-8") as f:
        user_template = f.read()
    # Append verified working patterns as few-shot reference (if the file exists)
    if CODE_PATTERNS_FILE.exists():
        patterns = CODE_PATTERNS_FILE.read_text(encoding="utf-8")
        system_prompt = (
            system_prompt.rstrip()
            + "\n\n"
            + "🔹 **Verified working code patterns — copy these idioms exactly:**\n"
            + "```python\n"
            + patterns
            + "\n```"
        )
    return system_prompt, user_template


def _extract_python_code(raw: str) -> str:
    """Extract Python from LLM output and strip any leftover markdown."""
    raw = raw.strip()
    m = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
    code = m.group(1).strip() if m else raw
    # Strip leading ```python or ``` and trailing ``` if still present
    code = re.sub(r"^\s*```(?:python)?\s*\n?", "", code)
    code = re.sub(r"\n?```\s*$", "", code)
    return code.strip()


def _sanitize_scene_code(code: str) -> str:
    """Remove stray markdown and normalize Kokoro to: from kokoro_mv import KokoroService; KokoroService(voice='af_sarah', lang='en-us')."""
    lines = code.splitlines()
    if lines and lines[0].strip() == "```python":
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    code = "\n".join(lines)
    # Use correct Kokoro import and API (no model_path/voices_path)
    code = code.replace("from kokoro_mv.koko import KokoroService", "from kokoro_mv import KokoroService")
    # Replace any KokoroService(...) inside set_speech_service with the correct call
    code = re.sub(
        r"self\.set_speech_service\s*\(\s*KokoroService\s*\([^)]*\)\s*\)",
        "self.set_speech_service(KokoroService(voice=\"af_sarah\", lang=\"en-us\"))",
        code,
        count=1,
        flags=re.DOTALL,
    )
    # Fix common manim API mistakes
    # camera_frame was renamed to camera.frame in manim >= 0.17
    code = code.replace(".camera_frame", ".camera.frame")
    # Rotate/animation 'radians=' kwarg should be 'angle='
    code = re.sub(r"\bradians\s*=", "angle=", code)
    # Upgrade GenScene(VoiceoverScene) -> GenScene(ThreeDScene, VoiceoverScene)
    code = re.sub(
        r"\bclass\s+GenScene\s*\(\s*VoiceoverScene\s*\)",
        "class GenScene(ThreeDScene, VoiceoverScene)",
        code,
    )
    return code.strip()


async def _generate_code_for_one_step(
    llm,
    step_id: str,
    description: str,
    system_prompt: str,
    user_template: str,
    ledger_text: str,
) -> tuple:
    """Generate Manim code for a single step (async). Returns (step_id, code)."""
    user_prompt = user_template.format(
        animation_prompt=description,
        ledger_text=ledger_text,
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = await llm.ainvoke(messages)
    raw = response.content if hasattr(response, "content") else str(response)
    return step_id, _extract_python_code(raw)


async def _generate_code_parallel_async(
    step_results: Dict[str, Any],
    ledger_text: str,
) -> Dict[str, str]:
    """Run code generation for all steps in parallel."""
    system_prompt, user_template = _load_code_prompts()
    llm = get_llm(stage="code", temperature=0, max_tokens=4096)
    tasks = [
        _generate_code_for_one_step(
            llm, step_id, data["description"], system_prompt, user_template, ledger_text
        )
        for step_id, data in step_results.items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    code_results = {}
    for r in results:
        if isinstance(r, Exception):
            continue
        step_id, code = r
        code_results[step_id] = code
    return code_results


def generate_code_for_descriptions(
    step_results: Dict[str, Any],
    ledger: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    step_results: {step_id: {"description": "..."}}.
    ledger: final ledger dict from step_agent (notation, visual_style, objects, ...).

    Generates code for all steps in parallel using the ledger for consistency,
    then writes one .py per step.
    Returns {"status": "success", "code_results": {...}}.
    """
    ledger_obj = Ledger.from_dict(ledger) if ledger else Ledger()
    ledger_text = ledger_obj.to_text()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        code_results = loop.run_until_complete(
            _generate_code_parallel_async(step_results, ledger_text)
        )
    finally:
        loop.close()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for step_id, code in code_results.items():
        code = _sanitize_scene_code(code)
        file_name = f"{step_id.lower()}.py"
        (OUTPUT_DIR / file_name).write_text(code, encoding="utf-8")
    (OUTPUT_DIR / "generated_code.json").write_text(
        json.dumps(code_results, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {"status": "success", "code_results": code_results}
