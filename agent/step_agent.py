"""
Step agent: generate animation description for one step with full memory of previous steps
and a running consistency ledger.

Runs sequentially so each step receives:
  - Accumulated descriptions of all prior steps (memory)
  - The current state of the ledger (notation, style, objects, story, constraints)

Each step returns an updated ledger that the next step inherits.
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from langchain_core.messages import HumanMessage

from .llm import get_llm
from .ledger import Ledger


PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"

DESC_MARKER = "===DESCRIPTION==="
LEDGER_MARKER = "===LEDGER_UPDATES==="


def _load_step_prompt() -> str:
    with open(PROMPT_DIR / "step_with_memory_prompt.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def _format_plan_text(plan: List[Dict[str, str]]) -> str:
    return "\n".join(
        f"  {i+1}. [{s['id']}] {s['goal']}" for i, s in enumerate(plan)
    )


def _format_memory(step_descriptions: List[Dict[str, Any]]) -> str:
    if not step_descriptions:
        return "(This is the first step; no previous content yet.)"
    parts = []
    for i, s in enumerate(step_descriptions, 1):
        step_id = s.get("id", f"Step{i}")
        desc = s.get("description", "")
        parts.append(f"Step {i} [{step_id}]:\n{desc}")
    return "\n\n---\n\n".join(parts)


def _parse_step_response(raw: str) -> Tuple[str, dict]:
    """
    Split LLM output into (description, ledger_updates_dict).
    Expects the two-marker format from step_with_memory_prompt.txt.
    Falls back gracefully if markers are absent.
    """
    raw = raw.strip()
    if DESC_MARKER in raw and LEDGER_MARKER in raw:
        desc_start = raw.index(DESC_MARKER) + len(DESC_MARKER)
        ledger_start = raw.index(LEDGER_MARKER)
        description = raw[desc_start:ledger_start].strip()
        ledger_raw = raw[ledger_start + len(LEDGER_MARKER):].strip()
        # Extract JSON block
        m = re.search(r"\{[\s\S]*\}", ledger_raw)
        if m:
            try:
                updates = json.loads(m.group())
            except json.JSONDecodeError:
                updates = {}
        else:
            updates = {}
    else:
        # Fallback: treat entire response as description, no ledger updates
        description = raw
        updates = {}
    return description, updates


def generate_step_descriptions_with_memory(
    parsed_input: Dict[str, Any],
    plan: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    For each step in the plan, generate an animation description.
    Each step receives:
      - The full plan
      - Descriptions of all previous steps (memory)
      - The current ledger (notation, style, objects, story, constraints)

    After each step the ledger is updated (append-only) from the LLM's response.

    Returns {
        "step_results": {step_id: {"description": "..."}},
        "ledger": {final ledger dict},
    }.
    """
    topic = parsed_input.get("content", "")
    template = _load_step_prompt()
    plan_text = _format_plan_text(plan)
    total = len(plan)

    llm = get_llm(stage="step", temperature=0.8, max_tokens=2048)
    ledger = Ledger()
    step_results = {}
    step_descriptions_so_far: List[Dict[str, Any]] = []

    for idx, step_spec in enumerate(plan):
        step_id = step_spec.get("id", f"STEP_{idx+1}")
        step_goal = step_spec.get("goal", "")
        memory_text = _format_memory(step_descriptions_so_far)

        user_content = template.format(
            topic=topic,
            plan_text=plan_text,
            memory_text=memory_text,
            ledger_text=ledger.to_text(),
            step_index=idx + 1,
            total_steps=total,
            step_id=step_id,
            step_goal=step_goal,
        )

        print(f"   [{idx+1}/{total}] {step_id}: {step_goal[:80]}")
        messages = [HumanMessage(content=user_content)]
        response = llm.invoke(messages)
        raw = response.content if hasattr(response, "content") else str(response)

        description, ledger_updates = _parse_step_response(raw)
        ledger.apply_updates(ledger_updates)

        step_results[step_id] = {"description": description.strip()}
        step_descriptions_so_far.append({"id": step_id, "description": description.strip()})
        print(f"   Step {idx+1}/{total} [{step_id}] done. "
              f"Ledger: {len(ledger.notation)} symbols, "
              f"{len(ledger.story_so_far)} story points.")

    return {"step_results": step_results, "ledger": ledger.to_dict()}
