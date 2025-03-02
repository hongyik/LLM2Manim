# storage.py
import json
import os
from datetime import datetime


# Define the storage file path (e.g., `storage.json` in the current directory)
STORE_FILE = "storage.json"

def save_record(question: dict, code: str, video_path: str):
    """Save a record of a problem-solving session, including the question content, generated code, and video path."""
    
    record = {
        "question": question.get("content", ""),
        "format": question.get("format", ""),
        "code": code,
        "video_path": video_path,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

