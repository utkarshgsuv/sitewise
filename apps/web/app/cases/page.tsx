"use client";

import { useEffect, useState } from "react";
import { listCases } from "../../lib/api";
import type { CaseSummary } from "../../lib/mock";

export default function CasesPage() {
  const [cases, setCases] = useState<CaseSummary[] | null>(null);
  const [err, setErr] = useState("");
  useEffect(() => {
    listCases().then(setCases).catch((e) => setErr(String(e.message ?? e)));
  }, []);
  if (err) return <p className="error">{err}</p>;
  if (!cases) return <p>Loading…</p>;
  return (
    <div>
      <div className="eyebrow">All projects / Meridian Infra</div>
      <h1 className="case-title">Cases</h1>
      <p className="meta">{cases.length} open investigation{cases.length === 1 ? "" : "s"}</p>
      {cases.map((c) => (
        <div className="card case" key={c.id}>
          <div className="case-top">
            <b>{c.invoice_number}</b>
            <span className="statuspill">{c.status}</span>
            <span className="spacer" style={{ flex: 1 }} />
            <a className="viewlink" href={`/cases/${c.id}`}>Open ↗</a>
          </div>
          <p className="meta">{c.vendor} · {c.total}</p>
        </div>
      ))}
    </div>
  );
}
