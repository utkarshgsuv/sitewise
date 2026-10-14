# Sitewise

Governed AI procurement & finance-ops agent (ArmorIQ Flow State 2026 hackathon).

Sitewise investigates a business exception across company records — POs, contracts,
invoice history, vendor-master changes — produces evidence-linked findings, and
prepares the review work (task + vendor-message draft). The point of the project:
the agent **cannot cross its authorized boundary unnoticed or unchecked**.

The 4-minute proof: a ₹18 lakh invoice yields risk signals + review task + draft;
a malicious invoice makes the agent really attempt `export_all_supplier_bids`;
live ArmorIQ blocks it, the MCP server independently refuses, and DB proof
(canary empty, no forbidden ledger rows, bids checksum unchanged) shows nothing happened.

> Live UI (mock data): https://sitewise-iota.vercel.app
> All demo data is fictional (`.example.test` domains, invented GSTINs).

## Stack

Python 3.12 (FastAPI, Google ADK, FastMCP, ArmorIQ SDK) · Neon PostgreSQL ·
Next.js + shadcn/ui · uv + pnpm · Docker Compose (local) / Vercel (web).

## Repo layout

```
packages/contracts/   shared frozen types: tool IO, events, enums, envelope JWT, digest
apps/api/             FastAPI runtime: auth/routes, ingest, deterministic engine, agents, gateway
apps/mcp/             FastMCP tool server: guards, tools, ledger, canary
apps/web/             Next.js UI (mock mode by default; real API with NEXT_PUBLIC_USE_MOCK=false)
db/migrations/        Alembic schema (Alembic)          db/security/  roles, RLS, append-only (raw SQL)
db/seed/              seed script + deterministic PDF fixtures
policies/             ArmorIQ policy source of truth    tests/        unit, security, redteam, e2e
```

Spec docs: `technical.md` (how), `plans.md` (schedule, task IDs), `team_distribution.md`
(Person A = Boundary, Person B = Product).

## Quickstart

```bash
cp .env.example .env        # fill Neon pooled/direct URLs + secrets (never commit .env)

# database
alembic -c db/migrations/alembic.ini upgrade head
uv run python db/seed/seed_demo.py        # or: make seed
# checksum must print 74a8d538820eed7697d537ba7a12baea

# backend
uv sync && uv run uvicorn sitewise_api.main:app --port 8000   # from repo root (.venv)

# frontend (runs on mock data; no backend needed)
cd apps/web && pnpm install && pnpm dev    # http://localhost:3000
```

Demo logins (seeded): any `*@*.example.test` email, e.g.
`asha@meridian.example.test` / password `Sitewise-Demo-1234`.

## Tests

```bash
uv run --with pytest pytest tests/unit -q
```

## Status

Active build (10–17 Oct 2026 window). Backend: schema + seed + comparison engine live
on Neon; agent pipeline, ArmorIQ path, and approvals in progress. UI runs on mock data
until the API routes land.
