# MI Trainer - Technology Stack

Technical decisions for the web application.

## Core Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | Next.js (App Router) | Full-stack React framework |
| Language | TypeScript | Type safety across the codebase |
| UI Library | React | Component-based UI |
| Styling | CSS Modules | Scoped styles, no runtime overhead |
| Database | PostgreSQL | Relational, robust, handles tree structures well |
| ORM | Prisma | Schema-first, excellent DX, strong Next.js integration |
| Authentication | Clerk | Managed auth, easy setup, good React components |
| LLM Integration | Vercel AI SDK + Anthropic | Built-in streaming patterns |
| Hosting | Vercel | Optimized for Next.js, simple deployment |

## Key Libraries

### LLM & Streaming

**Vercel AI SDK** (`ai` package)
- Handles streaming responses from Claude
- `useChat` and related hooks for React
- Server-side streaming utilities
- Works directly with Anthropic's API

**Anthropic SDK** (`@anthropic-ai/sdk`)
- Direct API access for Claude
- Used alongside or through Vercel AI SDK

### Database & ORM

**Prisma**
- Schema defined in `prisma/schema.prisma`
- Type-safe database client generated from schema
- Migrations via `prisma migrate`
- Works well with Vercel Postgres or external Postgres

### Authentication

**Clerk** (`@clerk/nextjs`)
- Pre-built sign-in/sign-up components
- User management dashboard
- Session handling via middleware
- React hooks for auth state

### UI Components

To be determined as needed. Candidates:
- **Radix UI** - Unstyled, accessible primitives
- **React Resizable Panels** - For split-pane layout
- **React Markdown** - Rendering markdown content

## Project Structure

```
mi-trainer/
├── app/                      # Next.js App Router
│   ├── (auth)/               # Auth routes (sign-in, sign-up)
│   ├── (app)/                # Authenticated app routes
│   │   ├── dashboard/        # Home/dashboard
│   │   ├── practice/         # Practice view
│   │   ├── drill/            # Drill view
│   │   ├── debrief/          # Debrief view
│   │   ├── progress/         # Progress view
│   │   ├── scenarios/        # Scenarios management
│   │   ├── sessions/         # Sessions list
│   │   ├── reference/        # MI reference
│   │   └── settings/         # User settings
│   ├── api/                  # API routes
│   │   ├── chat/             # LLM streaming endpoints
│   │   └── ...
│   ├── layout.tsx
│   └── page.tsx              # Landing page
├── components/               # React components
│   ├── ui/                   # Generic UI components
│   ├── practice/             # Practice-specific components
│   ├── drill/                # Drill-specific components
│   └── ...
├── lib/                      # Utilities and helpers
│   ├── agents/               # LLM agent configurations
│   ├── db/                   # Database utilities
│   └── ...
├── prisma/
│   └── schema.prisma         # Database schema
├── public/                   # Static assets
└── styles/                   # Global styles
```

## Database Schema (Outline)

Key entities:

**User** (managed by Clerk, referenced by ID)
- Links to sessions, scenarios, progress data

**Scenario**
- id, name, description, demographics, presenting_issue
- ambivalence (JSON), resistance_level, background
- personality_notes, change_talk_triggers, sustain_talk
- opening_statement, is_builtin, created_by

**Session**
- id, user_id, scenario_id, mode, status
- created_at, updated_at
- interviewer_skill_level (for Role Reversal)
- analyst_config (JSON)

**ConversationNode**
- id, session_id, parent_id
- role (user/client/interviewer)
- content, timestamp
- technique_feedback (JSON)
- response_feedback (JSON)

**DrillSession**
- id, user_id, drill_type, scenario_id
- started_at, completed_at
- prompts_count, results (JSON)

**Progress** (aggregated metrics)
- user_id, period, metrics (JSON)

## Environment Variables

```
# Database
DATABASE_URL=

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# Optional
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

## Development Workflow

```bash
# Install dependencies
npm install

# Set up database
npx prisma migrate dev

# Run development server
npm run dev

# Generate Prisma client after schema changes
npx prisma generate
```

## Deployment

Vercel handles:
- Automatic deployments from git
- Edge functions for API routes
- Environment variable management
- Preview deployments for PRs

Database options:
- Vercel Postgres (tight integration)
- Supabase (more features, separate dashboard)
- Neon (serverless Postgres)
- Any external Postgres provider
