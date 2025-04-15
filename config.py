# config.py
import os

# =============================================
# API Configuration
# =============================================

# API Keys
# Note: It's recommended to use environment variables for sensitive keys
DeepSeek_Prompt_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# GPT4_API_KEY = "sk-TmeRzxqaqBwUEfz2FHi3S73k9siM6gsBBrPDc0JXkcZb8xH9"  # "Your OpenAI API key"
GPT4_API_KEY = "sk-974L3UWhpQQPh1Ec19KXDSkabFW7ics5Fu7y9C8im9My4nOZ"  # Replace with your actual GPT-4 API key
CLAUDE_API_KEY = "Claude API key"  # Replace with your actual Claude API key

# API Selection
USE_CLAUDE = False  # Set to True to use Claude API
USE_GPT = True      # Set to True to use GPT-4 API

# API Endpoints
Free_Web = "https://api.chatanywhere.tech/v1"    # Free API endpoint
DeepSeek_Web = "https://api.deepseek.com/v1"     # DeepSeek API endpoint

# =============================================
# Manim Configuration
# =============================================

# Path Configuration
MANIM_CLI_PATH = "C:\\Users\\kehon\\AppData\\Roaming\\Python\\Python312\\Scripts\\manim.exe"

# Quality Settings
MANIM_RENDER_QUALITY = "l"  # Options: low (l), medium (m), high (h)

# =============================================
# Output Configuration
# =============================================

# Directory Settings
OUTPUT_DIR = "./outputs"  # Main output directory for all generated content

# =============================================
# Prompt Template Functions
# =============================================

def prompt_template(content):
    """
    Generate system and user prompts for animation description.
    
    Args:
        content (str): The content to be formatted into the prompt
        
    Returns:
        tuple: (system_prompt, user_prompt)
    """
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
    """
    Generate system and user prompts for code generation.
    
    Args:
        animation_prompt (str): The animation description to be formatted into the prompt
        
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    # Read system prompt from file
    with open('system_prompt_code.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Read user prompt template from file
    with open('user_prompt_code_template.txt', 'r', encoding='utf-8') as f:
        user_prompt_template = f.read()
    
    # Format user prompt with animation prompt
    user_prompt = user_prompt_template.format(animation_prompt=animation_prompt)
    
    return system_prompt, user_prompt