# MI Trainer - Design Document

A practice tool for Motivational Interviewing with LLM-powered simulation and real-time analysis.

## Purpose

Motivational Interviewing (MI) is a skill-based counseling approach that benefits from practice with feedback. This tool provides:

1. Simulated conversations with realistic MI dynamics
2. Real-time analysis of both practitioner technique and client responses
3. Two practice modes: as the practitioner or as the client
4. Session management with branching to explore different approaches

## Practice Modes

### Standard Mode

The user practices as the **practitioner**. A simulated client presents with ambivalence about change, and the user applies MI techniques to explore that ambivalence.

- User sends messages as the practitioner
- Client Agent responds in character
- Technique Analyst provides feedback on the user's MI skills
- Response Analyst identifies change talk, sustain talk, and client movement

This mode develops the core skills of conducting MI conversations.

### Role Reversal Mode

The user practices as the **client**. An Interviewer Agent demonstrates MI technique, and the user experiences what it's like to be on the receiving end.

- User sends messages as the client (guided by a scenario)
- Interviewer Agent responds with MI techniques
- Technique Analyst can highlight what good MI looks like
- Response Analyst can coach the user on realistic client responses

This mode builds empathy for the client experience and intuition for how MI techniques feel from the other side.

## Agents

Four LLM-powered agents support the practice experience:

### Client Agent

Roleplays as an ambivalent client in Standard Mode:

- Stays in character based on the scenario
- Responds to MI quality: good MI elicits more openness and change talk; poor MI elicits resistance and sustain talk
- Never breaks character or acknowledges being AI
- Exhibits realistic emotional responses and conversational patterns

### Interviewer Agent

Demonstrates MI technique in Role Reversal Mode:

- Models effective MI practice
- Responds appropriately to the user's client portrayal
- Uses a range of MI techniques (open questions, reflections, affirmations, summaries)
- Adapts to resistance and rolls with it

### Technique Analyst

Analyzes practitioner messages (user in Standard Mode, Interviewer Agent in Role Reversal):

- Identifies techniques used (open questions, reflections, affirmations, etc.)
- Notes MI-consistent behaviors with specific observations
- Flags MI-inconsistent behaviors (unsolicited advice, confrontation, etc.)
- Offers alternative approaches and suggestions
- Can run automatically after each message or on-demand

### Response Analyst

Analyzes client messages (Client Agent in Standard Mode, user in Role Reversal):

- Identifies **change talk** - statements favoring change
- Identifies **sustain talk** - statements favoring status quo
- Categorizes using **DARN-CAT** framework:
  - *Preparatory*: Desire ("I want..."), Ability ("I could..."), Reasons ("Because..."), Need ("I have to...")
  - *Mobilizing*: Commitment ("I will..."), Activation ("I'm ready..."), Taking steps ("I've started...")
- Tracks the ratio and progression of change talk vs sustain talk
- Can run automatically after each message or on-demand

## Scenarios

A scenario defines the client persona and context for a practice session. Scenarios are used in both modes - in Standard Mode for the Client Agent, in Role Reversal Mode as guidance for the user.

### Scenario Elements

- **Demographics** - Age, gender, occupation, relevant context
- **Presenting issue** - The topic bringing them to the conversation
- **Ambivalence** - Reasons they might want to change AND reasons they might stay the same (both must be genuine and balanced)
- **Resistance level** - How guarded or open they start (1-5 scale)
- **Background** - History and context that shapes their perspective
- **Personality notes** - Communication style, emotional patterns
- **Change talk triggers** - What MI approaches might elicit openness
- **Sustain talk patterns** - Common resistance statements
- **Opening statement** - How the client begins the conversation

### Built-in Scenarios

| Domain | Example | Key Theme |
|--------|---------|-----------|
| Substance | Smoking cessation | Long-term smoker, family pressure after father's death |
| Substance | Alcohol reduction | Professional questioning wine habit |
| Health | Exercise motivation | Sedentary office worker, doctor's orders |
| Health | Medication adherence | Bipolar, stops meds when stable |
| Life | Career change | Burned-out lawyer, golden handcuffs |
| Life | Relationship conflict | Conflict avoidance damaging marriage |

### Scenario Generation

New scenarios can be generated from brief descriptions:

> "College student, parents pressuring about grades, smoking weed daily"

The Scenario Builder agent produces a complete scenario with demographics, balanced ambivalence, personality, triggers, and opening statement.

## Analysis

### Real-time Feedback

Both analysts can provide feedback during the conversation:

- **Automatic mode** - Analysis appears after each relevant message
- **On-demand mode** - Analysis provided when requested

Users can configure which analysts are active and whether they run automatically or on-demand, allowing for focused practice or comprehensive feedback.

### Session Debrief

At the end of a session, a comprehensive debrief covers both sides of the conversation:

**Technique Analysis:**
- Overall MI adherence assessment
- MI adherence score
- Technique usage breakdown (counts and examples)
- Strengths with specific examples
- Areas for growth with suggestions

**Response Analysis:**
- Change talk vs sustain talk ratio
- Progression over time (did client movement occur?)
- DARN-CAT breakdown
- Correlation between techniques used and client responses

**Overall:**
- Key moments in the conversation
- Most effective interventions
- Missed opportunities
- Takeaways for future practice

## Conversation Tree

Conversations are stored as a tree rather than a linear history. This enables:

- **Rewind** - Go back to an earlier point in the conversation
- **Retry** - Try a different approach from that point
- **Compare** - See how different techniques lead to different outcomes
- **Branch preservation** - All paths are saved, nothing is lost

This structure supports the experimental nature of skill practice - trying different approaches and observing their effects.

## Key Capabilities

- **Practice modes** - Switch between practitioner and client roles
- **Configurable analysis** - Choose which analysts are active and when they provide feedback
- **Hints** - Ask for technique suggestions without getting exact words
- **Rewind** - Go back N messages and try a different approach
- **Branch navigation** - View and move between different conversation paths
- **Save/Load** - Persist sessions for later continuation or review
- **Generate scenarios** - Create new client personas from brief descriptions
- **Debrief** - Get comprehensive end-of-session analysis

## Design Principles

### Dual-Perspective Learning

Both practitioner and client perspectives matter. Standard Mode develops technique; Role Reversal develops empathy and intuition. The same analysis tools work in both modes, providing consistent feedback regardless of which role the user takes.

### Balanced Ambivalence

Each scenario includes genuine reasons for both change AND status quo. The client isn't "supposed to" change - they're genuinely ambivalent. This creates realistic practice conditions where MI techniques actually matter.

### Parallel Execution

Running agents simultaneously provides natural conversational flow. Users don't wait for sequential processing - responses and analysis stream as they're generated.

### Tree Structure for Experimentation

Linear conversation history would require starting over to try different approaches. The tree structure preserves all attempts, enabling direct comparison of how different techniques affect client responses.

### Flexible Analysis

Different learning goals call for different feedback configurations. A beginner might want automatic feedback on everything; an experienced practitioner might want analysis only on-demand. The tool adapts to the user's needs.

## Future Considerations

- Progress tracking across sessions
- Technique-specific drills
- Export capabilities
- MI concept reference
- Configurable agent skill levels
- Guided scenarios for Role Reversal (prompts for what to express)
- Audio/speech integration
