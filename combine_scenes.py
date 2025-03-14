import os
import subprocess
import json
from typing import Dict
from config import MANIM_RENDER_QUALITY
import shutil
from parallel_processing import read_animation_steps_from_json
# Animation steps from parallel_processing
ANIMATION_STEPS, SYSTEM_PROMPTS, USER_PROMPTS = read_animation_steps_from_json("animation_steps.json")

def load_scene_files(input_dir: str) -> Dict[str, str]:
    """Find scene files in the input directory."""
    scene_files = {}
    
    # Load descriptions.json
    descriptions_path = os.path.join(input_dir, "descriptions.json")
    with open(descriptions_path, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    
    # Map step names to file paths
    for step_name in ANIMATION_STEPS:
        if step_name in descriptions:
            file_name = f"{step_name.lower()}.py"
            file_path = os.path.join(input_dir, file_name)
            if os.path.exists(file_path):
                scene_files[step_name] = file_path
    
    return scene_files

def render_single_scene(scene_file: str, output_dir: str) -> str:
    """Render a single scene file."""
    # Extract class name (GenScene) from the file
    class_name = "GenScene"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get output name from file
    scene_file_base = os.path.basename(scene_file)
    output_name = os.path.splitext(scene_file_base)[0]
    
    # Run manim using python -m manim format with correct flag syntax
    # Quality flags should come as options with dashes, not as positional arguments
    cmd = f"python -m manim -q {MANIM_RENDER_QUALITY} {scene_file} {class_name} -o {output_name}"
    print(f"Rendering scene: {output_name}...")
    print(f"Running command: {cmd}")
    subprocess.run(cmd, check=True)    
    
    # Determine output path based on manim's output conventions
    quality_dir = "480p15"
        
    video_output = os.path.join("media", "videos", os.path.splitext(scene_file_base)[0], quality_dir, f"{output_name}.mp4")
    
    # Check if the video exists 
    if not os.path.exists(video_output):
        print(f"Warning: Expected output {video_output} not found.")
        # Try different quality directories
        possible_dirs = ["1080p60", "720p30", "480p15", "2160p60"]
        for try_dir in possible_dirs:
            alt_path = os.path.join("media", "videos", os.path.splitext(scene_file_base)[0], try_dir, f"{output_name}.mp4")
            if os.path.exists(alt_path):
                print(f"Found video at alternate path: {alt_path}")
                video_output = alt_path
                break
    
    # Copy to output directory
    dest_path = os.path.join(output_dir, f"{output_name}.mp4")
    shutil.copy(video_output, dest_path)
    
    return dest_path

def render_scenes_sequential(scene_files: Dict[str, str], output_dir: str) -> Dict[str, str]:
    """Render scenes sequentially one after another."""
    rendered_videos = {}
    
    # Temporary directory for individual rendered videos
    temp_dir = os.path.join(output_dir, "individual_scenes")
    os.makedirs(temp_dir, exist_ok=True)
    print(f"Rendering {len(scene_files)} scenes sequentially...")
    
    # Render each scene in the correct sequence
    for step_name in ANIMATION_STEPS:
        if step_name in scene_files:
            file_path = scene_files[step_name]
            try:
                result = render_single_scene(file_path, temp_dir)
                rendered_videos[step_name] = result
                print(f"✅ Rendered {step_name}")
            except Exception as e:
                print(f"❌ Error rendering {step_name}: {str(e)}")
    
    return rendered_videos

def merge_videos_with_ffmpeg(rendered_videos: Dict[str, str], output_dir: str) -> str:
    """Merge rendered videos using FFmpeg."""
    # Create a file listing all videos to concatenate
    video_list_file = os.path.join(output_dir, "video_list.txt")
    final_output = os.path.join(output_dir, "combined_animation.mp4")
    
    # Create list of video files in the correct sequence
    valid_videos = []
    for step_name in ANIMATION_STEPS:
        if step_name in rendered_videos:
            valid_videos.append(rendered_videos[step_name])
    
    # Create the video list file for ffmpeg - using only folder and filename
    with open(video_list_file, 'w', encoding='utf-8') as f:
        for video_path in valid_videos:
            # Extract just the folder and filename parts
            # This avoids issues with Chinese characters in the full path
            relative_path = os.path.join("individual_scenes", os.path.basename(video_path))
            f.write(f"file '{relative_path}'\n")
    
    # Merge videos using ffmpeg
    ffmpeg_cmd = [
        "ffmpeg", 
        "-f", "concat", 
        "-safe", "0", 
        "-i", video_list_file, 
        "-c", "copy",  # Copy without re-encoding for speed
        "-y",  # Overwrite output file if it exists
        final_output
    ]
    
    print(f"Running FFmpeg to merge {len(valid_videos)} videos...")
    try:
        # Change to the output directory before running ffmpeg
        # This makes the relative paths in the file list work correctly
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.join(current_dir, output_dir)))
        
        subprocess.run(ffmpeg_cmd, check=True)
        
        # Change back to the original directory
        os.chdir(current_dir)
        
        if os.path.exists(final_output):
            print(f"Successfully merged videos to: {final_output}")
        else:
            print(f"Warning: FFmpeg ran but output file not found at {final_output}")
    except Exception as e:
        print(f"Error running FFmpeg: {e}")
        # Change back to the original directory if an error occurred
        if os.getcwd() != current_dir:
            os.chdir(current_dir)
    
    return final_output

def render_combined_scene(input_dir: str = "animation_outputs", output_dir: str = "final_animation") -> str:
    """Render individual scenes and merge them into a final animation."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load scene files
    print(f"Loading scene files from {input_dir}...")
    scene_files = load_scene_files(input_dir)
    print(f"Found {len(scene_files)} scene files")
    
    # Render scenes sequentially
    rendered_videos = render_scenes_sequential(scene_files, output_dir)
    
    # Merge videos using FFmpeg
    print("Merging videos with FFmpeg...")
    final_video = merge_videos_with_ffmpeg(rendered_videos, output_dir)
    print(f"Combined animation created at: {final_video}")
    
    return final_video

if __name__ == "__main__":
    # Test the function directly if this script is run
    # scene_files = {"reynolds": "ReynoldsTransportation.py","renolds_transportation": "ReynoldsTransportationcopy.py"}
    # #render_scenes_sequential(scene_files,"final_animation")
    #render_single_scene("example/ReynoldsTransportation.py","final_animation")
    render_combined_scene("animation_outputs","final_animation")
