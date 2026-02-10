from pathlib import Path
from typing import Optional, Union

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_stage_llm_config
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None  # type: ignore


def get_llm(
    temperature: float = 0.7,
    max_tokens: int = 2048,
    stage: Optional[str] = None,
    *,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Union[BaseChatModel, ChatOpenAI]:
    """
    Build a chat model for a stage or with explicit API settings.
    Supports: deepseek, openai (GPT), anthropic (Claude).
    - If stage is set ("planner", "step", "code"), use that stage's config from env.
    - Otherwise use provider/model/api_key/base_url if given, or default (planner) config.
    """
    if stage:
        cfg = get_stage_llm_config(stage)
        provider = provider or cfg["provider"]
        model = model or cfg["model"]
        api_key = api_key or cfg["api_key"]
        base_url = base_url if base_url is not None else cfg.get("base_url")
    else:
        cfg = get_stage_llm_config("planner")
        provider = provider or cfg["provider"]
        model = model or cfg["model"]
        api_key = api_key or cfg["api_key"]
        base_url = base_url if base_url is not None else cfg.get("base_url")

    if provider == "anthropic":
        if ChatAnthropic is None:
            raise ImportError("anthropic provider requires: pip install langchain-anthropic")
        return ChatAnthropic(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )
