import { anthropic } from "@ai-sdk/anthropic";
import { streamText, tool, UIMessage, stepCountIs } from "ai";
import { z } from "zod";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { buildClientSystemPrompt } from "@/lib/prompts/client";

export const maxDuration = 60;

// Helper to extract text from UIMessage parts
function getTextFromMessage(msg: UIMessage): string {
  return msg.parts
    .filter((p) => p.type === "text")
    .map((p) => (p as { type: "text"; text: string }).text)
    .join("");
}

export async function POST(req: Request) {
  const { userId } = await auth();

  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }

  // In AI SDK v5, useChat sends messages array and sessionId in body
  const { messages: incomingMessages, sessionId } = await req.json();

  // Get session with scenario
  const session = await prisma.session.findUnique({
    where: { id: sessionId },
    include: {
      scenario: true,
    },
  });

  if (!session) {
    return new Response("Session not found", { status: 404 });
  }

  if (session.userId !== userId) {
    return new Response("Unauthorized", { status: 403 });
  }

  // Extract the latest user message
  const latestUserMessage = incomingMessages
    .filter((m: UIMessage) => m.role === "user")
    .pop();

  const userMessageText = latestUserMessage
    ? getTextFromMessage(latestUserMessage)
    : "";

  // Save user message if we have text
  if (userMessageText) {
    await prisma.message.create({
      data: {
        sessionId,
        role: "USER",
        content: userMessageText,
      },
    });
  }

  // Build conversation history for LLM from incoming messages
  const conversationHistory = incomingMessages.map((msg: UIMessage) => ({
    role: msg.role === "user" ? "user" : "assistant",
    content: getTextFromMessage(msg),
  })) as { role: "user" | "assistant"; content: string }[];

  const systemPrompt = buildClientSystemPrompt({
    name: session.scenario.name,
    demographics: session.scenario.demographics,
    presentingIssue: session.scenario.presentingIssue,
    ambivalence: session.scenario.ambivalence as {
      change: string[];
      statusQuo: string[];
    },
    resistanceLevel: session.scenario.resistanceLevel,
    background: session.scenario.background,
    personalityNotes: session.scenario.personalityNotes,
    changeTalkTriggers: session.scenario.changeTalkTriggers as string[],
    sustainTalk: session.scenario.sustainTalk as string[],
  });

  const result = streamText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: systemPrompt,
    messages: conversationHistory,
    tools: {
      signal_ending: tool({
        description:
          "Signal that the client wants to end the conversation naturally",
        inputSchema: z.object({
          reason: z
            .enum(["resolution", "clarity", "disengagement", "natural_end"])
            .describe("Why the client wants to end"),
        }),
      }),
    },
    stopWhen: stepCountIs(2),
    async onFinish({ text, toolCalls }) {
      // Save client response
      if (text) {
        await prisma.message.create({
          data: {
            sessionId,
            role: "CLIENT",
            content: text,
          },
        });
      }

      // Update session timestamp
      await prisma.session.update({
        where: { id: sessionId },
        data: { updatedAt: new Date() },
      });
    },
  });

  return result.toUIMessageStreamResponse();
}
