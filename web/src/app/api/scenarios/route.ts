import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const scenarios = await prisma.scenario.findMany({
    where: { isBuiltin: true },
    orderBy: { name: "asc" },
    select: {
      id: true,
      slug: true,
      name: true,
      description: true,
      demographics: true,
      presentingIssue: true,
      resistanceLevel: true,
    },
  });

  return NextResponse.json(scenarios);
}
