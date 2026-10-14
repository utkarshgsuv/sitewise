"""E-03 vendor bank-change risk (technical.md §12.3).

Latest bank_account change before the invoice: <=30d + unverified -> HIGH,
<=90d -> MEDIUM; email-only request bumps one step, capped at HIGH so the
engine never overclaims (T-01 expects HIGH on the seeded case).
Wording must say "requires independent verification", never "fraud".
"""
from __future__ import annotations

from datetime import date, datetime

from .findings import Finding, build_finding, evidence_record
from .types import BankChangeEvent

_STEPS = ["low", "medium", "high"]


def _as_date(v: date | datetime) -> date:
    return v.date() if isinstance(v, datetime) else v


def assess_bank_change(events: list[BankChangeEvent], invoice_date: date) -> Finding | None:
    day = _as_date(invoice_date)
    bank = [e for e in events
            if e.field == "bank_account" and _as_date(e.changed_at) <= day]
    if not bank:
        return None
    latest = max(bank, key=lambda e: _as_date(e.changed_at))
    changed = _as_date(latest.changed_at)
    age_days = (day - changed).days
    if age_days <= 30 and latest.verification_status != "verified":
        level = "high"
    elif age_days <= 90:
        level = "medium"
    else:
        return None
    if latest.requested_via == "email":
        level = _STEPS[min(_STEPS.index(level) + 1, len(_STEPS) - 1)]
    return build_finding(
        type="BANK_CHANGE_RISK", severity=level, confidence="high",
        title=(f"Vendor bank account changed {age_days} days before invoice "
               f"({latest.verification_status}); requires independent verification"),
        detail={"changed_at": changed.isoformat(), "age_days": age_days,
                "requested_via": latest.requested_via,
                "verification_status": latest.verification_status},
        evidence_refs=[evidence_record("vendor_change_events", latest.record_id)])
