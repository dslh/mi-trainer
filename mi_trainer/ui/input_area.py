"""Input area for user messages and commands."""

from typing import Callable, Optional

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window, ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import InMemoryHistory


class InputArea:
    """Text input area with command handling."""

    def __init__(
        self,
        on_submit: Optional[Callable[[str], None]] = None,
    ):
        self.on_submit = on_submit
        self._enabled = True
        self._prompt_text = "> "

        self.history = InMemoryHistory()
        self.buffer = Buffer(
            history=self.history,
            accept_handler=self._handle_accept,
            multiline=False,
        )

        self.control = BufferControl(
            buffer=self.buffer,
            focus_on_click=True,
        )

        self.window = Window(
            content=self.control,
            height=1,
            dont_extend_height=True,
        )

    def _handle_accept(self, buffer: Buffer) -> bool:
        """Handle input submission."""
        text = buffer.text.strip()
        if text and self.on_submit:
            self.on_submit(text)
        # Clear the buffer for next input
        buffer.reset()
        return False  # Don't add to history twice (reset already handles it)

    def get_prompt(self) -> str:
        """Get the current prompt text."""
        return self._prompt_text

    def set_prompt(self, prompt: str) -> None:
        """Set the prompt text."""
        self._prompt_text = prompt

    def enable(self) -> None:
        """Enable input."""
        self._enabled = True

    def disable(self) -> None:
        """Disable input."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if input is enabled."""
        return self._enabled

    def clear(self) -> None:
        """Clear the input buffer."""
        self.buffer.reset()

    def set_text(self, text: str) -> None:
        """Set the input text."""
        self.buffer.text = text
        self.buffer.cursor_position = len(text)
