# MI Trainer

A command-line tool for practicing Motivational Interviewing with AI-powered client simulation and real-time coaching feedback.

## What is Motivational Interviewing?

Motivational Interviewing (MI) is an evidence-based counseling approach that helps people resolve ambivalence and find internal motivation for change. It's widely used in healthcare, addiction treatment, social work, and coaching.

MI Trainer lets you practice MI skills in a safe environment with:
- **Realistic client personas** that respond naturally to your approach
- **Real-time coaching feedback** analyzing your technique after each response
- **Session recording** with branching to try different approaches

## Features

- **Split-pane interface**: Conversation on the left, coach feedback on the right
- **Six built-in scenarios** across substance use, health behaviors, and life changes
- **Custom scenario generation**: Describe a client, get a full persona
- **Real-time MI feedback**: Identifies techniques used, highlights strengths, flags issues
- **Hint system**: Get technique suggestions without being given exact words
- **Session debrief**: Full analysis with MI adherence score and technique breakdown
- **Conversation branching**: Rewind and try different approaches
- **Session persistence**: Save and load practice sessions
- **Vim keybindings**: For efficient text input

## Installation

### Prerequisites

- Python 3.11 or higher
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/yourusername/mi-trainer.git
cd mi-trainer

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .

# Set your API key
export ANTHROPIC_API_KEY=your_api_key_here
```

To make the API key permanent, add the export line to your `~/.bashrc`, `~/.zshrc`, or equivalent.

### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/yourusername/mi-trainer.git
cd mi-trainer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install the package
pip install -e .

# Set your API key (current session)
$env:ANTHROPIC_API_KEY = "your_api_key_here"
```

To make the API key permanent on Windows, set it as a system environment variable through System Properties > Environment Variables.

### Windows (Command Prompt)

```cmd
# Clone the repository
git clone https://github.com/yourusername/mi-trainer.git
cd mi-trainer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

# Install the package
pip install -e .

# Set your API key (current session)
set ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Starting a Session

```bash
# Launch with scenario selection
mi-trainer

# Start with a specific scenario
mi-trainer --scenario smoking

# List available scenarios
mi-trainer --list-scenarios

# Load a previous session
mi-trainer --load path/to/session.json
```

### Interface

```
┌─────────────────────────────────┬──────────────────────────┐
│  Conversation                   │  Coach Feedback          │
│                                 │                          │
│  Client: [their message]        │  Techniques: reflection  │
│                                 │                          │
│  You: [your response]           │  + Good use of empathy   │
│                                 │  > Consider exploring... │
│                                 │                          │
├─────────────────────────────────┴──────────────────────────┤
│ > [type here]                                              │
└────────────────────────────────────────────────────────────┘
```

### Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/hint` | Get a technique suggestion for your next response |
| `/debrief` | Full session analysis with MI adherence score |
| `/save` | Save current session |
| `/load <n>` | Load a saved session |
| `/scenario [n]` | List or select a scenario |
| `/new <desc>` | Generate a new scenario from a description |
| `/rewind [n]` | Go back n messages (default: 1) |
| `/branches` | Show conversation branches at current point |
| `/goto <id>` | Jump to a specific conversation node |
| `/quit` | Save and exit |

### Keyboard Shortcuts

**General:**
- `Ctrl+C` or `Ctrl+Q` - Exit
- `Ctrl+S` - Save session

**Scrolling (Conversation pane):**
- `Page Up` / `Page Down`
- `Ctrl+Up` / `Ctrl+Down`

**Scrolling (Feedback pane):**
- `Shift+Page Up` / `Shift+Page Down`
- `Shift+Up` / `Shift+Down`

**Input (Vim mode):**
- `Esc` - Enter normal mode
- `i`, `a`, `A` - Enter insert mode
- Standard vim navigation and editing

## Built-in Scenarios

| Scenario | Description | Resistance |
|----------|-------------|------------|
| Smoking Cessation | 45-year-old long-term smoker after family health scare | 3/5 |
| Alcohol Reduction | 38-year-old professional questioning drinking habits | 2/5 |
| Exercise Motivation | 52-year-old with doctor's orders to get active | 3/5 |
| Medication Adherence | 34-year-old with bipolar disorder stopping meds when stable | 3/5 |
| Career Change | 41-year-old burned-out lawyer considering teaching | 2/5 |
| Relationship Conflict | 29-year-old whose conflict avoidance is hurting marriage | 3/5 |

## Creating Custom Scenarios

Use `/new` with a brief description:

```
/new College student, junior year, parents worried about grades dropping.
Smoking weed daily, doesn't think it's a problem. Defensive about autonomy.
```

The AI will generate a complete persona with demographics, ambivalence factors, personality traits, and common responses.

## Tips for Effective Practice

1. **Start with `/hint`** if you're unsure what to say next
2. **Use `/rewind`** to try a different approach and see how the client responds differently
3. **Run `/debrief`** after 5-10 exchanges for meaningful feedback
4. **Focus on one skill** at a time (e.g., practice just reflections for a session)
5. **Review saved sessions** to track your progress over time

## MI Quick Reference

**OARS Skills:**
- **O**pen questions - Invite elaboration ("What concerns you about...?")
- **A**ffirmations - Recognize strengths ("You've shown real courage in...")
- **R**eflections - Mirror back understanding ("It sounds like...")
- **S**ummaries - Collect and link what's been shared

**Spirit of MI:**
- Partnership (collaborative, not expert-driven)
- Acceptance (unconditional positive regard)
- Compassion (client's welfare is priority)
- Evocation (draw out, don't install motivation)

**Avoid the "Righting Reflex":**
- Don't give unsolicited advice
- Don't argue for change
- Don't warn, lecture, or persuade
- Roll with resistance instead

## Data Storage

- Sessions are saved to `~/.mi-trainer/sessions/`
- Custom scenarios are saved to `~/.mi-trainer/scenarios/`
- All data is stored locally as JSON files

## License

MIT

## Acknowledgments

Built with:
- [Anthropic Claude](https://www.anthropic.com/) for AI capabilities
- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) for the terminal UI
- [Pydantic](https://pydantic.dev/) for data validation
