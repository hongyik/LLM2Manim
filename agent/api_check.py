"""
Fast AST-based pre-check for Manim scene files.

Runs BEFORE the expensive manim subprocess:
  1. Syntax check (ast.parse)
  2. Undefined name check (AST scan vs. manim allowlist + local defs)

Usage:
  from agent.api_check import check_scene, generate_allowlist

  # Generate/update allowlist from installed manim (run once per manim upgrade):
  #   python -m agent.api_check
"""
import ast
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

ALLOWLIST_FILE = Path(__file__).resolve().parent.parent / "prompts" / "manim_allowlist.json"

# Python builtins always in scope
import builtins as _builtins_mod
_BUILTINS: Set[str] = set(dir(_builtins_mod))
_BUILTINS.update({
    "True", "False", "None", "print", "range", "len", "list", "dict",
    "set", "tuple", "str", "int", "float", "bool", "enumerate", "zip",
    "map", "filter", "max", "min", "abs", "sum", "round", "sorted",
    "isinstance", "issubclass", "type", "super", "hasattr", "getattr",
    "setattr", "vars", "dir", "id", "repr", "hash", "any", "all",
    "open", "iter", "next", "reversed", "object", "property",
    "staticmethod", "classmethod", "NotImplemented",
})

# Names always in scope from the project's required import template
_ALWAYS_ALLOWED: Set[str] = {
    "VoiceoverScene", "KokoroService",          # explicit imports
    "np",                                        # numpy alias
    # Manim math/direction constants (exported via manim.*)
    "PI", "TAU", "E", "DEGREES",
    "UP", "DOWN", "LEFT", "RIGHT", "ORIGIN",
    "UR", "UL", "DR", "DL", "IN", "OUT",
    # Manim color constants safe to use
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE", "PINK",
    "TEAL", "GOLD", "MAROON", "WHITE", "GRAY", "GREY", "BLACK",
    "DARK_BLUE", "DARK_BROWN", "DARK_GRAY", "DARK_GREY",
    "LIGHT_GRAY", "LIGHT_GREY", "LIGHT_PINK", "LIGHT_BROWN",
    "RED_A", "RED_B", "RED_C", "RED_D", "RED_E",
    "GREEN_A", "GREEN_B", "GREEN_C", "GREEN_D", "GREEN_E",
    "BLUE_A", "BLUE_B", "BLUE_C", "BLUE_D", "BLUE_E",
    "YELLOW_A", "YELLOW_B", "YELLOW_C", "YELLOW_D", "YELLOW_E",
    "ORANGE_A", "ORANGE_B", "ORANGE_C", "ORANGE_D", "ORANGE_E",
    "GOLD_A", "GOLD_B", "GOLD_C", "GOLD_D", "GOLD_E",
    "TEAL_A", "TEAL_B", "TEAL_C", "TEAL_D", "TEAL_E",
    "MAROON_A", "MAROON_B", "MAROON_C", "MAROON_D", "MAROON_E",
    "PURPLE_A", "PURPLE_B", "PURPLE_C", "PURPLE_D", "PURPLE_E",
    "PINK", "PURE_RED", "PURE_GREEN", "PURE_BLUE",
    "GRAY_A", "GRAY_B", "GRAY_C", "GRAY_D", "GRAY_E",
}

# Color names that DO NOT exist in manim (common LLM hallucinations)
_FORBIDDEN_COLORS: Set[str] = {"MAGENTA", "CYAN", "VIOLET", "INDIGO", "LIME", "AMBER", "NAVY"}

_CAPS_RE = re.compile(r"^[A-Z][A-Z_0-9]{1,}$")


# ─────────────────────────────────────────────────────────────────────────────
# Allowlist management
# ─────────────────────────────────────────────────────────────────────────────

def load_allowlist() -> Set[str]:
    """Load the saved manim symbol allowlist. Returns empty set if not generated yet."""
    if ALLOWLIST_FILE.exists():
        data = json.loads(ALLOWLIST_FILE.read_text(encoding="utf-8"))
        return set(data.get("symbols", []))
    return set()


def generate_allowlist() -> None:
    """
    Generate prompts/manim_allowlist.json from the currently installed manim package.
    Run this once per manim upgrade:  python -m agent.api_check
    """
    import manim
    symbols = sorted(n for n in dir(manim) if not n.startswith("_"))
    version = getattr(manim, "__version__", "unknown")
    data = {
        "manim_version": version,
        "symbol_count": len(symbols),
        "symbols": symbols,
    }
    ALLOWLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    ALLOWLIST_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[api_check] Allowlist written: {len(symbols)} symbols from manim {version} -> {ALLOWLIST_FILE}")


# ─────────────────────────────────────────────────────────────────────────────
# AST helpers
# ─────────────────────────────────────────────────────────────────────────────

def _locally_defined(tree: ast.Module) -> Set[str]:
    """Names defined or imported in the file (excluding wildcard imports)."""
    names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            tgt = getattr(node, "target", None)
            if isinstance(tgt, ast.Name):
                names.add(tgt.id)
        elif isinstance(node, ast.For):
            tgt = node.target
            if isinstance(tgt, ast.Name):
                names.add(tgt.id)
            elif isinstance(tgt, ast.Tuple):
                for elt in tgt.elts:
                    if isinstance(elt, ast.Name):
                        names.add(elt.id)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                ov = item.optional_vars
                if ov and isinstance(ov, ast.Name):
                    names.add(ov.id)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for gen in getattr(node, "generators", []):
                if isinstance(gen.target, ast.Name):
                    names.add(gen.target.id)
    return names


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def check_scene(source: str, filename: str = "<scene>") -> Dict:
    """
    Fast AST-based API check for a Manim scene.

    Returns:
        {
          "ok": bool,
          "syntax_error": str | None,   # set if ast.parse fails
          "violations": [str],           # human-readable list of issues found
        }

    Catches:
      - SyntaxError / IndentationError
      - Calls to undefined functions/classes (not in allowlist + local defs)
      - Use of forbidden color constants (MAGENTA, CYAN, VIOLET, ...)
      - Use of ALL_CAPS constants not in the allowlist
    """
    # 1. Syntax check
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as e:
        return {"ok": False, "syntax_error": str(e), "violations": []}

    allowlist = load_allowlist()
    local = _locally_defined(tree)
    known = allowlist | _ALWAYS_ALLOWED | _BUILTINS | local

    violations: List[str] = []
    seen: Set[str] = set()

    def _report(key: str, line: int, msg: str) -> None:
        uid = f"{key}:{line}"
        if uid not in seen:
            seen.add(uid)
            violations.append(f"line {line}: {msg}")

    for node in ast.walk(tree):
        # Undefined bare function/class calls: SomeUndefined(...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name not in known:
                _report(name, node.lineno,
                        f"'{name}' is not defined (undefined function or class; "
                        f"check spelling and ensure it is exported by manim)")

        # ALL_CAPS constants — catch forbidden colors and unknown constants
        elif isinstance(node, ast.Name) and _CAPS_RE.match(node.id):
            name = node.id
            if name in _FORBIDDEN_COLORS:
                _report(name, node.lineno,
                        f"'{name}' is NOT a valid Manim color. "
                        f"Replace with: RED GREEN BLUE YELLOW ORANGE PURPLE PINK "
                        f"TEAL GOLD MAROON WHITE GRAY BLACK or hex '#RRGGBB'")
            elif name not in known:
                _report(name, node.lineno,
                        f"Constant '{name}' is not defined — "
                        f"check spelling or use a known Manim constant/color")

    return {"ok": len(violations) == 0, "syntax_error": None, "violations": violations}


if __name__ == "__main__":
    generate_allowlist()
