# MI Trainer - Design Document

A practice tool for Motivational Interviewing with LLM-powered simulation and real-time analysis.

## Purpose

Motivational Interviewing (MI) is a skill-based counseling approach that benefits from practice with feedback. This tool provides:

1. Simulated conversations with realistic MI dynamics
2. Real-time analysis of both practitioner technique and client responses
3. Multiple practice modes for different learning goals
4. Progress tracking to support skill development over time
5. Session management with branching to explore different approaches

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

- User sends messages as the client, guided by a scenario
- Interviewer Agent responds with MI techniques
- Technique Analyst can highlight what good MI looks like
- Response Analyst can coach the user on realistic client responses

**Guided client practice:** The scenario provides the user with context for their character - background, ambivalence, personality. The Response Analyst can offer suggestions for realistic responses: when to express sustain talk, how to voice ambivalence authentically, what change talk might emerge naturally given the scenario. This helps users develop intuition for the client experience.

**Interviewer skill levels:** The Interviewer Agent can be configured to demonstrate different skill levels:
- *Expert* - Models exemplary MI technique consistently
- *Competent* - Good overall with occasional missed opportunities
- *Learning* - Makes common mistakes (unsolicited advice, closed questions, premature focus) that users can observe and recognize

Seeing imperfect MI demonstrated helps users identify what *not* to do, complementing the expert demonstrations.

### Technique Drills

Focused practice on specific MI skills in isolation:

- **Reflections** - Practice forming simple and complex reflections in response to client statements
- **Open questions** - Develop skill in asking questions that invite exploration rather than yes/no answers
- **Affirmations** - Practice recognizing and affirming client strengths and efforts
- **Summaries** - Practice collecting and reflecting back key themes from a conversation segment
- **Rolling with resistance** - Practice responding to sustain talk without confrontation
- **Eliciting change talk** - Practice techniques that evoke client arguments for change

Drills present client statements or conversation segments and prompt the user to respond using the target technique. The Technique Analyst provides focused feedback on that specific skill, tracking improvement within the drill session.

## Agents

Four LLM-powered agents support the practice experience:

### Client Agent

Roleplays as an ambivalent client in Standard Mode and Technique Drills:

- Stays in character based on the scenario
- Responds to MI quality: good MI elicits more openness and change talk; poor MI elicits resistance and sustain talk
- Never breaks character or acknowledges being AI
- Exhibits realistic emotional responses and conversational patterns
- Always strives for realism and adherence to the scenario

### Interviewer Agent

Demonstrates MI technique in Role Reversal Mode:

- Models MI practice at a configurable skill level (expert, competent, or learning)
- Responds appropriately to the user's client portrayal
- Uses a range of MI techniques (open questions, reflections, affirmations, summaries)
- Adapts to resistance and rolls with it (at higher skill levels)
- At lower skill levels, exhibits common MI-inconsistent behaviors for educational contrast

### Technique Analyst

Analyzes practitioner messages (user in Standard Mode, Interviewer Agent in Role Reversal):

- Identifies techniques used (open questions, reflections, affirmations, etc.)
- Notes MI-consistent behaviors with specific observations
- Flags MI-inconsistent behaviors (unsolicited advice, confrontation, etc.)
- Offers alternative approaches and suggestions
- Can run automatically after each message or on-demand
- Provides focused feedback during Technique Drills

### Response Analyst

Analyzes client messages (Client Agent in Standard Mode, user in Role Reversal):

- Identifies **change talk** - statements favoring change
- Identifies **sustain talk** - statements favoring status quo
- Categorizes using **DARN-CAT** framework:
  - *Preparatory*: Desire ("I want..."), Ability ("I could..."), Reasons ("Because..."), Need ("I have to...")
  - *Mobilizing*: Commitment ("I will..."), Activation ("I'm ready..."), Taking steps ("I've started...")
- Tracks the ratio and progression of change talk vs sustain talk
- Can run automatically after each message or on-demand
- In Role Reversal, coaches users on authentic client responses

## Scenarios

A scenario defines the client persona and context for a practice session. Scenarios are used across all modes - in Standard Mode for the Client Agent, in Role Reversal Mode as guidance for the user, and in Technique Drills for context.

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

## Analysis & Feedback

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

### Progress Tracking

Skill development is tracked across sessions to support long-term learning:

**MI Adherence:**
- Adherence scores over time
- Trend analysis showing improvement or areas needing attention
- Breakdown by MI-consistent and MI-inconsistent behaviors

**Technique Development:**
- Frequency of each technique type across sessions
- Diversity of technique usage (are they developing range?)
- Quality trends within technique categories (e.g., simple vs complex reflections)

**Client Movement:**
- How often sessions produce client movement toward change
- Correlation between specific techniques and change talk
- Patterns in what approaches work best for the user

**Drill Performance:**
- Progress within specific technique drills
- Skills that have strengthened vs skills needing more practice

Progress data helps users identify what's working, what needs attention, and how their skills are developing over time.

## MI Reference

Built-in reference material supports learning during practice:

**Core Concepts:**
- The spirit of MI (partnership, acceptance, compassion, evocation)
- The four processes (engaging, focusing, evoking, planning)
- Change talk and sustain talk
- The DARN-CAT framework
- Ambivalence and the righting reflex

**Technique Reference:**
- OARS (Open questions, Affirmations, Reflections, Summaries)
- Types of reflections (simple, complex, amplified, double-sided)
- Strategies for evoking change talk
- Responding to sustain talk
- Common MI-inconsistent behaviors to avoid

**Contextual Help:**
- Reference material can be accessed on-demand during practice
- Relevant concepts can be highlighted in analyst feedback
- Debrief can link to reference material for areas needing development

## Conversation Tree

Conversations are stored as a tree rather than a linear history. This enables:

- **Rewind** - Go back to an earlier point in the conversation
- **Retry** - Try a different approach from that point
- **Compare** - See how different techniques lead to different outcomes
- **Branch preservation** - All paths are saved, nothing is lost

This structure supports the experimental nature of skill practice - trying different approaches and observing their effects.

## Sharing & Export

Sessions can be exported for sharing with peers, supervisors, or training groups. Export captures the conversation, analyst feedback, and debrief to support discussion and collaborative learning. The specific format and mechanism depends on the platform.

## Key Capabilities

- **Practice modes** - Standard (as practitioner), Role Reversal (as client), Technique Drills (focused skills)
- **Configurable analysis** - Choose which analysts are active and when they provide feedback
- **Interviewer skill levels** - See expert MI or learn from common mistakes
- **Guided client practice** - Coaching for realistic client responses in Role Reversal
- **Progress tracking** - Monitor skill development across sessions
- **MI reference** - Access concept and technique reference during practice
- **Hints** - Ask for technique suggestions without getting exact words
- **Rewind & branch** - Explore different approaches from any point
- **Save/Load** - Persist sessions for later continuation or review
- **Export** - Share sessions for discussion with others
- **Generate scenarios** - Create new client personas from brief descriptions
- **Debrief** - Get comprehensive end-of-session analysis

## Design Principles

### Dual-Perspective Learning

Both practitioner and client perspectives matter. Standard Mode develops technique; Role Reversal develops empathy and intuition. The same analysis tools work in both modes, providing consistent feedback regardless of which role the user takes.

### Skill Isolation and Integration

Technique Drills allow focused practice on individual skills in isolation. Standard Mode and Role Reversal integrate those skills into full conversations. Both are valuable - drills build component skills, full sessions develop integration and flow.

### Balanced Ambivalence

Each scenario includes genuine reasons for both change AND status quo. The client isn't "supposed to" change - they're genuinely ambivalent. This creates realistic practice conditions where MI techniques actually matter.

### Realism Over Ease

The Client Agent always strives for realistic, scenario-adherent behavior rather than being artificially easy or cooperative. Skill development requires realistic challenge. Difficulty is a function of the scenario (resistance level, complexity) rather than the agent being "nice."

### Parallel Execution

Running agents simultaneously provides natural conversational flow. Users don't wait for sequential processing - responses and analysis stream as they're generated.

### Tree Structure for Experimentation

Linear conversation history would require starting over to try different approaches. The tree structure preserves all attempts, enabling direct comparison of how different techniques affect client responses.

### Flexible Analysis

Different learning goals call for different feedback configurations. A beginner might want automatic feedback on everything; an experienced practitioner might want analysis only on-demand. The tool adapts to the user's needs.

### Long-term Development

Skill development happens over time, not in a single session. Progress tracking helps users see their trajectory, identify patterns, and focus practice where it's most needed.

## Future Considerations

- **Audio/speech integration** - Voice input and output would enable practice with realistic conversational dynamics including tone, pacing, and timing. Speech-to-speech models with prosody analysis could provide feedback on vocal delivery. This represents a significant expansion of complexity but could substantially enhance realism.
