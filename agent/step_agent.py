"""
Step agent: generate animation description for one step with full memory of previous steps.
Runs sequentially so each step receives the accumulated memory (previous step outputs).
"""
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm


PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load_step_prompt() -> str:
    with open(PROMPT_DIR / "step_with_memory_prompt.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def _format_plan_text(plan: List[Dict[str, str]]) -> str:
    return "\n".join(
        f"  {i+1}. [{s['id']}] {s['goal']}" for i, s in enumerate(plan)
    )


def _format_memory(step_descriptions: List[Dict[str, Any]]) -> str:
    """Format previous steps as memory context."""
    if not step_descriptions:
        return "(This is the first step; no previous content yet.)"
    parts = []
    for i, s in enumerate(step_descriptions, 1):
        step_id = s.get("id", f"Step{i}")
        desc = s.get("description", "")
        parts.append(f"Step {i} [{step_id}]:\n{desc}")
    return "\n\n---\n\n".join(parts)


def generate_step_descriptions_with_memory(
    parsed_input: Dict[str, Any],
    plan: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    For each step in the plan, generate an animation description.
    Each step receives the full plan and the descriptions of all previous steps (memory).
    Returns {"step_results": {step_id: {"description": "..."}}}.
    """
    topic = parsed_input.get("content", "")
    template = _load_step_prompt()
    plan_text = _format_plan_text(plan)
    total = len(plan)

    llm = get_llm(stage="step", temperature=0.8, max_tokens=2048)
    step_results = {}
    step_descriptions_so_far = []  # memory: list of {id, description}

    for idx, step_spec in enumerate(plan):
        step_id = step_spec.get("id", f"STEP_{idx+1}")
        step_goal = step_spec.get("goal", "")
        memory_text = _format_memory(step_descriptions_so_far)

        user_content = template.format(
            topic=topic,
            plan_text=plan_text,
            memory_text=memory_text,
            step_index=idx + 1,
            total_steps=total,
            step_id=step_id,
            step_goal=step_goal,
        )

        messages = [HumanMessage(content=user_content)]
        response = llm.invoke(messages)
        description = response.content if hasattr(response, "content") else str(response)

        step_results[step_id] = {"description": description.strip()}
        step_descriptions_so_far.append({"id": step_id, "description": description.strip()})

    return {"step_results": step_results}
