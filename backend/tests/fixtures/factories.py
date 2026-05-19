from dataclasses import dataclass
from typing import Any


@dataclass
class FakeUserDTO:
    id: int
    email: str
    name: str
    is_active: bool = True


def build_user(**overrides: Any) -> FakeUserDTO:
    data = {
        "id": 1,
        "email": "candidate@example.com",
        "name": "Casey Candidate",
        "is_active": True,
    }
    data.update(overrides)
    return FakeUserDTO(**data)
