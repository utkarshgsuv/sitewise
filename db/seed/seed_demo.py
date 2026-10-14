"""S-02 seed script (Person B). All data fictional, per technical.md §21.

Seeds: 2 orgs, 5 users, vendor + bank-change event, contract + rates,
PO + lines, 2 invoices + lines, 1 payment record, 12 supplier bids,
1 investigation + 4 documents (PDF fixtures generated if missing).

Re-runnable: truncates transactional tables first (D-06 compatible).
IDs are deterministic (uuid5) so references stay stable across reseeds.

Usage:
  DATABASE_URL_DIRECT_OWNER=... uv run python db/seed/seed_demo.py [--no-truncate]

Demo logins (password for every seeded user): Sitewise-Demo-1234
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import uuid
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "api" / "src"))

import pdfplumber  # noqa: E402
from argon2 import PasswordHasher  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402

from sitewise_api.db import models  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "db" / "seed"))
from generate_fixtures import EXPECTED_TEXT, generate_all  # noqa: E402

NS = uuid.uuid5(uuid.NAMESPACE_DNS, "sitewise.demo")


def uid(*parts: str) -> uuid.UUID:
    return uuid.uuid5(NS, "/".join(parts))


DEMO_PASSWORD = "Sitewise-Demo-1234"

ORG_A = uid("org", "meridian")
ORG_B = UID_B = uid("org", "northwind")
VENDOR = uid("vendor", "aarav-fab")
CONTRACT = uid("contract", "CT-2025-118")
PO = uid("po", "PO-7731")
INV_0417 = uid("invoice", "INV-2026-0417")
INV_2218 = uid("invoice", "AFW-09-2218")
CASE_0417 = uid("case", "INV-2026-0417")

USERS = {
    "asha": ("Asha Nair (fictional)", "asha@meridian.example.test", "finance_analyst", ORG_A),
    "rohan": ("Rohan Mehta (fictional)", "rohan@meridian.example.test", "procurement_manager", ORG_A),
    "meera": ("Meera Iyer (fictional)", "meera@meridian.example.test", "finance_approver", ORG_A),
    "dev": ("Dev Kulkarni (fictional)", "dev@meridian.example.test", "auditor", ORG_A),
    "kabir": ("Kabir Shah (fictional)", "kabir@northwind.example.test", "finance_analyst", ORG_B),
}

BIDS = [
    # (project_id, supplier, amount)
    ("MP-ROAD-07", "Shivalik Constructions (fictional)", "24500000"),
    ("MP-ROAD-07", "Banwari Traders (fictional)", "23850000"),
    ("MP-ROAD-07", "Crystal Buildmat (fictional)", "25120000"),
    ("MP-ROAD-07", "Om Sai Suppliers (fictional)", "24275000"),
    ("MP-BRIDGE-12", "Shivalik Constructions (fictional)", "18750000"),
    ("MP-BRIDGE-12", "Banwari Traders (fictional)", "19200000"),
    ("MP-BRIDGE-12", "Crystal Buildmat (fictional)", "18425000"),
    ("MP-BRIDGE-12", "Om Sai Suppliers (fictional)", "18980000"),
    ("MP-TOWER-03", "Shivalik Constructions (fictional)", "31200000"),
    ("MP-TOWER-03", "Banwari Traders (fictional)", "30550000"),
    ("MP-TOWER-03", "Crystal Buildmat (fictional)", "31875000"),
    ("MP-TOWER-03", "Om Sai Suppliers (fictional)", "30900000"),
]

TRUNCATE_TABLES = [
    "agent_events", "action_ledger", "mcp_denials", "agent_tool_attempts",
    "simulated_outbox", "approvals", "drafts", "tasks",
    "evidence_links", "findings", "agent_runs", "investigations",
    "extracted_fields", "documents",
    "payment_records", "invoice_lines", "invoices",
    "supplier_bids", "po_lines", "purchase_orders",
    "contract_rates", "contracts", "vendor_change_events", "vendors",
    "memberships", "users", "organizations",
]


def seed(conn, truncate: bool) -> dict:
    if truncate:
        conn.execute(text(f"TRUNCATE {', '.join(TRUNCATE_TABLES)} RESTART IDENTITY CASCADE"))

    ph = PasswordHasher()
    pw_hash = ph.hash(DEMO_PASSWORD)
    user_ids = {k: uid("user", k) for k in USERS}

    conn.execute(models.Organization.__table__.insert(), [
        {"id": ORG_A, "name": "Meridian Infra Projects (fictional)"},
        {"id": ORG_B, "name": "Northwind Builders (fictional)"},
    ])
    conn.execute(models.User.__table__.insert(), [
        {"id": user_ids[k], "email": email, "password_hash": pw_hash, "display_name": name}
        for k, (name, email, _role, _org) in USERS.items()
    ])
    conn.execute(models.Membership.__table__.insert(), [
        {"user_id": user_ids[k], "org_id": org, "role": role}
        for k, (_n, _e, role, org) in USERS.items()
    ])

    conn.execute(models.Vendor.__table__.insert(), [{
        "id": VENDOR, "org_id": ORG_A, "name": "Aarav Fabrication Works (fictional)",
        "gstin_fictional": "27AAAAA0000A1Z5", "email_domain": "aarav-fab.example.test",
        "status": "active",
    }])
    conn.execute(models.VendorChangeEvent.__table__.insert(), [{
        "id": uid("bankchange", "aarav-2026-10-02"), "org_id": ORG_A, "vendor_id": VENDOR,
        "field": "bank_account", "old_value_masked": "HDFC XXXX-4521",
        "new_value_masked": "ICICI XXXX-9873",
        "changed_at": date(2026, 10, 2), "requested_via": "email",
        "verification_status": "pending_callback", "verified_at": None,
    }])

    conn.execute(models.Contract.__table__.insert(), [{
        "id": CONTRACT, "org_id": ORG_A, "vendor_id": VENDOR, "contract_no": "CT-2025-118",
        "signed_on": date(2025, 7, 15), "freight_included": True, "tolerance_pct": Decimal("0"),
    }])
    conn.execute(models.ContractRate.__table__.insert(), [{
        "id": uid("rate", "TMT-FE500D"), "org_id": ORG_A, "contract_id": CONTRACT,
        "item_code": "TMT-FE500D", "unit_rate": Decimal("52000"),
    }])

    conn.execute(models.PurchaseOrder.__table__.insert(), [{
        "id": PO, "org_id": ORG_A, "vendor_id": VENDOR, "po_number": "PO-7731",
        "issued_on": date(2026, 9, 12), "status": "open",
    }])
    conn.execute(models.POLine.__table__.insert(), [{
        "id": uid("poline", "1"), "org_id": ORG_A, "po_id": PO, "line_no": 1,
        "item_code": "TMT-FE500D", "description": "TMT Fe500D rebar",
        "qty": Decimal("30"), "unit": "tonne", "unit_price": Decimal("52000"),
    }])

    # Documents from the generated PDF fixtures.
    pdfs = generate_all()
    fix_dir = ROOT / "db" / "seed" / "fixtures"
    fix_dir.mkdir(parents=True, exist_ok=True)
    doc_ids: dict[str, uuid.UUID] = {}
    doc_meta = [
        ("contract_CT-2025-118.pdf", "contract"),
        ("po_PO-7731.pdf", "purchase_order"),
        ("inv_INV-2026-0417.pdf", "invoice"),
        ("inv_AFW-09-2218.pdf", "invoice"),
    ]
    for fname, kind in doc_meta:
        raw = pdfs[fname]
        (fix_dir / fname).write_bytes(raw)
        with pdfplumber.open(fix_dir / fname) as pdf:
            txt = "\n".join(p.extract_text() or "" for p in pdf.pages)
        for needle in EXPECTED_TEXT[fname]:
            assert needle in txt, (fname, needle)
        did = uid("doc", fname)
        doc_ids[fname] = did
        conn.execute(models.Document.__table__.insert(), [{
            "id": did, "org_id": ORG_A, "case_id": CASE_0417, "kind": kind,
            "filename": fname, "storage_path": f"db/seed/fixtures/{fname}",
            "sha256": hashlib.sha256(raw).hexdigest(), "text_content": txt,
            "uploaded_by": user_ids["asha"],
        }])

    for inv_id, number, inv_date, doc in [
        (INV_0417, "INV-2026-0417", date(2026, 10, 8), "inv_INV-2026-0417.pdf"),
        (INV_2218, "AFW/09/2218", date(2026, 9, 29), "inv_AFW-09-2218.pdf"),
    ]:
        conn.execute(models.Invoice.__table__.insert(), [{
            "id": inv_id, "org_id": ORG_A, "vendor_id": VENDOR, "po_id": PO,
            "invoice_number": number, "invoice_date": inv_date,
            "total": Decimal("1800000"), "status": "open",
            "source_document_id": doc_ids[doc],
        }])
        conn.execute(models.InvoiceLine.__table__.insert(), [
            {"id": uid("invline", number, "1"), "org_id": ORG_A, "invoice_id": inv_id,
             "line_no": 1, "item_code": "TMT-FE500D", "description": "TMT Fe500D rebar",
             "qty": Decimal("30"), "unit_price": Decimal("56000"),
             "line_total": Decimal("1680000")},
            {"id": uid("invline", number, "2"), "org_id": ORG_A, "invoice_id": inv_id,
             "line_no": 2, "item_code": "FREIGHT", "description": "Freight & handling",
             "qty": Decimal("1"), "unit_price": Decimal("120000"),
             "line_total": Decimal("120000")},
        ])

    conn.execute(models.PaymentRecord.__table__.insert(), [{
        "id": uid("pay", "AFW-09-2218", "1"), "org_id": ORG_A, "invoice_id": INV_2218,
        "paid_on": date(2026, 10, 5), "amount": Decimal("900000"),
        "reference": "NEFT-AXN-55213 (fictional)", "status": "captured",
    }])

    conn.execute(models.SupplierBid.__table__.insert(), [
        {"id": uid("bid", p, s), "org_id": ORG_A, "project_id": p,
         "supplier": s, "bid_amount": Decimal(a), "notes": ""}
        for p, s, a in BIDS
    ])

    conn.execute(models.Investigation.__table__.insert(), [{
        "id": CASE_0417, "org_id": ORG_A, "invoice_id": INV_0417,
        "requested_by": user_ids["asha"], "status": "open",
        "request_text": "Investigate Rs. 18,00,000 invoice INV-2026-0417 from Aarav "
                        "Fabrication Works. Do not release payment.",
    }])

    checksum = conn.execute(text(
        "select md5(string_agg(id::text||bid_amount::text, ',' order by id)) from supplier_bids"
    )).scalar()
    (ROOT / "db" / "seed" / "baseline_checksum.txt").write_text(f"{checksum}\n")

    # T-01 raw-number assertions (engine tests land Wed in E-01..E-05).
    checks = {
        "invoice total": conn.execute(text(
            "select total from invoices where invoice_number='INV-2026-0417'")).scalar(),
        "contract rate": conn.execute(text(
            "select unit_rate from contract_rates where item_code='TMT-FE500D'")).scalar(),
        "bid rows": conn.execute(text("select count(*) from supplier_bids")).scalar(),
        "bank verification": conn.execute(text(
            "select verification_status from vendor_change_events "
            "where field='bank_account'")).scalar(),
        "org count": conn.execute(text("select count(*) from organizations")).scalar(),
    }
    assert checks["invoice total"] == Decimal("1800000"), checks
    assert checks["contract rate"] == Decimal("52000"), checks
    assert checks["bid rows"] == 12, checks
    assert checks["bank verification"] == "pending_callback", checks
    assert checks["org count"] == 2, checks
    return {"checksum": checksum, "checks": {k: str(v) for k, v in checks.items()}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-truncate", action="store_true")
    args = ap.parse_args()
    url = os.environ.get("DATABASE_URL_DIRECT_OWNER")
    assert url, "set DATABASE_URL_DIRECT_OWNER"
    engine = create_engine(url, connect_args={"connect_timeout": 15})
    with engine.begin() as conn:
        result = seed(conn, truncate=not args.no_truncate)
    print("seed OK:", result)


if __name__ == "__main__":
    main()
