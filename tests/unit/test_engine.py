"""Engine tests — E-01..E-05 incl. T-01 seeded numbers and T-15."""
from datetime import date
from decimal import Decimal

import pytest

from sitewise_api.engine import (
    BankChangeEvent,
    CandidateInvoice,
    ContractTerms,
    InvoiceLine,
    Payment,
    assess_bank_change,
    build_finding,
    payment_status,
    score_duplicates,
)
from sitewise_api.engine.duplicates import number_similarity
from sitewise_api.engine.variance import compare_lines

D = Decimal
TERMS = ContractTerms(rates={"TMT-FE500D": D("52000")}, freight_included=True,
                      tolerance_pct=D("0"), record_id="contract-1")
LINES_0417 = [
    InvoiceLine("TMT-FE500D", "TMT Fe500D rebar", D("30"), D("56000"), "line-1"),
    InvoiceLine("FREIGHT", "Freight & handling", D("1"), D("120000"), "line-2"),
]
LINE_SET = {("TMT-FE500D", D("30")), ("FREIGHT", D("1"))}


def test_price_variance_120000():
    findings = compare_lines(LINES_0417, TERMS)
    var = [f for f in findings if f.type == "PRICE_VARIANCE"]
    assert len(var) == 1
    assert var[0].detail["variance_amount"] == "120000"
    assert var[0].severity == "high"


def test_unapproved_freight_120000():
    findings = compare_lines(LINES_0417, TERMS)
    chg = [f for f in findings if f.type == "UNAPPROVED_CHARGE"]
    assert len(chg) == 1
    assert chg[0].detail["amount"] == "120000"


def test_within_tolerance_no_finding():
    terms = ContractTerms(rates={"TMT-FE500D": D("52000")}, freight_included=False,
                          tolerance_pct=D("0.10"), record_id="c")
    lines = [InvoiceLine("TMT-FE500D", "rebar", D("30"), D("56000"), "l")]
    assert compare_lines(lines, terms) == []  # 7.7% < 10% tolerance


def test_unmatched_line():
    lines = [InvoiceLine("CEMENT-OPC", "cement", D("10"), D("400"), "l")]
    findings = compare_lines(lines, TERMS)
    assert [f.type for f in findings] == ["UNMATCHED_LINE"]


def test_duplicate_scores_080_possible():
    out = score_duplicates(
        "INV-2026-0417", date(2026, 10, 8), D("1800000"), "po-1", LINE_SET,
        [{"record_id": "inv-2218", "number": "AFW/09/2218", "date": date(2026, 9, 29),
          "total": D("1800000"), "po_id": "po-1", "lines": LINE_SET}])
    assert len(out) == 1
    assert out[0].score == D("0.80")
    assert out[0].label == "POSSIBLE_DUPLICATE"
    assert set(out[0].signals) == {"same_po", "total_equal", "date_within_14d", "same_line_set"}


def test_duplicate_outside_window_ignored():
    out = score_duplicates(
        "INV-2026-0417", date(2026, 10, 8), D("1800000"), "po-1", LINE_SET,
        [{"record_id": "old", "number": "AFW/06/1001", "date": date(2026, 6, 1),
          "total": D("1800000"), "po_id": "po-1", "lines": LINE_SET}])
    assert out == []


def test_number_similarity():
    assert number_similarity("INV-2026-0417", "AFW/09/2218") < 0.8
    assert number_similarity("INV-2026-0417", "inv 2026 0417") >= 0.8


def test_bank_change_high_on_seed():
    f = assess_bank_change(
        [BankChangeEvent("ev-1", "bank_account", date(2026, 10, 2), "email", "pending_callback")],
        date(2026, 10, 8))
    assert f is not None and f.type == "BANK_CHANGE_RISK" and f.severity == "high"
    assert "requires independent verification" in f.title


def test_bank_change_old_event_none():
    f = assess_bank_change(
        [BankChangeEvent("ev-1", "bank_account", date(2026, 1, 1), "portal", "verified")],
        date(2026, 10, 8))
    assert f is None


def test_bank_change_accepts_datetimes():
    from datetime import datetime, timezone
    f = assess_bank_change(
        [BankChangeEvent("ev-1", "bank_account",
                         datetime(2026, 10, 2, 14, 30, tzinfo=timezone.utc),
                         "email", "pending_callback")],
        date(2026, 10, 8))
    assert f is not None and f.severity == "high"


def test_payment_statuses():
    unpaid = payment_status([], D("1800000"), "inv-0417")
    assert unpaid.detail["status"] == "UNPAID"
    partial = payment_status([Payment("pay-1", D("900000"))], D("1800000"), "inv-2218")
    assert partial.detail["status"] == "PARTIALLY_PAID"
    assert partial.detail["paid"] == "900000"
    settled = payment_status([Payment("p1", D("1000000")), Payment("p2", D("800000"))],
                             D("1800000"), "inv-x")
    assert settled.detail["status"] == "SETTLED"


def test_finding_without_evidence_rejected():
    with pytest.raises(ValueError):
        build_finding(type="PRICE_VARIANCE", severity="high", confidence="high",
                      title="x", detail={}, evidence_refs=[])
