# MI Trainer - MVP Scope

Minimum viable product: Standard Mode with core practice loop.

## Goal

A practitioner can sign in, select a scenario, practice MI with a simulated client, receive real-time technique feedback, and save their session.

## Included Features

### User Accounts
- Sign up / sign in via Clerk
- Basic profile (managed by Clerk)

### Home / Dashboard
- Welcome message
- Start new session button
- Recent sessions list (if any)

### Scenario Selection
- List of built-in scenarios
- Scenario preview (name, description, presenting issue, resistance level)
- Select to begin session

### Practice View
- Two-pane layout (conversation left, analysis right)
- Conversation thread with user and client messages
- Real-time streaming of client responses
- Real-time streaming of technique analysis
- Input area for user messages
- End session button

### Agents
- **Client Agent** - Responds in character based on scenario, reacts to MI quality
- **Technique Analyst** - Analyzes each user message, provides feedback on techniques used, MI-consistent/inconsistent behaviors, suggestions

### Session Persistence
- Auto-save during practice
- Session stored with full conversation
- Resume from sessions list

### Basic Debrief
- Shown when session ends
- Summary of techniques used
- Key strengths and areas for growth
- Option to return to dashboard

## Excluded from MVP

Deferred to later versions:

- Role Reversal Mode
- Technique Drills
- Response Analyst (change talk / sustain talk analysis)
- Progress tracking across sessions
- Scenario generation from description
- User-created scenarios
- Conversation branching (rewind/retry)
- Hints on demand
- MI reference material
- Export / sharing
- Configurable analyst settings (always automatic in MVP)

## Screens

```
Landing Page (public)
    ↓
Sign In / Sign Up
    ↓
Dashboard
    ↓
Scenario Selection
    ↓
Practice View
    ↓
Debrief
    ↓
Dashboard
```

## Data Model (MVP subset)

**User** - Managed by Clerk

**Scenario** (built-in only for MVP)
- id, name, description
- demographics, presenting_issue
- ambivalence, resistance_level
- background, personality_notes
- change_talk_triggers, sustain_talk
- opening_statement

**Session**
- id, user_id, scenario_id
- status (active, completed)
- created_at, updated_at

**Message**
- id, session_id
- role (user, client)
- content
- timestamp
- technique_feedback (JSON, nullable)

## API Routes

**POST /api/chat**
- Streams client response
- Input: session_id, user message
- Output: SSE stream of client response chunks

**POST /api/analyze**
- Streams technique analysis
- Input: session_id, user message, conversation context
- Output: SSE stream of analysis chunks

**POST /api/sessions**
- Create new session
- Input: scenario_id
- Output: session object

**GET /api/sessions**
- List user's sessions

**GET /api/sessions/[id]**
- Get session with messages

**PATCH /api/sessions/[id]**
- Update session (e.g., mark completed)

**GET /api/scenarios**
- List available scenarios

**GET /api/scenarios/[id]**
- Get scenario details

## Success Criteria

MVP is complete when a user can:

1. Create an account and sign in
2. See a dashboard with option to start practicing
3. Browse and select from built-in scenarios
4. Engage in a multi-turn conversation with a simulated client
5. See technique feedback updating in real-time alongside the conversation
6. End the session and see a debrief summary
7. Return to dashboard and see the session in their history
8. Resume or review a past session

## Decisions

- **Scenarios**: Use all 6 from Python prototype (`mi_trainer/scenarios/`)
- **Debrief**: LLM-generated for richer, contextual feedback
- **Conversation structure**: Linear for MVP (no branching/rewind)

## Reusable Assets

From the Python prototype:

**Prompts** (`mi_trainer/prompts/`)
- `client_system.md` - Client agent system prompt, works as-is
- `coach_system.md` - Technique analyst prompt, outputs structured JSON

**Scenarios** (`mi_trainer/scenarios/`)
- `smoking_cessation.json`
- `alcohol_reduction.json`
- `exercise_motivation.json`
- `medication_adherence.json`
- `career_change.json`
- `relationship_conflict.json`

**To Create**
- Debrief system prompt (LLM-generated session summary)
