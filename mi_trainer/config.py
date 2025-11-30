"""Configuration for MI Trainer."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_api_key() -> str:
    """Get the Anthropic API key from environment."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required. "
            "Set it in your environment or in a .env file."
        )
    return key


# Data directories
DATA_DIR = Path.home() / ".mi-trainer"
SESSIONS_DIR = DATA_DIR / "sessions"
USER_SCENARIOS_DIR = DATA_DIR / "scenarios"

# Ensure directories exist
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
USER_SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)

# Built-in scenarios location (within package)
BUILTIN_SCENARIOS_DIR = Path(__file__).parent / "scenarios"

# Model configuration
DEFAULT_MODEL = "claude-sonnet-4-20250514"
