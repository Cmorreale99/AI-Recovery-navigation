"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiPost } from "@/lib/api";

export default function ConsentPage() {
  const router = useRouter();
  const [agreed, setAgreed] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onContinue() {
    setSubmitting(true);
    setError(null);
    try {
      await apiPost("/consent", {
        consent_type: "data_processing",
        version: "v1",
        granted: true,
      });
      router.push("/intake");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
      setSubmitting(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-6 px-6 py-16">
      <h1 className="text-2xl font-semibold tracking-tight">Consent &amp; privacy</h1>

      <div className="space-y-3 text-slate-700">
        <p>
          The information you provide may include sensitive substance-use and
          mental-health details. It is used only to generate clinician-reviewable
          navigation artifacts for you.
        </p>
        <p className="rounded-md bg-slate-100 p-3 text-sm text-slate-600">
          This is a local MVP/demo, not production healthcare infrastructure. It is
          not medical advice, not emergency support, and not a replacement for
          treatment. Do not enter real patient data.
        </p>
      </div>

      <label className="flex items-start gap-3 text-sm text-slate-800">
        <input
          type="checkbox"
          className="mt-1 h-4 w-4"
          checked={agreed}
          onChange={(e) => setAgreed(e.target.checked)}
        />
        <span>
          I understand and consent to my provided information being processed to
          generate my recovery navigation artifacts.
        </span>
      </label>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div>
        <button
          type="button"
          disabled={!agreed || submitting}
          onClick={onContinue}
          className="inline-flex items-center rounded-md bg-slate-900 px-5 py-3 font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {submitting ? "Saving…" : "Agree and start intake"}
        </button>
      </div>
    </main>
  );
}
