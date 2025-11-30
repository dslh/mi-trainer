"""Scenario data model for client personas."""

from pydantic import BaseModel, Field


class Ambivalence(BaseModel):
    """Represents the client's ambivalence about change."""

    change: list[str] = Field(
        default_factory=list,
        description="Reasons the client might want to change",
    )
    status_quo: list[str] = Field(
        default_factory=list,
        description="Reasons the client might want to stay the same",
    )


class Scenario(BaseModel):
    """A client scenario for MI practice."""

    id: str = Field(description="Unique identifier for the scenario")
    name: str = Field(description="Human-readable name")
    description: str = Field(description="Brief description of the scenario")
    demographics: str = Field(description="Age, gender, occupation, etc.")
    presenting_issue: str = Field(description="The main issue bringing them in")
    ambivalence: Ambivalence = Field(
        default_factory=Ambivalence,
        description="The client's mixed feelings about change",
    )
    resistance_level: int = Field(
        default=3,
        ge=1,
        le=5,
        description="How resistant the client is (1=cooperative, 5=very resistant)",
    )
    background: str = Field(
        default="",
        description="Relevant history and context",
    )
    personality_notes: str = Field(
        default="",
        description="Personality traits affecting the interaction",
    )
    potential_change_talk_triggers: list[str] = Field(
        default_factory=list,
        description="Topics/approaches that might elicit change talk",
    )
    common_sustain_talk: list[str] = Field(
        default_factory=list,
        description="Typical sustain talk this client might express",
    )
    opening_statement: str = Field(
        default="",
        description="How the client might open the conversation",
    )

    def to_prompt_context(self) -> str:
        """Generate context for the client agent prompt."""
        ambivalence_text = "Reasons for change:\n"
        for reason in self.ambivalence.change:
            ambivalence_text += f"  - {reason}\n"
        ambivalence_text += "\nReasons to stay the same:\n"
        for reason in self.ambivalence.status_quo:
            ambivalence_text += f"  - {reason}\n"

        return f"""## Client Profile

**Demographics:** {self.demographics}
**Presenting Issue:** {self.presenting_issue}
**Resistance Level:** {self.resistance_level}/5

**Background:**
{self.background}

**Personality:**
{self.personality_notes}

**Ambivalence:**
{ambivalence_text}

**Things that might trigger change talk:**
{chr(10).join(f'- {t}' for t in self.potential_change_talk_triggers)}

**Common sustain talk patterns:**
{chr(10).join(f'- {s}' for s in self.common_sustain_talk)}
"""
