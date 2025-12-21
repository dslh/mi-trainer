import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import Link from "next/link";
import styles from "./page.module.css";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { userId } = await auth();

  // Get recent sessions for this user
  const recentSessions = await prisma.session.findMany({
    where: { userId: userId! },
    include: { scenario: true },
    orderBy: { updatedAt: "desc" },
    take: 5,
  });

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Welcome back</h1>
        <p className={styles.subtitle}>
          Ready to practice your MI skills?
        </p>
      </div>

      <div className={styles.actions}>
        <Link href="/scenarios" className={styles.startButton}>
          Start New Session
        </Link>
      </div>

      {recentSessions.length > 0 && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Recent Sessions</h2>
          <div className={styles.sessionList}>
            {recentSessions.map((session) => (
              <Link
                key={session.id}
                href={
                  session.status === "ACTIVE"
                    ? `/practice/${session.id}`
                    : `/debrief/${session.id}`
                }
                className={styles.sessionCard}
              >
                <div className={styles.sessionInfo}>
                  <h3 className={styles.scenarioName}>{session.scenario.name}</h3>
                  <p className={styles.sessionMeta}>
                    {session.status === "ACTIVE" ? "In progress" : "Completed"} •{" "}
                    {new Date(session.updatedAt).toLocaleDateString()}
                  </p>
                </div>
                <span className={styles.sessionAction}>
                  {session.status === "ACTIVE" ? "Continue →" : "Review →"}
                </span>
              </Link>
            ))}
          </div>
          <Link href="/sessions" className={styles.viewAll}>
            View all sessions →
          </Link>
        </section>
      )}

      {recentSessions.length === 0 && (
        <section className={styles.section}>
          <div className={styles.empty}>
            <p>No sessions yet. Start your first practice session!</p>
          </div>
        </section>
      )}
    </div>
  );
}
