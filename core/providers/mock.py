"""Mock provider implementation for deterministic REIGN testing."""

from __future__ import annotations

from core.providers.base import ModelProvider, ModelRequest, ModelResponse, ToolCall, ToolCallStatus, UsageInfo


class MockProvider(ModelProvider):
    """Deterministic mock provider used for tests and local development."""

    def __init__(self, mode: str = "calculator"):
        self.mode = mode

    @property
    def name(self) -> str:
        return "mock"

    @property
    def is_available(self) -> bool:
        return True

    async def generate(self, request: ModelRequest) -> ModelResponse:
        prompt = (request.prompt or "").strip().lower()

        if "25 * 48" in prompt or "25 x 48" in prompt or "25 times 48" in prompt or "25×48" in prompt:
            return ModelResponse(
                content="The calculation requires the calculator tool.",
                provider=self.name,
                tool_calls=[
                    ToolCall(
                        id="tool_mock_1",
                        name="calculator",
                        arguments={"expression": "25 * 48"},
                        status=ToolCallStatus.PENDING,
                    )
                ],
                usage=UsageInfo(input_tokens=12, output_tokens=8),
                stop_reason="tool_call",
            )

        if "hello" in prompt or "hi" in prompt:
            return ModelResponse(
                content="Hello! REIGN mock provider is ready.",
                provider=self.name,
                usage=UsageInfo(input_tokens=8, output_tokens=10),
            )

        if "what is" in prompt and "time" in prompt:
            return ModelResponse(
                content="The time tool should be used for this request.",
                provider=self.name,
                tool_calls=[
                    ToolCall(
                        id="tool_mock_2",
                        name="time",
                        arguments={},
                        status=ToolCallStatus.PENDING,
                    )
                ],
                usage=UsageInfo(input_tokens=16, output_tokens=8),
                stop_reason="tool_call",
            )

        return ModelResponse(
            content=f"Mock provider response to: {request.prompt}",
            provider=self.name,
            usage=UsageInfo(input_tokens=max(1, len(prompt.split())), output_tokens=10),
        )
