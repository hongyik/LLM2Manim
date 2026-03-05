# config.py - LangChain agent version
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT_DIR = Path(__file__).resolve().parent

# Load .env file if present (never overwrites already-set env vars)
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env", override=False)
except ImportError:
    pass
PROMPTS_DIR = ROOT_DIR / "prompts"

# Code prompt assets for Manim (stored under this project's prompts/ folder)
SYSTEM_PROMPT_CODE_FILE = PROMPTS_DIR / "system_prompt_code.txt"
USER_PROMPT_CODE_TEMPLATE_FILE = PROMPTS_DIR / "user_prompt_code_template.txt"
CODE_PATTERNS_FILE = PROMPTS_DIR / "code_patterns.txt"   # verified working snippets

# API keys and endpoints (shared)
# Supported providers: deepseek, openai, anthropic (add more below and in agent/llm.py)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GPT4_API_KEY = os.getenv("GPT4_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
# Only set for custom/proxy endpoints. None = let the official SDK use its default.
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # e.g. "https://my-proxy/v1"

DEEPSEEK_MODEL = "deepseek-reasoner"
OPENAI_MODEL = "gpt-4o"
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# Default provider (fallback when a stage does not set its own)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")

# Pipeline stages that call an LLM
STAGE_NAMES = ("planner", "step", "code", "fix")

# Default model per provider (used when STAGE_MODEL is not set)
_DEFAULT_MODEL = {
    "deepseek": DEEPSEEK_MODEL,
    "openai": OPENAI_MODEL,
    "anthropic": ANTHROPIC_MODEL,
}

# ── File-based LLM routing (llm_config.json) ──────────────────────────────────
LLM_CONFIG_FILE = ROOT_DIR / "llm_config.json"

def _load_llm_config() -> Dict[str, Any]:
    """Load llm_config.json. Returns {} if missing or invalid JSON."""
    if not LLM_CONFIG_FILE.exists():
        return {}
    try:
        data = json.loads(LLM_CONFIG_FILE.read_text(encoding="utf-8"))
        return {k: v for k, v in data.items() if not k.startswith("_")}
    except (json.JSONDecodeError, OSError):
        return {}

_LLM_FILE_CONFIG: Dict[str, Any] = _load_llm_config()


def get_stage_llm_config(stage: str) -> Dict[str, Any]:
    """
    Return API config for a given stage.
    Priority: env var > llm_config.json > built-in default.
    Stages: planner, step, code, fix
    Returns: dict with provider, model, api_key, base_url
    """
    stage_lower = stage.lower()
    env_prefix = stage_lower.upper() + "_"

    # File config for this stage, falling back to "default" section
    file_cfg: Dict[str, Any] = (
        _LLM_FILE_CONFIG.get(stage_lower)
        or _LLM_FILE_CONFIG.get("default")
        or {}
    )

    provider = (
        os.getenv(f"{env_prefix}PROVIDER")
        or file_cfg.get("provider")
        or os.getenv("LLM_PROVIDER", "deepseek")
    ).lower()
    model = (
        os.getenv(f"{env_prefix}MODEL")
        or file_cfg.get("model")
        or _DEFAULT_MODEL.get(provider, OPENAI_MODEL)
    )

    if provider == "deepseek":
        return {
            "provider": "deepseek",
            "model": model,
            "api_key": DEEPSEEK_API_KEY,
            "base_url": DEEPSEEK_BASE_URL,
        }
    if provider == "anthropic":
        return {
            "provider": "anthropic",
            "model": model,
            "api_key": ANTHROPIC_API_KEY,
            "base_url": None,
        }
    # openai — only pass base_url if a custom endpoint is configured
    return {
        "provider": "openai",
        "model": model,
        "api_key": GPT4_API_KEY,
        "base_url": OPENAI_BASE_URL or None,  # None = SDK default (api.openai.com)
    }


# =============================================
# Output: one run folder per process (date-time), with animation_outputs + final_animation inside
# Created once via init_run_dir() so a single run does not create multiple folders (e.g. from
# workers or re-imports). Must be called before any code uses RUN_DIR/OUTPUT_DIR/FINAL_VIDEO_DIR.
# =============================================
from datetime import datetime

_OUTPUT_BASE = Path(__file__).resolve().parent / "outputs"
_RUN_DIR: Optional[Path] = None
RUN_DIR: Path = None  # type: ignore[assignment]
OUTPUT_DIR: Path = None  # type: ignore[assignment]
FINAL_VIDEO_DIR: Path = None  # type: ignore[assignment]


def init_run_dir() -> None:
    """Create the single run directory for this process. Idempotent: safe to call multiple times."""
    global _RUN_DIR, RUN_DIR, OUTPUT_DIR, FINAL_VIDEO_DIR
    if _RUN_DIR is not None:
        return
    _RUN_DIR = _OUTPUT_BASE / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _RUN_DIR.mkdir(parents=True, exist_ok=True)
    RUN_DIR = _RUN_DIR
    OUTPUT_DIR = _RUN_DIR / "animation_outputs"
    FINAL_VIDEO_DIR = _RUN_DIR / "final_animation"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# =============================================
# Max number of scenes the planner is allowed to create per run.
# Override with env: MAX_SECTIONS (e.g. MAX_SECTIONS=3)
MAX_SECTIONS = int(os.getenv("MAX_SECTIONS", "7"))

# Render quality (Manim video output)
# =============================================
# Quality: "l" (low, 480p15), "m" (medium), "h" (high), "p" (production), "k" (4k)
# Override with env: MANIM_RENDER_QUALITY
MANIM_RENDER_QUALITY = os.getenv("MANIM_RENDER_QUALITY", "l")

# Manim CLI (command or path to executable)
# Use sys.executable so subprocesses always use the same venv Python, not the system Python.
MANIM_CLI = os.getenv("MANIM_CLI", f"{sys.executable} -m manim")
