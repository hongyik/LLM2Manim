"""
Long-term cross-run memory: common Manim errors → standard fix hints.

Purpose:
  When _fix_scene_with_llm encounters an error it has seen before,
  it injects the stored fix hint into the LLM prompt so the model
  doesn't need to rediscover the solution from scratch.

Storage: prompts/error_memory.json  (auto-created on first run)

Lifecycle:
  1. LOOKUP  — before LLM call: MemoryBlock.find_hints(error, category)
               → returns list of matching hint strings
  2. INJECT  — hints injected into _PATCH_USER prompt as "KNOWN FIX FROM MEMORY"
  3. RECORD  — after a successful fix: MemoryBlock.record_success(error, category)
               → increments success_count, saves example error for future matching
  4. SAVE    — written back to disk at end of each scene_fix run

Pattern matching:
  Each stored entry has a `pattern` regex.
  find_hints() returns all entries whose pattern matches the error string.
  Match is case-insensitive and searches the full error text.

Pre-seeded entries:
  Known Manim CE errors are seeded on first load so memory is useful
  from run 1 without requiring any prior successful fix.
"""
import json
import re
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

MEMORY_FILE = Path(__file__).resolve().parent.parent / "prompts" / "error_memory.json"

# ── Pre-seeded known Manim error patterns ─────────────────────────────────────
# key  = "{category}:{short_name}" (stable identifier, never changes)
# Each entry: description, fix_hint (injected into LLM prompt), pattern (regex)
_SEED: Dict[str, dict] = {

    # ── Forbidden colors ──────────────────────────────────────────────────────
    "import:MAGENTA": {
        "description": "MAGENTA is not a valid Manim CE color constant",
        "fix_hint": "Replace MAGENTA with RED or use hex '#FF00FF'. "
                    "Valid colors: RED GREEN BLUE YELLOW ORANGE PURPLE PINK TEAL GOLD MAROON WHITE GRAY BLACK.",
        "pattern": r"\bMAGENTA\b",
    },
    "import:CYAN": {
        "description": "CYAN is not a valid Manim CE color constant",
        "fix_hint": "Replace CYAN with TEAL or TEAL_A, or use hex '#00FFFF'.",
        "pattern": r"\bCYAN\b",
    },
    "import:VIOLET": {
        "description": "VIOLET is not a valid Manim CE color constant",
        "fix_hint": "Replace VIOLET with PURPLE or use hex '#EE82EE'.",
        "pattern": r"\bVIOLET\b",
    },
    "import:INDIGO": {
        "description": "INDIGO is not a valid Manim CE color constant",
        "fix_hint": "Replace INDIGO with PURPLE or DARK_BLUE, or use hex '#4B0082'.",
        "pattern": r"\bINDIGO\b",
    },
    "import:LIME": {
        "description": "LIME is not a valid Manim CE color constant",
        "fix_hint": "Replace LIME with GREEN or GREEN_A, or use hex '#00FF00'.",
        "pattern": r"\bLIME\b",
    },

    # ── API renames / argument errors ─────────────────────────────────────────
    "attribute:camera_frame": {
        "description": "self.camera_frame was renamed to self.camera.frame in Manim >= 0.17",
        "fix_hint": "Replace every occurrence of .camera_frame with .camera.frame.",
        "pattern": r"camera_frame|AttributeError.*camera",
    },
    "api:radians_kwarg": {
        "description": "Rotate() uses angle= keyword, not radians=",
        "fix_hint": "Replace radians=X with angle=X in all Rotate() and similar animation calls.",
        "pattern": r"\bradians\s*=|unexpected keyword.*radians",
    },
    "api:fadein_positional": {
        "description": "FadeIn/FadeOut direction must be a keyword argument (shift=)",
        "fix_hint": "Use FadeIn(obj, shift=UP) instead of FadeIn(obj, UP). "
                    "Direction is always a keyword argument in Manim CE.",
        "pattern": r"FadeIn.*takes.*positional|FadeOut.*takes.*positional|"
                   r"TypeError.*FadeIn|TypeError.*FadeOut",
    },
    "api:wrong_vgroup_string": {
        "description": "VGroup only accepts Mobject instances, not plain strings",
        "fix_hint": "Wrap any string inside Text() or Tex() before adding to VGroup. "
                    "Example: VGroup(Text('label'), equation) not VGroup('label', equation).",
        "pattern": r"VGroup.*str|expected.*Mobject.*got.*str|TypeError.*VGroup",
    },
    "api:dashed_line_zero": {
        "description": "DashedLine/Line with start == end crashes during Create()",
        "fix_hint": "Ensure start and end points are different. "
                    "If computed dynamically, add a guard: if np.allclose(start, end): skip or add small offset.",
        "pattern": r"DashedLine|zero.length|start.*equal.*end|Invalid point",
    },
    "api:create_text_deprecated": {
        "description": "TextMobject is deprecated; use Text() or Tex()",
        "fix_hint": "Replace TextMobject('...') with Text('...') for plain text "
                    "or Tex(r'...') for LaTeX text.",
        "pattern": r"TextMobject|TexMobject",
    },
    "api:number_plane_range": {
        "description": "NumberPlane x_range or y_range too large causes memory issues",
        "fix_hint": "Keep NumberPlane ranges reasonable: x_range=[-7, 7], y_range=[-4, 4]. "
                    "Very large ranges slow rendering significantly.",
        "pattern": r"NumberPlane.*range|MemoryError.*NumberPlane",
    },

    # ── Import errors ─────────────────────────────────────────────────────────
    "import:kokoro_koko": {
        "description": "Old kokoro_mv.koko import path no longer valid",
        "fix_hint": "Replace 'from kokoro_mv.koko import KokoroService' with "
                    "'from kokoro_mv import KokoroService'.",
        "pattern": r"kokoro_mv\.koko|ImportError.*kokoro",
    },
    "import:missing_numpy": {
        "description": "numpy not imported but np.array() or np.* used",
        "fix_hint": "Add 'import numpy as np' at the top of the file.",
        "pattern": r"NameError.*np\.|name 'np' is not defined",
    },
    "import:missing_manim": {
        "description": "Manim symbol used without importing",
        "fix_hint": "Ensure 'from manim import *' is the first import. "
                    "If a specific class is missing, check the Manim CE 0.17+ API — "
                    "some names changed (e.g. GraphScene → Axes).",
        "pattern": r"NameError.*is not defined",
    },

    # ── LaTeX errors ──────────────────────────────────────────────────────────
    "latex:missing_dollar": {
        "description": "LaTeX compilation error: stray $ or missing math mode",
        "fix_hint": "In MathTex(), do NOT add $ or $$ — they are added automatically. "
                    "Use raw strings: MathTex(r'\\frac{d}{dt}'). "
                    "In Tex(), use $...$ (single dollar) for inline math, never $$...$$.",
        "pattern": r"Missing \$|LaTeX Error|pdflatex|! Missing|runaway argument",
    },
    "latex:undefined_control": {
        "description": "LaTeX undefined control sequence in MathTex expression",
        "fix_hint": "Check all LaTeX commands are valid. Common mistakes: "
                    "\\text{} needs amsmath (use Tex() instead), "
                    "\\operatorname{} needs amsmath, "
                    "use r-strings to avoid Python escape issues.",
        "pattern": r"Undefined control sequence|! Undefined|\\mathbf.*error|LaTeX.*undefined",
    },
    "latex:brace_mismatch": {
        "description": "Mismatched braces in LaTeX expression",
        "fix_hint": "Count opening { and closing } in each MathTex argument. "
                    "Every { must have a matching }. "
                    "Split long expressions into multiple string arguments to MathTex().",
        "pattern": r"Extra.*}|Missing.*}|brace|Paragraph ended",
    },

    # ── Voiceover / KokoroService ─────────────────────────────────────────────
    "api:kokoro_model_path": {
        "description": "Old KokoroService API used model_path and voices_path arguments",
        "fix_hint": "Use: self.set_speech_service(KokoroService(voice='af_sarah', lang='en-us')). "
                    "Remove model_path=, voices_path=, and old voice='af' arguments entirely.",
        "pattern": r"model_path|voices_path|unexpected keyword.*model|KokoroService.*got.*unexpected",
    },
    "dependency:sox": {
        "description": "sox audio tool not found — required by manim-voiceover",
        "fix_hint": "This is a system dependency error, not a code error. "
                    "Install sox: https://sox.sourceforge.net/ or 'winget install sox'.",
        "pattern": r"sox.*not.*found|'sox'.*not.*recognized|sox.*command",
    },

    # ── Scene structure errors ────────────────────────────────────────────────
    "syntax:indentation": {
        "description": "Python IndentationError — likely caused by mixed tabs/spaces",
        "fix_hint": "Use 4 spaces per indent level throughout. "
                    "No tabs. Check that all code inside construct() is properly indented.",
        "pattern": r"IndentationError|unexpected indent|unindent does not match",
    },
    "api:self_play_outside": {
        "description": "self.play() called outside construct() or outside a voiceover block incorrectly",
        "fix_hint": "All self.play() calls must be inside construct(). "
                    "Animation code inside 'with self.voiceover(...):' blocks is correct. "
                    "Do not call self.play() inside list comprehensions or lambdas.",
        "pattern": r"self\.play.*outside|cannot call.*play",
    },
    "api:mobject_not_in_scene": {
        "description": "Animating a Mobject that was never added or already removed",
        "fix_hint": "Ensure each object is created and added to the scene before animating. "
                    "Do not FadeOut an object twice. "
                    "Updaters on removed objects cause this error — call clear_updaters() before FadeOut.",
        "pattern": r"not in scene|object.*not.*added|Mobject.*not.*scene|updater.*removed",
    },
}


class MemoryBlock:
    """
    Persistent cross-run memory for Manim error → fix mappings.

    Storage format (error_memory.json):
    {
      "import:MAGENTA": {
        "description": "...",
        "fix_hint": "...",
        "pattern": "...",
        "success_count": 3,
        "last_seen": "2026-03-03",
        "example_errors": ["NameError: name 'MAGENTA' is not defined"]
      },
      ...
    }
    """

    def __init__(self, patches: Dict[str, dict]):
        self._patches = patches   # key -> entry dict

    @classmethod
    def load(cls, path: Path = MEMORY_FILE) -> "MemoryBlock":
        """
        Load from disk. If file doesn't exist, seed from built-in patterns and save.
        Always merges built-in seed so new patterns added to code appear automatically.
        """
        path = Path(path)
        data: Dict[str, dict] = {}

        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}

        # Merge seed: add any new built-in entries, preserve existing runtime fields
        changed = False
        for key, seed_entry in _SEED.items():
            if key not in data:
                data[key] = {**seed_entry, "success_count": 0,
                             "last_seen": "", "example_errors": []}
                changed = True
            else:
                # Update description/fix_hint/pattern from seed (in case they changed)
                for field in ("description", "fix_hint", "pattern"):
                    if data[key].get(field) != seed_entry.get(field):
                        data[key][field] = seed_entry[field]
                        changed = True

        block = cls(data)
        if changed:
            block.save(path)
        return block

    def save(self, path: Path = MEMORY_FILE) -> None:
        """Persist to disk."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._patches, indent=2, ensure_ascii=False),
                        encoding="utf-8")

    # ── Lookup ────────────────────────────────────────────────────────────────

    def find_hints(self, error_text: str, category: str = "") -> List[str]:
        """
        Return fix hints for all entries whose pattern matches error_text.
        Ordered by: category match first, then by success_count descending.
        """
        matches = []
        for key, entry in self._patches.items():
            pat = entry.get("pattern", "")
            if not pat:
                continue
            try:
                if re.search(pat, error_text, re.IGNORECASE | re.DOTALL):
                    # Prefer entries whose key category matches
                    key_category = key.split(":")[0]
                    priority = (key_category == category, entry.get("success_count", 0))
                    matches.append((priority, entry["fix_hint"], key))
            except re.error:
                continue

        matches.sort(key=lambda x: x[0], reverse=True)
        # Return up to 3 most relevant hints (avoid prompt bloat)
        return [hint for _, hint, _ in matches[:3]]

    # ── Recording ─────────────────────────────────────────────────────────────

    def record_success(self, error_text: str, category: str) -> None:
        """
        Record that an error was successfully fixed this run.
        Updates success_count and stores a short example_error snippet.
        Also creates a new entry if the error doesn't match any stored pattern.
        """
        today = str(date.today())
        matched_any = False

        for key, entry in self._patches.items():
            pat = entry.get("pattern", "")
            if not pat:
                continue
            try:
                if re.search(pat, error_text, re.IGNORECASE | re.DOTALL):
                    entry["success_count"] = entry.get("success_count", 0) + 1
                    entry["last_seen"] = today
                    # Store a short snippet for human inspection
                    snippet = error_text.strip()[:200]
                    examples = entry.setdefault("example_errors", [])
                    if snippet not in examples:
                        examples.append(snippet)
                        if len(examples) > 5:
                            examples.pop(0)   # keep only 5 most recent
                    matched_any = True
            except re.error:
                continue

        if not matched_any and category and error_text.strip():
            # Unknown error fixed — store it so future runs benefit
            # Use first line of error as the pattern (escaped for regex)
            first_line = error_text.strip().splitlines()[0][:120]
            key = f"{category}:learned_{abs(hash(first_line)) % 100000}"
            if key not in self._patches:
                self._patches[key] = {
                    "description": f"Learned fix: {first_line[:80]}",
                    "fix_hint": f"This error was successfully fixed in a previous run. "
                                f"Error was: {first_line}",
                    "pattern": re.escape(first_line[:60]),
                    "success_count": 1,
                    "last_seen": today,
                    "example_errors": [error_text.strip()[:200]],
                }

    def summary(self) -> str:
        """Human-readable summary of stored patches (for debugging)."""
        lines = [f"MemoryBlock: {len(self._patches)} entries"]
        for key, entry in sorted(self._patches.items()):
            sc = entry.get("success_count", 0)
            ls = entry.get("last_seen", "never")
            lines.append(f"  {key:<45} success={sc:<3} last={ls}")
        return "\n".join(lines)
