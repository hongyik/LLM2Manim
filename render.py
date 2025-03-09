# render.py
import os
import subprocess
import logging
import uuid 
from config import MANIM_CLI_PATH, MANIM_RENDER_QUALITY
import re
import shutil

def render_animation(raw_text: str, output_dir: str = "./outputs") -> str:
    """Extracts Manim Python code from raw text, renames the class to GenScene, and saves it as a Python file."""

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename
    temp_filename = f"gen_scene_{uuid.uuid4().hex}.py"
    temp_filepath = os.path.join(output_dir, temp_filename)

    # Split and extract the code part
    parts = raw_text.split("```python")
    if len(parts) > 1:
        python_code = parts[1].split("```")[0].strip()  # Extracts the code block
    else:
        # If no code block markers found, treat the entire input as code
        python_code = raw_text.strip()

    # Replace class name with GenScene if it's not already GenScene
    class_pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\):'
    if 'class GenScene(Scene):' not in python_code:
        python_code = re.sub(class_pattern, 'class GenScene(Scene):', python_code)

    # Save the modified code to a Python file
    with open(temp_filepath, "w", encoding="utf-8") as f:
        f.write(python_code)
    
    print(f"Python code extracted, class renamed to GenScene, and saved as {temp_filepath}")

    # Construct the Manim rendering command
    manim_command = [
        MANIM_CLI_PATH or "manim", 
        temp_filepath,        
        "-q", MANIM_RENDER_QUALITY,  
        "--disable_caching",  
        "-o", f"{temp_filename}.mp4",  
        "GenScene"  
    ]
    
    try:
        print(f"Executing Manim command: {' '.join(manim_command)}")
        subprocess.run(manim_command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Manim rendering failed: {e}")
        raise RuntimeError("Animation rendering failed. Please check if the generated code is correct.")
    
    # Construct the output video path
    video_path = os.path.join("media", "videos", os.path.splitext(temp_filename)[0], "480p15", f"{temp_filename}.mp4")
    if not os.path.exists(video_path):
        raise RuntimeError("The rendering process did not generate the expected video file.")
    
    # Copy the video file to the outputs directory
    output_video_path = os.path.join(output_dir, f"{temp_filename}.mp4")
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    shutil.copy2(video_path, output_video_path)
    
    return output_video_path

