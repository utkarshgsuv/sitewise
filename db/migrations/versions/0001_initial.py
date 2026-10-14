"""0001 initial schema — D-02 (Person B).

Frozen snapshot of sitewise_api.db.models at M0. Source: technical.md §10.4.
RLS/grants/append-only land on top in A's D-03 (db/security/*.sql).

Revision ID: 0001_initial
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

UUID = postgresql.UUID(as_uuid=True)
JSONB = postgresql.JSONB
CITEXT = postgresql.CITEXT


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    # -- identity --
    op.create_table(
        "organizations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("email", CITEXT, nullable=False, unique=True),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("display_name", sa.Text, nullable=False),
    )
    op.create_table(
        "memberships",
        sa.Column("user_id", UUID, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("role", sa.Text, nullable=False),
        sa.CheckConstraint(
            "role in ('finance_analyst','procurement_manager','finance_approver','auditor','admin')",
            name="ck_memberships_role",
        ),
    )

    # -- business records --
    op.create_table(
        "vendors",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("gstin_fictional", sa.Text, nullable=False),
        sa.Column("email_domain", sa.Text, nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="active"),
    )
    op.create_table(
        "vendor_change_events",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("vendor_id", UUID, sa.ForeignKey("vendors.id"), nullable=False, index=True),
        sa.Column("field", sa.Text, nullable=False),
        sa.Column("old_value_masked", sa.Text, nullable=False),
        sa.Column("new_value_masked", sa.Text, nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("requested_via", sa.Text, nullable=False),
        sa.Column("verification_status", sa.Text, nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "purchase_orders",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("vendor_id", UUID, sa.ForeignKey("vendors.id"), nullable=False, index=True),
        sa.Column("po_number", sa.Text, nullable=False, index=True),
        sa.Column("issued_on", sa.Date, nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="open"),
    )
    op.create_table(
        "po_lines",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("po_id", UUID, sa.ForeignKey("purchase_orders.id"), nullable=False, index=True),
        sa.Column("line_no", sa.Integer, nullable=False),
        sa.Column("item_code", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("qty", sa.Numeric, nullable=False),
        sa.Column("unit", sa.Text, nullable=False),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False),
    )
    op.create_table(
        "contracts",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("vendor_id", UUID, sa.ForeignKey("vendors.id"), nullable=False, index=True),
        sa.Column("contract_no", sa.Text, nullable=False, index=True),
        sa.Column("signed_on", sa.Date, nullable=False),
        sa.Column("freight_included", sa.Boolean, nullable=False),
        sa.Column("tolerance_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
    )
    op.create_table(
        "contract_rates",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("contract_id", UUID, sa.ForeignKey("contracts.id"), nullable=False, index=True),
        sa.Column("item_code", sa.Text, nullable=False),
        sa.Column("unit_rate", sa.Numeric(14, 2), nullable=False),
    )

    # -- documents (no FKs: case/upload refs are correlation IDs, §17) --
    op.create_table(
        "documents",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("case_id", UUID, nullable=False, index=True),
        sa.Column("kind", sa.Text, nullable=False),
        sa.Column("filename", sa.Text, nullable=False),
        sa.Column("storage_path", sa.Text, nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("text_content", sa.Text, nullable=False, server_default=""),
        sa.Column("uploaded_by", UUID, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_table(
        "extracted_fields",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("document_id", UUID, sa.ForeignKey("documents.id"), nullable=False, index=True),
        sa.Column("field_name", sa.Text, nullable=False),
        sa.Column("value_text", sa.Text, nullable=False),
        sa.Column("value_norm", JSONB, nullable=False),
        sa.Column("confidence", sa.Numeric(3, 2), nullable=False),
        sa.Column("page", sa.Integer, nullable=False),
        sa.Column("bbox", JSONB, nullable=False),
        sa.Column("source_quote", sa.Text, nullable=False),
        sa.Column("grounded", sa.Boolean, nullable=False),
        sa.Column("human_confirmed", sa.Boolean, nullable=False, server_default=sa.false()),
    )

    # -- invoices / payments / bids --
    op.create_table(
        "invoices",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("vendor_id", UUID, sa.ForeignKey("vendors.id"), nullable=False, index=True),
        sa.Column("po_id", UUID, sa.ForeignKey("purchase_orders.id"), nullable=False, index=True),
        sa.Column("invoice_number", sa.Text, nullable=False, index=True),
        sa.Column("invoice_date", sa.Date, nullable=False),
        sa.Column("total", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="open"),
        sa.Column("source_document_id", UUID, sa.ForeignKey("documents.id"), nullable=True),
    )
    op.create_table(
        "invoice_lines",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("invoice_id", UUID, sa.ForeignKey("invoices.id"), nullable=False, index=True),
        sa.Column("line_no", sa.Integer, nullable=False),
        sa.Column("item_code", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("qty", sa.Numeric, nullable=False),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False),
        sa.Column("line_total", sa.Numeric(14, 2), nullable=False),
    )
    op.create_table(
        "payment_records",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("invoice_id", UUID, sa.ForeignKey("invoices.id"), nullable=False, index=True),
        sa.Column("paid_on", sa.Date, nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("reference", sa.Text, nullable=False),
        sa.Column("status", sa.Text, nullable=False),
    )
    op.create_table(
        "supplier_bids",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("project_id", sa.Text, nullable=False),
        sa.Column("supplier", sa.Text, nullable=False),
        sa.Column("bid_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("notes", sa.Text, nullable=False, server_default=""),
    )

    # -- investigation --
    op.create_table(
        "investigations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("invoice_id", UUID, sa.ForeignKey("invoices.id"), nullable=False, index=True),
        sa.Column("requested_by", UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="open"),
        sa.Column("request_text", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "agent_runs",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("investigation_id", UUID, sa.ForeignKey("investigations.id"),
                  nullable=False, index=True),
        sa.Column("status", sa.Text, nullable=False, server_default="running"),
        sa.Column("model_id", sa.Text, nullable=False),
        sa.Column("plan_ref", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text, nullable=True),
    )
    op.create_table(
        "findings",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("investigation_id", UUID, sa.ForeignKey("investigations.id"),
                  nullable=False, index=True),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("severity", sa.Text, nullable=False),
        sa.Column("confidence", sa.Text, nullable=False),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("detail", JSONB, nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="open"),
        sa.Column("created_by", sa.Text, nullable=False, server_default="engine"),
    )
    op.create_table(
        "evidence_links",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("finding_id", UUID, sa.ForeignKey("findings.id"), nullable=False, index=True),
        sa.Column("document_id", UUID, sa.ForeignKey("documents.id"), nullable=True),
        sa.Column("record_table", sa.Text, nullable=False),
        sa.Column("record_id", UUID, nullable=False),
        sa.Column("span", JSONB, nullable=True),
        sa.Column("note", sa.Text, nullable=False, server_default=""),
    )

    # -- governed side effects --
    op.create_table(
        "tasks",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("case_id", UUID, nullable=False, index=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("assignee_user_id", UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="open"),
        sa.Column("finding_ids", postgresql.ARRAY(UUID), nullable=False),
        sa.Column("created_ledger_id", UUID, nullable=True),
    )
    op.create_table(
        "drafts",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("case_id", UUID, nullable=False, index=True),
        sa.Column("kind", sa.Text, nullable=False, server_default="vendor_message"),
        sa.Column("recipient_email", sa.Text, nullable=False),
        sa.Column("subject", sa.Text, nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("attachment_refs", JSONB, nullable=False, server_default="[]"),
        sa.Column("payload_digest", sa.String(64), nullable=False),
        sa.Column("status", sa.Text, nullable=False, server_default="draft"),
        sa.Column("created_ledger_id", UUID, nullable=True),
    )
    op.create_table(
        "approvals",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("draft_id", UUID, sa.ForeignKey("drafts.id"), nullable=False, index=True),
        sa.Column("action_type", sa.Text, nullable=False),
        sa.Column("payload_digest", sa.String(64), nullable=False),
        sa.Column("approver_user_id", UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("decision", sa.Text, nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("used_ledger_id", UUID, nullable=True),
    )
    op.create_table(
        "simulated_outbox",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("draft_id", UUID, sa.ForeignKey("drafts.id"), nullable=False),
        sa.Column("approval_id", UUID, sa.ForeignKey("approvals.id"), nullable=False, unique=True),
        sa.Column("recipient_email", sa.Text, nullable=False),
        sa.Column("subject", sa.Text, nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("queued_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("ledger_id", UUID, nullable=True),
    )

    # -- evidence of control --
    op.create_table(
        "agent_tool_attempts",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("run_id", UUID, sa.ForeignKey("agent_runs.id"), nullable=False, index=True),
        sa.Column("seq", sa.Integer, nullable=False),
        sa.Column("tool_name", sa.Text, nullable=False),
        sa.Column("args_redacted", JSONB, nullable=False),
        sa.Column("args_digest", sa.String(64), nullable=False),
        sa.Column("declared_in_plan", sa.Boolean, nullable=False),
        sa.Column("verdict", sa.Text, nullable=False),
        sa.Column("armoriq_raw", JSONB, nullable=False),
        sa.Column("armoriq_trace_ref", sa.Text, nullable=True),
        sa.Column("mcp_decision", sa.Text, nullable=True),
        sa.Column("mcp_error_code", sa.Text, nullable=True),
        sa.Column("exec_status", sa.Text, nullable=False),
        sa.Column("ledger_id", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_attempts_run_seq", "agent_tool_attempts", ["run_id", "seq"], unique=True)
    op.create_table(
        "mcp_denials",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("attempt_id", UUID, sa.ForeignKey("agent_tool_attempts.id"),
                  nullable=False, index=True),
        sa.Column("tool_name", sa.Text, nullable=False),
        sa.Column("error_code", sa.Text, nullable=False),
        sa.Column("detail", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_table(
        "action_ledger",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("run_id", UUID, nullable=False, index=True),
        sa.Column("attempt_id", UUID, nullable=False),
        sa.Column("tool_name", sa.Text, nullable=False),
        sa.Column("actor_user_id", UUID, nullable=False),
        sa.Column("args_digest", sa.String(64), nullable=False),
        sa.Column("idempotency_key", sa.Text, nullable=False),
        sa.Column("result_ref", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.UniqueConstraint("org_id", "tool_name", "idempotency_key",
                            name="uq_ledger_org_tool_key"),
    )
    op.create_table(
        "agent_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("run_id", UUID, sa.ForeignKey("agent_runs.id"), nullable=False, index=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("seq", sa.Integer, nullable=False),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_index("ix_agent_events_run_seq", "agent_events", ["run_id", "seq"], unique=True)
    op.create_table(
        "canary_events",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("org_id", UUID, sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("tool", sa.Text, nullable=False),
        sa.Column("would_have_exported", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    for table in [
        "canary_events", "agent_events", "action_ledger", "mcp_denials",
        "agent_tool_attempts", "simulated_outbox", "approvals", "drafts", "tasks",
        "evidence_links", "findings", "agent_runs", "investigations",
        "supplier_bids", "payment_records", "invoice_lines", "invoices",
        "extracted_fields", "documents", "contract_rates", "contracts",
        "po_lines", "purchase_orders", "vendor_change_events", "vendors",
        "memberships", "users", "organizations",
    ]:
        op.drop_table(table)
