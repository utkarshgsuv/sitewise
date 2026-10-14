"use client";

import { useEffect, useState } from "react";
import RunTimeline from "../../../components/RunTimeline";
import { getCase } from "../../../lib/api";

const TABS = ["Overview", "Findings", "Evidence", "Actions", "Approvals", "Governance"] as const;

export default function CasePage({ params }: { params: { id: string } }) {
  const [data, setData] = useState<Awaited<ReturnType<typeof getCase>> | null>(null);
  const [err, setErr] = useState("");
  const [tab, setTab] = useState<(typeof TABS)[number]>("Overview");
  useEffect(() => {
    getCase(params.id).then(setData).catch((e) => setErr(e.message));
  }, [params.id]);
  if (err) return <p className="error">{err}</p>;
  if (!data) return <p>Loading…</p>;
  const { case: c, findings, attempts, docs, task, draft } = data as any;
  return (
    <div>
      <h2>{c.invoice_number} — {c.total}</h2>
      <p>{c.vendor} · status {c.status}</p>
      <div className="tabs">
        {TABS.map((t) => (
          <button key={t} className={tab === t ? "active" : ""} onClick={() => setTab(t)}>{t}</button>
        ))}
      </div>

      {tab === "Overview" && (
        <div>
          <div className="card"><b>Task:</b> {task.title} → {task.assignee} ({task.status})</div>
          <div className="card"><b>Draft:</b> {draft.subject} → {draft.recipient} (digest {draft.digest})</div>
          <h3>Run timeline</h3>
          <RunTimeline />
        </div>
      )}

      {tab === "Findings" && findings.map((f: any) => (
        <div className="card" key={f.id}>
          <span className={`badge sev-${f.severity}`}>{f.severity}</span>{" "}
          <span className="badge">confidence {f.confidence}</span>
          <h3>{f.title} <small>({f.type})</small></h3>
          {f.evidence.map((e: any, i: number) => (
            <div className="quote" key={i}><b>{e.label}:</b> {e.quote}</div>
          ))}
        </div>
      ))}

      {tab === "Evidence" && docs.map((d: any) => (
        <div className="card" key={d.id}><b>{d.filename}</b> <small>({d.kind})</small></div>
      ))}

      {tab === "Actions" && (
        <div>
          <div className="card"><b>Review task:</b> {task.title}<br />Assignee: {task.assignee} · {task.status}</div>
          <div className="card"><b>Vendor draft:</b> {draft.subject}<br />To: {draft.recipient} · digest {draft.digest} · {draft.status}</div>
        </div>
      )}

      {tab === "Approvals" && (
        <div className="card">
          <p>No approvals yet (outline). Approver queue + digest validity land Thu with P-06.</p>
        </div>
      )}

      {tab === "Governance" && (
        <div className="card">
          <table className="attempts">
            <thead><tr><th>Tool</th><th>In plan</th><th>Verdict</th><th>MCP</th><th>Status</th><th>Trace</th></tr></thead>
            <tbody>
              {attempts.map((a: any) => (
                <tr key={a.attempt_id} className={a.verdict === "BLOCK" ? "blocked" : ""}>
                  <td><code>{a.tool}</code></td>
                  <td>{a.declared_in_plan ? "yes" : "no"}</td>
                  <td><span className={`badge verdict-${a.verdict}`}>{a.verdict}</span></td>
                  <td>{a.mcp_decision ?? "—"}</td>
                  <td>{a.exec_status}</td>
                  <td><code>{a.trace_ref}</code></td>
                </tr>
              ))}
            </tbody>
          </table>
          {attempts.filter((a: any) => a.verdict === "BLOCK").map((a: any) => (
            <details className="raw" key={a.attempt_id}>
              <summary>raw ArmorIQ payload — {a.tool}</summary>
              <pre>{JSON.stringify({ verdict: a.verdict, reason: a.reason, trace_ref: a.trace_ref }, null, 2)}</pre>
            </details>
          ))}
        </div>
      )}
    </div>
  );
}
