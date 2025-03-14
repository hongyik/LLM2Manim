import os
import json
import datetime
from typing import Dict, Any

def save_process_summary(result: Dict[str, Any], output_dir: str = "animation_outputs") -> str:
    """
    Save process results to a JSON file.
    
    Args:
        result: Process result dictionary from main.py
        output_dir: Directory to save the summary file
        
    Returns:
        str: Path to the saved summary file
    """
    # Create a structured result summary
    summary = {
        "status": result["status"],
        "timestamp": datetime.datetime.now().isoformat(),
        "generated_files": {
            "descriptions": os.path.join(output_dir, "descriptions.json"),
            "generated_code": os.path.join(output_dir, "generated_code.json"),
            "test_results": os.path.join(output_dir, "scene_test_results.json"),
            "fix_results": os.path.join(output_dir, "scene_fix_results.json"),
            "combined_animation": os.path.join(output_dir, "combined_animation.py"),
            "individual_scenes": os.path.join(output_dir, "*.py")
        },
        "fix_attempts": []
    }

    # Add fix attempts data if any fixes were made
    if "scene_fixing_attempt_1" in result["stages"]:
        attempt = 1
        while f"scene_fixing_attempt_{attempt}" in result["stages"]:
            fix_result = result["stages"][f"scene_fixing_attempt_{attempt}"]
            summary["fix_attempts"].append({
                "attempt": attempt,
                "fixed_scenes": len(fix_result.get('fixed_files', [])),
                "failed_scenes": len(fix_result.get('failed_fixes', [])),
                "details": fix_result
            })
            attempt += 1

    # Add error information if process failed
    if result["status"] == "error":
        summary["error"] = result["error"]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save summary to JSON file
    summary_file = os.path.join(output_dir, "process_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print minimal feedback
    if result["status"] == "success":
        print(f"\n📄 Process summary saved to: {summary_file}")
    else:
        print(f"\n❌ Process failed. Details saved to: {summary_file}")

    return summary_file

if __name__ == "__main__":
    # Example usage when run directly
    example_result = {
        "status": "success",
        "stages": {
            "scene_fixing_attempt_1": {
                "fixed_files": ["scene1.py", "scene2.py"],
                "failed_fixes": ["scene3.py"]
            }
        }
    }
    save_process_summary(example_result) 