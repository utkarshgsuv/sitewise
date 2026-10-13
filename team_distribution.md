# SITEWISE — Team Distribution (2 people)

Companion to `technical.md` and `plans.md`. Task IDs (G-01, U-05, …) refer to `plans.md` Level 3.

> **Naming:** the proposal uses *Person A* and *Person B*. Decide today who is who (see §10). Everything below uses those labels.

---

## 1. Principle: split by *trust boundary*, not by tech

The product has two halves that meet at a frozen contract:

| | **Person A — "Boundary"** | **Person B — "Product"** |
|---|---|---|
| Question they answer | *Can the agent be trusted not to cross the line?* | *Can a finance manager actually use this?* |
| Owns | ArmorIQ, Gateway, MCP server, agents (ADK), DB security SQL, red-team, canary, ledger, proof queries | FastAPI, auth, Neon schema/migrations, seed + fixtures, ingestion, comparison engine, approvals API, all UI, README/demo packaging |
| Fails if | the block is fake, unproven, or bypassable | the demo is unusable, evidence is unclear, setup doesn't work |

**Rebalance vs proposal (D9):** the proposal gave Person A also the audit UI and everything agentic. We moved to B: the audit/governance/proof **UI**, the **comparison engine**, the **extraction grounding**, and the **seed/fixture generators**. A still defines the *data* those UIs show (event schema + SQL). Net: A's critical path shrinks by ~10–12 h.

---

## 2. Ownership map (directory = owner)

`CODEOWNERS` enforces this. Owner reviews every PR touching their paths; the *other* person must review any PR in the "shared" paths.

| Path | Owner | Reviewer |
|---|---|---|
| `packages/contracts/**` | **Shared** | both must approve |
| `apps/mcp/**` | A | B (security-relevant: required) |
| `apps/api/gateway/**` | A | B |
| `apps/api/agents/**` | A | B |
| `db/security/**` | A | B (review SQL, run negative tests) |
| `policies/**` | A | B |
| `tests/security/**`, `tests/redteam/**` | A | B |
| `apps/api/engine/**` | B | A (as MCP-tool consumer) |
| `apps/api/ingest/**` | B | A |
| `apps/api/routes/**`, `auth/**`, `services/**`, `db/**` (models) | B | A |
| `db/migrations/**` | B | A (security impact) |
| `db/seed/**` | B | A (fixtures tuned jointly) |
| `apps/web/**` | B | A (Governance/Proof panels must match event schema) |
| `README.md`, `docs/**` | B (A writes governance/threat sections) | A |
| `docker-compose.yml`, `Makefile`, CI | B | A |

---

## 3. Person A — "Boundary" (Governance & Agents)

### Mission
Prove that the useful workflow runs through live ArmorIQ, and that a forbidden action is genuinely attempted, blocked, and verifiably didn't happen.

### Deliverables (all P0 unless noted)
1. **ArmorIQ integration** — spike S1, adapter (Mode A/B), verdict normalization, fail-closed (G-01..G-05, G-07)
2. **Governed Gateway** — attempt logging, envelope signing, correlation IDs (G-03)
3. **MCP server** — envelope verification, guards, read tools, `compare_invoice_terms` wrapper, mutating tools, forbidden stubs, armed canary, approval guard, idempotency (M-01..M-07)
4. **Agent pipeline** — ADK spike S2, 4 stage agents, caps, blocked-attempt handling (A-01..A-07)
5. **DB security** — roles/grants/RLS/append-only (D-03, D-04) · *P2:* hash chain (D-05)
6. **Red-team** — fixture tuning, attempt-rate, route-around, 2×2 matrix (R-01..R-04)
7. **Data contracts for B's UI** — `/audit` and `/proof` SQL + event payload samples (feeds P-07, P-08)

### Skills / focus
Python async, security mindset, SQL (RLS), prompt/agent debugging.

### Estimated load
≈ 60 h P0. **First cut list if behind:** D-05, R-04 (keep manual table), R-05, G-07, A-08.

### Daily "definition of done" for A
| Day | Done means |
|---|---|
| Tue | S1+S2 answered in writing; MCP hello with envelope verify; contracts v0 merged |
| Wed | Gateway + MCP read tools + 4-stage pipeline produce findings on seeded case (with B's engine) |
| Thu | Forbidden attempt blocked live; T-05/06 green; approval guard + idempotency done; security suite green |
| Fri | Matrix + attempt-rate report; bug queue empty; rehearsals |
| Sat | Governance section of narration; evidence folder |

---

## 4. Person B — "Product" (Platform & Experience)

### Mission
Deliver a complete, understandable investigation workflow with evidence you can click into, an approval flow, and a fresh-clone setup that works the first time.

### Deliverables (all P0 unless noted)
1. **Repo, Compose, CI, Makefile (`up/seed/reset/test/demo`)** (F-01..F-03, D-06)
2. **Neon + schema** — project, branches, connection strings, Alembic migrations (D-01, D-02)
3. **Seed + fixtures** — 2 orgs, vendor, contract/PO/invoices, bank-change event, bids, 3 PDFs (S-01..S-03)
4. **Ingestion + extraction grounding + cross-validation** (I-01..I-03)
5. **Deterministic engine** — variance, duplicate, bank, payment, finding builder (E-01..E-05)
6. **FastAPI** — auth, tx helper (`app.org_id`), cases, run/SSE, findings, drafts, approvals (four-eyes), `/audit`, `/proof` (P-01..P-08)
7. **Next.js UI** — shell, timeline, findings/evidence, actions, approvals, **Governance panel**, **Proof panel** (U-01..U-07) · *P1:* policy view · *P2:* Arena, PDF highlight
8. **README, architecture diagram, demo script, submission package** (X-01..X-05)

### Skills / focus
FastAPI, Postgres/Alembic, Next.js/TypeScript, product polish, documentation.

### Estimated load
≈ 60 h P0. **First cut list if behind:** U-08..U-10, S-04, F-03, P-09, PDF bbox.

### Daily "definition of done" for B
| Day | Done means |
|---|---|
| Tue | Compose boots; Neon + roles; schema v1; fixture generator; S4 and S6 answered |
| Wed | Seed + extraction + engine tests green; auth + run/SSE skeleton; UI shell; engine handed to A by 13:00 |
| Thu | Findings/evidence + Governance panel on real events; drafts/approvals API+UI; `/audit` + `/proof` |
| Fri | Proof panel; README; reset/demo scripts; fresh-clone test on a different machine |
| Sat | Recording, packaging, submission |

---

## 5. Shared responsibilities (both)

| Item | How |
|---|---|
| **Contracts v0 freeze** (Tue ~13:00, 60–90 min pairing) | Walk through §9 of technical.md; agree tool IO, enums, envelope claims, event schema, error taxonomy, digest function. Merge to `main`. |
| **Evening integration sessions** (Wed, Thu, Fri) | 60–90 min on one screen: run the end-to-end flow, list drift, assign fixes. |
| **Security review swaps** | A reviews B's migrations, authz in routes, approvals API. B reviews A's SQL & MCP guards by *running negative tests*, not just reading. |
| **Rehearsals** | Fri evening ×3, one on B's cold clone, one on A's machine. |
| **Demo narration** | B: product story (0:00–1:30, 3:40–4:00). A: boundary story (1:30–3:40). |
| **Demo + submission QA** | Each person checks the other's part of the video before upload. |

---

## 6. Interface hand-offs (the places where work crosses)

| # | From → To | What | Due | Format / check |
|---|---|---|---|---|
| H1 | A+B | Contracts v0 | Tue 14:00 | merged `packages/contracts`; both ✅ |
| H2 | B → A | Schema v1 for business tables + seed numbers | Tue 20:00 | migrations on Neon dev branch |
| H3 | A → B | Security SQL (roles/RLS) applied on top | Wed 12:00 | `make migrate` order; T-14 passes |
| H4 | B → A | Engine (`compare_invoice_terms` core) | Wed 13:00 | importable pure functions + unit tests |
| H5 | A → B | Real event samples (`plan.declared`, `governance.decision`, `mcp.result`) JSON | Wed 15:00 | `docs/events_sample.jsonl` — B builds timeline + panel against it |
| H6 | B → A | Malicious PDF generator with wording hooks | Thu 09:30 | A tunes injection text in a single config file |
| H7 | A → B | `/audit` and `/proof` SQL | Thu 13:00 | views or query functions in `db/security/` |
| H8 | B → A | Approvals API + draft digest endpoints | Thu 14:00 | A's MCP guard consumes same digest fn |
| H9 | A → B | Governance section text + threat model | Fri 12:00 | markdown in `docs/` |
| H10 | B → A | Fresh-clone checklist outcome | Fri 20:00 | list of defects, A fixes MCP/agent ones |

If a hand-off is late by > 2 h, the receiver works against a **stub** (fixed JSON / fixture) and the sender gets pinged — never block idle.

---

## 7. Working agreements

### 7.1 Git
- `main` is always runnable. Short-lived branches `a/<id>-slug` or `b/<id>-slug`.
- PRs < 400 changed lines where possible; squash merge; PR title starts with the task ID.
- **Required reviewer** per §2. Contracts and security SQL need **both** approvals.
- No force-push to `main`. After M2: red `main` > 2 h → revert last merge.
- Tags: `m0` … `m6`, `v1.0-rc`, `v1.0`.

### 7.2 Communication
- One shared chat thread; **contract change announcements** prefixed `[CONTRACT]`.
- Blockers prefixed `[BLOCKED]` with what you tried; response expected within 30 min during work blocks.
- Decisions go into `technical.md` §23 (decision log) the same day — the doc stays the truth.
- Stand-up 09:00 (5 min), sync 13:00 (10 min), integration evening (60–90 min). Sleep is a feature: no work after ~01:00 Thu/Fri unless a gate is on fire.

### 7.3 Secrets
Shared via a password manager. `.env` is gitignored; gitleaks pre-commit. **Never** paste keys into chat or screenshots in the demo.

### 7.4 Mocking rule
Stubs for *neighbouring* components are fine while developing. **Mock governance only in `tests/unit` guarded by `SITEWISE_ENV=test`.** If you catch a mock in the demo path, it's a P0 bug.

### 7.5 Definition of Done for any task
Code merged to `main` · tests added (positive **and** one negative) · contract/docs updated if touched · checked with the other person if it crosses a hand-off · checkbox ticked in `plans.md`.

---

## 8. Day-by-day split (condensed view)

| Day | Person A | Person B | Together |
|---|---|---|---|
| **Tue 13** | S1 ArmorIQ spike → S2 ADK spike → MCP hello + envelope | Repo/Compose/CI → Neon + roles → schema v1 → fixture generator → S4, S6 | Contracts v0 freeze; M0 gate review |
| **Wed 14** | Security SQL → read tools → Gateway → ADK pipeline | Seed → extraction/grounding → engine → auth + run/SSE → UI shell | Evening integration #1 (happy path) |
| **Thu 15** | Stubs+canary → fixture tuning → block proof (M3) → approval guard → idempotency → fail-closed → security suite | Malicious PDF → findings/evidence UI → Governance panel → approvals API/UI → `/audit` `/proof` | Noon gate M3; evening gate M4; **feature freeze 21:00** |
| **Fri 16** | Matrix, attempt-rate, bug queue, governance docs | Proof panel, policy view (P1), README, reset/demo scripts, cold-clone test | Rehearsals ×3; hard freeze 23:59 |
| **Sat 17** | Pre-flight + governance narration + evidence folder | Recording setup + packaging + submission | Record, review, submit |

---

## 9. Coverage and backup (who covers whom)

| If… | Then |
|---|---|
| A is blocked on ArmorIQ > 90 min | B pairs on the spike (reads docs/organizer channel, tests tunnel), A keeps Gateway code moving against Mode B |
| B is blocked on UI/SSE | A supplies sample events; B builds against fixtures; A pairs 30 min |
| One person is sick/unavailable | Other drops P1/P2 and builds only the **P0 demo path**: seeded case → run → block → proof; use plain tables instead of polished UI |
| Merge conflicts in contracts | Contracts owner on duty = whoever opened the PR; other reviews within 30 min |

Cross-training moments (so either person can run the demo): Thu evening each person runs the **other's** half once from a clean state.

---

## 10. Choosing who is A and who is B

| Choose A if you… | Choose B if you… |
|---|---|
| are strongest in backend security, SQL/RLS, async Python, debugging agents | are strongest in full-stack product work, TypeScript/React, and polish |
| enjoy reading SDK docs and chasing "why did it allow that?" | enjoy shaping UX and writing clear docs |
| are comfortable being on the critical path | prefer many parallel, visible deliverables |

If both are strong full-stack, pick by who already has an ArmorIQ API key and has read its docs — that person is A.

---

## 11. Workload at a glance

| Area | A (hours) | B (hours) |
|---|---|---|
| Foundations & DB | ~4 | ~12 |
| Governance + Gateway | ~14 | – |
| MCP | ~15 | – |
| Agents | ~13 | – |
| Ingestion + engine + seed | ~2 | ~16 |
| API | – | ~13 |
| UI | – | ~16.5 |
| Red-team | ~4 | (fixture 1.5) |
| Docs + demo | ~4 | ~7 |
| **Total P0** | **≈ 58–62** | **≈ 58–62** |

Roughly balanced; A's work is on the critical path, B's is wider. Because A's tasks gate everything, **B should treat any request from A for a stub, sample, or review as top priority.**

---

## 12. Checklist for hour zero (do today)

- [ ] Decide who is A / B
- [ ] Both create ArmorIQ + Google AI Studio + Neon accounts/keys; share via password manager
- [ ] A starts S1 immediately; B scaffolds repo and Neon
- [ ] Schedule: stand-ups (09:00), sync (13:00), integration (evening) for Wed–Fri
- [ ] 60–90 min contracts pairing today
- [ ] Read the official event page rules once together

*End of team_distribution.md*
