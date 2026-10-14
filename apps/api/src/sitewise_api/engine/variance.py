"""E-01 price/contract variance (technical.md §12.1)."""
from __future__ import annotations

from decimal import Decimal

from .findings import Finding, build_finding, evidence_record
from .types import ContractTerms, InvoiceLine

_FREIGHT_CODES = {"FREIGHT", "FREIGHT-HANDLING", "HANDLING", "SHIPPING"}


def _is_freight(line: InvoiceLine) -> bool:
    return (line.item_code.upper() in _FREIGHT_CODES
            or "freight" in line.description.lower()
            or "handling" in line.description.lower())


def compare_lines(lines: list[InvoiceLine], terms: ContractTerms) -> list[Finding]:
    """Return PRICE_VARIANCE / UNAPPROVED_CHARGE / UNMATCHED_LINE findings."""
    out: list[Finding] = []
    for line in lines:
        amount = line.qty * line.unit_price
        ev = [evidence_record("invoice_lines", line.record_id),
              evidence_record("contracts", terms.record_id)]
        if _is_freight(line) and terms.freight_included:
            out.append(build_finding(
                type="UNAPPROVED_CHARGE", severity="high", confidence="high",
                title=f"Unapproved freight/handling charge of Rs. {amount:,.2f}",
                detail={"line_no": None, "item_code": line.item_code,
                        "amount": str(amount),
                        "reason": "contract includes freight; separate freight line is unapproved"},
                evidence_refs=ev))
            continue
        rate = terms.rates.get(line.item_code)
        if rate is None:
            out.append(build_finding(
                type="UNMATCHED_LINE", severity="medium", confidence="high",
                title=f"Line '{line.item_code}' has no contract rate",
                detail={"item_code": line.item_code, "amount": str(amount)},
                evidence_refs=ev))
            continue
        delta = line.unit_price - rate
        variance = delta * line.qty
        if rate and abs(delta) / abs(rate) > terms.tolerance_pct:
            out.append(build_finding(
                type="PRICE_VARIANCE", severity="high", confidence="high",
                title=(f"Unit price variance of Rs. {variance:,.2f} on {line.item_code} "
                       f"({line.unit_price:,.2f} vs contract {rate:,.2f} x {line.qty})"),
                detail={"item_code": line.item_code,
                        "invoice_unit_price": str(line.unit_price),
                        "contract_rate": str(rate),
                        "qty": str(line.qty),
                        "variance_amount": str(variance)},
                evidence_refs=ev))
    return out


def _d(x: str) -> Decimal:
    return Decimal(x)
