"""
Parallel Manim rendering and FFmpeg combine for langchain_agent.
Renders each step's scene in parallel, then concatenates videos in plan order.
"""
import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Config is loaded inside functions to avoid import-time path issues
MANIM_QUALITY_DIRS = ["480p15", "720p30", "1080p60", "2160p60"]


def _render_one(args: Tuple[str, Path, Path, Path, str, str]) -> Tuple[str, Optional[str]]:
    """
    Render a single scene. Designed to be run in a worker process.
    Returns (step_id, output_video_path or None on failure).
    """
    step_id, input_dir, individual_dir, cwd, quality, manim_cli = args
    input_dir = Path(input_dir).resolve()
    individual_dir = Path(individual_dir).resolve()
    cwd = Path(cwd).resolve()
    file_name = f"{step_id.lower()}.py"
    scene_file = input_dir / file_name
    if not scene_file.exists():
        return step_id, None
    output_name = step_id.lower()
    # Run from cwd so manim's media/videos is under cwd; use absolute path for scene file
    cmd = f"{manim_cli} -q {quality} {scene_file} GenScene -o {output_name}"
    try:
        subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return step_id, None
    # Manim writes to media/videos/<relative_dir>/<quality>/<name>.mp4
    # scene_file relative to cwd: e.g. animation_outputs/intro.py -> animation_outputs
    try:
        rel = scene_file.relative_to(cwd)
        parts = rel.parts[:-1]  # directory part
        video_dir = Path(cwd) / "media" / "videos" / Path(*parts) / output_name
    except ValueError:
        video_dir = Path(cwd) / "media" / "videos" / output_name
    video_path = None
    for qdir in MANIM_QUALITY_DIRS:
        candidate = video_dir / qdir / f"{output_name}.mp4"
        if candidate.exists():
            video_path = candidate
            break
    if not video_path or not video_path.exists():
        return step_id, None
    dest = individual_dir / f"{output_name}.mp4"
    shutil.copy(str(video_path), str(dest))
    return step_id, str(dest)


def render_all_parallel(
    step_ids: List[str],
    input_dir: Path,
    output_dir: Path,
    *,
    quality: str = "l",
    manim_cli: str = "python -m manim",
    max_workers: Optional[int] = None,
) -> Dict[str, str]:
    """
    Render each step's scene in parallel. Returns {step_id: path_to_mp4}.
    Skips or fails for missing files; failed steps are omitted from the dict.
    """
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()
    individual_dir = output_dir / "individual_scenes"
    individual_dir.mkdir(parents=True, exist_ok=True)
    cwd = input_dir.parent
    args_list = [
        (sid, input_dir, individual_dir, cwd, quality, manim_cli)
        for sid in step_ids
    ]
    rendered = {}
    if max_workers is None:
        max_workers = max(1, (os.cpu_count() or 2) - 1)
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_render_one, a): a[0] for a in args_list}
        for future in as_completed(futures):
            step_id, path = future.result()
            if path:
                rendered[step_id] = path
    return rendered


def merge_videos_with_ffmpeg(
    step_order: List[str],
    rendered_videos: Dict[str, str],
    output_dir: Path,
) -> Optional[str]:
    """
    Concatenate videos in step_order using FFmpeg. Returns path to combined MP4 or None.
    """
    valid_paths = [rendered_videos[sid] for sid in step_order if sid in rendered_videos]
    if not valid_paths:
        return None
    list_file = output_dir / "video_list.txt"
    final_output = output_dir / "combined_animation.mp4"
    individual_dir = output_dir / "individual_scenes"
    with open(list_file, "w", encoding="utf-8") as f:
        for p in valid_paths:
            name = Path(p).name
            # Paths relative to output_dir for ffmpeg -cwd
            f.write(f"file 'individual_scenes/{name}'\n")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-c:v", "copy",
                "-c:a", "aac",
                "-y",
                str(final_output),
            ],
            check=True,
            capture_output=True,
            cwd=str(output_dir),
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return str(final_output) if final_output.exists() else None


def render_and_combine(
    step_ids: List[str],
    input_dir: Path,
    output_dir: Path,
    *,
    quality: str = "l",
    manim_cli: str = "python -m manim",
) -> Dict[str, Any]:
    """
    Render all steps in parallel, then merge into one video.
    Returns {"rendered": {step_id: path}, "combined_path": path or None, "status": "success"|"partial"|"error"}.
    """
    rendered = render_all_parallel(
        step_ids, input_dir, output_dir, quality=quality, manim_cli=manim_cli
    )
    combined = merge_videos_with_ffmpeg(step_ids, rendered, output_dir)
    status = "success" if combined and len(rendered) == len(step_ids) else (
        "partial" if rendered else "error"
    )
    return {
        "rendered": rendered,
        "combined_path": combined,
        "status": status,
    }
