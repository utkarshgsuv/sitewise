"""SSE + audit event schema (technical.md §14.2)."""
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

EventType = Literal[
    "run.started", "stage.started", "stage.completed",
    "plan.declared", "plan.token_issued",
    "tool.attempted", "governance.decision", "mcp.result",
    "finding.created", "task.created", "draft.created",
    "approval.requested", "attack.detected",
    "run.completed", "run.failed",
]


class RunEvent(BaseModel):
    seq: int
    run_id: str
    ts: datetime
    type: EventType
    payload: dict[str, Any] = Field(default_factory=dict)


class GovernanceDecisionPayload(BaseModel):
    attempt_id: str
    tool: str
    verdict: str
    exec_status: str
    reason: str = ""
    armoriq_trace_ref: str | None = None
    declared_in_plan: bool = True
