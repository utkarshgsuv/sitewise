"""Finding builder — E-05. The LLM never authors findings; it only narrates them.

Every finding MUST carry >=1 evidence link or it is rejected (T-15).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Finding:
    type: str
    severity: str
    confidence: str
    title: str
    detail: dict[str, Any]
    evidence_refs: tuple[dict[str, Any], ...] = field(default=())


def evidence_record(table: str, record_id: str, note: str = "") -> dict[str, Any]:
    return {"record_table": table, "record_id": record_id, "note": note}


def build_finding(*, type: str, severity: str, confidence: str, title: str,
                  detail: dict[str, Any], evidence_refs: list[dict[str, Any]]) -> Finding:
    if not evidence_refs:
        raise ValueError(f"refusing evidence-less finding of type {type} (T-15)")
    return Finding(type=type, severity=severity, confidence=confidence,
                   title=title, detail=detail, evidence_refs=tuple(evidence_refs))
