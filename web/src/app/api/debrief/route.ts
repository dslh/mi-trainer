import { anthropic } from "@ai-sdk/anthropic";
import { generateText } from "ai";
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { DEBRIEF_SYSTEM_PROMPT } from "@/lib/prompts/debrief";

export async function POST(req: NextRequest) {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { sessionId } = await req.json();

  // Get session with all messages
  const session = await prisma.session.findUnique({
    where: { id: sessionId },
    include: {
      scenario: true,
      messages: {
        orderBy: { createdAt: "asc" },
      },
      debrief: true,
    },
  });

  if (!session) {
    return NextResponse.json({ error: "Session not found" }, { status: 404 });
  }

  if (session.userId !== userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  }

  // If debrief already exists, return it
  if (session.debrief) {
    return NextResponse.json({ content: session.debrief.content });
  }

  // Build conversation transcript
  const transcript = session.messages
    .map((msg) => `**${msg.role === "USER" ? "Practitioner" : "Client"}:** ${msg.content}`)
    .join("\n\n");

  const prompt = `Here is the complete conversation from a Motivational Interviewing practice session:

**Scenario:** ${session.scenario.name}
${session.scenario.description}

---

${transcript}

---

Please provide a comprehensive debrief of this session.`;

  // Generate debrief
  const result = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: DEBRIEF_SYSTEM_PROMPT,
    prompt,
    maxOutputTokens: 2000,
  });

  // Save debrief
  const debrief = await prisma.debrief.create({
    data: {
      sessionId,
      content: result.text,
    },
  });

  return NextResponse.json({ content: debrief.content });
}
