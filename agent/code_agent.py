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
    MANIM_RULES_FILE,
)
from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm
from .ledger import Ledger


CODE_AGENT_DEBUG = os.getenv("CODE_AGENT_DEBUG")

# ── Self-reflection ────────────────────────────────────────────────────────────
_MANIM_RULES: str = ""  # module-level cache; loaded once on first use


def _load_manim_rules() -> str:
    global _MANIM_RULES
    if not _MANIM_RULES and MANIM_RULES_FILE.exists():
        _MANIM_RULES = MANIM_RULES_FILE.read_text(encoding="utf-8")
    return _MANIM_RULES


_REFLECT_SYSTEM = (
    "You are a strict Manim code reviewer. "
    "Analyze the Python code against the rules provided. "
    "List only CLEAR violations as concise bullet points (one per line). "
    "If there are NO violations, respond with exactly: OK"
)


async def _self_reflect_and_fix(
    code: str,
    original_messages: list,
    code_llm,
    reviewer_llm,
    step_id: str,
) -> str:
    """
    Ask a cheap reviewer LLM to check `code` against manim_rules.md.
    If violations are found, regenerate once using the original prompt + violations.
    Returns (possibly improved) code. Always degrades gracefully on failure.
    """
    rules = _load_manim_rules()
    if not rules or not code.strip():
        return code

    try:
        review_prompt = (
            f"RULES:\n{rules}\n\n"
            f"CODE TO REVIEW:\n```python\n{code}\n```\n\n"
            "List any rule violations with brief explanation. "
            "If no violations, respond with exactly: OK"
        )
        review_resp = await reviewer_llm.ainvoke([
            SystemMessage(content=_REFLECT_SYSTEM),
            HumanMessage(content=review_prompt),
        ])
        violations = _content_to_str(
            review_resp.content if hasattr(review_resp, "content") else review_resp
        ).strip()

        if not violations or violations.upper().startswith("OK"):
            print(f"   [code_agent] Self-review OK for step '{step_id}'")
            return code

        # Count bullet points for the log line
        n = sum(1 for ln in violations.splitlines() if ln.strip()[:1] in "-•*" or ln.strip()[:1].isdigit())
        print(f"   [code_agent] Self-review: {n or 'some'} violation(s) in '{step_id}' — regenerating...")

        # Re-invoke the code LLM with violations appended to the original user message
        fix_note = (
            "\n\nSELF-REVIEW FOUND VIOLATIONS — your new code MUST fix ALL of these:\n"
            + violations
        )
        augmented = list(original_messages)
        augmented[-1] = HumanMessage(content=augmented[-1].content + fix_note)

        regen_resp = await code_llm.ainvoke(augmented)
        regen_raw = _content_to_str(
            regen_resp.content if hasattr(regen_resp, "content") else regen_resp
        )
        regen_code = _extract_python_code(regen_raw)
        if regen_code.strip():
            return regen_code
        print(f"   [code_agent] Regeneration empty for step '{step_id}' — keeping original")
        return code

    except Exception as exc:
        print(f"   [code_agent] Self-review skipped for step '{step_id}': {exc}")
        return code


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
    pseudocode_text: str = "",
    code_examples_text: str = "",
    reviewer_llm=None,
) -> tuple:
    """Generate Manim code for a single step (async). Returns (step_id, code)."""
    pseudocode_section = (
        f"\nSCENE PSEUDO-CODE OUTLINE (follow this structure):\n{pseudocode_text}\n"
        if pseudocode_text.strip() else ""
    )
    code_examples_section = (
        f"\nRELEVANT MANIM CODE EXAMPLES (use as reference):\n{code_examples_text}\n"
        if code_examples_text.strip() else ""
    )
    user_prompt = user_template.format(
        animation_prompt=description,
        ledger_text=ledger_text,
        layout_spec=layout_spec_text,
        pseudocode_section=pseudocode_section,
        code_examples_section=code_examples_section,
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

    # Self-reflection: ask reviewer LLM to check the code, regenerate if violations found
    if reviewer_llm is not None and code.strip():
        code = await _self_reflect_and_fix(code, messages, llm, reviewer_llm, step_id)

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
    pseudocode: Optional[Dict[str, str]] = None,
    code_examples: str = "",
) -> Dict[str, str]:
    """Run code generation for all steps sequentially to stay within TPM rate limits."""
    system_prompt, user_template = _load_code_prompts()
    llm = get_llm(stage="code", temperature=0, max_tokens=4096)
    # Cheap chat model used as reviewer (not the reasoning model — just rule-checking)
    reviewer_llm = get_llm(stage="planner", temperature=0, max_tokens=512)
    layout_specs = layout_specs or {}
    pseudocode = pseudocode or {}
    code_results = {}
    for step_id, data in step_results.items():
        try:
            _, code = await _generate_code_for_one_step(
                llm, step_id, data["description"],
                system_prompt, user_template,
                ledger_text,
                layout_specs.get(step_id, ""),
                pseudocode.get(step_id, ""),
                code_examples,
                reviewer_llm=reviewer_llm,
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
    pseudocode: Optional[Dict[str, str]] = None,
    code_examples: str = "",
) -> Dict[str, Any]:
    """
    step_results:  {step_id: {"description": "..."}}.
    ledger:        final ledger dict from step_agent (notation, visual_style, objects).
    layout_specs:  {step_id: layout_spec_prompt_text} from layout_engine.
    pseudocode:    {step_id: outline_text} from pseudocode_agent.
    code_examples: retrieved Manim code snippets from code_retrieval.

    Generates code for all steps sequentially, then writes one .py per step.
    Returns {"status": "success", "code_results": {...}}.
    """
    ledger_obj = Ledger.from_dict(ledger) if ledger else Ledger()
    ledger_text = ledger_obj.to_text()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        code_results = loop.run_until_complete(
            _generate_code_parallel_async(
                step_results, ledger_text, layout_specs, pseudocode, code_examples
            )
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
