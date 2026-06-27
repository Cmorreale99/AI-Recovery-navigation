// Thin client for the FastAPI backend. Base URL is injected at build/runtime
// via NEXT_PUBLIC_API_URL (see next.config.mjs).

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function handle(res: Response) {
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

export async function apiGet<T = any>(path: string): Promise<T> {
  return handle(await fetch(`${BASE}${path}`, { cache: "no-store" }));
}

export async function apiPost<T = any>(path: string, body?: unknown): Promise<T> {
  return handle(
    await fetch(`${BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    }),
  );
}

// --- Shared types ---
export type Question = {
  key: string;
  label: string;
  category: string;
  type: "text" | "textarea" | "single_select" | "multi_select" | "date";
  group: string;
  help: string | null;
  options: string[];
};
