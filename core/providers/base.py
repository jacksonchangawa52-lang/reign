"""Base provider interface and types for REIGN model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Sequence


class ToolCallStatus(str, Enum):
    """Status of a tool call in the model response."""
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"


@dataclass
class ToolCall:
    """Normalized representation of a model's tool call."""
    id: str
    name: str
    arguments: dict[str, Any]
    status: ToolCallStatus = ToolCallStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None


@dataclass
class UsageInfo:
    """Token/usage information from a model response."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    def update_totals(self) -> None:
        """Recalculate total tokens."""
        self.total_tokens = self.input_tokens + self.output_tokens


@dataclass
class ModelResponse:
    """Normalized response from any provider."""
    content: str
    provider: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: UsageInfo = field(default_factory=UsageInfo)
    stop_reason: str = "end_turn"  # "end_turn", "tool_call", "max_tokens", "error"
    error: Optional[str] = None


@dataclass
class ModelRequest:
    """Normalized request to any provider."""
    prompt: str
    system: str = ""
    conversation: Sequence[dict[str, str]] | None = None
    memory_context: Sequence[str] | None = None
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.95
    tools: list[dict[str, Any]] | None = None
    stream: bool = False


class ModelProvider(ABC):
    """Abstract base for all model providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name identifier."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is configured and ready."""
        raise NotImplementedError

    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse:
        """
        Generate a response to a request.

        Args:
            request: ModelRequest with prompt and context

        Returns:
            ModelResponse with normalized output
        """
        raise NotImplementedError

    async def stream(self, request: ModelRequest) -> Any:
        """
        Stream a response token-by-token.

        Default implementation falls back to generate() and returns
        the full response. Override for true streaming.

        Args:
            request: ModelRequest with prompt and context

        Yields:
            ModelResponse objects or chunks with partial content
        """
        yield await self.generate(request)

    def _build_conversation_string(self, conversation: Sequence[dict[str, str]] | None = None) -> str:
        """Build a formatted conversation string."""
        if not conversation:
            return ""
        return "\n".join(
            f"{msg.get('role', 'user')}: {msg.get('content', '')}"
            for msg in conversation
        )

    def _build_memory_string(self, memory_context: Sequence[str] | None = None) -> str:
        """Build a formatted memory context string."""
        if not memory_context:
            return ""
        return "\n".join(memory_context)
