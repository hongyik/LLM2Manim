# config.py
# LLM API keys and options
GPT4_API_KEY = "sk-TmeRzxqaqBwUEfz2FHi3S73k9siM6gsBBrPDc0JXkcZb8xH9"  # "Your OpenAI API key"
CLAUDE_API_KEY = "Claude API key"
USE_CLAUDE = False 
USE_GPT = True
Free_Web = "https://api.chatanywhere.tech/v1"

# Manim configuration
MANIM_CLI_PATH = "C:\\Users\\kehon\\AppData\\Roaming\\Python\\Python312\\Scripts\\manim.exe"  # Path to the Manim executable
MANIM_RENDER_QUALITY = "l"  # Rendering quality options: low (l), medium (m), high (h), etc.


# Output directory
OUTPUT_DIR = "./outputs"
def prompt_template(content):
    # Read system prompt from file
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        system_p = f.read()
    
    # Read user prompt template from file
    with open('user_prompt_template.txt', 'r', encoding='utf-8') as f:
        user_p_template = f.read()
    
    # Format user prompt with content
    user_p = user_p_template.format(content=content)
    
    return system_p, user_p
def prompt_template_code(animation_prompt):
    # Read system prompt from file
    with open('system_prompt_code.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Read user prompt template from file
    with open('user_prompt_code_template.txt', 'r', encoding='utf-8') as f:
        user_prompt_template = f.read()
    
    # Format user prompt with animation prompt
    user_prompt = user_prompt_template.format(animation_prompt=animation_prompt)
    
    return system_prompt, user_prompt