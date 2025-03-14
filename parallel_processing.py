# parallel_processing.py
import logging
import os
import json
from typing import Dict, Any, List
import asyncio
from openai import AsyncOpenAI
from config import DeepSeek_Prompt_API_KEY, DeepSeek_Web, GPT4_API_KEY, Free_Web

# deepseek_api = DeepSeek_Prompt_API_KEY
# deepseek_url = DeepSeek_Web

# gpt_api = GPT4_API_KEY
# gpt_url = Free_Web

gpt_api = DeepSeek_Prompt_API_KEY
gpt_url = DeepSeek_Web
def read_animation_steps_from_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f) 
    animation_steps = data['steps']
    system_prompts = data['system_prompts']
    user_prompts = data['user_prompts']
    return animation_steps, system_prompts, user_prompts

def save_default_steps_to_json(output_file: str = "animation_steps.json") -> None:
    """
    Save the default animation steps and prompts to a JSON file.
    
    Args:
        output_file: Path where to save the JSON file
    """
    data = {
        "steps": ANIMATION_STEPS,
        "system_prompts": SYSTEM_PROMPTS,
        "user_prompts": USER_PROMPTS
    }
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Animation steps and prompts saved to {output_file}")

#Set Prompt and Steps
ANIMATION_STEPS, SYSTEM_PROMPTS, USER_PROMPTS = read_animation_steps_from_json("animation_steps.json")

async def call_llm_api(client: AsyncOpenAI, step: str, system_prompt: str, user_prompt: str) -> str:
    """Make an async API call to the LLM using the OpenAI client."""
    try:
        response = await client.chat.completions.create(
            #model="gpt-3.5-turbo",
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2048,
            temperature=0.7,
            stream=False
        )
        return response.choices[0].message.content
            
    except Exception as e:
        logging.error(f"Failed to generate description for {step}: {str(e)}")
        return f"Error generating {step.replace('_', ' ')} description: {str(e)}"

async def process_animation_step(client: AsyncOpenAI, step: str, topic: str):
    """Process a single animation step to generate its description."""
    user_prompt = USER_PROMPTS[step].format(topic=topic)
    
    system_prompt = SYSTEM_PROMPTS[step]
    
    description = await call_llm_api(client, step, system_prompt, user_prompt)
    
    return {
        "step": step,
        "description": description
    }

async def process_all_steps(topic: str):
    """Process all animation steps in parallel using AsyncOpenAI client."""
    client = AsyncOpenAI(
        api_key=gpt_api,   
        base_url=gpt_url
    )
    
    tasks = [
        process_animation_step(client, step, topic)
        for step in ANIMATION_STEPS
    ]
    
    results = await asyncio.gather(*tasks)
    organized_results = {result["step"]: {"description": result["description"]} for result in results}
    return organized_results

def generate_parallel_animation(parsed_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate animation descriptions by breaking it down into parallel steps.

    Args:
        parsed_input: The parsed user input containing only the content

    Returns:
        Dict with animation descriptions for each step
    """
    topic = parsed_input["content"]
    # loop = asyncio.get_running_loop()
    # task = loop.create_task(process_all_steps(topic))
    # step_results = await task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    step_results = loop.run_until_complete(process_all_steps(topic))
    loop.close()
    # Create output directory
    output_dir = "animation_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON for easy parsin
    json_path = os.path.join(output_dir, "descriptions.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(step_results, f, indent=2, ensure_ascii=False)
    
    logging.info(f"\n💾 Descriptions saved to {output_dir}/descriptions.txt")
    
    # Prepare the result
    result = {
        "step_results": step_results
    }
    
    return result
if __name__ == "__main__":

    # Test the animation generation
    generate_parallel_animation({"content": "Mass conservation in fluid dynamics"})