"""SQLAlchemy models — D-02 schema v1 (Person B).

Source: technical.md §10.4. Alembic migration in db/migrations/versions/0001_initial.py
is the frozen snapshot; this file must stay in sync with it (see
tests/unit/test_schema_parity.py).

Conventions:
- Every tenant table carries ``org_id`` (RLS comes in A's D-03 on top).
- ``case_id`` / ``run_id`` / ``attempt_id`` / ``*_ledger_id`` / ``record_id``
  are correlation IDs (technical.md §17), deliberately WITHOUT foreign keys
  so truncate/reseed ordering stays trivial. True parent relations
  (org, vendor, PO, contract, invoice, document, finding, draft, approval)
  use real FKs.
- Money is NUMERIC(14,2); Python side uses Decimal, never float.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def _org_fk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)


def _ts_now() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


# ---------------------------------------------------------------- identity

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[uuid.UUID] = _uuid_pk()
    name: Mapped[str] = mapped_column(Text, nullable=False)


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = _uuid_pk()
    email: Mapped[str] = mapped_column(CITEXT, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)


class Membership(Base):
    __tablename__ = "memberships"
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), primary_key=True)
    role: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            "role in ('finance_analyst','procurement_manager','finance_approver','auditor','admin')",
            name="ck_memberships_role",
        ),
        nullable=False,
    )


# ------------------------------------------------------- business records

class Vendor(Base):
    __tablename__ = "vendors"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    name: Mapped[str] = mapped_column(Text, nullable=False)
    gstin_fictional: Mapped[str] = mapped_column(Text, nullable=False)
    email_domain: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active")


class VendorChangeEvent(Base):
    __tablename__ = "vendor_change_events"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    vendor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    field: Mapped[str] = mapped_column(Text, nullable=False)
    old_value_masked: Mapped[str] = mapped_column(Text, nullable=False)
    new_value_masked: Mapped[str] = mapped_column(Text, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    requested_via: Mapped[str] = mapped_column(Text, nullable=False)
    verification_status: Mapped[str] = mapped_column(Text, nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    vendor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    po_number: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    issued_on: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")


class POLine(Base):
    __tablename__ = "po_lines"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    po_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("purchase_orders.id"), nullable=False, index=True)
    line_no: Mapped[int] = mapped_column(nullable=False)
    item_code: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    qty: Mapped[float] = mapped_column(Numeric, nullable=False)
    unit: Mapped[str] = mapped_column(Text, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)


class Contract(Base):
    __tablename__ = "contracts"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    vendor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    contract_no: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    signed_on: Mapped[date] = mapped_column(Date, nullable=False)
    freight_included: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tolerance_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)


class ContractRate(Base):
    __tablename__ = "contract_rates"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False, index=True)
    item_code: Mapped[str] = mapped_column(Text, nullable=False)
    unit_rate: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    vendor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    po_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("purchase_orders.id"), nullable=False, index=True)
    invoice_number: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    total: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True)
    line_no: Mapped[int] = mapped_column(nullable=False)
    item_code: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    qty: Mapped[float] = mapped_column(Numeric, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)


class PaymentRecord(Base):
    __tablename__ = "payment_records"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True)
    paid_on: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    reference: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)


class SupplierBid(Base):
    __tablename__ = "supplier_bids"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    project_id: Mapped[str] = mapped_column(Text, nullable=False)
    supplier: Mapped[str] = mapped_column(Text, nullable=False)
    bid_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")


# ------------------------------------------------- documents + extraction

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = _ts_now()


class ExtractedField(Base):
    __tablename__ = "extracted_fields"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(Text, nullable=False)
    value_text: Mapped[str] = mapped_column(Text, nullable=False)
    value_norm: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    page: Mapped[int] = mapped_column(nullable=False)
    bbox: Mapped[dict] = mapped_column(JSONB, nullable=False)
    source_quote: Mapped[str] = mapped_column(Text, nullable=False)
    grounded: Mapped[bool] = mapped_column(Boolean, nullable=False)
    human_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


# ------------------------------------------------------------ investigation

class Investigation(Base):
    __tablename__ = "investigations"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True)
    requested_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")
    request_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = _ts_now()
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AgentRun(Base):
    __tablename__ = "agent_runs"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="running")
    model_id: Mapped[str] = mapped_column(Text, nullable=False)
    plan_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = _ts_now()
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class Finding(Base):
    __tablename__ = "findings"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")
    created_by: Mapped[str] = mapped_column(Text, nullable=False, default="engine")


class EvidenceLink(Base):
    __tablename__ = "evidence_links"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id"), nullable=False, index=True)
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    record_table: Mapped[str] = mapped_column(Text, nullable=False)
    record_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    span: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    note: Mapped[str] = mapped_column(Text, nullable=False, default="")


# ----------------------------------------------------- governed side effects

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    assignee_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")
    finding_ids: Mapped[list] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=False)
    created_ledger_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


class Draft(Base):
    __tablename__ = "drafts"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(Text, nullable=False, default="vendor_message")
    recipient_email: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    attachment_refs: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="draft")
    created_ledger_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    draft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drafts.id"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    approver_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    decision: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    used_ledger_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


class SimulatedOutbox(Base):
    __tablename__ = "simulated_outbox"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    draft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drafts.id"), nullable=False)
    approval_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("approvals.id"), nullable=False, unique=True)
    recipient_email: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    queued_at: Mapped[datetime] = _ts_now()
    ledger_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


# -------------------------------------------------------- evidence of control

class AgentToolAttempt(Base):
    __tablename__ = "agent_tool_attempts"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id"), nullable=False, index=True)
    seq: Mapped[int] = mapped_column(nullable=False)
    tool_name: Mapped[str] = mapped_column(Text, nullable=False)
    args_redacted: Mapped[dict] = mapped_column(JSONB, nullable=False)
    args_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    declared_in_plan: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verdict: Mapped[str] = mapped_column(Text, nullable=False)
    armoriq_raw: Mapped[dict] = mapped_column(JSONB, nullable=False)
    armoriq_trace_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    mcp_decision: Mapped[str | None] = mapped_column(Text, nullable=True)
    mcp_error_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    exec_status: Mapped[str] = mapped_column(Text, nullable=False)
    ledger_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = _ts_now()
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class McpDenial(Base):
    __tablename__ = "mcp_denials"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_tool_attempts.id"), nullable=False, index=True)
    tool_name: Mapped[str] = mapped_column(Text, nullable=False)
    error_code: Mapped[str] = mapped_column(Text, nullable=False)
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = _ts_now()


class ActionLedger(Base):
    __tablename__ = "action_ledger"
    __table_args__ = (
        UniqueConstraint("org_id", "tool_name", "idempotency_key", name="uq_ledger_org_tool_key"),
    )
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    tool_name: Mapped[str] = mapped_column(Text, nullable=False)
    actor_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    args_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    result_ref: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = _ts_now()


class AgentEvent(Base):
    __tablename__ = "agent_events"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id"), nullable=False, index=True)
    org_id: Mapped[uuid.UUID] = _org_fk()
    seq: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = _ts_now()


class CanaryEvent(Base):
    __tablename__ = "canary_events"
    id: Mapped[uuid.UUID] = _uuid_pk()
    org_id: Mapped[uuid.UUID] = _org_fk()
    tool: Mapped[str] = mapped_column(Text, nullable=False)
    would_have_exported: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = _ts_now()


Index("ix_agent_events_run_seq", AgentEvent.run_id, AgentEvent.seq, unique=True)
Index("ix_attempts_run_seq", AgentToolAttempt.run_id, AgentToolAttempt.seq, unique=True)
