# MI Trainer - Design Document

A practice tool for Motivational Interviewing with LLM-powered client simulation and real-time coaching feedback.

## Purpose

Motivational Interviewing (MI) is a skill-based counseling approach that benefits from practice with feedback. This tool provides:

1. A simulated client that responds realistically to MI techniques
2. A coach that analyzes the practitioner's responses in real-time
3. Session management with branching to explore different approaches

## Core Components

### Agents

Three LLM-powered agents work together:

**Client Agent** - Roleplays as the client persona:
- Stays in character based on the scenario
- Responds to MI quality: good MI → more openness and change talk; poor MI → resistance and sustain talk
- Never breaks character or acknowledges being AI

**Coach Agent** - Analyzes practitioner technique:
- Provides real-time feedback after each user message (what techniques were used, what was MI-consistent or inconsistent, suggestions)
- Offers hints on request (technique suggestions without giving exact words)
- Delivers end-of-session debriefs with scores, strengths, areas for growth, and client movement analysis

**Scenario Builder Agent** - Generates client personas from brief descriptions:
- Input: "College student, parents pressuring about grades, smoking weed daily"
- Output: Complete scenario with demographics, ambivalence, personality, triggers, etc.

### Scenarios

A scenario defines the client persona for a practice session:

- **Demographics** - Age, gender, occupation, relevant context
- **Presenting issue** - The topic bringing them to the conversation
- **Ambivalence** - Reasons they might want to change AND reasons they might stay the same (both must be genuine and balanced)
- **Resistance level** - How guarded or open they start (1-5 scale)
- **Background** - History and context that shapes their perspective
- **Personality notes** - Communication style, emotional patterns
- **Change talk triggers** - What MI approaches might elicit openness
- **Sustain talk patterns** - Common resistance statements

Built-in scenarios cover different domains:

| Domain | Example | Key Theme |
|--------|---------|-----------|
| Substance | Smoking cessation | Long-term smoker, family pressure after father's death |
| Substance | Alcohol reduction | Professional questioning wine habit |
| Health | Exercise motivation | Sedentary office worker, doctor's orders |
| Health | Medication adherence | Bipolar, stops meds when stable |
| Life | Career change | Burned-out lawyer, golden handcuffs |
| Life | Relationship conflict | Conflict avoidance damaging marriage |

### Conversation Tree

Conversations are stored as a tree rather than a linear history. This enables:

- **Rewind** - Go back to an earlier point in the conversation
- **Retry** - Try a different approach from that point
- **Compare** - See how different techniques lead to different outcomes
- **Branch preservation** - All paths are saved, nothing is lost

### Coach Feedback

After each practitioner message, the coach provides structured feedback:

- **Techniques used** - Open questions, reflections, affirmations, etc.
- **MI-consistent** - What aligned well with MI principles
- **MI-inconsistent** - What worked against MI principles
- **Suggestions** - Alternative approaches to consider
- **Overall note** - Brief summary

The coach analyzes *what the practitioner said*, not the client's response to it. This focuses feedback on technique rather than outcomes.

### Session Debrief

At the end of a session, the coach provides:

- Overall assessment
- MI adherence score (X/10)
- Technique usage breakdown
- Strengths with specific examples
- Areas for growth with suggestions
- Client movement analysis (change talk vs sustain talk over time)
- Key takeaway

## User Experience

### Core Flow

1. User selects or generates a scenario
2. Client delivers opening statement
3. User responds to client
4. In parallel:
   - Client responds to user (primary interaction)
   - Coach provides feedback on user's message (secondary panel)
5. Repeat until user ends session or requests debrief

### Key Capabilities

- **Hint** - Ask the coach for technique suggestions without getting exact words
- **Rewind** - Go back N messages and try a different approach
- **Branch** - View and navigate between different conversation paths
- **Save/Load** - Persist sessions for later continuation or review
- **Generate** - Create new scenarios from brief descriptions

## Design Principles

### Parallel Agent Execution

Running coach and client simultaneously provides natural conversational flow. The user doesn't wait for sequential analysis - the client response streams as the primary focus while coach feedback appears alongside.

### Tree Structure for Learning

Linear conversation history would require starting over to try different approaches. The tree structure preserves all attempts, enabling direct comparison of how different techniques affect client responses.

### Balanced Scenarios

Each scenario includes genuine reasons for both change AND status quo. The client isn't "supposed to" change - they're genuinely ambivalent. This creates realistic practice conditions where MI techniques actually matter.

### Streaming Responses

Both client and coach responses stream in real-time. Users see responses forming rather than waiting for complete generation, maintaining engagement and natural conversational rhythm.

## Future Considerations

- Progress tracking across sessions
- Technique-specific drills
- Export capabilities
- MI concept reference
- Configurable coach focus/strictness
- Audio/speech integration
