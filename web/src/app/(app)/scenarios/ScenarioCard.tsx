"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./ScenarioCard.module.css";

interface Scenario {
  id: string;
  slug: string;
  name: string;
  description: string;
  demographics: string;
  presentingIssue: string;
  resistanceLevel: number;
}

export function ScenarioCard({ scenario }: { scenario: Scenario }) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleStart = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenarioId: scenario.id }),
      });

      if (!response.ok) {
        throw new Error("Failed to create session");
      }

      const session = await response.json();
      router.push(`/practice/${session.id}`);
    } catch (error) {
      console.error("Error creating session:", error);
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.content}>
        <h3 className={styles.name}>{scenario.name}</h3>
        <p className={styles.description}>{scenario.description}</p>
        <div className={styles.details}>
          <p className={styles.demographics}>{scenario.demographics}</p>
          <p className={styles.issue}>
            <strong>Issue:</strong> {scenario.presentingIssue}
          </p>
          <div className={styles.resistance}>
            <span>Resistance:</span>
            <div className={styles.resistanceBar}>
              {[1, 2, 3, 4, 5].map((level) => (
                <div
                  key={level}
                  className={`${styles.resistanceDot} ${
                    level <= scenario.resistanceLevel ? styles.filled : ""
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
      <button
        className={styles.startButton}
        onClick={handleStart}
        disabled={isLoading}
      >
        {isLoading ? "Starting..." : "Start Session"}
      </button>
    </div>
  );
}
