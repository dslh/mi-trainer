"""Styles and color schemes for the UI."""

from prompt_toolkit.styles import Style

# Main application style
APP_STYLE = Style.from_dict({
    # Conversation pane
    "conversation": "bg:#1a1a2e",
    "conversation.client": "#e94560 bold",
    "conversation.client-label": "#e94560 bold",
    "conversation.user": "#0f3460",
    "conversation.user-label": "#00ff88 bold",
    "conversation.message": "#eaeaea",
    "conversation.branch-indicator": "#ffc107 italic",

    # Feedback pane
    "feedback": "bg:#16213e",
    "feedback.header": "#00d9ff bold",
    "feedback.good": "#00ff88",
    "feedback.warning": "#ffc107",
    "feedback.bad": "#ff4757",
    "feedback.suggestion": "#a29bfe italic",
    "feedback.technique": "#74b9ff",
    "feedback.note": "#dfe6e9",

    # Input area
    "input": "bg:#0f0f23",
    "input.prompt": "#00d9ff bold",
    "input.text": "#ffffff",

    # Borders and separators
    "separator": "#333366",
    "border": "#333366",

    # Dialog styles
    "dialog": "bg:#1a1a2e",
    "dialog.body": "bg:#16213e",
    "dialog.title": "#00d9ff bold",

    # Status
    "status": "bg:#0f0f23 #888888",
    "status.key": "#00d9ff",
})

# ANSI color codes for simple terminal output
class Colors:
    """ANSI color codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    # Foreground
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    @classmethod
    def client(cls, text: str) -> str:
        return f"{cls.BRIGHT_MAGENTA}{cls.BOLD}{text}{cls.RESET}"

    @classmethod
    def user(cls, text: str) -> str:
        return f"{cls.BRIGHT_BLUE}{text}{cls.RESET}"

    @classmethod
    def good(cls, text: str) -> str:
        return f"{cls.BRIGHT_GREEN}{text}{cls.RESET}"

    @classmethod
    def warning(cls, text: str) -> str:
        return f"{cls.BRIGHT_YELLOW}{text}{cls.RESET}"

    @classmethod
    def bad(cls, text: str) -> str:
        return f"{cls.BRIGHT_RED}{text}{cls.RESET}"

    @classmethod
    def info(cls, text: str) -> str:
        return f"{cls.BRIGHT_CYAN}{text}{cls.RESET}"

    @classmethod
    def dim(cls, text: str) -> str:
        return f"{cls.DIM}{text}{cls.RESET}"
