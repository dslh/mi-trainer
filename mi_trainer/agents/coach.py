"""Coach agent for MI feedback."""

import json
from typing import AsyncIterator

from mi_trainer.agents.base import BaseAgent
from mi_trainer.models.feedback import CoachFeedback


class CoachAgent(BaseAgent):
    """Agent that provides MI coaching feedback."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._system_prompt = self._load_prompt("coach_system")

    async def analyze(
        self,
        conversation: list[dict[str, str]],
        latest_user_message: str,
    ) -> CoachFeedback:
        """Analyze the user's message and provide feedback."""
        # Build the analysis request
        analysis_messages = [
            {
                "role": "user",
                "content": self._build_analysis_request(conversation, latest_user_message),
            }
        ]

        response = await self.get_response(self._system_prompt, analysis_messages)
        return self._parse_feedback(response)

    async def analyze_streaming(
        self,
        conversation: list[dict[str, str]],
        latest_user_message: str,
    ) -> AsyncIterator[str]:
        """Stream the analysis for display while generating."""
        analysis_messages = [
            {
                "role": "user",
                "content": self._build_analysis_request(conversation, latest_user_message),
            }
        ]

        async for chunk in self.stream_response(self._system_prompt, analysis_messages):
            yield chunk

    def _build_analysis_request(
        self,
        conversation: list[dict[str, str]],
        latest_user_message: str,
    ) -> str:
        """Build the request for feedback analysis."""
        # Format conversation history
        history_text = ""
        for msg in conversation[:-1]:  # Exclude the latest message
            role_label = "Practitioner" if msg["role"] == "user" else "Client"
            history_text += f"{role_label}: {msg['content']}\n\n"

        return f"""## Conversation History

{history_text}

## Message to Analyze

Practitioner: {latest_user_message}

Please analyze this practitioner response and provide feedback in the specified JSON format."""

    def _parse_feedback(self, response: str) -> CoachFeedback:
        """Parse the JSON response into a CoachFeedback object."""
        try:
            # Try to extract JSON from the response
            # Handle case where model wraps JSON in markdown code blocks
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())
            return CoachFeedback(**data)
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            # If parsing fails, return a basic feedback object
            return CoachFeedback(
                overall_note=f"Unable to parse feedback: {response[:200]}..."
            )

    async def get_hint(self, conversation: list[dict[str, str]]) -> str:
        """Get a hint about what technique to try next."""
        # Format conversation history
        history_text = ""
        for msg in conversation:
            role_label = "Practitioner" if msg["role"] == "user" else "Client"
            history_text += f"{role_label}: {msg['content']}\n\n"

        hint_prompt = """You are an MI coach. Based on the conversation so far, suggest what technique or approach the practitioner might try next.

Focus on:
- Which MI technique would be most helpful here (open question, reflection, affirmation, summary, etc.)
- Why this technique fits the current moment
- What aspect of what the client said to focus on

Do NOT provide exact words to say. Give guidance on the approach, not a script.

Keep your response to 2-3 sentences."""

        messages = [
            {
                "role": "user",
                "content": f"## Conversation So Far\n\n{history_text}\n\nWhat technique should the practitioner consider using next?",
            }
        ]

        return await self.get_response(hint_prompt, messages)
