"""Base agent class with Anthropic client setup."""

from pathlib import Path
from typing import AsyncIterator

import anthropic

from mi_trainer.config import get_api_key, DEFAULT_MODEL


class BaseAgent:
    """Base class for all LLM agents."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.client = anthropic.AsyncAnthropic(api_key=get_api_key())
        self.model = model

    def _load_prompt(self, prompt_name: str) -> str:
        """Load a prompt template from the prompts directory."""
        prompt_path = Path(__file__).parent.parent / "prompts" / f"{prompt_name}.md"
        return prompt_path.read_text()

    async def stream_response(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        """Stream a response from the model."""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def get_response(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:
        """Get a complete response from the model."""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
