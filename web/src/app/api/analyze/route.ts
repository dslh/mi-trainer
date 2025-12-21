import { anthropic } from "@ai-sdk/anthropic";
import { streamText } from "ai";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { TECHNIQUE_ANALYST_SYSTEM_PROMPT } from "@/lib/prompts/analyst";

export const maxDuration = 60;

export async function POST(req: Request) {
  const { userId } = await auth();

  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { sessionId, message } = await req.json();

  // Get session with messages for context
  const session = await prisma.session.findUnique({
    where: { id: sessionId },
    include: {
      scenario: true,
      messages: {
        orderBy: { createdAt: "asc" },
        take: 20, // Last 20 messages for context
      },
    },
  });

  if (!session) {
    return new Response("Session not found", { status: 404 });
  }

  if (session.userId !== userId) {
    return new Response("Unauthorized", { status: 403 });
  }

  // Build context showing recent conversation
  const conversationContext = session.messages
    .map((msg) => `${msg.role === "USER" ? "Practitioner" : "Client"}: ${msg.content}`)
    .join("\n\n");

  const analysisPrompt = `Here is the conversation so far:

${conversationContext}

The practitioner just said:
"${message}"

Analyze this response and provide feedback in the required JSON format.`;

  const result = streamText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: TECHNIQUE_ANALYST_SYSTEM_PROMPT,
    messages: [
      {
        role: "user",
        content: analysisPrompt,
      },
    ],
  });

  return result.toTextStreamResponse();
}
