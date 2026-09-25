"""Local model provider implementation."""

from __future__ import annotations

import os
from pathlib import Path

from core.config import get_settings
from core.providers.base import ModelProvider, ModelRequest, ModelResponse, ToolCall, ToolCallStatus, UsageInfo


class LocalProvider(ModelProvider):
    """Local model provider using GGUF-compatible runtime."""

    def __init__(self, model_path: str | None = None):
        """Initialize local provider with optional model path override."""
        self.model_path = model_path or get_settings().reign_model_path
        self.context_size = get_settings().reign_model_context_size
        self.max_tokens = get_settings().reign_max_tokens

    @property
    def name(self) -> str:
        """Provider name."""
        return "local"

    @property
    def is_available(self) -> bool:
        """Check if model file exists."""
        if not self.model_path:
            return False
        return os.path.exists(self.model_path)

    async def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate response from local model."""
        if not self.is_available:
            return ModelResponse(
                content=(
                    "Local model not configured. "
                    "Please set REIGN_MODEL_PATH to a valid GGUF model file and restart."
                ),
                provider=self.name,
                stop_reason="error",
                error="Model not found",
            )

        # For now, return structured response indicating model would be called
        # In production, this would call llama.cpp, ollama, or similar runtime
        conversation_str = self._build_conversation_string(request.conversation)
        memory_str = self._build_memory_string(request.memory_context)

        context_parts = []
        if request.system:
            context_parts.append(f"System: {request.system}")
        if memory_str:
            context_parts.append(f"Memory Context:\n{memory_str}")
        if conversation_str:
            context_parts.append(f"Conversation:\n{conversation_str}")

        context_str = "\n\n".join(context_parts)

        # Build response indicating local processing
        response_content = f"[Local model response]\nPrompt: {request.prompt}\n"
        if context_str:
            response_content += f"\n{context_str}\n"

        # Check if prompt indicates a tool call
        tool_calls = []
        if "calculate" in request.prompt.lower() or "math" in request.prompt.lower():
            # Indicate that a calculation tool would be called
            tool_calls.append(
                ToolCall(
                    id="local_tool_1",
                    name="calculator",
                    arguments={"expression": "0"},
                    status=ToolCallStatus.PENDING,
                )
            )

        return ModelResponse(
            content=response_content,
            provider=self.name,
            tool_calls=tool_calls,
            usage=UsageInfo(input_tokens=len(request.prompt.split()), output_tokens=10),
        )
