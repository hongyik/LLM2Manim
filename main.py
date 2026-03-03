"""
Pipeline runs as a LangGraph: each stage is a node.
  parse -> planner -> step_descriptions -> code_gen -> scene_fix -> render -> END
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Force UTF-8 output on Windows (avoids UnicodeEncodeError for Greek/math symbols in print)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import config
config.init_run_dir()  # single run dir per process (avoids multiple output folders)
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
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Math/physics topic: ")
    result = process_visualization(user_input)
    if result["status"] == "success":
        print("\nDone. Run folder:", RUN_DIR)
        print("   animation_outputs:", OUTPUT_DIR, "| final_animation:", FINAL_VIDEO_DIR)
        return 0
    print("\nError:", result.get("error"))
    return 1


if __name__ == "__main__":
    main()
