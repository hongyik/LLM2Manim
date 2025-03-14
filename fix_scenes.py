import json
import os
import asyncio
import multiprocessing
from typing import Dict, Any, List
from openai import AsyncOpenAI
from config import *

# Configure OpenAI client settings
# gpt_api = GPT4_API_KEY
# gpt_url = Free_Web

gpt_api = DeepSeek_Prompt_API_KEY
gpt_url = DeepSeek_Web

def read_test_results(directory: str = "animation_outputs") -> Dict[str, Any]:
    """Read the test results from the JSON file."""
    results_path = os.path.join(directory, "scene_test_results.json")
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_scene_file(file_path: str) -> str:
    """Read the content of a scene file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_fixed_scene(file_path: str, fixed_code: str) -> None:
    """Save the fixed scene code back to the file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_code)

async def fix_single_scene(client: AsyncOpenAI, file_path: str, error_info: Dict[str, str]) -> Dict[str, Any]:
    """
    Try to fix a single scene using LLM.
    
    Args:
        client: AsyncOpenAI client instance
        file_path: Path to the scene file
        error_info: Dictionary containing error information
        
    Returns:
        Dictionary containing fix results
    """
    try:
        # Read the original scene code
        original_code = read_scene_file(file_path)
        
        # Construct the system prompt
        system_prompt = """You are an expert in Manim animation programming. Your task is to fix the provided scene code that failed to render.
Please analyze the error message and the code, then provide a corrected version that maintains the same animation logic but fixes the technical issues.
Ensure you keep all the mathematical concepts and visualization steps intact while only fixing the technical problems."""

        # Construct the user prompt with the code and error
        user_prompt = f"""Here is a Manim scene that failed to render:

Error message:
{error_info['error']}

Command that failed:
{error_info['command']}

Original code:
```python
{original_code}
```
return all codes in one file.
Please provide a fixed version of this code that will render correctly. Keep all other codes the same, only fix technical issues."""

        # Call LLM API
        response = await client.chat.completions.create(
            #model="gpt-3.5-turbo",
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4000,
            temperature=0.3,
            stream=False
        )
        
        # Extract the fixed code from the response
        raw_text = response.choices[0].message.content
        
        # Split and extract the code part
        fixed_code = raw_text
        if "```python" in raw_text:
            fixed_code = raw_text.split("```python")[1].split("```")[0].strip()
        elif "```" in raw_text:
            fixed_code = raw_text.split("```")[1].strip()
            
        # Save the fixed code
        save_fixed_scene(file_path, fixed_code)
        
        return {
            "status": "success",
            "file": file_path,
            "original_error": error_info['error'],
            "fixed_code": fixed_code
        }
        
    except Exception as e:
        return {
            "status": "error",
            "file": file_path,
            "error": str(e)
        }

async def _process_failed_scenes_async(failed_files: List[str], errors: Dict[str, Dict[str, str]], directory: str) -> List[Dict[str, Any]]:
    """The async part of processing failed scenes."""
    client = AsyncOpenAI(
        api_key=gpt_api,
        base_url=gpt_url
    )
    
    try:
        tasks = []
        for failed_file in failed_files:
            file_path = os.path.join(directory, failed_file)
            error_info = errors[failed_file]
            task = fix_single_scene(client, file_path, error_info)
            tasks.append(task)
        
        # Run all tasks concurrently
        fix_results = await asyncio.gather(*tasks)
        return fix_results
    finally:
        await client.close()

def _run_in_new_process(failed_files, errors, directory, result_queue):
    """Run the async code in a completely separate process."""
    try:
        # Create a brand new event loop in this process
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async function and get results
        results = loop.run_until_complete(_process_failed_scenes_async(failed_files, errors, directory))
        
        # Put results in the queue for the parent process
        result_queue.put(results)
    except Exception as e:
        result_queue.put({"error": str(e)})
    finally:
        loop.close()

def fix_failed_scenes(directory: str = "animation_outputs") -> Dict[str, Any]:
    """
    Attempt to fix all failed scenes in the test results.
    
    Args:
        directory: Directory containing the scene files and test results
        
    Returns:
        Dictionary containing results of fix attempts
    """
    results = {
        "status": "success",
        "fixed_files": [],
        "failed_fixes": [],
        "fixes": {}
    }
    
    try:
        # Read test results
        test_results = read_test_results(directory)
        
        if not test_results.get("failed_files"):
            return {
                "status": "success",
                "message": "No failed scenes to fix"
            }
        
        # Use multiprocessing to completely isolate the event loop
        result_queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=_run_in_new_process,
            args=(
                test_results["failed_files"],
                test_results["errors"],
                directory,
                result_queue
            )
        )
        
        # Start the process and wait for it to complete
        process.start()
        fix_results = result_queue.get()
        process.join()
        
        # Check if we got an error
        if isinstance(fix_results, dict) and "error" in fix_results:
            raise Exception(f"Error in async processing: {fix_results['error']}")
        
        # Process results
        for fix_result in fix_results:
            file_name = os.path.basename(fix_result["file"])
            if fix_result["status"] == "success":
                results["fixed_files"].append(file_name)
                results["fixes"][file_name] = {
                    "original_error": fix_result["original_error"],
                    "fixed": True
                }
            else:
                results["failed_fixes"].append(file_name)
                results["fixes"][file_name] = {
                    "original_error": test_results["errors"][file_name]["error"],
                    "fix_error": fix_result["error"],
                    "fixed": False
                }
        
        # Update overall status
        if results["failed_fixes"]:
            results["status"] = "error"
            
        # Save fix results
        output_path = os.path.join(directory, "scene_fix_results.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    # Test all scenes and save results
    results = fix_failed_scenes()
    
    # Print summary
    print(f"\n🔧 Scene Fixing Summary:")
    print(f"Total files fixed: {len(results.get('fixed_files', []))}")
    print(f"Failed fixes: {len(results.get('failed_fixes', []))}")
    
    if results.get('failed_fixes'):
        print("\n❌ Failed fixes:")
        for file in results['failed_fixes']:
            print(f"\n{file}:")
            print(f"Original Error: {results['fixes'][file]['original_error']}")
            print(f"Fix Error: {results['fixes'][file]['fix_error']}")
    else:
        print("\n✅ All scenes fixed successfully!")
    
    print(f"\nDetailed results saved to: animation_outputs/scene_fix_results.json") 