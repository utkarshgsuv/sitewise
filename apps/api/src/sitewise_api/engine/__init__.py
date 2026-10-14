"""Deterministic comparison engine — E-01..E-05 (Person B).

Pure functions, no I/O. Person A wraps these as MCP `compare_invoice_terms`
(H4 hand-off). Money is Decimal throughout; finding `detail` dicts are
JSON-safe (Decimals rendered as strings).
"""
from .bank_risk import assess_bank_change
from .duplicates import score_duplicates
from .findings import Finding, build_finding
from .payments import payment_status
from .types import BankChangeEvent, CandidateInvoice, ContractTerms, InvoiceLine, Payment
from .variance import compare_lines

__all__ = [
    "assess_bank_change", "score_duplicates", "build_finding", "Finding",
    "payment_status", "compare_lines",
    "BankChangeEvent", "CandidateInvoice", "ContractTerms", "InvoiceLine", "Payment",
]
