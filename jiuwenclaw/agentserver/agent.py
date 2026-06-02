"""Agent — minimal LLM bridge for single-turn chat."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, AsyncIterator

# Wire up vendored openjiuwen so it's importable
_vendor_root = Path(__file__).resolve().parent.parent / "vendor" / "openjiuwen"
if str(_vendor_root) not in sys.path:
    sys.path.insert(0, str(_vendor_root))

from jiuwenclaw.config import get_config

_logger = logging.getLogger(__name__)
from openjiuwen.core.foundation.llm.model import Model
from openjiuwen.core.foundation.llm.schema.config import (
    ModelClientConfig,
    ModelRequestConfig,
)
from openjiuwen.core.foundation.llm.schema.message import UserMessage
from openjiuwen.core.foundation.llm.schema.message import UserMessage

class Agent:
    """Thin wrapper around openjiuwen's Model for single-turn chat.

    No React loop, no tools, no session state. Just take a query,
    call the LLM, return the response.
    """

    def __init__(self):
        self._model: Any = None

    def _get_model(self) -> Any:
        """Lazy-init the openjiuwen Model from current config."""
        if self._model is not None:
            return self._model



        cfg = get_config()
        models = cfg.get("models", {})
        default = models.get("default", {})
        mcc = default.get("model_client_config", {})

        client_config = ModelClientConfig(
            api_key=mcc.get("api_key", ""),
            api_base=mcc.get("api_base", ""),
            model_name=mcc.get("model_name", ""),
            client_provider=mcc.get("client_provider", "openai"),
            timeout=int(mcc.get("timeout", 1800)),
            max_retries=int(mcc.get("max_retries", 1)),
            verify_ssl=bool(mcc.get("verify_ssl", False)),
        )
        model_config = ModelRequestConfig(
            temperature=default.get("model_config_obj", {}).get("temperature", 0.95),
        )

        self._model = Model(
            model_client_config=client_config,
            model_config=model_config,
        )
        return self._model

    async def chat(self, query: str) -> str:
        """Send a query to the LLM and return the full response."""
        

        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        messages = [UserMessage(content=query)]
        response = await model.invoke(messages, model=model_name)
        return response.content if hasattr(response, "content") else str(response)

    async def chat_stream(self, query: str) -> AsyncIterator[str]:
        """Send a query and yield tokens as they arrive."""
        

        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        messages = [UserMessage(content=query)]
        async for chunk in model.stream(messages, model=model_name):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content
