# MI Trainer - Design Document

A CLI tool for practicing Motivational Interviewing with LLM-powered client simulation and real-time coaching feedback.

## Overview

### Purpose

Motivational Interviewing (MI) is a skill-based counseling approach that benefits from practice with feedback. This tool provides:

1. A simulated client that responds realistically to MI techniques
2. A coach that analyzes the practitioner's responses in real-time
3. Session management with branching to explore different approaches

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      prompt_toolkit UI                       │
│  ┌─────────────────────────┬─────────────────────────────┐  │
│  │   Conversation Pane     │     Feedback Pane           │  │
│  │   (70% width)           │     (30% width)             │  │
│  │   - Client messages     │     - Coach analysis        │  │
│  │   - User messages       │     - Technique IDs         │  │
│  │   - Branch indicators   │     - Suggestions           │  │
│  ├─────────────────────────┴─────────────────────────────┤  │
│  │   Input Area (vim keybindings)                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  - Command parsing (/help, /hint, /rewind, etc.)            │
│  - Session management                                        │
│  - Async coordination of agents                              │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     ┌────────────┐   ┌────────────┐   ┌────────────────┐
     │   Client   │   │   Coach    │   │   Scenario     │
     │   Agent    │   │   Agent    │   │   Builder      │
     └────────────┘   └────────────┘   └────────────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Anthropic API  │
                    │  (Claude)       │
                    └─────────────────┘
```

### Technology Stack

- **Python 3.11+**
- **prompt_toolkit** - Terminal UI with split panes, vim keybindings
- **anthropic** - Claude API client
- **pydantic** - Data validation and serialization
- **python-dotenv** - Environment configuration

## Project Structure

```
mi_trainer/
├── __init__.py
├── main.py                     # Entry point, CLI argument parsing
├── app.py                      # Main application orchestration
├── config.py                   # API keys, paths, settings
├── ui/
│   ├── __init__.py
│   ├── layout.py               # Main prompt_toolkit layout composition
│   ├── conversation_pane.py    # Left pane - conversation display
│   ├── feedback_pane.py        # Right pane - coach feedback
│   ├── input_area.py           # Bottom input with buffer management
│   └── styles.py               # Color schemes
├── agents/
│   ├── __init__.py
│   ├── base.py                 # Base agent with Anthropic client
│   ├── client.py               # Client persona agent
│   ├── coach.py                # MI feedback agent
│   └── scenario_builder.py     # Generates personas from descriptions
├── models/
│   ├── __init__.py
│   ├── scenario.py             # Client persona data model
│   ├── conversation.py         # Conversation tree with branching
│   └── feedback.py             # Coach feedback structure
├── storage/
│   ├── __init__.py
│   ├── sessions.py             # Save/load conversation sessions
│   └── scenarios.py            # Scenario library management
├── prompts/
│   ├── client_system.md        # Client agent system prompt
│   ├── coach_system.md         # Coach agent system prompt
│   └── scenario_builder.md     # Scenario generator prompt
└── scenarios/                  # Built-in scenario JSON files
    ├── smoking_cessation.json
    ├── alcohol_reduction.json
    ├── exercise_motivation.json
    ├── medication_adherence.json
    ├── career_change.json
    └── relationship_conflict.json
```

## Data Models

### Scenario

Represents a client persona for practice sessions.

```python
class Ambivalence(BaseModel):
    change: list[str]       # Reasons client might want to change
    status_quo: list[str]   # Reasons client might stay the same

class Scenario(BaseModel):
    id: str                                  # Unique identifier
    name: str                                # Display name
    description: str                         # Brief description
    demographics: str                        # Age, gender, occupation
    presenting_issue: str                    # Main issue being discussed
    ambivalence: Ambivalence                 # Mixed feelings about change
    resistance_level: int                    # 1-5 scale
    background: str                          # History and context
    personality_notes: str                   # How they communicate
    potential_change_talk_triggers: list[str]
    common_sustain_talk: list[str]
    opening_statement: str                   # How client starts conversation
```

### ConversationTree

Supports branching conversations for rewind/retry functionality.

```python
class ConversationNode(BaseModel):
    id: str                              # Short UUID
    role: Literal["user", "client"]
    content: str
    timestamp: datetime
    parent_id: Optional[str]             # For tree structure
    children: list[str]                  # Child node IDs
    coach_feedback: Optional[CoachFeedback]

class ConversationTree(BaseModel):
    nodes: dict[str, ConversationNode]   # All nodes by ID
    root_id: Optional[str]
    current_id: Optional[str]            # Current position in tree

    # Key methods:
    # - add_message(role, content) -> adds child to current, moves current
    # - rewind(steps) -> moves current up the tree
    # - get_path_to_current() -> returns linear path for display
    # - get_branches_at_current() -> returns children for branch selection
    # - get_conversation_for_llm() -> formats path as messages list
```

### CoachFeedback

Structured feedback from the coach agent.

```python
class CoachFeedback(BaseModel):
    techniques_used: list[str]     # e.g., ["open_question", "reflection"]
    mi_consistent: list[str]       # Positive observations
    mi_inconsistent: list[str]     # Issues to address
    suggestions: list[str]         # Alternative approaches
    overall_note: str              # Brief summary
```

### Session

Combines scenario and conversation for persistence.

```python
class Session(BaseModel):
    scenario: Scenario
    conversation: ConversationTree
    created_at: datetime
    updated_at: datetime
```

## Agents

### Base Agent

All agents inherit from BaseAgent which provides:
- Anthropic async client initialization
- Prompt loading from markdown files
- Streaming and non-streaming response methods

```python
class BaseAgent:
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.AsyncAnthropic(api_key=get_api_key())
        self.model = model

    async def stream_response(self, system_prompt, messages) -> AsyncIterator[str]
    async def get_response(self, system_prompt, messages, max_tokens=1024) -> str
```

### Client Agent

Roleplays as the client persona. Key behaviors:
- Stays in character based on scenario
- Responds to MI quality: good MI → more openness/change talk; poor MI → resistance/sustain talk
- Never breaks character or acknowledges being AI

**System prompt structure:**
1. Role definition (roleplay as ambivalent client)
2. Scenario context (injected from Scenario.to_prompt_context())
3. Response guidelines based on MI quality
4. Instructions to maintain character

### Coach Agent

Analyzes practitioner responses. Provides:
- **analyze()** - Real-time feedback after each user message (returns CoachFeedback)
- **get_hint()** - Technique suggestion without exact words
- **get_debrief()** - Full session analysis with scores and breakdown

**Feedback JSON schema:**
```json
{
  "techniques_used": ["open_question", "complex_reflection"],
  "mi_consistent": ["Good empathic listening", "Rolled with resistance well"],
  "mi_inconsistent": ["Gave advice without permission"],
  "suggestions": ["Try reflecting the ambivalence back"],
  "overall_note": "Solid response, watch the advice-giving"
}
```

**Debrief structure:**
- Overall Assessment
- MI Adherence Score (X/10)
- Techniques Used (counts)
- Strengths (with examples)
- Areas for Growth (with suggestions)
- Client Movement (change talk vs sustain talk progression)
- Key Takeaway

### Scenario Builder Agent

Generates complete Scenario from brief description. Input example:
> "College student, parents pressuring about grades, smoking weed daily"

Output: Full Scenario JSON with demographics, ambivalence map, personality, triggers, etc.

## UI Components

### Layout

Uses prompt_toolkit's HSplit/VSplit for structure:
```
HSplit([
    VSplit([
        Frame(conversation_pane),      # 70%
        Window(char="│"),              # Separator
        Frame(feedback_pane),          # 30%
    ]),
    Window(char="─"),                  # Separator
    VSplit([prompt, input_area]),      # Input line
    status_bar,                        # Bottom status
])
```

### Conversation Pane

- Displays messages with role labels ("Client:" in magenta, "You:" in green)
- Word-wraps text at whitespace boundaries (not mid-word)
- Shows branch indicators when at a branch point
- Supports streaming display during response generation

### Feedback Pane

- Shows coach feedback with color coding:
  - Green (+) for MI-consistent behaviors
  - Red (-) for MI-inconsistent behaviors
  - Yellow/italic (>) for suggestions
- Word-wraps to fit narrower pane
- Clears and repopulates for debrief display

### Input Area

- Single-line input with vim keybindings (EditingMode.VI)
- Command history (up/down arrows)
- Clears after submission
- Handles both messages and /commands

## Commands

| Command | Handler | Description |
|---------|---------|-------------|
| `/help` | `_cmd_help` | Display command list |
| `/hint` | `_cmd_hint` | Get technique suggestion from coach |
| `/debrief` | `_cmd_debrief` | Full session analysis |
| `/quit` | `_cmd_quit` | Save and exit |
| `/save` | `_cmd_save` | Save current session |
| `/load [n]` | `_cmd_load` | List or load saved sessions |
| `/scenario [n]` | `_cmd_scenario` | List or select scenarios |
| `/new <desc>` | `_cmd_new` | Generate scenario from description |
| `/rewind [n]` | `_cmd_rewind` | Go back n messages in tree |
| `/branches` | `_cmd_branches` | Show branches at current point |
| `/goto <id>` | `_cmd_goto` | Jump to specific node |

## Key Bindings

```python
kb = KeyBindings()

# Application control
kb.add("c-c", "c-q")     # Exit
kb.add("c-s")            # Save

# Scroll conversation pane
kb.add("pageup", "c-up")      # Scroll up
kb.add("pagedown", "c-down")  # Scroll down

# Scroll feedback pane
kb.add("s-pageup", "s-up")    # Scroll up
kb.add("s-pagedown", "s-down") # Scroll down
```

## Main Loop

```python
async def run(self, scenario, load_path):
    # 1. Initialize session (load or create)
    # 2. Create client agent with scenario
    # 3. Get client opening statement if new session
    # 4. Run prompt_toolkit application

    await self.app.run_async()

def _handle_input(self, text):
    # Called synchronously by input buffer accept_handler
    # Schedules async processing
    asyncio.create_task(self._process_input(text))

async def _process_input(self, text):
    if text.startswith("/"):
        await self._handle_command(text)
    else:
        await self._handle_message(text)

async def _handle_message(self, text):
    # 1. Add user message to conversation tree
    # 2. Update conversation pane
    # 3. Run coach and client agents in parallel:
    asyncio.gather(
        self._run_coach(conversation, text),   # -> feedback pane
        self._run_client(conversation),        # -> conversation pane
    )
    # 4. Both stream their output to respective panes
```

## Storage

### Locations

```python
DATA_DIR = Path.home() / ".mi-trainer"
SESSIONS_DIR = DATA_DIR / "sessions"
USER_SCENARIOS_DIR = DATA_DIR / "scenarios"
BUILTIN_SCENARIOS_DIR = Path(__file__).parent / "scenarios"
```

### Session Files

JSON files named `{timestamp}_{scenario_id}.json` containing:
- Full Scenario object
- Complete ConversationTree with all branches
- Timestamps

### Scenario Files

JSON files with Scenario schema. Built-in scenarios ship with package; user scenarios saved to ~/.mi-trainer/scenarios/.

## Built-in Scenarios

Six scenarios covering different domains and resistance levels:

| ID | Domain | Resistance | Key Theme |
|----|--------|------------|-----------|
| smoking_cessation | Substance | 3/5 | Long-term smoker, family pressure after father's death |
| alcohol_reduction | Substance | 2/5 | Professional questioning wine habit, mother had problems |
| exercise_motivation | Health | 3/5 | Sedentary office worker, doctor's orders |
| medication_adherence | Health | 3/5 | Bipolar, stops meds when stable, partner ultimatum |
| career_change | Life | 2/5 | Burned-out lawyer, golden handcuffs, teaching dream |
| relationship_conflict | Life | 3/5 | Conflict avoidance damaging marriage |

Each scenario includes:
- Detailed demographics and background
- Balanced ambivalence (real reasons for and against change)
- Personality notes affecting communication style
- Change talk triggers and sustain talk patterns
- Realistic opening statement

## Design Decisions

### Why conversation tree instead of linear history?

Enables rewind/retry - a key learning technique. Users can go back, try a different approach, and see how the client responds differently. Branches are preserved for comparison.

### Why parallel agent execution?

Running coach and client simultaneously provides natural conversational flow. The client response (primary) streams to the conversation pane while coach feedback streams to the side panel. User doesn't wait for sequential API calls.

### Why vim keybindings?

Target users (practitioners, researchers) often work in terminals. Vim bindings provide efficient text editing. Falls back to standard editing for those unfamiliar.

### Why word-wrap manually instead of prompt_toolkit's wrap_lines?

prompt_toolkit's built-in wrapping breaks mid-word. Manual wrapping with textwrap.fill() respects word boundaries for better readability.

### Why JSON for storage instead of SQLite?

Session data is tree-structured and naturally maps to JSON. Files are human-readable, easy to debug, and don't require database dependencies. Could add SQLite index layer later for cross-session queries.

### Why stream responses?

Streaming provides immediate feedback and maintains engagement. Users see the response forming rather than waiting for complete generation.

## Dependencies

```toml
[project]
dependencies = [
    "anthropic>=0.40.0",
    "prompt_toolkit>=3.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]
```

## Future Enhancements

Potential additions not in MVP:
- Progress tracking across sessions (SQLite for metrics)
- Technique drills (focused practice on single skills)
- Export to markdown/PDF
- Quick reference command for MI concepts
- Configurable coach strictness/focus
- Audio/speech integration
