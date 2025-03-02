# input_processing.py
import re

def parse_input(user_input: str) -> dict:
    """Parses user input (text or LaTeX) and returns standardized content and format.
    Example return: {"content": "Integral problem x^2 ...", "format": "text"} 
    or {"content": "E = mc^2", "format": "latex"}"""
    
    if user_input is None or user_input.strip() == "":
        raise ValueError("Input is empty. Please provide a math/physics problem.")
    
    content = user_input.strip()
    
    # Simple check for LaTeX formula markers (e.g., $...$ or \begin{equation})
    if re.search(r"\$.*\$|\\begin\{.*?\}", content):
        input_format = "latex"
    else:
        input_format = "text"
    
    # Additional parsing and cleaning logic can be added here, such as removing extra spaces
    parsed = {
        "content": content,
        "format": input_format
    }
    return parsed

