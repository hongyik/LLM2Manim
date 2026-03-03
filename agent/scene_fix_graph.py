"""
LangGraph-based auto-fix for Manim scenes.

Graph:  api_check -> (violations) -> fix -> api_check -> ...
                  -> (ok)         -> validate -> (fail) -> fix -> api_check -> ...
                                             -> (ok)   -> END

Improvements:
  A) api_check node: fast AST scan before the expensive manim subprocess.
     Catches undefined names, forbidden color constants, and syntax errors
     with precise line numbers — giving the LLM better fix context.
  B) Patch-first: LLM returns targeted SEARCH/REPLACE diffs; falls back to
     full rewrite only if patches fail to apply.
  C) Error classification: maps stderr patterns to fix hints so the LLM
     targets the right kind of fix (import, API, LaTeX, syntax, ...).
  D) Invariant enforcement: after every fix, verifies that GenScene still
     exists, KokoroService call is intact, and the file is syntactically valid.
"""
import ast
import asyncio
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import MANIM_CLI, MANIM_RENDER_QUALITY, ROOT_DIR
from .llm import get_llm
from .api_check import check_scene


class SceneFixState(TypedDict):
    file_path: str
    code: str
    error: str
    error_category: str
    attempt: int
    max_attempts: int
    status: Literal["pending", "ok", "fail"]
    history: List[Dict[str, Any]]   # per-attempt failure log written to report file


# ──────────────────────────────────────────────────────────────────────────────
# B) Error classification
# ──────────────────────────────────────────────────────────────────────────────

_ERROR_PATTERNS: List[Tuple[str, List[str]]] = [
    # dependency must be checked first — these are unfixable by code edits
    ("dependency", [r"'sox' is not recognized", r"sox.*not found",
                    r"command not found.*sox", r"ffmpeg.*not recognized",
                    r"ffmpeg.*not found", r"no such file or directory.*sox"]),
    ("import",    [r"NameError.*not defined", r"ImportError", r"ModuleNotFoundError"]),
    ("api",       [r"TypeError.*argument", r"TypeError.*takes", r"TypeError.*got",
                   r"TypeError.*unexpected"]),
    ("attribute", [r"AttributeError"]),
    ("latex",     [r"LaTeX", r"pdflatex", r"! Missing", r"! Undefined",
                   r"Missing \$"]),
    ("syntax",    [r"SyntaxError", r"IndentationError"]),
    ("timeout",   [r"TimeoutExpired", r"timed out"]),
]

_ERROR_HINTS: Dict[str, str] = {
    "dependency": "Missing system binary (sox, ffmpeg, etc.). "
                  "This cannot be fixed by code changes — install the missing tool.",
    "import":    "A name is undefined or an import is missing. "
                 "Add the correct import (from manim import *, numpy, etc.). "
                 "If it is an unknown color name (e.g. MAGENTA, CYAN, VIOLET), "
                 "replace it with a valid Manim color: RED, GREEN, BLUE, YELLOW, "
                 "ORANGE, PURPLE, PINK, TEAL, GOLD, MAROON, WHITE, GRAY, BLACK.",
    "api":       "A function is called with wrong arguments. "
                 "Check Manim's API for the correct signature.",
    "attribute": "A method or attribute does not exist on that object. "
                 "Check Manim docs for the correct attribute name.",
    "latex":     "LaTeX compilation failed. "
                 "Use raw strings r'...', check braces/dollars in MathTex expressions.",
    "syntax":    "Python syntax or indentation error. Fix the offending line.",
    "timeout":   "Manim timed out. Reduce run_time, simplify animations.",
    "unknown":   "Analyze the full traceback and apply the most targeted fix possible.",
}


def _classify_error(error: str) -> str:
    for category, patterns in _ERROR_PATTERNS:
        for pat in patterns:
            if re.search(pat, error, re.IGNORECASE):
                return category
    return "unknown"


# ──────────────────────────────────────────────────────────────────────────────
# A) SEARCH/REPLACE patch system
# ──────────────────────────────────────────────────────────────────────────────

_PATCH_SYSTEM = """\
You are an expert Manim CE (v0.17+) debugging assistant. Fix ONLY the reported error.

MANIM API CONSTRAINTS (enforce in every fix):
- Valid colors: RED GREEN BLUE YELLOW ORANGE PURPLE PINK TEAL GOLD MAROON WHITE GRAY BLACK DARK_BLUE and variants (RED_A..RED_E etc). Use hex "#RRGGBB" for others. NEVER: MAGENTA CYAN VIOLET.
- Rotate: use angle= kwarg, NEVER radians=.
- Camera: self.camera.frame — NEVER self.camera_frame.
- VGroup: only Mobject instances, never strings.
- DashedLine/Line: start and end must be different points (non-zero length).
- MathTex: use raw strings r"..."; do NOT add $ or $$ — MathTex wraps automatically.
- FadeIn/FadeOut direction: keyword only — FadeIn(mob, shift=UP), not FadeIn(mob, UP).

Return one or more targeted SEARCH/REPLACE patches. Do NOT rewrite the whole file.

Patch format (use exactly — markers on their own lines):
<<<SEARCH>>>
[exact verbatim lines from the original code — enough context to be unique]
<<<REPLACE>>>
[fixed replacement lines]
<<<END>>>

Rules:
- Each SEARCH block MUST match verbatim text in the original file.
- Make the smallest change that fixes the error.
- NEVER change: the class name GenScene, the KokoroService(voice="af_sarah", lang="en-us") call.
- If multiple separate edits are needed, emit multiple patch blocks.
- FULL_REWRITE is allowed ONLY if the error requires restructuring too large for patches.
  In that case write exactly: FULL_REWRITE
  followed by the complete corrected file in ```python ... ```.\
"""

_PATCH_USER = """\
Manim scene failed to render.

Error category: {category}
Fix hint: {hint}

Error output (stderr/stdout):
{error}

Original code:
```python
{code}
```

Return patch(es). If a full rewrite is truly necessary, write FULL_REWRITE then the code.
Preserve: class GenScene, KokoroService(voice="af_sarah", lang="en-us"), all step logic.\
"""


def _parse_patches(raw: str) -> List[Tuple[str, str]]:
    """Extract (search, replace) pairs from LLM patch response."""
    return [
        (m.group(1).strip(), m.group(2).strip())
        for m in re.finditer(
            r"<<<SEARCH>>>(.*?)<<<REPLACE>>>(.*?)<<<END>>>", raw, re.DOTALL
        )
        if m.group(1).strip()
    ]


def _apply_patches(code: str, patches: List[Tuple[str, str]]) -> Tuple[str, List[str]]:
    """Apply SEARCH/REPLACE patches. Returns (patched_code, list_of_failed_searches)."""
    failed = []
    for search, replace in patches:
        if search in code:
            code = code.replace(search, replace, 1)
        else:
            failed.append(search.splitlines()[0][:60] if search else "")
    return code, failed


def _extract_full_rewrite(raw: str) -> Optional[str]:
    """Extract code from a FULL_REWRITE response."""
    if "FULL_REWRITE" not in raw:
        return None
    m = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    idx = raw.index("FULL_REWRITE") + len("FULL_REWRITE")
    code = raw[idx:].strip()
    return code or None


# ──────────────────────────────────────────────────────────────────────────────
# C) Invariant enforcement
# ──────────────────────────────────────────────────────────────────────────────

def _check_invariants(code: str) -> List[str]:
    """Return list of violated invariants (empty list = all good)."""
    violations = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        violations.append(f"SyntaxError after patch: {e}")
    if "class GenScene" not in code:
        violations.append("GenScene class missing")
    if "KokoroService" not in code:
        violations.append("KokoroService call missing")
    return violations


def _sanitize(code: str) -> str:
    """Normalize Kokoro import/call and fix common manim API mistakes."""
    code = code.replace(
        "from kokoro_mv.koko import KokoroService",
        "from kokoro_mv import KokoroService",
    )
    code = re.sub(
        r"self\.set_speech_service\s*\(\s*KokoroService\s*\([^)]*\)\s*\)",
        'self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))',
        code, count=1, flags=re.DOTALL,
    )
    # camera_frame was renamed to camera.frame in manim >= 0.17
    code = code.replace(".camera_frame", ".camera.frame")
    # Rotate/animation 'radians=' kwarg should be 'angle='
    code = re.sub(r"\bradians\s*=", "angle=", code)
    # Upgrade GenScene(VoiceoverScene) -> GenScene(ThreeDScene, VoiceoverScene)
    # so all scenes have 3D camera access (matches verified example files)
    code = re.sub(
        r"\bclass\s+GenScene\s*\(\s*VoiceoverScene\s*\)",
        "class GenScene(ThreeDScene, VoiceoverScene)",
        code,
    )
    return code.strip()


# ──────────────────────────────────────────────────────────────────────────────
# LangGraph nodes
# ──────────────────────────────────────────────────────────────────────────────

def _api_check_node(state: SceneFixState) -> SceneFixState:
    """
    Fast AST pre-check BEFORE the expensive manim subprocess.
    Catches undefined names, forbidden color constants, and syntax errors
    with precise line numbers so the LLM fix prompt is maximally informative.
    Sets status='pending' (→ proceed to validate) or status='fail'.
    """
    file_path = Path(state["file_path"])
    attempt = state.get("attempt", 0)
    label = f"{file_path.stem}" + (f" (attempt {attempt})" if attempt else "")

    history: List[Dict[str, Any]] = list(state.get("history") or [])

    if not file_path.exists():
        err = f"File not found: {file_path}"
        history.append({"attempt": attempt, "node": "api_check", "category": "unknown",
                        "error": err})
        return {**state, "status": "fail", "error": err,
                "error_category": "unknown", "history": history}

    source = file_path.read_text(encoding="utf-8")
    result = check_scene(source, filename=str(file_path))

    if result["syntax_error"]:
        err = f"SyntaxError: {result['syntax_error']}"
        print(f"     [API]  {label}: {err[:100]}")
        history.append({"attempt": attempt, "node": "api_check", "category": "syntax",
                        "error": err})
        return {**state, "status": "fail", "error": err, "error_category": "syntax",
                "history": history}

    if result["violations"]:
        lines = "\n".join(f"  - {v}" for v in result["violations"])
        err = f"API violations (caught before running manim):\n{lines}"
        first = result["violations"][0][:100]
        print(f"     [API]  {label}: {first}")
        history.append({"attempt": attempt, "node": "api_check", "category": "import",
                        "error": err})
        return {**state, "status": "fail", "error": err, "error_category": "import",
                "history": history}

    # All clear — proceed to the full manim render
    return {**state, "status": "pending", "error": "", "error_category": "",
            "history": history}


def _route_after_api_check(state: SceneFixState) -> Literal["fix", "validate", "__end__"]:
    if state["status"] == "pending":       # api_check passed → run manim
        return "validate"
    if state.get("error_category") == "dependency":
        return "__end__"
    if state.get("attempt", 0) >= state.get("max_attempts", 2):
        return "__end__"
    return "fix"


def _validate_scene(state: SceneFixState) -> SceneFixState:
    """Run manim on the scene file; set status='ok' or 'fail'."""
    file_path = Path(state["file_path"])
    attempt = state.get("attempt", 0)
    label = f"{file_path.stem} (attempt {attempt})" if attempt else file_path.stem
    print(f"     Validating {label}...")

    history: List[Dict[str, Any]] = list(state.get("history") or [])

    if not file_path.exists():
        err = f"File not found: {file_path}"
        print(f"     [FAIL] {file_path.stem}: file not found")
        history.append({"attempt": attempt, "node": "validate", "category": "unknown",
                        "error": err})
        return {**state, "status": "fail", "error": err,
                "error_category": "unknown", "history": history}

    cwd = ROOT_DIR  # project root: kokoro model files live here
    out_name = file_path.stem
    cmd = f"{MANIM_CLI} -q {MANIM_RENDER_QUALITY} {file_path} GenScene -o {out_name}"
    env = {**os.environ, "PYTHONUTF8": "1"}
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=str(cwd), env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        err = "Manim render timed out (120s)."
        print(f"     [FAIL] {file_path.stem}: {err}")
        history.append({"attempt": attempt, "node": "validate", "category": "timeout",
                        "error": err})
        return {**state, "status": "fail", "error": err, "error_category": "timeout",
                "history": history}
    except Exception as e:
        err = str(e)
        print(f"     [FAIL] {file_path.stem}: {err}")
        history.append({"attempt": attempt, "node": "validate", "category": "unknown",
                        "error": err})
        return {**state, "status": "fail", "error": err, "error_category": "unknown",
                "history": history}

    if result.returncode == 0:
        print(f"     [OK]   {file_path.stem}")
        return {**state, "status": "ok", "error": "", "error_category": "",
                "history": history}

    raw_err = (result.stderr or result.stdout or "Unknown error").strip()

    # Strip Python UserWarning/DeprecationWarning header lines (e.g. from pkg_resources)
    # so the real error is visible and the LLM targets the actual failure.
    _warn_pat = re.compile(r"^\s*.*?: (UserWarning|DeprecationWarning|FutureWarning)", re.MULTILINE)
    filtered_lines = []
    skip_next = False
    for line in raw_err.splitlines():
        if _warn_pat.match(line):
            skip_next = True   # also skip the "  import pkg_resources" continuation line
            continue
        if skip_next and line.startswith("  "):
            continue  # keep skipping all indented continuation lines
        skip_next = False
        filtered_lines.append(line)
    err = "\n".join(filtered_lines).strip() or raw_err

    category = _classify_error(err)
    first_line = err.splitlines()[0] if err else "unknown error"
    print(f"     [FAIL] {file_path.stem} [{category}]: {first_line[:120]}")
    history.append({"attempt": attempt, "node": "validate", "category": category,
                    "error": err[:2000]})
    return {**state, "status": "fail", "error": err[:3000], "error_category": category,
            "history": history}


def _fix_scene_with_llm(state: SceneFixState) -> SceneFixState:
    """Patch the scene code with targeted SEARCH/REPLACE edits; fall back to full rewrite."""
    file_path = Path(state["file_path"])
    original_code = state.get("code") or file_path.read_text(encoding="utf-8")
    error = state.get("error", "")
    category = state.get("error_category", "unknown")
    hint = _ERROR_HINTS.get(category, _ERROR_HINTS["unknown"])
    attempt = state.get("attempt", 0) + 1
    max_attempts = state.get("max_attempts", 2)

    print(f"     Patching {file_path.stem} [{category}] (attempt {attempt}/{max_attempts})...")

    llm = get_llm(stage="code", temperature=0.2, max_tokens=4096)
    user_content = _PATCH_USER.format(
        category=category, hint=hint, error=error, code=original_code,
    )
    messages = [SystemMessage(content=_PATCH_SYSTEM), HumanMessage(content=user_content)]
    response = llm.invoke(messages)
    raw = response.content if hasattr(response, "content") else str(response)

    # A) Try targeted patches first
    patches = _parse_patches(raw)
    fixed = original_code

    if patches:
        patched, failed = _apply_patches(original_code, patches)
        if not failed:
            print(f"     Applied {len(patches)} patch(es).")
            fixed = patched
        else:
            print(f"     {len(failed)} patch(es) didn't match; falling back to full rewrite.")
            full = _extract_full_rewrite(raw)
            if full:
                fixed = full
            else:
                # Partial success: keep what applied
                fixed = patched
    else:
        # No patches — check for FULL_REWRITE
        full = _extract_full_rewrite(raw)
        if full:
            print(f"     Full rewrite accepted.")
            fixed = full
        else:
            # Last resort: treat raw output as code
            m = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
            fixed = m.group(1).strip() if m else raw.strip()
            print(f"     No structured output found; treating raw response as code.")

    fixed = _sanitize(fixed)

    # C) Invariant check — don't write if broken
    violations = _check_invariants(fixed)
    if violations:
        print(f"     Invariant violations after fix: {violations}. Keeping original.")
        fixed = original_code

    file_path.write_text(fixed, encoding="utf-8")
    history: List[Dict[str, Any]] = list(state.get("history") or [])
    history.append({"attempt": attempt, "node": "fix", "category": category,
                    "fix_strategy": "patch" if patches else "rewrite"})
    return {**state, "code": fixed, "attempt": attempt, "max_attempts": max_attempts,
            "status": "pending", "history": history}


def _route_after_validate(state: SceneFixState) -> Literal["fix", "__end__"]:
    if state["status"] == "ok":
        return "__end__"
    if state.get("error_category") == "dependency":
        print(f"     [SKIP] {Path(state['file_path']).stem}: system dependency missing "
              f"({_ERROR_HINTS['dependency']})")
        return "__end__"
    if state.get("attempt", 0) >= state.get("max_attempts", 2):
        return "__end__"
    return "fix"


def build_scene_fix_graph() -> StateGraph:
    """
    Build the scene fix graph:
      api_check → (violations) → fix → api_check → ...
                → (ok)        → validate → (fail) → fix → api_check → ...
                                         → (ok)   → END
    After every fix, api_check runs first (cheap AST scan) before the
    expensive manim subprocess, catching obvious regressions immediately.
    """
    graph = StateGraph(SceneFixState)
    graph.add_node("api_check", _api_check_node)
    graph.add_node("validate", _validate_scene)
    graph.add_node("fix", _fix_scene_with_llm)
    graph.add_conditional_edges(
        "api_check", _route_after_api_check,
        {"fix": "fix", "validate": "validate", "__end__": END},
    )
    graph.add_conditional_edges(
        "validate", _route_after_validate, {"fix": "fix", "__end__": END}
    )
    graph.add_edge("fix", "api_check")   # after every fix, re-check API first
    graph.set_entry_point("api_check")
    return graph.compile()


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def run_auto_fix_for_scene(
    file_path: str | Path,
    max_attempts: int = 2,
) -> Dict[str, Any]:
    """Run the LangGraph auto-fix for a single scene file (synchronously)."""
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        return {"fixed": False, "error": "File not found", "attempts": 0, "history": []}
    code = file_path.read_text(encoding="utf-8")
    initial: SceneFixState = {
        "file_path": str(file_path),
        "code": code,
        "error": "",
        "error_category": "",
        "attempt": 0,
        "max_attempts": max_attempts,
        "status": "pending",
        "history": [],
    }
    app = build_scene_fix_graph()
    final = app.invoke(initial)
    return {
        "fixed": final.get("status") == "ok",
        "attempts": final.get("attempt", 0),
        "final_error": final.get("error", ""),
        "file_path": str(file_path),
        "history": final.get("history", []),
    }


async def _auto_fix_scene_async(
    file_path: Path,
    max_attempts: int = 2,
) -> Dict[str, Any]:
    """Async variant for parallel execution via ainvoke()."""
    file_path = file_path.resolve()
    if not file_path.exists():
        return {"fixed": False, "error": "File not found", "attempts": 0,
                "file_path": str(file_path), "history": []}
    code = file_path.read_text(encoding="utf-8")
    initial: SceneFixState = {
        "file_path": str(file_path),
        "code": code,
        "error": "",
        "error_category": "",
        "attempt": 0,
        "max_attempts": max_attempts,
        "status": "pending",
        "history": [],
    }
    app = build_scene_fix_graph()
    final = await app.ainvoke(initial)
    return {
        "fixed": final.get("status") == "ok",
        "attempts": final.get("attempt", 0),
        "final_error": final.get("error", ""),
        "file_path": str(file_path),
        "history": final.get("history", []),
    }


def run_auto_fix_for_all_scenes(
    step_ids: list,
    output_dir: Path,
    max_attempts_per_scene: int = 2,
) -> Dict[str, Any]:
    """
    For each step's scene file, run the LangGraph scene-fix loop in parallel.
    Returns summary: fixed list, still_failed list, details per file.
    """
    async def _run_all() -> Dict[str, Any]:
        results: Dict[str, Any] = {"fixed": [], "still_failed": [], "details": {}}
        tasks: List[asyncio.Task] = []
        task_ids: List[str] = []

        for step_id in step_ids:
            path = output_dir / f"{step_id.lower()}.py"
            if not path.exists():
                results["details"][step_id] = {"error": "file not found"}
                continue
            task_ids.append(step_id)
            tasks.append(asyncio.create_task(
                _auto_fix_scene_async(path, max_attempts=max_attempts_per_scene)
            ))

        if not tasks:
            return results

        scene_results = await asyncio.gather(*tasks)

        for step_id, scene_result in zip(task_ids, scene_results):
            results["details"][step_id] = scene_result
            if scene_result.get("fixed"):
                results["fixed"].append(step_id)
                print(f"   Scene {step_id}: OK ({scene_result.get('attempts', 0)} attempt(s))")
            else:
                results["still_failed"].append(step_id)
                err = scene_result.get("final_error") or ""
                first = err.splitlines()[0][:100] if err else "unknown"
                print(f"   Scene {step_id}: FAILED after {scene_result.get('attempts', 0)} attempt(s) -- {first}")

        _write_validation_report(results, output_dir)
        return results

    return asyncio.run(_run_all())


def _write_validation_report(results: Dict[str, Any], output_dir: Path) -> None:
    """Write validation_report.json and validation_report.txt to output_dir."""
    output_dir = Path(output_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── JSON (full detail) ────────────────────────────────────────────────────
    report_json = {
        "generated": timestamp,
        "summary": {
            "fixed": results.get("fixed", []),
            "still_failed": results.get("still_failed", []),
        },
        "scenes": {},
    }
    for step_id, detail in results.get("details", {}).items():
        report_json["scenes"][step_id] = {
            "fixed": detail.get("fixed", False),
            "attempts": detail.get("attempts", 0),
            "final_error": detail.get("final_error", ""),
            "history": detail.get("history", []),
        }
    json_path = output_dir / "validation_report.json"
    json_path.write_text(json.dumps(report_json, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── TXT (human-readable) ──────────────────────────────────────────────────
    lines: List[str] = [
        "SCENE VALIDATION REPORT",
        f"Generated : {timestamp}",
        f"Fixed     : {', '.join(results.get('fixed', [])) or '(none)'}",
        f"Failed    : {', '.join(results.get('still_failed', [])) or '(none)'}",
        "",
    ]
    for step_id, detail in results.get("details", {}).items():
        fixed = detail.get("fixed", False)
        attempts = detail.get("attempts", 0)
        status = "FIXED" if fixed else "FAILED"
        lines.append("=" * 60)
        lines.append(f"SCENE: {step_id}  [{status} after {attempts} attempt(s)]")
        lines.append("=" * 60)
        history: List[Dict] = detail.get("history", [])
        if not history:
            lines.append("  (no failure history recorded — passed on first try)")
        for entry in history:
            node = entry.get("node", "?")
            cat = entry.get("category", "?")
            att = entry.get("attempt", "?")
            if node == "fix":
                strategy = entry.get("fix_strategy", "?")
                lines.append(f"  attempt {att} → fix ({strategy}, error type: {cat})")
            else:
                err_text = entry.get("error", "")
                # Show first 3 lines of error, indented
                err_lines = [l for l in err_text.splitlines() if l.strip()][:3]
                lines.append(f"  attempt {att} [{node}] [{cat}]:")
                for el in err_lines:
                    lines.append(f"      {el.strip()[:120]}")
        if not fixed:
            final_err = detail.get("final_error", "")
            if final_err:
                lines.append("  --- FINAL ERROR (first 5 lines) ---")
                for el in [l for l in final_err.splitlines() if l.strip()][:5]:
                    lines.append(f"      {el.strip()[:120]}")
        lines.append("")

    txt_path = output_dir / "validation_report.txt"
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n   Validation report written to: {txt_path}")
    print(f"   Full JSON report            : {json_path}")
