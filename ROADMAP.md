# MI Trainer - Roadmap

Phased approach from MVP to full vision.

## Phase 1: MVP - Standard Mode

The core practice loop.

- [ ] Project setup (Next.js, Prisma, Clerk, Vercel)
- [ ] User authentication (sign up, sign in, sign out)
- [ ] Landing page
- [ ] Dashboard (start session, recent sessions)
- [ ] Scenario selection (display built-in scenarios)
- [ ] Practice view (two-pane layout)
- [ ] Client Agent integration (streaming responses)
- [ ] Technique Analyst integration (streaming feedback)
- [ ] Session persistence (save messages, resume sessions)
- [ ] Basic debrief (LLM-generated summary)
- [ ] Sessions list (view history, resume/review)

**Outcome**: Users can practice MI with a simulated client and receive real-time technique feedback.

## Phase 2: Enhanced Analysis

Richer feedback and insight.

- [ ] Response Analyst (change talk, sustain talk, DARN-CAT)
- [ ] Enhanced debrief (technique + response analysis combined)
- [ ] Recommended drills in debrief (placeholder for Phase 4)
- [ ] Configurable analyst settings (automatic vs on-demand)
- [ ] Analyst toggle in practice view

**Outcome**: Users get comprehensive analysis of both their technique and client responses.

## Phase 3: Conversation Branching

Experimentation and comparison.

- [ ] Conversation tree data model
- [ ] Rewind functionality (go back N messages)
- [ ] Branch navigation UI (arrows or alternative)
- [ ] Branch comparison view
- [ ] Hints on demand (technique suggestions from analyst)

**Outcome**: Users can rewind, try different approaches, and compare outcomes.

## Phase 4: Technique Drills

Focused skill practice.

- [ ] Drill view (compact, rapid-fire interface)
- [ ] Drill types (reflections, open questions, affirmations, summaries, rolling with resistance, eliciting change talk)
- [ ] Drill prompt generation
- [ ] Drill-specific feedback
- [ ] Drill summary (completion stats, strengths, focus areas)
- [ ] Link drills from debrief recommendations

**Outcome**: Users can practice specific MI techniques in isolation.

## Phase 5: Role Reversal

Client perspective practice.

- [ ] Role Reversal mode in session setup
- [ ] Interviewer Agent (demonstrates MI technique)
- [ ] Interviewer skill levels (expert, competent, learning)
- [ ] Adapted analyst behavior for role reversal
- [ ] Guided client practice (Response Analyst coaching)

**Outcome**: Users can experience MI from the client side and learn by observing.

## Phase 6: Progress Tracking

Long-term development support.

- [ ] Progress data model (aggregated metrics)
- [ ] MI adherence trends over time
- [ ] Technique usage patterns
- [ ] Client movement correlation
- [ ] Drill performance tracking
- [ ] Progress view with visualizations

**Outcome**: Users can see their skill development trajectory over time.

## Phase 7: Content & Reference

Learning resources.

- [ ] MI Reference content (core concepts, techniques)
- [ ] Reference view (browsable, searchable)
- [ ] Reference sidebar in practice view
- [ ] Hyperlinked concepts in analyst feedback
- [ ] Contextual tooltips

**Outcome**: Users have learning resources accessible during practice.

## Phase 8: Scenarios & Sharing

User-generated content and collaboration.

- [ ] Scenario Builder agent
- [ ] Generate scenario from description
- [ ] User-created scenarios (save, edit, delete)
- [ ] Session export (format TBD)
- [ ] Share session for peer discussion

**Outcome**: Users can create custom scenarios and share sessions for feedback.

## Future / Exploratory

Not scheduled, but on the radar:

- Audio/speech integration (voice input/output, prosody analysis)
- Mobile-optimized experience
- Team/cohort features (shared progress, group scenarios)
- Integration with training programs
- API for third-party integrations

---

## Notes

- Phases are roughly ordered by dependency and value
- Phases 2-3 could potentially be swapped based on user feedback
- Each phase should be deployable - no "big bang" releases
- Scope within phases may shift as we learn
