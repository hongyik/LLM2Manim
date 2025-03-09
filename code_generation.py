# code_generation.py
import logging
import openai
from openai import OpenAI
from config import GPT4_API_KEY,Free_Web,prompt_template_code

openai.api_key = GPT4_API_KEY

def generate_code(animation_prompt: str) -> str:
    """Convert animation description into Manim Python code."""
    # Prompt the coding model to generate code. 
    system_prompt, user_prompt = prompt_template_code(animation_prompt)
    
    try:
        client = OpenAI(api_key=GPT4_API_KEY, base_url=Free_Web)
        response = client.chat.completions.create(
            #model="gpt-4o",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0  # Set to 0 to increase determinism and avoid random variations.
        )
        code_text = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Failed to call the code generation model: {e}")
        raise RuntimeError("Failed to generate Manim code, please try again later.")
    
    # # Simple validation: check if the output contains a Manim Scene class definition
    # if "class" not in code_text or "Scene" not in code_text:
    #     raise RuntimeError("The generated code is incomplete or does not meet expectations.")
    
    return code_text
