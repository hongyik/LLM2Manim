# prompt_generation.py
import logging
# Assuming the use of the OpenAI SDK (API keys must be configured in config.py)
import openai
import ollama
from openai import OpenAI
from config import GPT4_API_KEY, USE_CLAUDE,USE_GPT, Free_Web, prompt_template

# If Claude is needed, you can import the corresponding API library or use HTTP requests. This example omits that part.

# Set the OpenAI API key
openai.api_key = GPT4_API_KEY

def generate_prompt(question: dict) -> str:
    """Calls the LLM model to generate a step-by-step derivation process and animation description.
    question: A dictionary returned by parse_input, containing the question content and format."""
    
    content = question["content"]
    format = question.get("format", "text")
    
    # Construct the prompt based on the question to generate an animation description
    system_prompt, user_prompt = prompt_template(content)
    
    try:
        if USE_CLAUDE:
            # Example of calling the Claude API (actual implementation depends on the Claude SDK or HTTP interface)
            response = call_claude_api(system_prompt, user_prompt)  # Placeholder function for calling Claude
            result_text = response["content"]
        elif USE_GPT:
            # Use OpenAI's GPT-4 API
            client = OpenAI(api_key=GPT4_API_KEY, base_url=Free_Web)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            result_text = response.choices[0].message.content
        else:
            response = ollama.chat(
                model="deepseek-r1:7b",
                messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ]
                )
            result_text = response["message"]["content"]
    except Exception as e:
        logging.error(f"LLM API call failed: {e}")
        raise RuntimeError("Failed to generate the derivation process description. Please try again later.")
    
    return result_text

