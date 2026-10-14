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
  const { case: c, findings, attempts, docs, task, draft } = data;
  const blocked = attempts.filter((a) => a.verdict === "BLOCK");
  const segs = findings.map((f) => (f.severity === "high" ? "hi" : f.severity === "medium" ? "md" : ""));

  return (
    <div>
      <div className="eyebrow">Case · {c.status}</div>
      <h1 className="case-title">{c.invoice_number}</h1>
      <p className="meta">{c.vendor}</p>

      <div className="tabs">
        {TABS.map((t) => (
          <button key={t} className={tab === t ? "active" : ""} onClick={() => setTab(t)}>{t}</button>
        ))}
      </div>

      {tab === "Overview" && (
        <div>
          <div className="stats">
            <div className="stat">
              <span className="stat-label">Invoice total</span>
              <span className="stat-num">{c.total.replace("Rs. ", "₹")}</span>
              <span className="stat-sub">30 t · PO-7731</span>
            </div>
            <div className="stat">
              <span className="stat-label">Over contract</span>
              <span className="stat-num">₹2,40,000<span className="deltapill">+15.4%</span></span>
              <span className="stat-sub">variance + freight</span>
            </div>
            <div className="stat">
              <span className="stat-label">Findings</span>
              <span className="stat-num">{findings.length}</span>
              <div className="segbar">{segs.map((s, i) => <i key={i} className={s} />)}</div>
            </div>
            <div className="stat">
              <span className="stat-label">Blocked attempts</span>
              <span className="stat-num">{blocked.length}</span>
              <span className="stat-sub">boundary held</span>
            </div>
          </div>
          <div className="card">
            <div className="eyebrow">Review task</div>
            <p style={{ margin: "6px 0 0" }}><b>{task.title}</b></p>
            <p className="meta">{task.assignee} · {task.status}</p>
          </div>
          <div className="card">
            <div className="eyebrow">Vendor draft</div>
            <p style={{ margin: "6px 0 0" }}><b>{draft.subject}</b></p>
            <p className="meta">{draft.recipient} · digest {draft.digest} · {draft.status}</p>
          </div>
          <h3 className="section">Run timeline</h3>
          <div className="card"><RunTimeline /></div>
        </div>
      )}

      {tab === "Findings" && findings.map((f) => (
        <div className="card" key={f.id}>
          <div className="finding-head">
            <h3>{f.title}<small>{f.type} · confidence {f.confidence}</small></h3>
            <span className={`badge sev-${f.severity}`}>{f.severity}</span>
          </div>
          <div className="chips">
            {Object.entries(f.detail).map(([k, v]) => (
              <span className="chip" key={k}>{k}: <b>{v}</b></span>
            ))}
          </div>
          {f.evidence.map((e, i) => (
            <div className="quote" key={i}><b>{e.label}:</b> {e.quote}</div>
          ))}
        </div>
      ))}

      {tab === "Evidence" && (
        <div className="card">
          {docs.map((d) => (
            <div className="docrow" key={d.id}>
              <span className="fileicon">PDF</span>
              <div><b>{d.filename}</b><small>{d.kind}</small></div>
            </div>
          ))}
        </div>
      )}

      {tab === "Actions" && (
        <div>
          <div className="card">
            <div className="eyebrow">Review task</div>
            <p style={{ margin: "6px 0 0" }}><b>{task.title}</b></p>
            <p className="meta">Assignee: {task.assignee} · {task.status}</p>
          </div>
          <div className="card">
            <div className="eyebrow">Vendor draft</div>
            <p style={{ margin: "6px 0 0" }}><b>{draft.subject}</b></p>
            <p className="meta">To: {draft.recipient} · digest {draft.digest} · {draft.status}</p>
          </div>
        </div>
      )}

      {tab === "Approvals" && (
        <div className="card">
          <div className="eyebrow">Approval queue</div>
          <p className="meta">Empty in the outline — approver queue with digest validity lands Thu (P-06).</p>
        </div>
      )}

      {tab === "Governance" && (
        <div>
          <div className="darkcard">
            <div className="eyebrow">Boundary held</div>
            <h3><code>export_all_supplier_bids</code> was blocked</h3>
            <p>Attempted outside the declared plan · ArmorIQ BLOCK · trace <code>{blocked[0]?.trace_ref ?? "—"}</code></p>
            <div className="proofrow">
              <div><b>0</b><span>canary events</span></div>
              <div><b>0</b><span>forbidden ledger rows</span></div>
              <div><b>unchanged</b><span>bids checksum</span></div>
            </div>
          </div>
          <div className="card">
            <table className="attempts">
              <thead><tr><th>Tool</th><th>In plan</th><th>Verdict</th><th>MCP</th><th>Status</th><th>Trace</th></tr></thead>
              <tbody>
                {attempts.map((a) => (
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
            {blocked.map((a) => (
              <details className="raw" key={a.attempt_id}>
                <summary>raw ArmorIQ payload — {a.tool}</summary>
                <pre>{JSON.stringify({ verdict: a.verdict, reason: a.reason, trace_ref: a.trace_ref }, null, 2)}</pre>
              </details>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
