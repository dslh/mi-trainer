"""Session storage for conversation trees."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from mi_trainer.config import SESSIONS_DIR
from mi_trainer.models.conversation import ConversationTree
from mi_trainer.models.scenario import Scenario


class Session(BaseModel):
    """A complete practice session with scenario and conversation."""

    scenario: Scenario
    conversation: ConversationTree
    created_at: datetime
    updated_at: datetime


def save_session(session: Session, filename: Optional[str] = None) -> Path:
    """Save a session to disk."""
    if filename is None:
        timestamp = session.created_at.strftime("%Y%m%d_%H%M%S")
        safe_name = session.scenario.id.replace(" ", "_").lower()
        filename = f"{timestamp}_{safe_name}.json"

    filepath = SESSIONS_DIR / filename
    session.updated_at = datetime.now()

    with open(filepath, "w") as f:
        f.write(session.model_dump_json(indent=2))

    return filepath


def load_session(filepath: Path) -> Session:
    """Load a session from disk."""
    with open(filepath) as f:
        data = json.load(f)
    return Session(**data)


def list_sessions() -> list[tuple[Path, str, datetime]]:
    """List all saved sessions with their names and dates."""
    sessions = []
    for filepath in SESSIONS_DIR.glob("*.json"):
        try:
            with open(filepath) as f:
                data = json.load(f)
            scenario_name = data.get("scenario", {}).get("name", "Unknown")
            created_at = datetime.fromisoformat(data.get("created_at", ""))
            sessions.append((filepath, scenario_name, created_at))
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    return sorted(sessions, key=lambda x: x[2], reverse=True)


def create_session(scenario: Scenario) -> Session:
    """Create a new session with a scenario."""
    now = datetime.now()
    return Session(
        scenario=scenario,
        conversation=ConversationTree(),
        created_at=now,
        updated_at=now,
    )
