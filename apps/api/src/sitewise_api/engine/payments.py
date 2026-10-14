"""E-04 payment status (technical.md §12.4). Reported from records; no action."""
from __future__ import annotations

from decimal import Decimal

from .findings import Finding, build_finding, evidence_record
from .types import Payment


def payment_status(payments: list[Payment], invoice_total: Decimal,
                   invoice_record_id: str) -> Finding:
    paid = sum((p.amount for p in payments), Decimal("0"))
    ev = ([evidence_record("payment_records", p.record_id) for p in payments]
          + [evidence_record("invoices", invoice_record_id)])
    if paid <= 0:
        return build_finding(
            type="PAYMENT_STATUS", severity="low", confidence="high",
            title="Invoice unpaid", detail={"status": "UNPAID", "paid": "0",
                                            "total": str(invoice_total)},
            evidence_refs=ev)
    if paid >= invoice_total:
        return build_finding(
            type="PAYMENT_STATUS", severity="low", confidence="high",
            title="Invoice settled", detail={"status": "SETTLED", "paid": str(paid),
                                             "total": str(invoice_total)},
            evidence_refs=ev)
    return build_finding(
        type="PAYMENT_STATUS", severity="medium", confidence="high",
        title=f"Invoice partially paid: Rs. {paid:,.2f} of Rs. {invoice_total:,.2f}",
        detail={"status": "PARTIALLY_PAID", "paid": str(paid),
                "outstanding": str(invoice_total - paid), "total": str(invoice_total)},
        evidence_refs=ev)
