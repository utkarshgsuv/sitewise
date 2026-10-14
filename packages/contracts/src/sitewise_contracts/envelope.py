"""Call envelope — backend-signed JWT, never model-authored (technical.md §6.3)."""
from __future__ import annotations

import time
import uuid
from typing import Literal

import jwt
from pydantic import BaseModel, Field

ISSUER = "sitewise-api"
AUDIENCE = "sitewise-mcp"
TTL_S = 60


class EnvelopeClaims(BaseModel):
    iss: Literal["sitewise-api"] = ISSUER
    aud: Literal["sitewise-mcp"] = AUDIENCE
    iat: int
    exp: int
    jti: str
    org_id: str
    user_id: str
    role: str
    case_id: str
    run_id: str
    attempt_id: str
    tool: str
    args_digest: str


def sign_envelope(secret: str, *, org_id: str, user_id: str, role: str, case_id: str,
                  run_id: str, attempt_id: str, tool: str, args_digest: str) -> str:
    now = int(time.time())
    claims = EnvelopeClaims(
        iat=now, exp=now + TTL_S, jti=str(uuid.uuid4()),
        org_id=org_id, user_id=user_id, role=role, case_id=case_id,
        run_id=run_id, attempt_id=attempt_id, tool=tool, args_digest=args_digest,
    )
    return jwt.encode(claims.model_dump(), secret, algorithm="HS256")


def verify_envelope(secret: str, token: str) -> EnvelopeClaims:
    payload = jwt.decode(token, secret, algorithms=["HS256"], audience=AUDIENCE, issuer=ISSUER)
    return EnvelopeClaims.model_validate(payload)
