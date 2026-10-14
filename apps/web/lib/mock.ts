// Mock dataset mirroring the live seed (technical.md §21 + T-01).
//
// Used by lib/api.ts while P-01..P-03 routes are unbuilt. Shape matches the
// contracts in packages/contracts so the swap to real fetch is mechanical.
export type CaseSummary = {
  id: string;
  invoice_number: string;
  vendor: string;
  total: string;
  status: string;
};

export type Evidence = { label: string; quote: string };

export type Finding = {
  id: string;
  type: string;
  severity: "low" | "medium" | "high" | "critical";
  confidence: string;
  title: string;
  detail: Record<string, string>;
  evidence: Evidence[];
};

export type FindingDetail = Record<string, string>;

export type Attempt = {
  attempt_id: string;
  tool: string;
  declared_in_plan: boolean;
  verdict: "ALLOW" | "HOLD" | "BLOCK" | "ERROR";
  exec_status: string;
  mcp_decision: string | null;
  trace_ref: string | null;
  reason: string;
};

export const MOCK_USER = {
  email: "asha@meridian.example.test",
  display_name: "Asha Nair (fictional)",
  role: "finance_analyst",
};

export const MOCK_CASES: CaseSummary[] = [
  {
    id: "case-0417",
    invoice_number: "INV-2026-0417",
    vendor: "Aarav Fabrication Works (fictional)",
    total: "Rs. 18,00,000",
    status: "open",
  },
];

export const MOCK_FINDINGS: Finding[] = [
  {
    id: "f-variance",
    type: "PRICE_VARIANCE",
    severity: "high",
    confidence: "high",
    title: "Unit price variance of Rs. 1,20,000 on TMT-FE500D",
    detail: { invoice_unit_price: "56000", contract_rate: "52000", variance_amount: "120000" },
    evidence: [
      { label: "invoice_lines #1", quote: "30 tonne @ Rs. 56,000 = Rs. 16,80,000" },
      { label: "contracts CT-2025-118", quote: "Rs. 52,000 per tonne" },
    ],
  },
  {
    id: "f-freight",
    type: "UNAPPROVED_CHARGE",
    severity: "high",
    confidence: "high",
    title: "Unapproved freight/handling charge of Rs. 1,20,000",
    detail: { amount: "120000" },
    evidence: [
      { label: "invoice_lines #2", quote: "Freight & handling — Rs. 1,20,000" },
      { label: "contracts CT-2025-118", quote: "Freight: Included in contract rate" },
    ],
  },
  {
    id: "f-dupe",
    type: "POSSIBLE_DUPLICATE",
    severity: "medium",
    confidence: "medium",
    title: "Possible duplicate of AFW/09/2218 (score 0.80)",
    detail: { score: "0.80", signals: "same_po,total_equal,date_within_14d,same_line_set" },
    evidence: [{ label: "invoices AFW/09/2218", quote: "Rs. 18,00,000, same PO, 29 Sep 2026" }],
  },
  {
    id: "f-bank",
    type: "BANK_CHANGE_RISK",
    severity: "high",
    confidence: "high",
    title: "Vendor bank account changed 6 days before invoice; requires independent verification",
    detail: { age_days: "6", verification_status: "pending_callback" },
    evidence: [{ label: "vendor_change_events", quote: "requested via email, pending_callback" }],
  },
];

export const MOCK_ATTEMPTS: Attempt[] = [
  { attempt_id: "att-01", tool: "list_case_documents", declared_in_plan: true, verdict: "ALLOW", exec_status: "READ_OK", mcp_decision: "ok", trace_ref: "tr-allow-001", reason: "" },
  { attempt_id: "att-02", tool: "read_document", declared_in_plan: true, verdict: "ALLOW", exec_status: "READ_OK", mcp_decision: "ok", trace_ref: "tr-allow-002", reason: "" },
  { attempt_id: "att-03", tool: "get_purchase_order", declared_in_plan: true, verdict: "ALLOW", exec_status: "READ_OK", mcp_decision: "ok", trace_ref: "tr-allow-003", reason: "" },
  { attempt_id: "att-04", tool: "compare_invoice_terms", declared_in_plan: true, verdict: "ALLOW", exec_status: "READ_OK", mcp_decision: "ok", trace_ref: "tr-allow-004", reason: "" },
  { attempt_id: "att-05", tool: "create_review_task", declared_in_plan: true, verdict: "ALLOW", exec_status: "EXECUTED", mcp_decision: "ok", trace_ref: "tr-allow-005", reason: "" },
  {
    attempt_id: "att-06", tool: "export_all_supplier_bids", declared_in_plan: false,
    verdict: "BLOCK", exec_status: "BLOCKED", mcp_decision: null,
    trace_ref: "tr-block-001", reason: "action outside declared plan + deny policy",
  },
];

export const MOCK_TIMELINE = [
  { seq: 1, type: "run.started", text: "Run started on INV-2026-0417" },
  { seq: 2, type: "plan.declared", text: "Plan declared: 9 allowed actions, 4 forbidden" },
  { seq: 3, type: "tool.attempted", text: "list_case_documents attempted" },
  { seq: 4, type: "governance.decision", text: "ALLOW — list_case_documents" },
  { seq: 5, type: "finding.created", text: "PRICE_VARIANCE finding created" },
  { seq: 6, type: "finding.created", text: "UNAPPROVED_CHARGE finding created" },
  { seq: 7, type: "tool.attempted", text: "export_all_supplier_bids attempted (not in plan)" },
  { seq: 8, type: "governance.decision", text: "BLOCK — export_all_supplier_bids" },
  { seq: 9, type: "task.created", text: "Review task created" },
  { seq: 10, type: "draft.created", text: "Vendor message draft created" },
  { seq: 11, type: "run.completed", text: "Run completed with blocks" },
];

export const MOCK_DOCS = [
  { id: "doc-1", kind: "contract", filename: "contract_CT-2025-118.pdf" },
  { id: "doc-2", kind: "purchase_order", filename: "po_PO-7731.pdf" },
  { id: "doc-3", kind: "invoice", filename: "inv_INV-2026-0417.pdf" },
  { id: "doc-4", kind: "invoice", filename: "inv_AFW-09-2218.pdf" },
];

export const MOCK_TASK = {
  title: "Review INV-2026-0417: Rs. 2,40,000 over contract",
  assignee: "Rohan Mehta (fictional)",
  status: "open",
};

export const MOCK_DRAFT = {
  recipient: "accounts@aarav-fab.example.test",
  subject: "Clarification on invoice INV-2026-0417 (fictional)",
  digest: "9f2c…a41b",
  status: "draft",
};
