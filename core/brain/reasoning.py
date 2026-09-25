from __future__ import annotations


class ReasoningEngine:
    """Basic request classification for V0.1."""

    def classify(self, text: str) -> str:
        lowered = text.lower().strip()
        if not lowered:
            return "unknown"
        if any(token in lowered for token in ["remember", "memory", "preference", "save", "forget"]):
            return "memory"
        if any(token in lowered for token in ["what is", "who is", "why", "how", "can you", "explain", "describe"]):
            return "question"
        if any(token in lowered for token in ["calculate", "+", "-", "*", "/", "sum", "multiply", "sqrt", "equation"]):
            return "calculation"
        if any(token in lowered for token in ["start", "run", "execute", "launch", "open", "set", "update"]):
            return "command"
        if any(token in lowered for token in ["hello", "hi", "good morning", "good evening", "thanks", "thank you"]):
            return "conversation"
        return "unknown"

    def analyze(self, text: str) -> dict[str, str | bool]:
        category = self.classify(text)
        return {
            "category": category,
            "is_question": category == "question",
            "is_calculation": category == "calculation",
            "needs_memory": category == "memory",
            "is_command": category == "command",
        }
