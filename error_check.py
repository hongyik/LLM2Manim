import json
import os
import re
import subprocess
from typing import Dict, Any, List
from config import MANIM_RENDER_QUALITY,MANIM_CLI_PATH


def modify_scene_class(file_path: str) -> None:
    """
    Modify the scene class name in the file to GenScene.
    
    Args:
        file_path: Path to the Python file to modify
    """
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Replace class name with GenScene if it's not already GenScene
        class_pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\):'
        if 'class GenScene(Scene):' not in python_code:
            python_code = re.sub(class_pattern, 'class GenScene(Scene):', python_code)
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
                
    except Exception as e:
        raise Exception(f"Failed to modify scene class: {str(e)}")

def test_single_scene(file_path: str) -> Dict[str, Any]:
    """
    Test a single scene by attempting to render it.
    First modifies the scene class name to GenScene, then renders using Manim.
    
    Args:
        file_path: Path to the Python file containing the scene
        
    Returns:
        Dictionary containing test results
    """
    try:
        # First modify the scene class name
        modify_scene_class(file_path)
        
        # Get filename without extension for output
        filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # Construct the Manim rendering command
        manim_command = [
            MANIM_CLI_PATH,
            file_path,
            "-q", MANIM_RENDER_QUALITY,
            "--disable_caching",
            "-o", f"{filename}.mp4",
            "GenScene"
        ]
        
        # Run the command
        result = subprocess.run(
            manim_command,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero return code
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "file": file_path,
                "output": result.stdout,
                "rendered_file": f"{filename}.mp4"
            }
        else:
            return {
                "status": "error",
                "file": file_path,
                "error": result.stderr,
                "command": " ".join(manim_command)  # Include command for debugging
            }
            
    except Exception as e:
        return {
            "status": "error",
            "file": file_path,
            "error": str(e),
            "type": "execution_error"
        }

def test_all_scenes(directory: str = "animation_outputs") -> Dict[str, Any]:
    """
    Test all generated scene files in the specified directory.
    
    Args:
        directory: Directory containing the generated scene files
        
    Returns:
        Dictionary containing test results for all scenes
    """
    results = {
        "status": "success",
        "tested_files": [],
        "successful_files": [],
        "failed_files": [],
        "errors": {},
        "rendered_files": []  # Track successfully rendered files
    }
    
    # Get all Python files in the directory except combined_animation.py
    scene_files = [f for f in os.listdir(directory) 
                   if f.endswith('.py') and f != 'combined_animation.py']
    
    if not scene_files:
        return {
            "status": "error",
            "error": "No scene files found to test"
        }
    
    # Test each scene file
    for scene_file in scene_files:
        file_path = os.path.join(directory, scene_file)
        results["tested_files"].append(scene_file)
        
        test_result = test_single_scene(file_path)
        
        if test_result["status"] == "success":
            results["successful_files"].append(scene_file)
            if "rendered_file" in test_result:
                results["rendered_files"].append(test_result["rendered_file"])
        else:
            results["failed_files"].append(scene_file)
            results["errors"][scene_file] = {
                "error": test_result["error"],
                "command": test_result.get("command", "N/A")
            }
    
    # Update overall status - only success if all files pass
    if results["failed_files"]:
        results["status"] = "error"
    
    return results

def save_test_results(results: Dict[str, Any], directory: str = "animation_outputs") -> str:
    """
    Save test results to a JSON file.
    
    Args:
        results: Dictionary containing test results
        directory: Directory to save the results
        
    Returns:
        Path to the saved results file
    """
    output_path = os.path.join(directory, "scene_test_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    return output_path

if __name__ == "__main__":
    # Test all scenes and save results
    results = test_all_scenes()
    results_file = save_test_results(results)
    
    # Print summary
    print(f"\n📊 Scene Testing Summary:")
    print(f"Total files tested: {len(results['tested_files'])}")
    print(f"Successful: {len(results['successful_files'])}")
    print(f"Failed: {len(results['failed_files'])}")
    
    if results['failed_files']:
        print("\n❌ Failed scenes:")
        for file in results['failed_files']:
            print(f"\n{file}:")
            print(f"Error: {results['errors'][file]['error']}")
            print(f"Command: {results['errors'][file]['command']}")
    else:
        print("\n✅ All scenes rendered successfully!")
        print("\nRendered files:")
        for file in results.get('rendered_files', []):
            print(f"  - {file}")
    
    print(f"\nDetailed results saved to: {results_file}") 