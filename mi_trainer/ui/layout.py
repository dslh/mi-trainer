"""Main layout composition for the application."""

from prompt_toolkit.layout import Layout, HSplit, VSplit, Window, FormattedTextControl
from prompt_toolkit.layout.containers import FloatContainer, Float
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import Box, Frame, Label

from mi_trainer.ui.conversation_pane import ConversationPane
from mi_trainer.ui.feedback_pane import FeedbackPane
from mi_trainer.ui.input_area import InputArea
from mi_trainer.ui.styles import APP_STYLE


class AppLayout:
    """Main application layout with split panes."""

    def __init__(self, on_input: callable):
        # Create panes
        self.conversation_pane = ConversationPane()
        self.feedback_pane = FeedbackPane()
        self.input_area = InputArea(on_submit=on_input)

        # Status bar content
        self._status_text = "MI Trainer | /help for commands | /quit to exit"

        # Build layout
        self.layout = self._build_layout()

    def _build_layout(self) -> Layout:
        """Build the complete layout."""
        # Main content area with vertical split
        main_content = VSplit([
            # Conversation pane (left, 70%)
            Frame(
                body=self.conversation_pane.container,
                title="Conversation",
            ),
            # Vertical separator
            Window(width=1, char="│", style="class:separator"),
            # Feedback pane (right, 30%)
            Frame(
                body=self.feedback_pane.container,
                title="Coach Feedback",
            ),
        ])

        # Prompt line
        prompt_line = VSplit([
            Window(
                content=FormattedTextControl(lambda: self.input_area.get_prompt()),
                width=Dimension.exact(2),
                style="class:input.prompt",
            ),
            self.input_area.window,
        ], style="class:input")

        # Status bar
        status_bar = Window(
            content=FormattedTextControl(lambda: self._status_text),
            height=1,
            style="class:status",
        )

        # Full layout
        root = HSplit([
            main_content,
            Window(height=1, char="─", style="class:border"),
            prompt_line,
            status_bar,
        ])

        container = FloatContainer(
            content=root,
            floats=[],  # Can add dialogs here later
        )

        return Layout(container, focused_element=self.input_area.window)

    def set_status(self, text: str) -> None:
        """Update the status bar text."""
        self._status_text = text

    def focus_input(self) -> None:
        """Focus the input area."""
        self.layout.focus(self.input_area.window)

    def get_style(self):
        """Get the application style."""
        return APP_STYLE
