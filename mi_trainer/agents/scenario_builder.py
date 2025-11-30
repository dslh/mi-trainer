"""Scenario builder agent for generating client profiles."""

import json

from mi_trainer.agents.base import BaseAgent
from mi_trainer.models.scenario import Scenario


class ScenarioBuilderAgent(BaseAgent):
    """Agent that generates full scenarios from short descriptions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._system_prompt = self._load_prompt("scenario_builder")

    async def build_scenario(self, description: str) -> Scenario:
        """Generate a full scenario from a short description."""
        messages = [
            {
                "role": "user",
                "content": f"Create a detailed MI practice scenario based on this description:\n\n{description}",
            }
        ]

        response = await self.get_response(self._system_prompt, messages)
        return self._parse_scenario(response)

    def _parse_scenario(self, response: str) -> Scenario:
        """Parse the JSON response into a Scenario object."""
        try:
            # Handle markdown code blocks
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())
            return Scenario(**data)
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            raise ValueError(f"Failed to parse scenario response: {e}\n\nResponse: {response[:500]}")
