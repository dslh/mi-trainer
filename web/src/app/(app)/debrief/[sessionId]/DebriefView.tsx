"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import styles from "./DebriefView.module.css";

interface Message {
  role: "user" | "client";
  content: string;
}

interface Scenario {
  id: string;
  name: string;
  description: string;
}

interface Props {
  sessionId: string;
  scenario: Scenario;
  messages: Message[];
  existingDebrief: string | null;
}

export function DebriefView({
  sessionId,
  scenario,
  messages,
  existingDebrief,
}: Props) {
  const [debrief, setDebrief] = useState<string | null>(existingDebrief);
  const [isLoading, setIsLoading] = useState(!existingDebrief);
  const [showTranscript, setShowTranscript] = useState(false);

  useEffect(() => {
    if (!existingDebrief) {
      generateDebrief();
    }
  }, [existingDebrief]);

  const generateDebrief = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/debrief", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId }),
      });

      if (response.ok) {
        const data = await response.json();
        setDebrief(data.content);
      }
    } catch (error) {
      console.error("Error generating debrief:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Simple markdown to HTML conversion for headers and lists
  const renderMarkdown = (text: string) => {
    const lines = text.split("\n");
    const elements: React.ReactNode[] = [];
    let inList = false;
    let listItems: string[] = [];

    const flushList = () => {
      if (listItems.length > 0) {
        elements.push(
          <ul key={`list-${elements.length}`} className={styles.list}>
            {listItems.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        );
        listItems = [];
      }
      inList = false;
    };

    lines.forEach((line, index) => {
      const trimmed = line.trim();

      if (trimmed.startsWith("## ")) {
        flushList();
        elements.push(
          <h2 key={index} className={styles.sectionTitle}>
            {trimmed.slice(3)}
          </h2>
        );
      } else if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
        inList = true;
        listItems.push(trimmed.slice(2));
      } else if (trimmed.startsWith("**") && trimmed.endsWith("**")) {
        flushList();
        elements.push(
          <p key={index} className={styles.bold}>
            {trimmed.slice(2, -2)}
          </p>
        );
      } else if (trimmed) {
        flushList();
        // Handle inline bold
        const parts = trimmed.split(/(\*\*[^*]+\*\*)/g);
        elements.push(
          <p key={index} className={styles.paragraph}>
            {parts.map((part, i) => {
              if (part.startsWith("**") && part.endsWith("**")) {
                return <strong key={i}>{part.slice(2, -2)}</strong>;
              }
              return part;
            })}
          </p>
        );
      }
    });

    flushList();
    return elements;
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Link href="/dashboard" className={styles.back}>
          ← Back to Dashboard
        </Link>
        <h1 className={styles.title}>Session Debrief</h1>
        <p className={styles.scenarioName}>{scenario.name}</p>
      </div>

      <div className={styles.content}>
        {isLoading ? (
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>Generating your session debrief...</p>
          </div>
        ) : debrief ? (
          <div className={styles.debrief}>{renderMarkdown(debrief)}</div>
        ) : (
          <div className={styles.error}>
            <p>Failed to generate debrief. Please try again.</p>
            <button onClick={generateDebrief} className={styles.retryButton}>
              Retry
            </button>
          </div>
        )}

        <div className={styles.transcriptSection}>
          <button
            className={styles.transcriptToggle}
            onClick={() => setShowTranscript(!showTranscript)}
          >
            {showTranscript ? "Hide" : "Show"} Conversation Transcript
          </button>

          {showTranscript && (
            <div className={styles.transcript}>
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`${styles.transcriptMessage} ${
                    msg.role === "user"
                      ? styles.transcriptUser
                      : styles.transcriptClient
                  }`}
                >
                  <span className={styles.transcriptRole}>
                    {msg.role === "user" ? "You" : "Client"}:
                  </span>{" "}
                  {msg.content}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className={styles.actions}>
          <Link href="/scenarios" className={styles.newSession}>
            Start New Session
          </Link>
          <Link href="/sessions" className={styles.viewSessions}>
            View All Sessions
          </Link>
        </div>
      </div>
    </div>
  );
}
