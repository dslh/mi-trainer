import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { redirect } from "next/navigation";
import { DebriefView } from "./DebriefView";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ sessionId: string }>;
}

export default async function DebriefPage({ params }: Props) {
  const { userId } = await auth();
  const { sessionId } = await params;

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
    redirect("/dashboard");
  }

  if (session.userId !== userId) {
    redirect("/dashboard");
  }

  return (
    <DebriefView
      sessionId={session.id}
      scenario={session.scenario}
      messages={session.messages.map((m) => ({
        role: m.role.toLowerCase() as "user" | "client",
        content: m.content,
      }))}
      existingDebrief={session.debrief?.content || null}
    />
  );
}
