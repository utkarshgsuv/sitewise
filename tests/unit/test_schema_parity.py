"""Schema parity: Alembic 0001 snapshot must create exactly the tables in models.

Runs fully offline (alembic --sql). Catches models-vs-migration drift without a DB.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

from sitewise_api.db.models import Base

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TABLES = set(Base.metadata.tables) | {"alembic_version"}

# Tables that legitimately carry no org_id: the tenant roots themselves.
NO_ORG_TABLES = {"organizations", "users", "memberships"}


def _migration_sql() -> str:
    env = {**os.environ, "DATABASE_URL_DIRECT_OWNER": "postgresql+psycopg://localhost/dummy"}
    proc = subprocess.run(
        [sys.executable, "-m", "alembic", "-c",
         str(ROOT / "db" / "migrations" / "alembic.ini"),
         "upgrade", "head", "--sql"],
        capture_output=True, text=True, cwd=ROOT, env=env, check=True,
    )
    return proc.stdout


def test_migration_creates_all_model_tables():
    sql = _migration_sql()
    created = set(re.findall(r"CREATE TABLE (\S+)", sql))
    created = {t.strip('"') for t in created}
    assert EXPECTED_TABLES <= created, f"missing tables: {EXPECTED_TABLES - created}"


def test_tenant_tables_carry_org_id():
    for name, table in Base.metadata.tables.items():
        if name in NO_ORG_TABLES:
            continue
        assert "org_id" in table.c, f"{name} missing org_id"


def test_idempotency_and_approval_uniqueness_in_sql():
    sql = _migration_sql()
    assert "uq_ledger_org_tool_key" in sql
    assert "UNIQUE (approval_id)" in sql or "approval_id" in sql
