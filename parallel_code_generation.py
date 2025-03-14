# parallel_code_generation.py
import json
import os
import asyncio
from typing import Dict, Any, List
from openai import AsyncOpenAI
from config import *

# Configure OpenAI client settings
# gpt_api = GPT4_API_KEY
# gpt_url = Free_Web

gpt_api = DeepSeek_Prompt_API_KEY
gpt_url = DeepSeek_Web

async def generate_code_for_step(client: AsyncOpenAI, step: str, description: str, system_prompt: str, user_prompt: str) -> str:
    """Generate Manim code for a single animation step."""
    try:
        response = await client.chat.completions.create(
            #model="gpt-3.5-turbo",
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=8192,
            temperature=0,
            stream=False
        )
        
        raw_text = response.choices[0].message.content
        
        # Split and extract the code part
        parts = raw_text.split("```python")
        if len(parts) > 1:
            python_code = parts[1].split("```")[0].strip()
        else:
            python_code = raw_text.strip()
            
        return python_code
    except Exception as e:
        return f"Error generating code for {step}: {str(e)}"

async def process_all_code_steps(descriptions: Dict[str, Any], system_prompt: str, user_prompt: str) -> Dict[str, str]:
    """Generate code for all animation steps in parallel."""
    client = AsyncOpenAI(
        api_key=gpt_api,
        base_url=gpt_url
    )
    
    tasks = []
    for step, data in descriptions.items():
        task = generate_code_for_step(client, step, data["description"], system_prompt, user_prompt)
        tasks.append(task)
    
    # Run all tasks concurrently
    code_results = await asyncio.gather(*tasks)
    
    # Organize results
    organized_code = {
        step: code for step, code in zip(descriptions.keys(), code_results)
    }
    
    return organized_code

def generate_parallel_code(stage2_output: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Manim code for each animation step in parallel."""

    descriptions = stage2_output["stages"]["descriptions"]["step_results"]
    system_prompt, user_prompt = prompt_template_code(descriptions)
      
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    code_results = loop.run_until_complete(process_all_code_steps(descriptions, system_prompt, user_prompt))
    loop.close()
        
    # Create output directory
    output_dir = "animation_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual code files
    for step, code in code_results.items():
        file_name = f"{step.lower()}.py"
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
            f.write(code)
    
    # Save as JSON for reference
    json_path = os.path.join(output_dir, "generated_code.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(code_results, f, indent=2, ensure_ascii=False)
    
    return {
        "status": "success",
        "code_results": code_results
    }
if __name__ == "__main__":
    # Test the code generation with a realistic example
    test_input = {
        "stages": {
            "descriptions": {
                "step_results": {
                    "INTUITIVE_OPENING": {
                        "description": "Create an animation that introduces the concept of derivatives using a car's motion. Show a car moving along a straight road with its position changing over time. Highlight how the car's speed represents the rate of change of position."
                    },
                    "VISUALIZE_CONCEPT": {
                        "description": "Create a graph showing position vs time curve. Animate tangent lines at different points to visualize instantaneous rate of change. Use different colors to highlight the slope changes."
                    }
                }
            }
        }
    }
    
    result = generate_parallel_code(test_input)
    print("\nGeneration Status:", result["status"])
    if result["status"] == "success":
        print("\nGenerated code files saved in 'animation_outputs' directory")
        for step, code in result["code_results"].items():
            print(f"\n{'-'*50}\n{step}:")
            print(code[:200] + "..." if len(code) > 200 else code)
