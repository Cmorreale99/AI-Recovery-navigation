import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-8 px-6 py-16">
      <div className="space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight">
          AI Relapse-Prevention &amp; Care-Navigation Planner
        </h1>
        <p className="text-lg text-slate-600">
          Turn your own intake, journals, and notes into clinician-reviewable
          decision-support: a relapse-risk map, urge decoder, resource plan,
          clinician handoff, and a personalized relapse-prevention protocol.
        </p>
      </div>

      <section className="rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        <p className="font-medium">Please read before starting:</p>
        <ul className="mt-2 list-disc space-y-1 pl-5">
          <li>This is not medical advice.</li>
          <li>This is not emergency or crisis support.</li>
          <li>This is not a replacement for treatment or a clinician.</li>
          <li>
            If there is immediate danger, contact emergency services or crisis
            support now.
          </li>
        </ul>
      </section>

      <div>
        <Link
          href="/consent"
          className="inline-flex items-center rounded-md bg-slate-900 px-5 py-3 font-medium text-white transition hover:bg-slate-700"
        >
          Start intake
        </Link>
      </div>
    </main>
  );
}
