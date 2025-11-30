"""Scenario storage and library management."""

import json
from pathlib import Path
from typing import Optional

from mi_trainer.config import BUILTIN_SCENARIOS_DIR, USER_SCENARIOS_DIR
from mi_trainer.models.scenario import Scenario


def list_builtin_scenarios() -> list[Scenario]:
    """List all built-in scenarios."""
    scenarios = []
    for filepath in BUILTIN_SCENARIOS_DIR.glob("*.json"):
        try:
            scenarios.append(load_scenario_from_file(filepath))
        except (json.JSONDecodeError, ValueError):
            continue
    return scenarios


def list_user_scenarios() -> list[Scenario]:
    """List all user-created scenarios."""
    scenarios = []
    for filepath in USER_SCENARIOS_DIR.glob("*.json"):
        try:
            scenarios.append(load_scenario_from_file(filepath))
        except (json.JSONDecodeError, ValueError):
            continue
    return scenarios


def list_all_scenarios() -> list[Scenario]:
    """List all available scenarios (built-in and user)."""
    return list_builtin_scenarios() + list_user_scenarios()


def load_scenario_from_file(filepath: Path) -> Scenario:
    """Load a scenario from a JSON file."""
    with open(filepath) as f:
        data = json.load(f)
    return Scenario(**data)


def load_scenario_by_id(scenario_id: str) -> Optional[Scenario]:
    """Load a scenario by its ID."""
    # Check built-in scenarios first
    for scenario in list_builtin_scenarios():
        if scenario.id == scenario_id:
            return scenario

    # Check user scenarios
    for scenario in list_user_scenarios():
        if scenario.id == scenario_id:
            return scenario

    return None


def load_scenario_by_name(name: str) -> Optional[Scenario]:
    """Load a scenario by name (case-insensitive partial match)."""
    name_lower = name.lower()
    for scenario in list_all_scenarios():
        if name_lower in scenario.name.lower():
            return scenario
    return None


def save_user_scenario(scenario: Scenario) -> Path:
    """Save a scenario to the user scenarios directory."""
    filename = f"{scenario.id}.json"
    filepath = USER_SCENARIOS_DIR / filename

    with open(filepath, "w") as f:
        f.write(scenario.model_dump_json(indent=2))

    return filepath


def delete_user_scenario(scenario_id: str) -> bool:
    """Delete a user scenario by ID."""
    filepath = USER_SCENARIOS_DIR / f"{scenario_id}.json"
    if filepath.exists():
        filepath.unlink()
        return True
    return False
