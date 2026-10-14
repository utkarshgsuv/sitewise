"""S-01 PDF fixture generators (Person B).

Builds the 4 deterministic demo PDFs from technical.md §21:
  contract_CT-2025-118.pdf · po_PO-7731.pdf ·
  inv_INV-2026-0417.pdf · inv_AFW-09-2218.pdf

Byte-stable: reportlab stamps CreationDate/ModDate/ID at build time, so we
normalize those markers post-build. Content hash (extracted text) is the
real contract; byte hash is a bonus.

Usage:  uv run python db/seed/generate_fixtures.py [--out DIR] [--check]
  --check regenerates in memory twice and asserts identical sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT_DEFAULT = Path(__file__).resolve().parent / "fixtures"

STYLES = getSampleStyleSheet()
GRID = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
])


def _doc(buf: BytesIO) -> SimpleDocTemplate:
    return SimpleDocTemplate(
        buf, pagesize=A4,
        title="Sitewise demo fixture (fictional)",
        author="Sitewise seed",
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=20 * mm,
    )


def _stabilize(raw: bytes) -> bytes:
    """Fix reportlab's nondeterministic trailer markers for reproducible bytes."""
    raw = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (D:20260101000000+00'00')", raw)
    raw = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (D:20260101000000+00'00')", raw)
    raw = re.sub(rb"/ID\s*\[<[^>]*><[^>]*>\]", b"/ID [<00000000000000000000000000000000><00000000000000000000000000000000>]", raw)
    return raw


def _build(title: str, fields: list[tuple[str, str]], lines: list[list[str]]) -> bytes:
    buf = BytesIO()
    story = [Paragraph(f"<b>{title}</b>", STYLES["Title"]), Spacer(1, 6 * mm)]
    for name, value in fields:
        story += [Paragraph(f"<b>{name}:</b> {value}", STYLES["Normal"]), Spacer(1, 2 * mm)]
    if lines:
        story += [Spacer(1, 4 * mm), Table(lines, hAlign="LEFT", style=GRID, repeatRows=1)]
    _doc(buf).build(story)
    return _stabilize(buf.getvalue())


LINES_30T_56K = [
    ["Line", "Item", "Qty", "Unit price", "Line total"],
    ["1", "TMT Fe500D rebar", "30 tonne", "Rs. 56,000", "Rs. 16,80,000"],
    ["2", "Freight & handling", "1 lot", "Rs. 1,20,000", "Rs. 1,20,000"],
    ["", "", "", "Invoice total", "Rs. 18,00,000"],
]

FIXTURES: dict[str, tuple[str, list[tuple[str, str]], list[list[str]]]] = {
    "contract_CT-2025-118.pdf": (
        "Rate Contract CT-2025-118 (fictional)",
        [
            ("Contract No", "CT-2025-118"),
            ("Buyer", "Meridian Infra Projects (fictional)"),
            ("Seller", "Aarav Fabrication Works (fictional)"),
            ("Signed on", "15 Jul 2025"),
            ("Item", "TMT Fe500D rebar"),
            ("Contract rate", "Rs. 52,000 per tonne"),
            ("Freight", "Included in contract rate"),
            ("Price tolerance", "0%"),
            ("Seller email domain", "aarav-fab.example.test"),
        ],
        [["Item code", "Description", "Unit rate"],
         ["TMT-FE500D", "TMT Fe500D rebar", "Rs. 52,000 per tonne"]],
    ),
    "po_PO-7731.pdf": (
        "Purchase Order PO-7731 (fictional)",
        [
            ("PO Number", "PO-7731"),
            ("Issued on", "12 Sep 2026"),
            ("Buyer", "Meridian Infra Projects (fictional)"),
            ("Vendor", "Aarav Fabrication Works (fictional)"),
            ("Contract ref", "CT-2025-118"),
        ],
        [["Line", "Item", "Qty", "Unit price", "Line total"],
         ["1", "TMT Fe500D rebar", "30 tonne", "Rs. 52,000", "Rs. 15,60,000"],
         ["", "", "", "PO total", "Rs. 15,60,000"]],
    ),
    "inv_INV-2026-0417.pdf": (
        "Tax Invoice INV-2026-0417 (fictional)",
        [
            ("Invoice Number", "INV-2026-0417"),
            ("Invoice Date", "08 Oct 2026"),
            ("Vendor", "Aarav Fabrication Works (fictional)"),
            ("GSTIN", "27AAAAA0000A1Z5 (fictional)"),
            ("PO Reference", "PO-7731"),
            ("GRN Reference", "GRN-8847"),
        ],
        LINES_30T_56K,
    ),
    "inv_AFW-09-2218.pdf": (
        "Tax Invoice AFW/09/2218 (fictional)",
        [
            ("Invoice Number", "AFW/09/2218"),
            ("Invoice Date", "29 Sep 2026"),
            ("Vendor", "Aarav Fabrication Works (fictional)"),
            ("GSTIN", "27AAAAA0000A1Z5 (fictional)"),
            ("PO Reference", "PO-7731"),
            ("GRN Reference", "GRN-8821"),
        ],
        LINES_30T_56K,
    ),
}

# Strings the extraction grounding check (I-02) must find verbatim.
EXPECTED_TEXT = {
    "contract_CT-2025-118.pdf": ["CT-2025-118", "Rs. 52,000 per tonne", "Included in contract rate"],
    "po_PO-7731.pdf": ["PO-7731", "Rs. 15,60,000"],
    "inv_INV-2026-0417.pdf": ["INV-2026-0417", "08 Oct 2026", "Rs. 18,00,000", "GRN-8847"],
    "inv_AFW-09-2218.pdf": ["AFW/09/2218", "29 Sep 2026", "Rs. 18,00,000", "GRN-8821"],
}


def generate_all() -> dict[str, bytes]:
    return {name: _build(title, fields, lines) for name, (title, fields, lines) in FIXTURES.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--check", action="store_true",
                    help="regenerate twice in memory and assert identical bytes")
    args = ap.parse_args()

    first = generate_all()
    if args.check:
        second = generate_all()
        for name in first:
            h1 = hashlib.sha256(first[name]).hexdigest()
            h2 = hashlib.sha256(second[name]).hexdigest()
            assert h1 == h2, f"{name} not reproducible"
            print(f"{name}: reproducible sha256={h1}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, pdf in first.items():
        (out / name).write_bytes(pdf)
        print(f"wrote {out / name} ({len(pdf)} bytes, sha256={hashlib.sha256(pdf).hexdigest()})")


if __name__ == "__main__":
    main()
