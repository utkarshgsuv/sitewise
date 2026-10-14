"""Shared input types for the engine. IDs are caller-supplied (DB record UUIDs as str)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class InvoiceLine:
    item_code: str
    description: str
    qty: Decimal
    unit_price: Decimal
    record_id: str  # invoice_lines.id


@dataclass(frozen=True)
class ContractTerms:
    rates: dict[str, Decimal]  # item_code -> unit_rate
    freight_included: bool
    tolerance_pct: Decimal  # e.g. Decimal("0") for 0%
    record_id: str  # contracts.id


@dataclass(frozen=True)
class CandidateInvoice:
    record_id: str  # invoices.id
    invoice_number: str
    invoice_date: date
    total: Decimal
    po_id: str | None
    lines: tuple[tuple[str, Decimal], ...]  # (item_code, qty) set for comparison


@dataclass(frozen=True)
class SubjectInvoice:
    record_id: str
    invoice_number: str
    invoice_date: date
    total: Decimal
    po_id: str | None
    lines: tuple[tuple[str, Decimal], ...] = field(default=())


@dataclass(frozen=True)
class BankChangeEvent:
    record_id: str  # vendor_change_events.id
    field: str
    changed_at: date
    requested_via: str
    verification_status: str


@dataclass(frozen=True)
class Payment:
    record_id: str  # payment_records.id
    amount: Decimal
