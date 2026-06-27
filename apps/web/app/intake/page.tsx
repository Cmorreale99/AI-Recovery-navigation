"use client";

import { useEffect, useMemo, useState } from "react";

import { apiGet, apiPost, type Question } from "@/lib/api";

type AnswerValue = string | string[];

export default function IntakePage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, AnswerValue>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<{ questions: Question[] }>("/intake/questions")
      .then((data) => setQuestions(data.questions))
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  // Preserve catalog order while grouping.
  const groups = useMemo(() => {
    const order: string[] = [];
    const byGroup: Record<string, Question[]> = {};
    for (const q of questions) {
      if (!byGroup[q.group]) {
        byGroup[q.group] = [];
        order.push(q.group);
      }
      byGroup[q.group].push(q);
    }
    return order.map((g) => ({ group: g, items: byGroup[g] }));
  }, [questions]);

  function setText(key: string, value: string) {
    setAnswers((prev) => ({ ...prev, [key]: value }));
  }

  function toggleMulti(key: string, option: string) {
    setAnswers((prev) => {
      const current = Array.isArray(prev[key]) ? (prev[key] as string[]) : [];
      const next = current.includes(option)
        ? current.filter((o) => o !== option)
        : [...current, option];
      return { ...prev, [key]: next };
    });
  }

  async function onSubmit() {
    setSubmitting(true);
    setError(null);
    try {
      const session = await apiPost<{ id: string }>("/intake/start");
      const payload = Object.entries(answers)
        .filter(([, v]) => (Array.isArray(v) ? v.length > 0 : v !== ""))
        .map(([question_key, value]) => ({ question_key, value }));
      await apiPost("/intake/answers", {
        session_id: session.id,
        answers: payload,
        complete: true,
      });
      setDone(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <CenteredNote>Loading intake questions…</CenteredNote>;
  }

  if (done) {
    return (
      <CenteredNote>
        <h1 className="text-2xl font-semibold">Intake saved</h1>
        <p className="mt-2 text-slate-600">
          Thank you. Your structured intake has been recorded. The dashboard and
          generated artifacts will become available in a later step.
        </p>
      </CenteredNote>
    );
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="text-2xl font-semibold tracking-tight">
        Structured intake questions
      </h1>
      <p className="mt-2 text-sm text-slate-600">
        These are symptom and support questions. This app does not diagnose. All
        fields are optional — share only what you choose.
      </p>

      <div className="mt-8 space-y-10">
        {groups.map(({ group, items }) => (
          <section key={group} className="space-y-5">
            <h2 className="border-b border-slate-200 pb-1 text-lg font-medium text-slate-800">
              {group}
            </h2>
            {items.map((q) => (
              <Field
                key={q.key}
                question={q}
                value={answers[q.key]}
                onText={(v) => setText(q.key, v)}
                onToggle={(opt) => toggleMulti(q.key, opt)}
              />
            ))}
          </section>
        ))}
      </div>

      {error && <p className="mt-6 text-sm text-red-600">{error}</p>}

      <button
        type="button"
        onClick={onSubmit}
        disabled={submitting}
        className="mt-8 inline-flex items-center rounded-md bg-slate-900 px-5 py-3 font-medium text-white transition hover:bg-slate-700 disabled:opacity-40"
      >
        {submitting ? "Saving…" : "Submit intake"}
      </button>
    </main>
  );
}

function Field({
  question,
  value,
  onText,
  onToggle,
}: {
  question: Question;
  value: AnswerValue | undefined;
  onText: (v: string) => void;
  onToggle: (option: string) => void;
}) {
  const textValue = typeof value === "string" ? value : "";
  const multiValue = Array.isArray(value) ? value : [];

  return (
    <div className="space-y-2">
      <label className="block font-medium text-slate-800">{question.label}</label>
      {question.help && <p className="text-xs text-slate-500">{question.help}</p>}

      {question.type === "text" && (
        <input
          type="text"
          value={textValue}
          onChange={(e) => onText(e.target.value)}
          className="w-full rounded-md border border-slate-300 px-3 py-2"
        />
      )}

      {question.type === "textarea" && (
        <textarea
          rows={3}
          value={textValue}
          onChange={(e) => onText(e.target.value)}
          className="w-full rounded-md border border-slate-300 px-3 py-2"
        />
      )}

      {question.type === "single_select" && (
        <div className="flex flex-wrap gap-2">
          {question.options.map((opt) => (
            <button
              key={opt}
              type="button"
              onClick={() => onText(opt)}
              className={`rounded-full border px-3 py-1 text-sm ${
                textValue === opt
                  ? "border-slate-900 bg-slate-900 text-white"
                  : "border-slate-300 text-slate-700"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}

      {question.type === "multi_select" && (
        <div className="flex flex-wrap gap-2">
          {question.options.map((opt) => (
            <button
              key={opt}
              type="button"
              onClick={() => onToggle(opt)}
              className={`rounded-full border px-3 py-1 text-sm ${
                multiValue.includes(opt)
                  ? "border-slate-900 bg-slate-900 text-white"
                  : "border-slate-300 text-slate-700"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function CenteredNote({ children }: { children: React.ReactNode }) {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center px-6 py-16 text-center">
      {children}
    </main>
  );
}
