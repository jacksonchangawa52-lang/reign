from __future__ import annotations


class Planner:
    """Minimal planner abstraction for future execution flows."""

    def plan(self, request: str) -> list[str]:
        if not request.strip():
            return ["No task requested."]
        return [
            "Understand the request",
            "Classify the request",
            "Gather required context",
            "Provide a safe, relevant response",
        ]
