import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { redirect } from "next/navigation";
import { PracticeView } from "./PracticeView";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ sessionId: string }>;
}

export default async function PracticePage({ params }: Props) {
  const { userId } = await auth();
  const { sessionId } = await params;

  const session = await prisma.session.findUnique({
    where: { id: sessionId },
    include: {
      scenario: true,
      messages: {
        orderBy: { createdAt: "asc" },
      },
    },
  });

  if (!session) {
    redirect("/dashboard");
  }

  if (session.userId !== userId) {
    redirect("/dashboard");
  }

  if (session.status === "COMPLETED") {
    redirect(`/debrief/${sessionId}`);
  }

  return (
    <PracticeView
      sessionId={session.id}
      scenario={session.scenario}
      initialMessages={session.messages.map((m) => ({
        id: m.id,
        role: m.role.toLowerCase() as "user" | "client",
        content: m.content,
      }))}
    />
  );
}
