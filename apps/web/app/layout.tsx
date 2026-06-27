import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Relapse-Prevention & Care-Navigation Planner",
  description:
    "A clinician-reviewable decision-support planner. Not medical advice, not emergency support, not a replacement for treatment.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
