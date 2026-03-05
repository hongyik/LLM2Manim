"""
Parallel Manim rendering and FFmpeg combine for langchain_agent.
Renders each step's scene in parallel, then concatenates videos in plan order.
"""
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import ROOT_DIR

# Config is loaded inside functions to avoid import-time path issues
MANIM_QUALITY_DIRS = ["480p15", "720p30", "1080p60", "2160p60"]


def _render_one(args: Tuple[str, Path, Path, Path, str, str]) -> Tuple[str, Optional[str], str]:
    """
    Render a single scene. Designed to be run in a worker process.
    Returns (step_id, output_video_path or None on failure, error_msg).
    """
    step_id, input_dir, individual_dir, cwd, quality, manim_cli = args
    input_dir = Path(input_dir).resolve()
    individual_dir = Path(individual_dir).resolve()
    cwd = Path(cwd).resolve()
    file_name = f"{step_id.lower()}.py"
    scene_file = input_dir / file_name
    if not scene_file.exists():
        return step_id, None, "scene file not found"
    output_name = step_id.lower()
    # Run from project root so kokoro model files are found and media/ is written there
    cmd = f"{manim_cli} -q {quality} {scene_file} GenScene -o {output_name}"
    env = {**os.environ, "PYTHONUTF8": "1"}
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        if result.returncode != 0:
            raw_err = (result.stderr or result.stdout or "").strip()
            # Strip UserWarning/DeprecationWarning lines (and their indented continuation)
            import re as _re
            _warn_pat = _re.compile(
                r"^\s*.*?: (UserWarning|DeprecationWarning|FutureWarning)", _re.MULTILINE
            )
            filtered, skip_next = [], False
            for ln in raw_err.splitlines():
                if _warn_pat.match(ln):
                    skip_next = True
                    continue
                if skip_next and ln.startswith("  "):
                    continue  # keep skipping all indented continuation lines
                skip_next = False
                filtered.append(ln)
            err = "\n".join(filtered).strip() or raw_err
            first = err.splitlines()[0][:120] if err else "non-zero exit"
            return step_id, None, first
    except subprocess.TimeoutExpired:
        return step_id, None, "render timed out (300s)"
    except subprocess.CalledProcessError as e:
        return step_id, None, str(e)
    # Manim writes to media/videos/<stem>/<quality>/<name>.mp4 relative to cwd
    video_dir = Path(cwd) / "media" / "videos" / output_name
    video_path = None
    for qdir in MANIM_QUALITY_DIRS:
        candidate = video_dir / qdir / f"{output_name}.mp4"
        if candidate.exists():
            video_path = candidate
            break
    if not video_path or not video_path.exists():
        return step_id, None, "rendered but output .mp4 not found"
    dest = individual_dir / f"{output_name}.mp4"
    shutil.copy(str(video_path), str(dest))
    return step_id, str(dest), ""


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
    cwd = ROOT_DIR  # project root: kokoro model files live here, media/ written here
    args_list = [
        (sid, input_dir, individual_dir, cwd, quality, manim_cli)
        for sid in step_ids
    ]
    rendered = {}
    if max_workers is None:
        # Kokoro TTS is memory-intensive; cap at 2 to avoid OOM when running in parallel.
        max_workers = 2
    print(f"   Rendering {len(step_ids)} scene(s) in parallel (max {max_workers} workers)...")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_render_one, a): a[0] for a in args_list}
        for future in as_completed(futures):
            step_id, path, err = future.result()
            if path:
                rendered[step_id] = path
                print(f"   [OK]   {step_id} -> {Path(path).name}")
            else:
                print(f"   [FAIL] {step_id}: {err}")
    return rendered


def merge_videos_with_ffmpeg(
    step_order: List[str],
    rendered_videos: Dict[str, str],
    output_dir: Path,
) -> Optional[str]:
    """
    Concatenate videos in step_order using FFmpeg. Returns path to combined MP4 or None.
    """
    valid = [sid for sid in step_order if sid in rendered_videos]
    valid_paths = [rendered_videos[sid] for sid in valid]
    if not valid_paths:
        print("   No rendered videos to merge.")
        return None
    print(f"   Merging {len(valid_paths)}/{len(step_order)} scene(s) with FFmpeg...")
    list_file = output_dir / "video_list.txt"
    final_output = output_dir / "combined_animation.mp4"
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
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"   FFmpeg merge failed: {e}")
        return None
    if final_output.exists():
        print(f"   Combined video: {final_output}")
        return str(final_output)
    return None


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
    failed = [sid for sid in step_ids if sid not in rendered]
    if failed:
        print(f"   Scenes that failed to render: {failed}")
    combined = merge_videos_with_ffmpeg(step_ids, rendered, output_dir)
    status = "success" if combined and len(rendered) == len(step_ids) else (
        "partial" if rendered else "error"
    )
    return {
        "rendered": rendered,
        "combined_path": combined,
        "status": status,
    }
