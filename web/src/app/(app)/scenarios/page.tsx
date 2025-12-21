import { prisma } from "@/lib/db";
import Link from "next/link";
import styles from "./page.module.css";
import { ScenarioCard } from "./ScenarioCard";

export const dynamic = "force-dynamic";

export default async function ScenariosPage() {
  const scenarios = await prisma.scenario.findMany({
    where: { isBuiltin: true },
    orderBy: { name: "asc" },
  });

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Link href="/dashboard" className={styles.back}>
          ← Back to Dashboard
        </Link>
        <h1 className={styles.title}>Choose a Scenario</h1>
        <p className={styles.subtitle}>
          Select a client scenario to begin your practice session.
        </p>
      </div>

      <div className={styles.grid}>
        {scenarios.map((scenario) => (
          <ScenarioCard key={scenario.id} scenario={scenario} />
        ))}
      </div>
    </div>
  );
}
