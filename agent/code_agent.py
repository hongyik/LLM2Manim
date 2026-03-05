"""
Code agent: generate Manim code for each step description.
Runs all steps in parallel (simultaneously) since each step only needs its own description.
The final ledger from the step agent is injected into every code generation call
so all scenes use consistent symbols, colors, and object names.

This module also logs per-step diagnostics so we can debug empty/failed generations:
- For each step we print a short status line.
- If the LLM raw response is empty, we log a warning.
- If extracted Python code is empty but the raw response is not, we log a warning
  and (optionally) dump debug files when CODE_AGENT_DEBUG is set in the environment.
"""
import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
config.init_run_dir()
from config import (
    SYSTEM_PROMPT_CODE_FILE,
    USER_PROMPT_CODE_TEMPLATE_FILE,
    CODE_PATTERNS_FILE,
)
from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm
from .ledger import Ledger


CODE_AGENT_DEBUG = os.getenv("CODE_AGENT_DEBUG")


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


def _content_to_str(content) -> str:
    """Normalize LLM response content to a plain string.
    Newer OpenAI models can return content as a list of blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return str(content) if content is not None else ""


async def _generate_code_for_one_step(
    llm,
    step_id: str,
    description: str,
    system_prompt: str,
    user_template: str,
    ledger_text: str,
    layout_spec_text: str = "",
) -> tuple:
    """Generate Manim code for a single step (async). Returns (step_id, code)."""
    user_prompt = user_template.format(
        animation_prompt=description,
        ledger_text=ledger_text,
        layout_spec=layout_spec_text,
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = await llm.ainvoke(messages)
    raw = _content_to_str(response.content if hasattr(response, "content") else response)

    if not raw.strip():
        print(f"   [code_agent] WARNING: empty raw response for step '{step_id}'")
        return step_id, ""

    code = _extract_python_code(raw)
    if not code.strip():
        print(
            f"   [code_agent] WARNING: extracted empty code for step '{step_id}'. "
            f"Raw preview: {raw[:240]!r}"
        )

    if CODE_AGENT_DEBUG:
        try:
            debug_dir = config.OUTPUT_DIR / "code_agent_debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            (debug_dir / f"{step_id.lower()}_prompt.txt").write_text(
                json.dumps(
                    {
                        "step_id": step_id,
                        "description": description,
                        "ledger_text": ledger_text,
                        "layout_spec": layout_spec_text,
                        "user_prompt": user_prompt,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (debug_dir / f"{step_id.lower()}_raw.txt").write_text(
                raw, encoding="utf-8"
            )
            (debug_dir / f"{step_id.lower()}_code.txt").write_text(
                code, encoding="utf-8"
            )
        except Exception as exc:  # best-effort debug logging only
            print(f"   [code_agent] DEBUG write failed for step '{step_id}': {exc}")

    return step_id, code


async def _generate_code_parallel_async(
    step_results: Dict[str, Any],
    ledger_text: str,
    layout_specs: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Run code generation for all steps sequentially to stay within TPM rate limits."""
    system_prompt, user_template = _load_code_prompts()
    llm = get_llm(stage="code", temperature=0, max_tokens=4096)
    layout_specs = layout_specs or {}
    code_results = {}
    for step_id, data in step_results.items():
        try:
            _, code = await _generate_code_for_one_step(
                llm, step_id, data["description"],
                system_prompt, user_template,
                ledger_text, layout_specs.get(step_id, ""),
            )
            code_results[step_id] = code
        except Exception as exc:
            print(f"   [code_agent] ERROR for step '{step_id}': {type(exc).__name__}: {exc}")
            code_results[step_id] = ""
    return code_results


def generate_code_for_descriptions(
    step_results: Dict[str, Any],
    ledger: Optional[Dict[str, Any]] = None,
    layout_specs: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    step_results:  {step_id: {"description": "..."}}.
    ledger:        final ledger dict from step_agent (notation, visual_style, objects).
    layout_specs:  {step_id: layout_spec_prompt_text} from layout_engine.

    Generates code for all steps in parallel, then writes one .py per step.
    Returns {"status": "success", "code_results": {...}}.
    """
    ledger_obj = Ledger.from_dict(ledger) if ledger else Ledger()
    ledger_text = ledger_obj.to_text()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        code_results = loop.run_until_complete(
            _generate_code_parallel_async(step_results, ledger_text, layout_specs)
        )
    finally:
        loop.close()

    # Ensure run directory is initialized (important for direct calls from tests/scripts)
    if config.OUTPUT_DIR is None:
        config.init_run_dir()
    out_dir = config.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    for step_id, code in code_results.items():
        code = _sanitize_scene_code(code)
        file_name = f"{step_id.lower()}.py"
        (out_dir / file_name).write_text(code, encoding="utf-8")
    (out_dir / "generated_code.json").write_text(
        json.dumps(code_results, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {"status": "success", "code_results": code_results}
