"use client";

import { useEffect, useState } from "react";
import { listCases } from "../../lib/api";
import type { CaseSummary } from "../../lib/mock";

export default function CasesPage() {
  const [cases, setCases] = useState<CaseSummary[] | null>(null);
  const [err, setErr] = useState("");
  useEffect(() => {
    listCases().then(setCases).catch((e) => setErr(e.message));
  }, []);
  if (err) return <p className="error">{err}</p>;
  if (!cases) return <p>Loading…</p>;
  return (
    <div>
      <h2>Cases</h2>
      {cases.map((c) => (
        <div className="card case" key={c.id}>
          <a href={`/cases/${c.id}`}><b>{c.invoice_number}</b></a>
          <p>{c.vendor} · {c.total} · {c.status}</p>
        </div>
      ))}
    </div>
  );
}
