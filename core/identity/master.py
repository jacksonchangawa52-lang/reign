from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MasterProfile:
    id: str
    display_name: str
    designation: str = "Master"
    created_at: datetime | None = None
    preferences: dict[str, Any] = field(default_factory=dict)
    authentication_status: str = "authenticated"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "designation": self.designation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "preferences": self.preferences,
            "authentication_status": self.authentication_status,
        }


def create_master_profile(
    user_id: str = "master-primary",
    display_name: str = "MASTER",
    designation: str = "Master",
    preferences: dict[str, Any] | None = None,
    authentication_status: str = "authenticated",
) -> MasterProfile:
    return MasterProfile(
        id=user_id,
        display_name=display_name,
        designation=designation,
        created_at=datetime.utcnow(),
        preferences=preferences or {},
        authentication_status=authentication_status,
    )


def default_master_profile() -> MasterProfile:
    return create_master_profile(
        user_id="master-primary",
        display_name="MASTER",
        designation="Master",
        preferences={"theme": "dark", "mode": "local"},
        authentication_status="authenticated",
    )
