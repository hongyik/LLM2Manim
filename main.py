# main.py
import sys
import logging
import asyncio
from typing import Dict, Any, Optional
from input_processing import parse_input
from parallel_processing import generate_parallel_animation
from parallel_code_generation import generate_parallel_code
from error_check import test_all_scenes, save_test_results
from fix_scenes import fix_failed_scenes
from combine_scenes import render_combined_scene
from process_summary import save_process_summary
def process_visualization(user_input: str) -> Dict[str, Any]:
    """
    Process a mathematical visualization request to generate descriptions and code.
    
    Args:
        user_input (str): The user's mathematical/physics problem description
        
    Returns:
        Dict[str, Any]: Process results including descriptions and code for each step
    """
    result = {
        "status": "success",
        "stages": {},
        "error": None
    }
    
    try:
        # Stage 1: Parse input
        print("\n📝 Stage 1/6: Parsing input...")
        parsed_input = parse_input(user_input)
        result["stages"]["input_analysis"] = {
            "content": parsed_input["content"]
        }
        
        # Stage 2: Generate structured animation descriptions
        print("\n🤖 Stage 2/6: Generating structured animation descriptions...")
        parallel_result = generate_parallel_animation(parsed_input)
        result["stages"]["descriptions"] = {
            "step_results": parallel_result["step_results"]
        }
        
        # Stage 3: Generate Manim code for each step
        print("\n💻 Stage 3/6: Generating Manim code for each step...")
        code_result = generate_parallel_code(result)
        result["stages"]["code_generation"] = code_result
        
        # Stages 4-5: Test and fix scenes in a loop until all pass or max retries reached
        MAX_FIX_ATTEMPTS = 2
        attempt = 1
        all_scenes_pass = False
        
        while not all_scenes_pass and attempt <= MAX_FIX_ATTEMPTS:
            print(f"\n📋 Fix Attempt {attempt}/{MAX_FIX_ATTEMPTS}")
            
            # Stage 4: Test individual scenes
            print("\n🧪 Stage 4/6: Testing individual scenes...")
            test_results = test_all_scenes()
            save_test_results(test_results)
            result["stages"][f"scene_testing_attempt_{attempt}"] = test_results
            
            # Check if all scenes pass
            if test_results["status"] == "success":
                print("\n✅ All scenes passed testing!")
                all_scenes_pass = True
                break
                
            # Stage 5: Fix failed scenes
            print(f"\n🔧 Stage 5/6: Fixing failed scenes (Attempt {attempt}/{MAX_FIX_ATTEMPTS})...")
            fix_results = fix_failed_scenes()
            result["stages"][f"scene_fixing_attempt_{attempt}"] = fix_results
            
            attempt += 1
        
        # Stage 6: Combine all generated code parts
        print("\n🔄 Stage 6/6: Rendering final animation...")
        combine_result = render_combined_scene(input_dir="animation_outputs", output_dir="final_animation")
        result["stages"]["combined_scene_path"] = combine_result
        
    except Exception as e:
        error_msg = f"Process failed: {str(e)}"
        logging.error(error_msg)
        result["status"] = "error"
        result["error"] = error_msg
    
    return result

def main():
    # Configure logging - only show errors
    logging.basicConfig(
        level=logging.ERROR,
        format='%(message)s'
    )
    
    # Get user input
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Please enter a math/physics problem description: ")
    
    # Run the async process
    result = process_visualization(user_input)
    return result

if __name__ == "__main__":
    result = main()
    save_process_summary(result)