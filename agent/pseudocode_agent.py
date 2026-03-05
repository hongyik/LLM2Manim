"""
Pseudo-code Generator: produces a structured per-scene animation outline.

For each step, calls an LLM to generate a blueprint (objects, animations, voiceover beats)
that is injected into the Manim code generation prompt. This bridges the prose description
and the final Python code, reducing LLM hallucinations and improving code quality.

Processing is sequential (TPM rate limits).
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config
from .llm import get_llm
from .ledger import Ledger

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_SYSTEM_PROMPT_FILE = PROMPTS_DIR / "pseudocode_system_prompt.txt"


def _load_system_prompt() -> str:
    if _SYSTEM_PROMPT_FILE.exists():
        return _SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()
    # Inline fallback (should not happen in normal usage)
    return (
        "You are a Manim animation architect. Produce a concise structured outline "
        "(objects, animations, voiceover beats) for the given scene. "
        "Do NOT write full Python code."
    )


def _build_user_message(
    step_id: str,
    step_goal: str,
    description: str,
    concept_context: str,
    code_examples: str,
    ledger_text: str,
) -> str:
    parts = [
        f"Scene ID: {step_id}",
        f"Goal: {step_goal}",
        "",
        "Animation Description:",
        description,
    ]
    if ledger_text.strip():
        parts += ["", "Consistency Ledger (reuse these symbols/colors/names):", ledger_text]
    if concept_context.strip():
        parts += ["", "Relevant Concept Context (from textbooks):", concept_context]
    if code_examples.strip():
        parts += ["", "Relevant Manim Code Examples (reference these patterns):", code_examples]
    parts += ["", "Now write the structured pseudo-code outline for this scene."]
    return "\n".join(parts)


def generate_pseudocode(
    step_results: Dict[str, Any],
    concept_context: str = "",
    code_examples: str = "",
    ledger: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Generate a structured per-scene outline for each step.
    Returns {step_id: outline_text}.
    Processes steps sequentially to respect TPM rate limits.
    """
    if not step_results:
        return {}

    system_prompt = _load_system_prompt()
    ledger_obj = Ledger.from_dict(ledger) if ledger else Ledger()
    ledger_text = ledger_obj.to_text()
    llm = get_llm(stage="pseudocode", temperature=0.4, max_tokens=1024)

    pseudocode: Dict[str, str] = {}

    for step_id, data in step_results.items():
        description = data.get("description", "")
        step_goal = data.get("goal", step_id)
        print(f"   [pseudocode] Generating outline for {step_id}...")

        try:
            user_msg = _build_user_message(
                step_id, step_goal, description,
                concept_context, code_examples, ledger_text,
            )
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_msg),
            ]
            response = llm.invoke(messages)
            raw = response.content if hasattr(response, "content") else str(response)
            if isinstance(raw, list):
                raw = "\n".join(
                    b.get("text", "") if isinstance(b, dict) else str(b) for b in raw
                )
            outline = raw.strip()
            pseudocode[step_id] = outline
        except Exception as exc:
            print(f"   [pseudocode] ERROR for step '{step_id}': {type(exc).__name__}: {exc}")
            pseudocode[step_id] = ""

    # Save for debugging
    try:
        out_dir = config.OUTPUT_DIR
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "pseudocode.json").write_text(
                json.dumps(pseudocode, indent=2, ensure_ascii=False), encoding="utf-8"
            )
    except Exception:
        pass

    return pseudocode
