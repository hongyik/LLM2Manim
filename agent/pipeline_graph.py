"""
LangGraph pipeline: each LangChain stage is a node.
State flows: parse -> planner -> step_descriptions -> code_gen -> scene_fix -> render -> END

The pipeline carries a short-term working-memory LEDGER across the description and code stages
so that all scenes share consistent notation, visual style, and object naming.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config
config.init_run_dir()
from config import OUTPUT_DIR, FINAL_VIDEO_DIR, MANIM_RENDER_QUALITY, MANIM_CLI

from .planner import plan_animation_steps
from .step_agent import generate_step_descriptions_with_memory
from .code_agent import generate_code_for_descriptions
from .scene_fix_graph import run_auto_fix_for_all_scenes
from .render import render_and_combine


class PipelineState(TypedDict, total=False):
    """State passed between pipeline nodes."""
    user_input: str
    parsed: Dict[str, Any]
    plan: List[Dict[str, str]]
    descriptions: Dict[str, Any]
    ledger: Dict[str, Any]          # short-term working memory ledger
    code_result: Dict[str, Any]
    fix_result: Dict[str, Any]
    render_result: Dict[str, Any]
    error: Optional[str]
    stages: Dict[str, Any]


def _parse_node(state: PipelineState) -> Dict[str, Any]:
    """Node 1: Parse user input."""
    print("\n Stage 1/6: Parsing input...")
    user_input = (state.get("user_input") or "").strip()
    if not user_input:
        return {"error": "Input is empty. Please provide a math/physics topic."}
    return {
        "parsed": {"content": user_input},
        "stages": {**(state.get("stages") or {}), "input_analysis": {"content": user_input}},
    }


def _planner_node(state: PipelineState) -> Dict[str, Any]:
    """Node 2: Dynamic animation plan from input."""
    if state.get("error"):
        return {}
    print("\n Stage 2/6: Planning animation steps (dynamic from input)...")
    parsed = state.get("parsed") or {}
    plan = plan_animation_steps(parsed)
    print(f"   Planned {len(plan)} steps: {[s['id'] for s in plan]}")
    stages = {**(state.get("stages") or {}), "plan": {"steps": plan}}
    return {"plan": plan, "stages": stages}


def _step_descriptions_node(state: PipelineState) -> Dict[str, Any]:
    """Node 3: Step descriptions with memory of previous steps and running ledger."""
    if state.get("error"):
        return {}
    print("\n Stage 3/6: Generating step descriptions (with step memory + ledger)...")
    parsed = state.get("parsed") or {}
    plan = state.get("plan") or []
    desc_result = generate_step_descriptions_with_memory(parsed, plan)

    # Save descriptions and ledger snapshot
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "animation_descriptions.json").write_text(
        json.dumps(desc_result["step_results"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "ledger.json").write_text(
        json.dumps(desc_result["ledger"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    stages = {**(state.get("stages") or {}), "descriptions": desc_result}
    return {
        "descriptions": desc_result,
        "ledger": desc_result["ledger"],
        "stages": stages,
    }


def _code_gen_node(state: PipelineState) -> Dict[str, Any]:
    """Node 4: Generate Manim code for each step, injecting the ledger for consistency."""
    if state.get("error"):
        return {}
    print("\n Stage 4/6: Generating Manim code (ledger-consistent)...")
    desc = state.get("descriptions") or {}
    step_results = desc.get("step_results") or {}
    ledger = state.get("ledger")
    code_result = generate_code_for_descriptions(step_results, ledger=ledger)
    stages = {**(state.get("stages") or {}), "code_generation": code_result}
    return {"code_result": code_result, "stages": stages}


def _scene_fix_node(state: PipelineState) -> Dict[str, Any]:
    """Node 5: LangGraph auto-fix failed Manim scenes."""
    if state.get("error"):
        return {}
    print("\n Stage 5/6: Auto-fixing scenes (validate -> fix -> validate)...")
    plan = state.get("plan") or []
    step_ids = [s["id"] for s in plan]
    fix_result = run_auto_fix_for_all_scenes(
        step_ids, OUTPUT_DIR, max_attempts_per_scene=3
    )
    if fix_result.get("still_failed"):
        print(f"   Fixed: {fix_result.get('fixed', [])}; still failed: {fix_result['still_failed']}")
    else:
        print("   All scenes OK (fixed or already passing).")
    stages = {**(state.get("stages") or {}), "scene_auto_fix": fix_result}
    return {"fix_result": fix_result, "stages": stages}


def _render_node(state: PipelineState) -> Dict[str, Any]:
    """Node 6: Render videos in parallel and combine."""
    if state.get("error"):
        return {}
    print("\n Stage 6/6: Rendering videos in parallel and combining...")
    plan = state.get("plan") or []
    step_ids = [s["id"] for s in plan]
    render_result = render_and_combine(
        step_ids,
        OUTPUT_DIR,
        FINAL_VIDEO_DIR,
        quality=MANIM_RENDER_QUALITY,
        manim_cli=MANIM_CLI,
    )
    stages = {**(state.get("stages") or {})}
    stages["render"] = render_result
    if render_result.get("combined_path"):
        stages["combined_scene_path"] = render_result["combined_path"]
        print(f"   Combined video: {render_result['combined_path']}")
    else:
        print("   Render/combine failed or skipped (check Manim & FFmpeg).")
    return {"render_result": render_result, "stages": stages}


def _route_after_parse(state: PipelineState) -> str:
    """If parse set error, end; else continue to planner."""
    return "__end__" if state.get("error") else "planner"


def build_pipeline_graph() -> StateGraph:
    """Build the full pipeline as a LangGraph (linear chain)."""
    graph = StateGraph(PipelineState)
    graph.add_node("parse", _parse_node)
    graph.add_node("planner", _planner_node)
    graph.add_node("step_descriptions", _step_descriptions_node)
    graph.add_node("code_gen", _code_gen_node)
    graph.add_node("scene_fix", _scene_fix_node)
    graph.add_node("render", _render_node)

    graph.set_entry_point("parse")
    graph.add_conditional_edges("parse", _route_after_parse, {"planner": "planner", "__end__": END})
    graph.add_edge("planner", "step_descriptions")
    graph.add_edge("step_descriptions", "code_gen")
    graph.add_edge("code_gen", "scene_fix")
    graph.add_edge("scene_fix", "render")
    graph.add_edge("render", END)
    return graph.compile()


def run_pipeline(user_input: str) -> Dict[str, Any]:
    """
    Run the full pipeline via LangGraph. Returns the same shape as process_visualization().
    Sets status "error" when: parse error, any stage raises, scene_fix has still_failed, or render status is not "success".
    """
    app = build_pipeline_graph()
    initial: PipelineState = {"user_input": user_input, "stages": {}}
    final = app.invoke(initial)
    stages = final.get("stages") or {}

    if final.get("error"):
        return {"status": "error", "stages": stages, "error": final["error"]}

    # Treat scene-fix or render failures as overall failure so callers can test with result["status"] == "error"
    fix_result = stages.get("scene_auto_fix") or {}
    if fix_result.get("still_failed"):
        return {
            "status": "error",
            "stages": stages,
            "error": f"Scenes still failed after auto-fix: {fix_result['still_failed']}",
        }
    render_result = stages.get("render") or {}
    if render_result.get("status") and render_result["status"] != "success":
        combined = render_result.get("combined_path") or "(none)"
        return {
            "status": "error",
            "stages": stages,
            "error": f"Render failed (status={render_result['status']}, combined_path={combined})",
        }

    return {"status": "success", "stages": stages, "error": None}
