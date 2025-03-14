# input_processing.py
from typing import Dict, Any

def parse_input(user_input: str) -> Dict[str, Any]:
    """Parses user input and returns standardized content.
    
    Returns:
        dict: Contains processed input with:
            - content: Original cleaned content
    """
    if user_input is None or user_input.strip() == "":
        raise ValueError("Input is empty. Please provide a math/physics problem.")
    
    content = user_input.strip()
    
    parsed = {
        "content": content
    }
    
    return parsed

