"""
Planner agent: given user input (topic), produce a dynamic animation plan.
Plan is a list of steps with id and goal; number and content depend on the input.
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm


PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load_plan_prompt() -> str:
    with open(PROMPT_DIR / "plan_prompt.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def _parse_plan_response(raw: str) -> List[Dict[str, str]]:
    """Extract JSON list of steps from LLM response."""
    raw = raw.strip()
    # Try to find JSON block
    match = re.search(r"\{[\s\S]*\"steps\"[\s\S]*\}", raw)
    if match:
        raw = match.group(0)
    data = json.loads(raw)
    steps = data.get("steps", data) if isinstance(data, dict) else data
    if not isinstance(steps, list):
        return [{"id": "STEP_1", "goal": str(steps)}]
    return [{"id": s.get("id", f"STEP_{i+1}"), "goal": s.get("goal", "")} for i, s in enumerate(steps)]


def plan_animation_steps(parsed_input: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Dynamic planning: from user input (topic), return a list of steps.
    Each step: {"id": "...", "goal": "..."}.
    """
    topic = parsed_input.get("content", "")
    system_text = _load_plan_prompt()
    user_text = f"Topic or concept to plan:\n\n{topic}"

    llm = get_llm(stage="planner", temperature=0.5, max_tokens=1024)
    messages = [SystemMessage(content=system_text), HumanMessage(content=user_text)]
    response = llm.invoke(messages)
    raw = response.content if hasattr(response, "content") else str(response)
    return _parse_plan_response(raw)
