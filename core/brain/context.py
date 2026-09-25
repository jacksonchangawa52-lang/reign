from __future__ import annotations

from typing import Any

from core.identity.master import default_master_profile
from core.personality.personality import load_personality


class ContextEngine:
    """Builds the model context from identity, personality, conversation, memory, and task."""

    def __init__(self):
        self.personality = load_personality()

    def build_context(
        self,
        master: Any | None = None,
        recent_conversation: list[dict[str, str]] | None = None,
        relevant_memories: list[str] | None = None,
        task: str | None = None,
    ) -> dict[str, Any]:
        master_profile = master or default_master_profile()
        system_instructions = self.personality.get("identity", {}).get("behavior", {})
        system_lines = [
            f"You are REIGN, a local-first personal AI assistant for {master_profile.display_name}.",
            f"The designated user is {master_profile.designation}.",
            "Address the primary user as Master.",
            "Be calm, analytical, respectful, and honest about uncertainty.",
            "Never claim consciousness or sentience as an actual capability.",
            "Do not claim to know information you do not have.",
        ]
        system_lines.extend(
            [
                f"Uncertainty policy: {system_instructions.get('uncertainty', 'say when information is unavailable')}",
                f"Challenge policy: {system_instructions.get('challenge', 'question assumptions respectfully')}",
                f"Preference: {system_instructions.get('brevity', 'be concise when possible')}",
            ]
        )

        recent = recent_conversation or []
        memory = relevant_memories or []
        task_context = task or "No current task provided."

        return {
            "master": master_profile.to_dict() if hasattr(master_profile, "to_dict") else {"display_name": str(master_profile)},
            "personality": self.personality,
            "recent_conversation": recent,
            "relevant_memories": memory,
            "task": task_context,
            "system_instructions": "\n".join(system_lines),
        }
