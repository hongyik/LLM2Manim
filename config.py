# config.py - LangChain agent version
import os
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parent.parent

# Parent project assets (code prompts for Manim)
SYSTEM_PROMPT_CODE_FILE = ROOT_DIR / "system_prompt_code.txt"
USER_PROMPT_CODE_TEMPLATE_FILE = ROOT_DIR / "user_prompt_code_template.txt"

# API keys and endpoints (shared)
# Supported providers: deepseek, openai, anthropic (add more below and in agent/llm.py)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GPT4_API_KEY = os.getenv("GPT4_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

DEEPSEEK_MODEL = "deepseek-reasoner"
OPENAI_MODEL = "gpt-4o"
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# Default provider (fallback when a stage does not set its own)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")

# Per-stage API/model selection (optional)
# Example: DeepSeek for planner, GPT for code, Claude for step:
#   PLANNER_PROVIDER=deepseek  STEP_PROVIDER=anthropic  CODE_PROVIDER=openai  CODE_MODEL=gpt-4o
# Stages: planner, step, code
STAGE_NAMES = ("planner", "step", "code")

# Default model per provider (used when STAGE_MODEL is not set)
_DEFAULT_MODEL = {
    "deepseek": DEEPSEEK_MODEL,
    "openai": OPENAI_MODEL,
    "anthropic": ANTHROPIC_MODEL,
}


def get_stage_llm_config(stage: str) -> Dict[str, Any]:
    """
    Return API config for a given stage. Each stage can override provider and model.
    stage: one of "planner", "step", "code"
    Returns: dict with provider, model, api_key, base_url (base_url may be None for anthropic)
    """
    stage_lower = stage.lower()
    env_prefix = stage_lower.upper() + "_"
    provider = (os.getenv(f"{env_prefix}PROVIDER") or os.getenv("LLM_PROVIDER", "deepseek")).lower()
    model = os.getenv(f"{env_prefix}MODEL") or _DEFAULT_MODEL.get(provider, OPENAI_MODEL)

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
    # openai or any OpenAI-compatible endpoint
    return {
        "provider": "openai",
        "model": model,
        "api_key": GPT4_API_KEY,
        "base_url": OPENAI_BASE_URL,
    }


# =============================================
# Output: one run folder per process (date-time), with animation_outputs + final_animation inside
# =============================================
from datetime import datetime

_OUTPUT_BASE = Path(__file__).resolve().parent / "outputs"
_RUN_DIR = _OUTPUT_BASE / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
_RUN_DIR.mkdir(parents=True, exist_ok=True)

RUN_DIR = _RUN_DIR  # e.g. outputs/2025-02-09_14-30-00
OUTPUT_DIR = _RUN_DIR / "animation_outputs"
FINAL_VIDEO_DIR = _RUN_DIR / "final_animation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FINAL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# =============================================
# Render quality (Manim video output)
# =============================================
# Quality: "l" (low, 480p15), "m" (medium), "h" (high), "p" (production), "k" (4k)
# Override with env: MANIM_RENDER_QUALITY
MANIM_RENDER_QUALITY = os.getenv("MANIM_RENDER_QUALITY", "l")

# Manim CLI (command or path to executable)
MANIM_CLI = os.getenv("MANIM_CLI", "python -m manim")
