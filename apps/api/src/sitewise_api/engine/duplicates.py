"""E-02 possible-duplicate scoring (technical.md §12.2).

Weights: same PO 0.30 · total equal 0.30 (0.20 within 1%) · number
similarity>=0.8 0.20 · date within 14d 0.10 · same line set 0.10.
>=0.90 LIKELY_DUPLICATE, >=0.70 POSSIBLE_DUPLICATE. Never "confirmed".
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from difflib import SequenceMatcher


@dataclass(frozen=True)
class DuplicateScore:
    candidate_id: str
    score: Decimal
    signals: tuple[str, ...]
    label: str | None  # LIKELY_DUPLICATE | POSSIBLE_DUPLICATE | None


def _norm_number(n: str) -> str:
    return re.sub(r"[^0-9a-z]", "", n.casefold())


def number_similarity(a: str, b: str) -> float:
    na, nb = _norm_number(a), _norm_number(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def score_pair(subject_number: str, subject_date: date, subject_total: Decimal,
               subject_po: str | None, subject_lines: set[tuple[str, Decimal]],
               cand_number: str, cand_date: date, cand_total: Decimal,
               cand_po: str | None, cand_lines: set[tuple[str, Decimal]]) -> DuplicateScore | None:
    if abs((subject_date - cand_date).days) > 45:
        return None
    score = Decimal("0")
    signals: list[str] = []
    if subject_po and subject_po == cand_po:
        score += Decimal("0.30")
        signals.append("same_po")
    if subject_total == cand_total and subject_total != 0:
        score += Decimal("0.30")
        signals.append("total_equal")
    elif subject_total and abs(subject_total - cand_total) / abs(subject_total) <= Decimal("0.01"):
        score += Decimal("0.20")
        signals.append("total_within_1pct")
    if number_similarity(subject_number, cand_number) >= 0.8:
        score += Decimal("0.20")
        signals.append("number_similar")
    if abs((subject_date - cand_date).days) <= 14:
        score += Decimal("0.10")
        signals.append("date_within_14d")
    if subject_lines and subject_lines == cand_lines:
        score += Decimal("0.10")
        signals.append("same_line_set")
    label = ("LIKELY_DUPLICATE" if score >= Decimal("0.90")
             else "POSSIBLE_DUPLICATE" if score >= Decimal("0.70") else None)
    return DuplicateScore(candidate_id="", score=score, signals=tuple(signals), label=label)


def score_duplicates(subject_number: str, subject_date: date, subject_total: Decimal,
                     subject_po: str | None, subject_lines: set[tuple[str, Decimal]],
                     candidates: list[dict]) -> list[DuplicateScore]:
    """candidates: dicts with keys record_id/number/date/total/po_id/lines."""
    out: list[DuplicateScore] = []
    for c in candidates:
        s = score_pair(subject_number, subject_date, subject_total, subject_po, subject_lines,
                       c["number"], c["date"], c["total"], c["po_id"], c["lines"])
        if s is not None and s.label is not None:
            out.append(DuplicateScore(candidate_id=c["record_id"], score=s.score,
                                      signals=s.signals, label=s.label))
    return sorted(out, key=lambda s: s.score, reverse=True)
