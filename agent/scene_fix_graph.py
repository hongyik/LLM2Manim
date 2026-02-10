"""
LangGraph-based auto-fix for Manim scenes: validate -> (if fail) fix with LLM -> validate -> ...
"""
import asyncio
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Literal, TypedDict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import MANIM_CLI, MANIM_RENDER_QUALITY
from .llm import get_llm


class SceneFixState(TypedDict):
    file_path: str
    code: str
    error: str
    attempt: int
    max_attempts: int
    status: Literal["pending", "ok", "fail"]


FIX_SYSTEM = """You are an expert in Manim animation programming. Fix the provided scene code that failed to render.
- Analyze the error message and the code; correct only technical issues (syntax, imports, API usage).
- Keep the scene class name as GenScene and all animation logic intact.
- Return the complete fixed Python file. Output only the code, optionally wrapped in ```python ... ```."""

FIX_USER_TEMPLATE = """Manim scene that failed to render:

Error:
{error}

Command (for reference): {manim_cli} -q {quality} <file> GenScene -o <name>

Code:
```python
{code}
```

Provide the full corrected code (one file). Preserve imports, GenScene(VoiceoverScene), and KokoroService(voice="af_sarah", lang="en-us")."""


def _validate_scene(state: SceneFixState) -> SceneFixState:
    """Run manim on the scene file; set status='ok' or 'fail' and error message."""
    file_path = Path(state["file_path"])
    if not file_path.exists():
        return {**state, "status": "fail", "error": f"File not found: {file_path}"}
    cwd = file_path.resolve().parent.parent  # langchain_agent
    out_name = file_path.stem
    cmd = f"{MANIM_CLI} -q {MANIM_RENDER_QUALITY} {file_path} GenScene -o {out_name}"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {**state, "status": "fail", "error": "Manim render timed out (120s)."}
    except Exception as e:
        return {**state, "status": "fail", "error": str(e)}
    if result.returncode == 0:
        return {**state, "status": "ok", "error": ""}
    err = (result.stderr or result.stdout or "Unknown error").strip()
    return {**state, "status": "fail", "error": err[:2000]}


def _fix_scene_with_llm(state: SceneFixState) -> SceneFixState:
    """Use LLM to fix the code from state; write back to file and return updated state."""
    file_path = Path(state["file_path"])
    code = state.get("code") or file_path.read_text(encoding="utf-8")
    error = state.get("error", "")
    attempt = state.get("attempt", 0) + 1
    max_attempts = state.get("max_attempts", 2)

    llm = get_llm(stage="code", temperature=0.2, max_tokens=4096)
    user_content = FIX_USER_TEMPLATE.format(
        error=error,
        manim_cli=MANIM_CLI,
        quality=MANIM_RENDER_QUALITY,
        code=code,
    )
    messages = [SystemMessage(content=FIX_SYSTEM), HumanMessage(content=user_content)]
    response = llm.invoke(messages)
    raw = response.content if hasattr(response, "content") else str(response)
    # Extract code
    m = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
    fixed = (m.group(1).strip() if m else raw.strip())
    fixed = re.sub(r"^\s*```(?:python)?\s*\n?", "", fixed)
    fixed = re.sub(r"\n?```\s*$", "", fixed)
    fixed = fixed.strip()
    file_path.write_text(fixed, encoding="utf-8")
    return {
        **state,
        "code": fixed,
        "attempt": attempt,
        "max_attempts": max_attempts,
        "status": "pending",
    }


def _route_after_validate(state: SceneFixState) -> Literal["fix", "__end__"]:
    if state["status"] == "ok":
        return "__end__"
    if state.get("attempt", 0) >= state.get("max_attempts", 2):
        return "__end__"
    return "fix"


def build_scene_fix_graph() -> StateGraph:
    """Build the validate -> fix -> validate loop."""
    graph = StateGraph(SceneFixState)
    graph.add_node("validate", _validate_scene)
    graph.add_node("fix", _fix_scene_with_llm)
    graph.add_conditional_edges("validate", _route_after_validate, {"fix": "fix", "__end__": END})
    graph.add_edge("fix", "validate")
    graph.set_entry_point("validate")
    return graph.compile()


def run_auto_fix_for_scene(
    file_path: str | Path,
    max_attempts: int = 2,
) -> Dict[str, Any]:
    """
    Run the LangGraph auto-fix for a single scene file (synchronously).
    Returns dict with final_state, fixed (bool), attempts (int).
    """
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        return {"fixed": False, "error": "File not found", "attempts": 0}
    code = file_path.read_text(encoding="utf-8")
    initial: SceneFixState = {
        "file_path": str(file_path),
        "code": code,
        "error": "",
        "attempt": 0,
        "max_attempts": max_attempts,
        "status": "pending",
    }
    app = build_scene_fix_graph()
    final_state = app.invoke(initial)
    return {
        "fixed": final_state.get("status") == "ok",
        "attempts": final_state.get("attempt", 0),
        "final_error": final_state.get("error", ""),
        "file_path": str(file_path),
    }


async def _auto_fix_scene_async(
    file_path: Path,
    max_attempts: int = 2,
) -> Dict[str, Any]:
    """
    Async helper: run the LangGraph auto-fix for a single scene using ainvoke().
    This lets us run many scene-fix graphs in parallel.
    """
    file_path = file_path.resolve()
    if not file_path.exists():
        return {
            "fixed": False,
            "error": "File not found",
            "attempts": 0,
            "file_path": str(file_path),
        }

    code = file_path.read_text(encoding="utf-8")
    initial: SceneFixState = {
        "file_path": str(file_path),
        "code": code,
        "error": "",
        "attempt": 0,
        "max_attempts": max_attempts,
        "status": "pending",
    }
    app = build_scene_fix_graph()
    final_state = await app.ainvoke(initial)
    return {
        "fixed": final_state.get("status") == "ok",
        "attempts": final_state.get("attempt", 0),
        "final_error": final_state.get("error", ""),
        "file_path": str(file_path),
    }


def run_auto_fix_for_all_scenes(
    step_ids: list,
    output_dir: Path,
    max_attempts_per_scene: int = 2,
) -> Dict[str, Any]:
    """
    Public API: for each step's scene file, run the LangGraph scene-fix loop.
    Scenes are processed in parallel using asyncio and LangGraph's ainvoke().

    Returns summary: fixed list, still_failed list, details per file.
    """

    async def _run_all_scenes_async() -> Dict[str, Any]:
        results: Dict[str, Any] = {"fixed": [], "still_failed": [], "details": {}}

        tasks: List[asyncio.Task] = []
        step_ids_for_tasks: List[str] = []

        for step_id in step_ids:
            fname = f"{step_id.lower()}.py"
            path = output_dir / fname
            if not path.exists():
                results["details"][step_id] = {"error": "file not found"}
                continue
            step_ids_for_tasks.append(step_id)
            tasks.append(
                asyncio.create_task(
                    _auto_fix_scene_async(path, max_attempts=max_attempts_per_scene)
                )
            )

        if not tasks:
            return results

        scene_results = await asyncio.gather(*tasks)

        for step_id, scene_result in zip(step_ids_for_tasks, scene_results):
            results["details"][step_id] = scene_result
            if scene_result.get("fixed"):
                results["fixed"].append(step_id)
            else:
                results["still_failed"].append(step_id)

        return results

    return asyncio.run(_run_all_scenes_async())
