"""Feedback pane displaying coach analysis."""

import shutil
import textwrap

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window

from mi_trainer.models.feedback import CoachFeedback


class FeedbackPane:
    """Displays MI coaching feedback."""

    def __init__(self):
        self._content: list[tuple[str, str]] = []
        self._streaming_text = ""
        self._is_streaming = False
        self._wrap_width = 35
        self.control = FormattedTextControl(
            text=self._get_formatted_text,
            focusable=False,
        )
        self.window = Window(
            content=self.control,
            wrap_lines=False,  # We handle wrapping ourselves
        )
        self.container = ScrollablePane(self.window)

    def _wrap_text(self, text: str, indent: str = "") -> str:
        """Wrap text at word boundaries."""
        try:
            term_width = shutil.get_terminal_size().columns
            self._wrap_width = max(25, int(term_width * 0.30) - 5)
        except Exception:
            self._wrap_width = 35

        paragraphs = text.split('\n')
        wrapped = []
        for para in paragraphs:
            if para.strip():
                wrapped.append(textwrap.fill(
                    para,
                    width=self._wrap_width,
                    initial_indent=indent,
                    subsequent_indent=indent + "  "
                ))
            else:
                wrapped.append('')
        return '\n'.join(wrapped)

    def _get_formatted_text(self) -> FormattedText:
        """Generate the formatted text for display."""
        result = list(self._content)

        if self._is_streaming:
            result.append(("class:feedback.note", f"\n{self._streaming_text}"))

        if not result:
            result.append(("class:feedback.note", "Coach feedback will appear here..."))

        return FormattedText(result)

    def show_feedback(self, feedback: CoachFeedback) -> None:
        """Display parsed feedback."""
        self._content.append(("class:feedback.header", "\n--- Coach Feedback ---\n"))

        # Techniques used
        if feedback.techniques_used:
            self._content.append(("class:feedback.technique", "Techniques: "))
            self._content.append(("class:feedback.note", ", ".join(feedback.techniques_used)))
            self._content.append(("", "\n"))

        # MI-consistent (good)
        for item in feedback.mi_consistent:
            self._content.append(("class:feedback.good", "+ "))
            self._content.append(("class:feedback.note", f"{self._wrap_text(item)}\n"))

        # MI-inconsistent (issues)
        for item in feedback.mi_inconsistent:
            self._content.append(("class:feedback.bad", "- "))
            self._content.append(("class:feedback.note", f"{self._wrap_text(item)}\n"))

        # Suggestions
        for item in feedback.suggestions:
            self._content.append(("class:feedback.suggestion", "> "))
            self._content.append(("class:feedback.note", f"{self._wrap_text(item)}\n"))

        # Overall note
        if feedback.overall_note:
            self._content.append(("class:feedback.note", f"\n{self._wrap_text(feedback.overall_note)}\n"))

    def start_streaming(self) -> None:
        """Start streaming feedback."""
        self._is_streaming = True
        self._streaming_text = ""
        self._content.append(("class:feedback.header", "\n--- Coach Feedback ---\n"))

    def append_streaming(self, text: str) -> None:
        """Append text to streaming feedback."""
        self._streaming_text += text

    def finish_streaming(self) -> str:
        """Finish streaming feedback."""
        content = self._streaming_text
        self._is_streaming = False
        self._streaming_text = ""
        return content

    def show_info(self, message: str) -> None:
        """Show an informational message."""
        self._content.append(("class:feedback.note", f"\n{self._wrap_text(message)}\n"))

    def show_error(self, message: str) -> None:
        """Show an error message."""
        self._content.append(("class:feedback.bad", f"\nError: {self._wrap_text(message)}\n"))

    def clear(self) -> None:
        """Clear the feedback display."""
        self._content = []
        self._streaming_text = ""
        self._is_streaming = False
