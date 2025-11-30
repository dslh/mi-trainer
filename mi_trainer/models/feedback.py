"""Coach feedback data model."""

from pydantic import BaseModel, Field


class CoachFeedback(BaseModel):
    """Feedback from the MI coach on a user's response."""

    techniques_used: list[str] = Field(
        default_factory=list,
        description="MI techniques identified (e.g., 'open_question', 'reflection', 'affirmation')",
    )
    mi_consistent: list[str] = Field(
        default_factory=list,
        description="Positive observations about MI-consistent behaviors",
    )
    mi_inconsistent: list[str] = Field(
        default_factory=list,
        description="MI-inconsistent behaviors to avoid",
    )
    suggestions: list[str] = Field(
        default_factory=list,
        description="Alternative approaches or improvements",
    )
    overall_note: str = Field(
        default="",
        description="Brief overall assessment",
    )

    def has_issues(self) -> bool:
        """Check if there are MI-inconsistent behaviors flagged."""
        return len(self.mi_inconsistent) > 0

    def has_suggestions(self) -> bool:
        """Check if there are suggestions for improvement."""
        return len(self.suggestions) > 0
