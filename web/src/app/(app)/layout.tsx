import { UserButton } from "@clerk/nextjs";
import Link from "next/link";
import styles from "./layout.module.css";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <Link href="/dashboard" className={styles.logo}>
          MI Trainer
        </Link>
        <nav className={styles.nav}>
          <Link href="/dashboard" className={styles.navLink}>
            Dashboard
          </Link>
          <Link href="/scenarios" className={styles.navLink}>
            Scenarios
          </Link>
          <Link href="/sessions" className={styles.navLink}>
            Sessions
          </Link>
        </nav>
        <div className={styles.user}>
          <UserButton afterSignOutUrl="/" />
        </div>
      </header>
      <main className={styles.main}>{children}</main>
    </div>
  );
}
