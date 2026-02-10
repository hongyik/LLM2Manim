"""
Pipeline runs as a LangGraph: each stage is a node.
  parse -> planner -> step_descriptions -> code_gen -> scene_fix -> render -> END
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import RUN_DIR, OUTPUT_DIR, FINAL_VIDEO_DIR
from agent.pipeline_graph import run_pipeline


def process_visualization(user_input: str) -> dict:
    """Run the full pipeline via LangGraph (each stage is a node)."""
    try:
        return run_pipeline(user_input)
    except Exception as e:
        logging.exception("Pipeline failed")
        return {"status": "error", "stages": {}, "error": str(e)}


def main():
    logging.basicConfig(level=logging.ERROR, format="%(message)s")
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Math/physics topic: ")
    result = process_visualization(user_input)
    if result["status"] == "success":
        print("\n✅ Done. Run folder:", RUN_DIR)
        print("   animation_outputs:", OUTPUT_DIR, "| final_animation:", FINAL_VIDEO_DIR)
    else:
        print("\n❌ Error:", result.get("error"))
    return result


if __name__ == "__main__":
    main()
