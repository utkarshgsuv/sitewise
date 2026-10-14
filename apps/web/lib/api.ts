import {
  MOCK_ATTEMPTS,
  MOCK_CASES,
  MOCK_DOCS,
  MOCK_DRAFT,
  MOCK_FINDINGS,
  MOCK_TASK,
  MOCK_USER,
} from "./mock";
import type { Attempt, CaseSummary, Finding } from "./mock";

export type CaseDetail = {
  case: CaseSummary;
  findings: Finding[];
  attempts: Attempt[];
  docs: { id: string; kind: string; filename: string }[];
  task: typeof MOCK_TASK;
  draft: typeof MOCK_DRAFT;
};

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== "false";
const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function real<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`${API}${path}`, { ...init, credentials: "include" });
  if (!r.ok) throw new Error(`${path} -> ${r.status}`);
  return r.json() as Promise<T>;
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function login(email: string, password: string) {
  if (USE_MOCK) {
    await delay(200);
    if (password !== "Sitewise-Demo-1234" || !email.endsWith(".example.test"))
      throw new Error("invalid credentials (hint: Sitewise-Demo-1234)");
    localStorage.setItem("sitewise-user", JSON.stringify({ ...MOCK_USER, email }));
    return MOCK_USER;
  }
  return real("/api/auth/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export async function listCases(): Promise<CaseSummary[]> {
  if (USE_MOCK) {
    await delay(150);
    return MOCK_CASES;
  }
  return real<CaseSummary[]>("/api/cases");
}

export async function getCase(id: string): Promise<CaseDetail> {
  if (USE_MOCK) {
    await delay(150);
    const c = MOCK_CASES.find((x) => x.id === id);
    if (!c) throw new Error("case not found");
    return {
      case: c,
      findings: MOCK_FINDINGS,
      attempts: MOCK_ATTEMPTS,
      docs: MOCK_DOCS,
      task: MOCK_TASK,
      draft: MOCK_DRAFT,
    };
  }
  return real<CaseDetail>(`/api/cases/${id}`);
}

export function currentUser() {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("sitewise-user");
  return raw ? JSON.parse(raw) : null;
}
