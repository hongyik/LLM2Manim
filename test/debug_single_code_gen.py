# debug_single_code_gen.py
from pathlib import Path
import json
import sys

# 项目根目录（test 的上一级）
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from agent.code_agent import generate_code_for_descriptions

def main():
    run_dir = ROOT_DIR / "outputs/2026-03-03_22-33-18/animation_outputs"  # 换成你想测的 run
    descriptions = json.loads((run_dir / "animation_descriptions.json").read_text(encoding="utf-8"))

    # 用一个 step 当测试用例
    step_id = "MOTIVATION"
    step_results = {step_id: descriptions[step_id]}
    print(step_results)
    result = generate_code_for_descriptions(step_results, ledger=None, layout_specs=None)
    code = result["code_results"][step_id]
    print("Generated code length:", len(code))
    print(code[:800])

if __name__ == "__main__":
    main()