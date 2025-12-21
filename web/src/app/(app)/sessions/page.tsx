import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import Link from "next/link";
import styles from "./page.module.css";

export const dynamic = "force-dynamic";

export default async function SessionsPage() {
  const { userId } = await auth();

  const sessions = await prisma.session.findMany({
    where: { userId: userId! },
    include: {
      scenario: {
        select: {
          name: true,
          description: true,
        },
      },
      _count: {
        select: { messages: true },
      },
    },
    orderBy: { updatedAt: "desc" },
  });

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Link href="/dashboard" className={styles.back}>
          ← Back to Dashboard
        </Link>
        <h1 className={styles.title}>Your Sessions</h1>
        <p className={styles.subtitle}>
          Review past sessions or continue where you left off.
        </p>
      </div>

      {sessions.length > 0 ? (
        <div className={styles.sessionsList}>
          {sessions.map((session) => (
            <Link
              key={session.id}
              href={
                session.status === "ACTIVE"
                  ? `/practice/${session.id}`
                  : `/debrief/${session.id}`
              }
              className={styles.sessionCard}
            >
              <div className={styles.sessionMain}>
                <h3 className={styles.scenarioName}>{session.scenario.name}</h3>
                <p className={styles.scenarioDescription}>
                  {session.scenario.description}
                </p>
              </div>
              <div className={styles.sessionMeta}>
                <span
                  className={`${styles.status} ${
                    session.status === "ACTIVE"
                      ? styles.statusActive
                      : styles.statusCompleted
                  }`}
                >
                  {session.status === "ACTIVE" ? "In Progress" : "Completed"}
                </span>
                <span className={styles.messageCount}>
                  {session._count.messages} messages
                </span>
                <span className={styles.date}>
                  {new Date(session.updatedAt).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </span>
              </div>
              <span className={styles.action}>
                {session.status === "ACTIVE" ? "Continue →" : "Review →"}
              </span>
            </Link>
          ))}
        </div>
      ) : (
        <div className={styles.empty}>
          <p>No sessions yet.</p>
          <Link href="/scenarios" className={styles.startButton}>
            Start Your First Session
          </Link>
        </div>
      )}
    </div>
  );
}
