# storage.py
import json
import os
from datetime import datetime


# Define the storage file path (e.g., `storage.json` in the current directory)
STORE_FILE = "storage.json"

def save_record(question, animation_prompt=None, manim_code=None, video_path=None, error=None, fix_attempts=0):
    """
    Save a record of the animation generation attempt, including any errors.
    
    Args:
        question (str): The original question or parsed question
        animation_prompt (str, optional): The generated animation description
        manim_code (str, optional): The generated Manim code
        video_path (str, optional): Path to the rendered video file
        error (str, optional): Error message if any step failed
        fix_attempts (int, optional): Number of fix attempts made
    """
    record = {
        'timestamp': datetime.now().isoformat(),
        'question': question,
        'animation_prompt': animation_prompt,
        'manim_code': manim_code,
        'video_path': video_path,
        'error': error,
        'fix_attempts': fix_attempts,
        'status': 'success' if not error else 'failed'
    }
    
    # Read existing records
    data = []
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []  # If the file is corrupted or empty, reset it to an empty list
    
    # Add the new record and write it back to the file
    data.append(record)
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_records():
    """Load all saved records."""
    
    if not os.path.exists(STORE_FILE):
        return []
    
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    
    return data

