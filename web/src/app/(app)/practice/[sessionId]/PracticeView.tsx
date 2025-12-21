"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import styles from "./PracticeView.module.css";

interface Message {
  id: string;
  role: "user" | "client";
  content: string;
}

interface Scenario {
  id: string;
  name: string;
  description: string;
}

interface Feedback {
  techniques_used: string[];
  mi_consistent: string[];
  mi_inconsistent: string[];
  suggestions: string[];
  overall_note: string;
}

interface Props {
  sessionId: string;
  scenario: Scenario;
  initialMessages: Message[];
}

export function PracticeView({ sessionId, scenario, initialMessages }: Props) {
  const router = useRouter();
  const [input, setInput] = useState("");
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showEndingPrompt, setShowEndingPrompt] = useState(false);
  const [isEnding, setIsEnding] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const feedbackEndRef = useRef<HTMLDivElement>(null);

  const { messages, status, sendMessage } = useChat({
    transport: new DefaultChatTransport({
      api: "/api/chat",
      body: { sessionId },
    }),
    messages: initialMessages.map((m) => ({
      id: m.id,
      role: m.role === "client" ? ("assistant" as const) : ("user" as const),
      parts: [{ type: "text" as const, text: m.content }],
    })),
    onFinish: async ({ message }) => {
      // Check for tool calls (signal_ending)
      // In AI SDK v5, tool parts have type `tool-${toolName}` or could be dynamic-tool
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const parts = message.parts as any[];
      if (parts?.some((p) =>
        p.type === "tool-signal_ending" ||
        (p.type === "dynamic-tool" && p.toolName === "signal_ending")
      )) {
        setShowEndingPrompt(true);
      }
    },
  });

  const isLoading = status === "streaming" || status === "submitted";

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Scroll feedback when it changes
  useEffect(() => {
    feedbackEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [feedback]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");

    // Submit to chat
    sendMessage({ text: userMessage });

    // Run analysis in parallel
    setIsAnalyzing(true);
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId, message: userMessage }),
      });

      if (response.ok) {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let result = "";

        if (reader) {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            result += decoder.decode(value);
          }
        }

        // Parse the streamed response - extract JSON from the stream
        // The AI SDK streams data in a specific format
        const lines = result.split("\n");
        let jsonContent = "";
        for (const line of lines) {
          if (line.startsWith("0:")) {
            // Text content
            const content = line.slice(2);
            try {
              jsonContent += JSON.parse(content);
            } catch {
              // Not JSON, skip
            }
          }
        }

        // Try to parse as feedback JSON
        try {
          // Find JSON in the content
          const jsonMatch = jsonContent.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            const parsed = JSON.parse(jsonMatch[0]);
            setFeedback(parsed);
          }
        } catch {
          console.error("Failed to parse feedback");
        }
      }
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleEndSession = async () => {
    setIsEnding(true);
    try {
      await fetch(`/api/sessions/${sessionId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "COMPLETED" }),
      });
      router.push(`/debrief/${sessionId}`);
    } catch (error) {
      console.error("Error ending session:", error);
      setIsEnding(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.scenarioInfo}>
          <h1 className={styles.scenarioName}>{scenario.name}</h1>
          <p className={styles.scenarioDescription}>{scenario.description}</p>
        </div>
        <button
          className={styles.endButton}
          onClick={() => setShowEndingPrompt(true)}
          disabled={isEnding}
        >
          End Session
        </button>
      </div>

      <div className={styles.main}>
        {/* Conversation Pane */}
        <div className={styles.conversationPane}>
          <div className={styles.messages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${
                  message.role === "user" ? styles.userMessage : styles.clientMessage
                }`}
              >
                <span className={styles.messageRole}>
                  {message.role === "user" ? "You" : "Client"}
                </span>
                <p className={styles.messageContent}>
                  {message.parts?.filter(p => p.type === "text").map(p => p.text).join("") || ""}
                </p>
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.clientMessage}`}>
                <span className={styles.messageRole}>Client</span>
                <p className={styles.messageContent}>
                  <span className={styles.typing}>...</span>
                </p>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className={styles.inputArea} onSubmit={handleSendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your response..."
              className={styles.input}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </form>
        </div>

        {/* Analysis Pane */}
        <div className={styles.analysisPane}>
          <h2 className={styles.analysisPaneTitle}>Technique Analysis</h2>

          {isAnalyzing && (
            <div className={styles.analyzing}>Analyzing...</div>
          )}

          {feedback && !isAnalyzing && (
            <div className={styles.feedback}>
              {feedback.techniques_used.length > 0 && (
                <div className={styles.feedbackSection}>
                  <h3 className={styles.feedbackLabel}>Techniques Used</h3>
                  <div className={styles.techniques}>
                    {feedback.techniques_used.map((t, i) => (
                      <span key={i} className={styles.technique}>
                        {t.replace(/_/g, " ")}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {feedback.mi_consistent.length > 0 && (
                <div className={styles.feedbackSection}>
                  <h3 className={styles.feedbackLabel}>MI-Consistent</h3>
                  <ul className={styles.feedbackList}>
                    {feedback.mi_consistent.map((item, i) => (
                      <li key={i} className={styles.positive}>
                        + {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {feedback.mi_inconsistent.length > 0 && (
                <div className={styles.feedbackSection}>
                  <h3 className={styles.feedbackLabel}>MI-Inconsistent</h3>
                  <ul className={styles.feedbackList}>
                    {feedback.mi_inconsistent.map((item, i) => (
                      <li key={i} className={styles.negative}>
                        - {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {feedback.suggestions.length > 0 && (
                <div className={styles.feedbackSection}>
                  <h3 className={styles.feedbackLabel}>Suggestions</h3>
                  <ul className={styles.feedbackList}>
                    {feedback.suggestions.map((item, i) => (
                      <li key={i} className={styles.suggestion}>
                        → {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {feedback.overall_note && (
                <div className={styles.overallNote}>
                  {feedback.overall_note}
                </div>
              )}
              <div ref={feedbackEndRef} />
            </div>
          )}

          {!feedback && !isAnalyzing && (
            <div className={styles.noFeedback}>
              Send a message to receive technique feedback.
            </div>
          )}
        </div>
      </div>

      {/* Ending Prompt Modal */}
      {showEndingPrompt && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2>End Session?</h2>
            <p>
              {messages.length > 2
                ? "Ready to see your session debrief?"
                : "Are you sure? The session has just started."}
            </p>
            <div className={styles.modalActions}>
              <button
                className={styles.modalCancel}
                onClick={() => setShowEndingPrompt(false)}
                disabled={isEnding}
              >
                Continue Practicing
              </button>
              <button
                className={styles.modalConfirm}
                onClick={handleEndSession}
                disabled={isEnding}
              >
                {isEnding ? "Ending..." : "End & View Debrief"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
