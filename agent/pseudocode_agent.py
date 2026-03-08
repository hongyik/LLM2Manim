"""
Pseudo-code Generator: produces a structured JSON blueprint per scene.

Schema:
{
  "objects":   ["<ClassName>(<args>) as <var>"],
  "animations":[{"beat": 1, "narration": "...", "calls": ["Create(axes)"]}],
  "layout":    {"<var>": "<position>"},
  "forbidden_patterns": ["ImageMobject", "SVGMobject", ...]
}

The JSON is validated then rendered to a formatted string injected into the
code_gen prompt. On invalid JSON the agent retries once before falling back
to an empty string (graceful degradation — scene_fix handles remaining issues).

Processing is sequential (TPM rate limits).
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage, SystemMessage

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config
from .llm import get_llm
from .ledger import Ledger

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_SYSTEM_PROMPT_FILE = PROMPTS_DIR / "pseudocode_system_prompt.txt"

# Required top-level keys and their expected types
_REQUIRED_KEYS: Dict[str, type] = {
    "objects": list,
    "animations": list,
    "layout": dict,
    "forbidden_patterns": list,
}

# Patterns always forbidden regardless of what the LLM returns
_BASE_FORBIDDEN = ["ImageMobject", "SVGMobject", "MAGENTA", "CYAN", "VIOLET", "INDIGO", "LIME"]


# ── Prompt loading ─────────────────────────────────────────────────────────────

def _load_system_prompt() -> str:
    if _SYSTEM_PROMPT_FILE.exists():
        return _SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()
    return (
        "You are a Manim animation architect. Output ONLY a JSON blueprint with keys: "
        "objects (list), animations (list of {beat, narration, calls}), "
        "layout (dict), forbidden_patterns (list). No prose."
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
    parts += ["", "Output the JSON blueprint for this scene. Remember: ONLY the JSON object, nothing else."]
    return "\n".join(parts)


# ── JSON extraction & validation ───────────────────────────────────────────────

def _extract_json(raw: str) -> Optional[str]:
    """Extract JSON from raw LLM response (handles markdown code fences)."""
    raw = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` fences if present
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if m:
        return m.group(1).strip()
    # Look for a bare JSON object
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        return m.group(0)
    return raw  # try parsing as-is


def _validate(data: Any) -> Optional[Dict]:
    """
    Validate the parsed JSON against the schema.
    Returns the (possibly patched) dict on success, None on failure.
    """
    if not isinstance(data, dict):
        return None
    # Check required keys
    for key, expected_type in _REQUIRED_KEYS.items():
        if key not in data or not isinstance(data[key], expected_type):
            return None
    # animations: each entry must be a dict with beat, narration, calls
    for item in data["animations"]:
        if not isinstance(item, dict):
            return None
        if not isinstance(item.get("calls"), list):
            return None
    # Ensure base forbidden patterns are always present
    existing = set(data.get("forbidden_patterns", []))
    data["forbidden_patterns"] = sorted(existing | set(_BASE_FORBIDDEN))
    return data


def _parse_and_validate(raw: str) -> Optional[Dict]:
    """Try to extract and validate JSON from the LLM's raw response."""
    json_str = _extract_json(raw)
    if not json_str:
        return None
    try:
        data = json.loads(json_str)
        return _validate(data)
    except (json.JSONDecodeError, ValueError):
        return None


# ── Text renderer (JSON → prompt string for code_gen) ─────────────────────────

def _render_to_text(schema: Dict) -> str:
    """Render the validated JSON blueprint to a human-readable string for injection into code_gen."""
    lines = []

    # Objects
    lines.append("OBJECTS TO CREATE:")
    for obj in schema.get("objects", []):
        lines.append(f"  - {obj}")

    # Animations
    lines.append("")
    lines.append("ANIMATION BEATS (each beat = one voiceover block):")
    for beat in schema.get("animations", []):
        n = beat.get("beat", "?")
        narration = beat.get("narration", "")
        calls = beat.get("calls", [])
        lines.append(f"  [Beat {n}] \"{narration}\"")
        for call in calls:
            lines.append(f"    → {call}")

    # Layout
    layout = schema.get("layout", {})
    if layout:
        lines.append("")
        lines.append("LAYOUT (use move_to / next_to / to_edge to match these positions):")
        for var, pos in layout.items():
            lines.append(f"  - {var}: {pos}")

    # Forbidden patterns
    forbidden = schema.get("forbidden_patterns", [])
    if forbidden:
        lines.append("")
        lines.append(f"DO NOT USE any of these in the code: {', '.join(forbidden)}")

    return "\n".join(lines)


# ── Main entry point ───────────────────────────────────────────────────────────

def generate_pseudocode(
    step_results: Dict[str, Any],
    concept_context: str = "",
    code_examples: str = "",
    ledger: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Generate a structured JSON blueprint for each step, validate it, and
    return {step_id: rendered_text} for injection into the code_gen prompt.

    Falls back to empty string per step on persistent failure.
    """
    if not step_results:
        return {}

    system_prompt = _load_system_prompt()
    ledger_obj = Ledger.from_dict(ledger) if ledger else Ledger()
    ledger_text = ledger_obj.to_text()
    llm = get_llm(stage="pseudocode", temperature=0.2, max_tokens=1024)

    pseudocode: Dict[str, str] = {}
    raw_schemas: Dict[str, Any] = {}  # for debug dump

    for step_id, data in step_results.items():
        description = data.get("description", "")
        step_goal = data.get("goal", step_id)
        print(f"   [pseudocode] Generating JSON blueprint for {step_id}...")

        schema = None
        try:
            user_msg = _build_user_message(
                step_id, step_goal, description,
                concept_context, code_examples, ledger_text,
            )
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_msg),
            ]

            # First attempt
            response = llm.invoke(messages)
            raw = response.content if hasattr(response, "content") else str(response)
            if isinstance(raw, list):
                raw = "\n".join(
                    b.get("text", "") if isinstance(b, dict) else str(b) for b in raw
                )
            schema = _parse_and_validate(raw)

            # Retry once if invalid
            if schema is None:
                print(f"   [pseudocode] Invalid JSON for '{step_id}', retrying...")
                retry_messages = messages + [
                    HumanMessage(content=raw),  # echo back the bad response
                    HumanMessage(
                        content=(
                            "Your response was not valid JSON matching the required schema. "
                            "Output ONLY the JSON object — no prose, no markdown fences."
                        )
                    ),
                ]
                response2 = llm.invoke(retry_messages)
                raw2 = response2.content if hasattr(response2, "content") else str(response2)
                if isinstance(raw2, list):
                    raw2 = "\n".join(
                        b.get("text", "") if isinstance(b, dict) else str(b) for b in raw2
                    )
                schema = _parse_and_validate(raw2)

            if schema is not None:
                raw_schemas[step_id] = schema
                pseudocode[step_id] = _render_to_text(schema)
                n_objects = len(schema.get("objects", []))
                n_beats = len(schema.get("animations", []))
                print(f"   [pseudocode] {step_id}: {n_objects} object(s), {n_beats} beat(s)")
            else:
                print(f"   [pseudocode] WARNING: could not produce valid JSON for '{step_id}', using empty outline")
                pseudocode[step_id] = ""
                raw_schemas[step_id] = None

        except Exception as exc:
            print(f"   [pseudocode] ERROR for step '{step_id}': {type(exc).__name__}: {exc}")
            pseudocode[step_id] = ""
            raw_schemas[step_id] = None

    # Save both validated schemas and rendered text for debugging
    try:
        out_dir = config.OUTPUT_DIR
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "pseudocode.json").write_text(
                json.dumps(raw_schemas, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            (out_dir / "pseudocode_rendered.json").write_text(
                json.dumps(pseudocode, indent=2, ensure_ascii=False), encoding="utf-8"
            )
    except Exception:
        pass

    return pseudocode
