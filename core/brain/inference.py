from __future__ import annotations

from pathlib import Path

from core.brain.provider import LocalProvider


class ModelNotConfiguredError(RuntimeError):
    """Raised when no local model path is available."""


class LocalInferenceRuntime:
    """Minimal local inference runtime adapter for REIGN."""

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path or "models/your-model.gguf"

    def is_available(self) -> bool:
        return bool(self.model_path) and Path(self.model_path).exists()

    async def generate(
        self,
        prompt: str,
        system: str = "",
        conversation: list[dict[str, str]] | None = None,
        memory_context: list[str] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> str:
        provider = LocalProvider(self.model_path)
        if not provider.is_available():
            raise ModelNotConfiguredError(
                "REIGN's local brain is not configured yet. Please install a compatible local model and configure REIGN_MODEL_PATH."
            )
        return await provider.generate(
            prompt=prompt,
            system=system,
            conversation=conversation,
            memory_context=memory_context,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
