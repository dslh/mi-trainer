"""Conversation pane displaying the dialogue."""

from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window

from mi_trainer.models.conversation import ConversationTree, ConversationNode


class ConversationPane:
    """Displays the conversation between user and client."""

    def __init__(self):
        self._content: list[tuple[str, str]] = []
        self._streaming_text = ""
        self._streaming_role = ""
        self.control = FormattedTextControl(
            text=self._get_formatted_text,
            focusable=False,
        )
        self.window = Window(
            content=self.control,
            wrap_lines=True,
        )
        self.container = ScrollablePane(self.window)

    def _get_formatted_text(self) -> FormattedText:
        """Generate the formatted text for display."""
        result = list(self._content)

        # Add streaming content if present
        if self._streaming_text:
            if self._streaming_role == "client":
                result.append(("class:conversation.client-label", "\nClient: "))
                result.append(("class:conversation.message", self._streaming_text))
            else:
                result.append(("class:conversation.user-label", "\nYou: "))
                result.append(("class:conversation.message", self._streaming_text))

        if not result:
            result.append(("class:conversation.message", "Start the conversation by typing below..."))

        return FormattedText(result)

    def load_conversation(self, tree: ConversationTree) -> None:
        """Load a conversation tree into the pane."""
        self._content = []
        path = tree.get_path_to_current()

        for node in path:
            self._add_node(node)

        # Check for branches
        branches = tree.get_branches_at_current()
        if len(branches) > 1:
            self._content.append(("class:conversation.branch-indicator", f"\n[{len(branches)} branches from here]"))

    def _add_node(self, node: ConversationNode) -> None:
        """Add a node to the display."""
        if node.role == "client":
            self._content.append(("class:conversation.client-label", "\nClient: "))
        else:
            self._content.append(("class:conversation.user-label", "\nYou: "))

        self._content.append(("class:conversation.message", node.content))
        self._content.append(("", "\n"))

    def add_message(self, role: str, content: str) -> None:
        """Add a complete message to the display."""
        if role == "client":
            self._content.append(("class:conversation.client-label", "\nClient: "))
        else:
            self._content.append(("class:conversation.user-label", "\nYou: "))

        self._content.append(("class:conversation.message", content))
        self._content.append(("", "\n"))

    def start_streaming(self, role: str) -> None:
        """Start streaming a new message."""
        self._streaming_role = role
        self._streaming_text = ""

    def append_streaming(self, text: str) -> None:
        """Append text to the streaming message."""
        self._streaming_text += text

    def finish_streaming(self) -> str:
        """Finish streaming and commit the message."""
        content = self._streaming_text
        if content:
            self.add_message(self._streaming_role, content)
        self._streaming_text = ""
        self._streaming_role = ""
        return content

    def clear(self) -> None:
        """Clear the conversation display."""
        self._content = []
        self._streaming_text = ""
        self._streaming_role = ""
