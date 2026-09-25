from __future__ import annotations

import json
from pathlib import Path


def load_personality(path: str | Path | None = None) -> dict:
    personality_path = Path(path) if path else Path(__file__).with_name("reign_identity.json")
    with personality_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
