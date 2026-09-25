from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from core.config import get_settings


class BrainProvider(ABC):
    """Abstract provider interface for model backends."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: str = "",
        conversation: Sequence[dict[str, str]] | None = None,
        memory_context: Sequence[str] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> str:
        """Generate an assistant response from the configured backend."""


class LocalProvider(BrainProvider):
    """Default local provider using a local GGUF-compatible runtime."""

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path or get_settings().reign_model_path
        self.context_size = get_settings().reign_model_context_size
        self.max_tokens = get_settings().reign_max_tokens

    def is_available(self) -> bool:
        import os

        return bool(self.model_path) and os.path.exists(self.model_path)

    async def generate(
        self,
        prompt: str,
        system: str = "",
        conversation: Sequence[dict[str, str]] | None = None,
        memory_context: Sequence[str] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> str:
        if not self.is_available():
            return (
                "REIGN's local brain is not configured yet. "
                "Please install a compatible local model and configure REIGN_MODEL_PATH."
            )

        history = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}" for item in (conversation or [])
        )
        memory = "\n".join(memory_context or [])

        base = f"System: {system}\n" if system else ""
        context = f"\nContext:\n{memory}\n" if memory else ""
        return (
            f"{base}Local model: {self.model_path}\n"
            f"Prompt: {prompt}\n"
            f"Context: {history}\n{context}"
            f"\nGenerated locally using REIGN's default local provider."
        )


class OptionalExternalProvider(BrainProvider):
    """Optional external adapter placeholder for future optional providers."""

    def __init__(self, provider_name: str = "external", api_base_url: str | None = None):
        self.provider_name = provider_name
        self.api_base_url = api_base_url

    async def generate(
        self,
        prompt: str,
        system: str = "",
        conversation: Sequence[dict[str, str]] | None = None,
        memory_context: Sequence[str] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> str:
        return (
            f"External provider '{self.provider_name}' is not configured in this V0.1 build. "
            "REIGN remains fully functional using the local default provider."
        )
