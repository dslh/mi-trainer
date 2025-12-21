import Link from "next/link";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import styles from "./page.module.css";

export default async function LandingPage() {
  const { userId } = await auth();

  if (userId) {
    redirect("/dashboard");
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.logo}>MI Trainer</div>
        <nav className={styles.nav}>
          <Link href="/sign-in" className={styles.signIn}>
            Sign In
          </Link>
          <Link href="/sign-up" className={styles.signUp}>
            Get Started
          </Link>
        </nav>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <h1 className={styles.title}>
            Practice Motivational Interviewing
            <br />
            <span className={styles.highlight}>with AI-Powered Feedback</span>
          </h1>
          <p className={styles.subtitle}>
            Develop your MI skills through realistic conversations with simulated
            clients. Receive real-time technique analysis and personalized coaching.
          </p>
          <Link href="/sign-up" className={styles.cta}>
            Start Practicing
          </Link>
        </section>

        <section className={styles.features}>
          <div className={styles.feature}>
            <h3>Realistic Clients</h3>
            <p>
              Practice with AI clients who respond authentically to your
              technique. Good MI elicits openness; poor MI triggers resistance.
            </p>
          </div>
          <div className={styles.feature}>
            <h3>Real-Time Analysis</h3>
            <p>
              Get immediate feedback on your techniques. See what you did well,
              what to improve, and specific suggestions for alternatives.
            </p>
          </div>
          <div className={styles.feature}>
            <h3>Session Debriefs</h3>
            <p>
              End each session with a comprehensive analysis of your MI
              adherence, technique usage, and key moments.
            </p>
          </div>
        </section>

        <section className={styles.whatIsMI}>
          <h2>What is Motivational Interviewing?</h2>
          <p>
            Motivational Interviewing (MI) is a collaborative, goal-oriented style
            of communication designed to strengthen personal motivation for change.
            Developed by William R. Miller and Stephen Rollnick, MI is used across
            healthcare, counseling, social work, and coaching.
          </p>
          <p>
            Core to MI is the spirit of partnership, acceptance, compassion, and
            evocation—drawing out a person&apos;s own motivations rather than imposing
            external ones. Practitioners use open questions, affirmations,
            reflections, and summaries (OARS) to explore ambivalence and support
            change.
          </p>
          <p>
            <a
              href="https://motivationalinterviewing.org/"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn more about MI →
            </a>
          </p>
        </section>
      </main>

      <footer className={styles.footer}>
        <p>MI Trainer — Practice makes progress</p>
      </footer>
    </div>
  );
}
