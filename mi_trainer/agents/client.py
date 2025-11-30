"""Client persona agent for MI practice."""

from typing import AsyncIterator

from mi_trainer.agents.base import BaseAgent
from mi_trainer.models.scenario import Scenario


class ClientAgent(BaseAgent):
    """Agent that roleplays as a client in MI practice."""

    def __init__(self, scenario: Scenario, **kwargs):
        super().__init__(**kwargs)
        self.scenario = scenario
        self._system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt with scenario context."""
        template = self._load_prompt("client_system")
        return template.replace("{scenario_context}", self.scenario.to_prompt_context())

    def update_scenario(self, scenario: Scenario) -> None:
        """Update the scenario and rebuild the system prompt."""
        self.scenario = scenario
        self._system_prompt = self._build_system_prompt()

    async def respond(
        self,
        conversation: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        """Generate a response to the practitioner's message."""
        async for chunk in self.stream_response(self._system_prompt, conversation):
            yield chunk

    async def get_opening(self) -> str:
        """Get the client's opening statement."""
        if self.scenario.opening_statement:
            return self.scenario.opening_statement

        # Generate an opening if not provided
        messages = [
            {
                "role": "user",
                "content": "Please begin the conversation with your opening statement. "
                "Introduce yourself briefly and share what brings you here today.",
            }
        ]
        return await self.get_response(self._system_prompt, messages)
