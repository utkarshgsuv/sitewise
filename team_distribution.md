# Sitewise: Team Distribution (2 people, parallel branches)

**Updated:** Mon 12 Oct 2026 · **Deadline:** Sat 17 Oct 2026
**Companions:** `plans.md` (milestones, day-by-day lanes, full task backlog) · `technical_project.md` (all technical decisions)

**Update:** both of you build with AI coding assistants, so the scope target is the **best version possible** (technical doc §21) and the workflow includes AI-specific rules (§14). Writing code is no longer the constraint. Verification, integration and the ArmorIQ unknowns are.

**Database update:** the database is one **Neon** project (golden `main` branch plus one branch per person) and **Docker is no longer part of the dev loop** (technical doc §24, section 15 below). The schema travels through git and Alembic, the data lives in your own Neon branch, so there are no images to keep in sync.

You are **Person A** and **Person B**. Replace those labels with your names in the first commit.

---

## 1. Principles: how two people build one project in parallel

1. **Split by area, not by file.** Each of you owns whole directories. Almost nobody edits the other's files.
2. **Contracts first.** On Monday morning you spend about 90 minutes together freezing the shared interfaces (§6). After that, each side codes against a contract and a stub, never against the other person's unfinished code.
3. **Stubs remove waiting.** Every dependency across the split has a stand-in the consumer can use today (§5).
4. **Own branches, frequent checkpoints.** You each work on your own long-lived branch and merge into `main` at fixed checkpoints (§7). You asked for a final merge; the checkpoints are small safety merges on the way, because merging two six-day branches only at the end is the single biggest avoidable risk.
5. **Pair only where the seams are.** Five short joint sessions (§8.2) handle integration. Everything else is solo.
6. **Say it early.** If you change something the other person depends on, tell them in one line, immediately.

---

## 2. Roles

### Person A: Governance and Agents lead
**Owns the "boundary holds" half of the product.**
- ArmorIQ integration and spike (S1 to S10), per-persona policies, fail-closed behaviour
- Google ADK agents (investigator, recorder), orchestrator, circuit breaker, attempt logging
- MCP tool server: every tool, the forbidden stubs, canary table, idempotency, ledger writes
- Comparison engine, DB roles, RLS and append-only triggers (`db/sql/`, applied by `make db-init` on Neon)
- Audit pane and lab page
- Governance tests (T01 to T04, T07 to T17, T19, T20) and the red-team set
- Narrates the second half of the demo (hostile document, block, proof)
- **Showcase lane (§4.1):** Attack Arena, policy conformance matrix, tamper-evident ledger, Row-Level Security, replay, supplier-reply and RFI agent tools, FollowUpAgent

**Skills this lane needs:** Python async, ADK, careful reading of SDK docs, security thinking.

### Person B: Platform and Product lead
**Owns the "useful work" half of the product.**
- Repo skeleton, Makefile and `Procfile.dev` (native `make up`, no Docker), Neon project and branches, `.env.example`, CI
- Schema, models, migrations, auth, `authz.py`, API, SSE, uploads
- Fixtures and seed data (including Case B and the hostile PDF)
- Ingestion and extraction (text layer, vision agent, cross-check, confirmation)
- State machine and approval hashing; approvals and resolve endpoints
- Main UI: login, intake with live timeline, extraction review, issue detail, approvals
- README, architecture diagram, packaging; API and e2e tests (T05, T06, T18, Playwright)
- Narrates the first half of the demo
- **Showcase lane (§4.1):** evidence pack PDF, supplier portal, spec ingestion and RFI UI, Hindi and voice, PWA, email sink, hosted demo, extraction evaluation

**Skills this lane needs:** FastAPI, SQLAlchemy, Next.js/TypeScript, multimodal extraction.

### Why this split
- The riskiest unknowns (ArmorIQ plan semantics, header passthrough, HOLD flow) all sit in A's lane, so one person focuses on them fully instead of two people half-learning them.
- B's lane is more predictable and unblocks the demo story.
- Work is split about evenly, including the showcase features (§4.1). Plan by **size and risk**, not by hours: with AI assistance the slow parts are the ArmorIQ unknowns, live-model tuning and verification.

---

## 3. Ownership map

"Owner edits freely. Others: ask first, or use the listed exception."

| Path | Owner | Notes and exceptions |
|---|---|---|
| `backend/sitewise/agents/**` | A | Includes prompts, orchestrator, plugins, `ScriptedLlm`. Must not import DB models (test T19). |
| `backend/sitewise/mcp_server/**` | A | All MCP tools and middleware. |
| `backend/sitewise/runtime/**` | A | DB-backed `RunRepository` and `AttemptRepository` implementations. |
| `backend/sitewise/domain/compare.py`, `units.py` | A | |
| `backend/sitewise/db/sql/**` | A | Roles, RLS and triggers as plain idempotent SQL, applied by `make db-init` after migrations. Roles are created by SQL, never in the Neon console. |
| `policies/**` | A | Mirror of the ArmorIQ console. |
| `backend/sitewise/api/routers/audit.py`, `lab.py` | A | **Exception:** A adds these two files inside B's `api/`. B's `main.py` auto-includes every router module, so `main.py` is never edited. |
| `backend/seed/a_governance.py` | A | **Exception:** auto-loaded by B's seed runner. |
| `web/app/audit/**`, `web/app/lab/**`, `web/components/audit/**` | A | B pre-creates the nav links on Day 1. |
| `backend/tests/contract`, `integration`, `live`, `redteam` | A | |
| `docs/spike_results.md`, `docs/threat_tests.md` | A | |
| `backend/sitewise/api/**` (except A's two routers) | B | |
| `backend/sitewise/db/models*`, `backend/alembic/**` | B | **Only B creates migrations** (§7.4). |
| `backend/sitewise/authz.py` | B | A imports it and requests changes. |
| `backend/sitewise/domain/state.py`, `approvals.py` | B | A imports them. |
| `backend/sitewise/ingest/**` | B | Implements `FactsRepository`. |
| `backend/seed/**` (except `a_governance.py`) | B | |
| `web/**` (except A's folders) | B | |
| `Procfile.dev`, `Makefile`, `.env.example`, `.github/**` | B | **Exception:** A appends lines under an `# --- A: governance ---` header. |
| `backend/tests/unit` (API/domain), `e2e/` | B | |
| `README.md`, `docs/architecture*` | B | A writes the governance and limitations sections in `docs/governance.md`, which B links into README. |
| `backend/sitewise/contracts/**` | **Shared** | Change only by agreement (§10). |
| `backend/pyproject.toml`, lockfiles | **Shared** | Rules in §7.4. |

---

### 3.1 Ownership for the showcase features

| Path | Owner | Notes |
|---|---|---|
| `redteam/**` (Arena attack catalogue, runner) | A | |
| `backend/sitewise/api/routers/arena.py`, `replay.py` | A | Same exception as `audit.py`: auto-discovered, no edit to B's `main.py`. |
| `web/app/arena/**`, `web/app/policy/**`, `web/app/replay/**` | A | B pre-creates nav links on Day 1. |
| `backend/sitewise/db/sql/**` (RLS policies, chain triggers) | A | |
| `backend/sitewise/runtime/**` (`verify_chain`, ledger chaining) | A | B calls it through the contract Protocol. |
| `backend/sitewise/ingest/specs/**` (chunking, embeddings, pgvector) | B | A consumes `spec_chunks` through `search_project_specs`. |
| `backend/sitewise/api/**` evidence PDF, supplier portal, voice, digest endpoints | B | |
| `web/**` portal, evidence button, Hindi, voice, PWA | B | |
| `deploy/**` (Caddy, VM service setup), `scripts/` (except `check_ownership.py`) | B | A reviews anything about MCP or ArmorIQ hosting. |
| `OWNERSHIP.yaml`, `AGENTS.md`, `scripts/check_ownership.py` | Shared | Created at kickoff; changes need agreement. |

---

## 4. Task assignment summary

Full details, estimates and acceptance criteria are in `plans.md` Level 4.

| Person A | Person B |
|---|---|
| **WS6:** G1 to G9 (ArmorIQ) | **WS1:** P1, P2, P4, P5, P6, P7, P8, C2 · **WS-DB:** N1, N2, N4, N5 |
| **WS-LLM:** L1, L2, L3, L5 (model factory, qualification, rate limiter, two-model Arena) | **WS-LLM:** L4, L6, L7 (vision qualification, hosted-demo key, embeddings and STT) |
| **WS5:** M1 to M7 (MCP tools) | **WS2:** D1, D2, D3, D5, D6 |
| **WS4:** A1 to A7 (agents) | **WS3:** E1 to E5 |
| D4, P3, N3 (compare, SQL roles, Neon spike) | **WS7a:** U1 to U5, U8, U9 |
| U6, U7 (audit, lab) | T-A, T-B2, T-D2, T-F |
| T-B1, T-C, T-D1, T-E | S1, S2 (README, diagram) |
| S6 (limitations) | **Both:** C1, S3, S4, S5, I1 to I4 |

---

### 4.1 Showcase assignments (full detail in `plans.md` Level 4B)

| Person A | Person B |
|---|---|
| X1 Attack Arena (15+ attacks, 3 live runs each, report) | X4 Evidence pack PDF |
| X2 Policy conformance matrix (live) | X5 Supplier portal and tokens |
| X3 Hash-chained ledger and `verify_chain` | X6 Spec ingestion, pgvector, RFI UI |
| X9 Postgres Row-Level Security | X7 Digest UI and spoken digest |
| X10 Replay page and OpenTelemetry | X8 Hindi/English and voice notes |
| X5 evidence stage (`EvidenceAgent`, tools) | X11 Hosted demo |
| X6 RFI tools (`search_project_specs`, `draft_rfi`, `send_rfi`) | X12 PWA with offline queue |
| X7 `FollowUpAgent` | X13 Email sink (Mailpit) |
| X14 ADK multi-agent (if S11 positive), X17 quote comparison | X15 Extraction evaluation, X18 WhatsApp sandbox |
| X16a property tests (compare, tools, hashing) | X16b property tests (authz, state machine, approvals) |

Both: **AI1 to AI4** (AGENTS.md, ownership guard, verified-snippet registry, ignore lists).

---

## 5. Seams and stubs: how each side works without the other

| # | Seam | Who produces | Who consumes | The consumer's stub until the real thing lands |
|---|---|---|---|---|
| 1 | DB schema and models | B (Mon 13:00) | A | A writes pure logic first (comparison, middleware, spike), then builds tools on the schema after CP0 |
| 2 | `authz.authorize(...)` | B | A (MCP tools) | `contracts/authz_stub.py` implements the permission matrix in memory |
| 3 | `RunService.start_run` and `RunEvent` stream | A | B (runs endpoint, UI) | B's `FakeRunService` replays canned events, so the UI and SSE are built without the orchestrator |
| 4 | `EventBus.publish` | B | A (orchestrator) | In-memory list bus for A's tests |
| 5 | `FactsRepository.confirmed_facts` | B | A (stage input) | JSON fixture of confirmed Case A facts |
| 6 | Approvals table and `payload_hash(draft)` | B | A (send tool) | A hand-inserts an approval row in tests |
| 7 | Audit data (`agent_tool_attempts`, `action_ledger`) | A | A's own UI | A owns the whole chain; B only provides the nav link |
| 8 | Seed and fixed IDs | B | A | A adds `seed/a_governance.py` (personas for policies) |
| 9 | `DocumentStore.get` (file bytes in `document_blobs`) | B (`ingest/`) | A (`read_document`) | `InMemoryDocumentStore` in `tests/` |
| 10 | Neon project, branches, role passwords | B | A | None needed before CP0 (A's spike and comparison engine are pure code); then A's own branch `dev-a` |

**Rule for stubs:** a stub lives in `contracts/` or in `tests/`, never inside the other person's directory. When the real implementation lands, the consumer deletes the stub in one commit.

---

### 5.1 Seams added by the showcase features

| Seam | Producer → Consumer | Stub |
|---|---|---|
| `supplier_replies` and portal tokens | B → A (`attach_supplier_evidence`) | A inserts a reply row by hand |
| `spec_chunks` | B → A (`search_project_specs`) | A seeds a few chunks (keyword fallback) |
| `verify_chain(project_id)` | A → B (evidence pack, UI badge) | Stub returns `valid` |
| `Digest` model | A → B (UI, TTS) | Fixture JSON |
| `lang` claim | B → A (agent output language) | Default `en` |
| Hosting requirements (env, MCP URL, S4 result) | A ↔ B | Written in `docs/decisions.md` |

---

## 6. Contracts to freeze at the Monday kickoff (WS0 / C1)

Location: `backend/sitewise/contracts/`. Python and Pydantic only, no business logic. Target: about 90 minutes together, one person types, both review.

| File | Contents |
|---|---|
| `enums.py` | `Role`, `IssueState` (§6.4 of the technical doc), `Decision` (ALLOW/HOLD/BLOCK/ERROR), `ApprovalStatus`, `Stage`, `ToolClass` |
| `ids.py` | Fixed UUIDs for personas, Project A and B, suppliers, PO-2026-0117, documents (so tests and seeds agree) |
| `extraction.py` | `ExtractedField`, `ExtractionResult`, `ConfirmedFact` (from technical doc §7.3) |
| `tools.py` | Pydantic arg and result models for **every MCP tool** (the tool contract from §9.1). Includes error codes (`PROJECT_MISMATCH` etc.) |
| `events.py` | `RunEvent` types: `stage_started`, `tool_proposed`, `policy_decision`, `tool_result`, `agent_text`, `awaiting_input`, `awaiting_approval`, `error`, `done` |
| `protocols.py` | `RunService`, `EventBus`, `FactsRepository`, `DocumentStore`, `RunRepository`, `AttemptRepository` |
| `authz_types.py` | `Actor`, `Action`, `Decision`, plus `authorize(actor, action, project_id=None, resource=None)` signature |
| `claims.py` | Run-context JWT claims (technical doc Appendix B) plus an optional `lang` (`en` or `hi`): a presentation hint, **never authority**. Add it now so it is not a late contract change |
| `digest.py` | `Digest` model for the FollowUpAgent output (X7) |

Sketch of the key protocols:

```python
class RunService(Protocol):                       # A implements, B calls
    async def start_run(self, *, actor_id: UUID, project_id: UUID, message_id: UUID) -> UUID: ...
    async def resume_run(self, *, run_id: UUID, actor_id: UUID) -> None: ...

class EventBus(Protocol):                         # B implements, A publishes to it
    async def publish(self, run_id: UUID, event: RunEvent) -> None: ...
    def subscribe(self, run_id: UUID) -> AsyncIterator[RunEvent]: ...

class FactsRepository(Protocol):                  # B implements (ingest/), A consumes
    async def confirmed_facts(self, *, project_id: UUID, message_id: UUID) -> list[ConfirmedFact]: ...

class DocumentStore(Protocol):                 # B implements (ingest/storage.py), A's read_document consumes
    async def put(self, *, project_id: UUID, content_type: str, data: bytes) -> UUID: ...
    async def get(self, *, project_id: UUID, document_id: UUID) -> bytes: ...
```

**Freeze rule:** after kickoff, *additive* changes (a new field with a default, a new enum value) need only a one-line heads-up. *Breaking* changes (rename, remove, retype, new required field) need the other person's agreement (§10).

**Kickoff checklist**
- [ ] GitHub repo created, both added; branch protection on `main` (no force-push, PR required)
- [ ] Branches `a/governance` and `b/platform` created from the skeleton commit
- [ ] `contracts/` committed and reviewed by both
- [ ] Ports agreed: web 3000, api 8000, mcp 8001 (no local db port: the database is Neon)
- [ ] Neon: B creates the project (Postgres 16, region `aws-ap-southeast-1`, which cannot be changed later), invites A as a collaborator and creates `dev-b`. The three role passwords are shared once through a password manager. Each person's `.env` points at their own branch (technical doc §24)
- [ ] `.env.example` has every variable from the technical doc §18.1
- [ ] Keys: A creates the ArmorIQ key. **Each of you creates your own OpenRouter account and key and makes the one-time $10 credit purchase** (limits are per account, so two accounts double the free quota and unlock 1,000 free requests a day each). Optional Gemini key as a fallback provider. Share nothing in the repo or in public chat
- [ ] `docs/decisions.md` created (empty log)
- [ ] Both can run `make up` on an empty skeleton

---

## 7. Git workflow and merge checkpoints

### 7.1 Branches

| Branch | Purpose | Who pushes |
|---|---|---|
| `main` | Always demo-able at end of day. Updated only by checkpoint PRs. | Through PRs only |
| `a/governance` | A's long-lived working branch | A |
| `b/platform` | B's long-lived working branch | B |

Commit often on your own branch and push at least every couple of hours. Short-lived sub-branches are optional; if you use them, merge them into your own long-lived branch.

### 7.2 Daily routine (each person, on their own branch)

```bash
git checkout a/governance            # or b/platform
git fetch origin
git merge origin/main                # bring in whatever the other person checkpointed
# ... work, commit often ...
git commit -m "[A] G6: run_stage with fresh agent per run"
git push origin a/governance
```

Commit message prefix: `[A]` or `[B]` plus the task ID from `plans.md`.

### 7.3 Checkpoint merge into `main` (CP0 to CP5)

Whoever is ready first goes first.

```bash
# 1. On your branch, bring in the latest main and fix conflicts HERE, not on main
git fetch origin
git merge origin/main
make test                            # must pass
# 2. Push and open a PR  a/governance -> main  (or b/platform -> main)
git push origin a/governance
# 3. The other person reviews for ~15 minutes (§7.6), then merge with a MERGE COMMIT
```

- **Use merge commits, not squash and not rebase,** for these long-lived branches. Squashing makes git forget what was already merged and causes the same conflicts again at the next checkpoint.
- The **second person** to finish must do step 1 again (their `origin/main` now contains the first person's work), run tests, then PR.
- Right after each merge, both of you run `git merge origin/main` on your own branch so you start from the same base.
- If the merge brought in migrations or `db/sql/` changes: the person who merged runs `make promote-schema` (Neon `main` becomes golden again), then both run `make db-reset` on their own branch (§15).
- Tag each milestone: `git tag m1 && git push --tags` (m1 to m4, then `rc1`).

| Checkpoint | When | What must be true |
|---|---|---|
| CP0 | Mon ~13:00 | B's schema and `contracts/` on `main`; A merges `main` into `a/governance` |
| CP1 | Mon evening | Both merged; `make up` from a clean clone |
| CP2 | Tue evening, after the integration session | Case A works through the real API with ArmorIQ ON |
| CP3 | Wed evening | Core boundaries complete **plus showcase wave 1** (ledger chain, policy matrix, supplier portal loop, evidence pack, email sink) |
| CP4 | Thu evening | T01 to T38 results recorded; Arena report shows `executed = 0`; flags decided at 18:00; data model frozen |
| CP5 | Fri evening | Final merge; tag `rc1`; outsider follows README |

After CP5, only small fixes, made directly on `main` by agreement and announced in chat.

### 7.4 Conflict-prone files and the rule for each

| File | Rule |
|---|---|
| `backend/pyproject.toml` | Add dependencies on separate lines in alphabetical order. After a merge, run `uv lock` instead of hand-editing the lockfile. |
| `uv.lock`, `pnpm-lock.yaml` | **Never hand-merge.** On conflict, take `main`'s version, then re-run `uv lock` or `pnpm install`. |
| `backend/alembic/versions/**` | **Only B creates migrations.** If A needs a schema change, send a change request (§10); B adds the migration within about an hour. Migrations are **additive only until CP5** (no drops, renames or type changes). After a merge that carries migrations, run `make promote-schema` and then `make db-reset` on both branches (§15). If two heads ever appear, run `alembic merge heads` together. |
| `backend/sitewise/contracts/**` | Agreement required (§10). |
| `.env.example`, `Procfile.dev`, `Makefile` | B owns. A appends only under the `# --- A: governance ---` header. |
| `backend/sitewise/api/main.py`, `web` nav | Nobody edits for new pages. Routers are auto-discovered; B pre-creates nav links to `/audit` and `/lab`. |
| `backend/seed/**` | B owns the runner; each person adds their own file (`seed/a_governance.py`). |
| `README.md` | B edits. A writes in `docs/governance.md`. |
| `OWNERSHIP.yaml`, `AGENTS.md` | Shared. Change only by agreement; the ownership guard reads `OWNERSHIP.yaml`. |
| `backend/sitewise/db/sql/**` | A. RLS and chain triggers are plain SQL; B's migrations must not recreate them. |

### 7.5 If a merge conflict happens anyway
1. Stop. Do not resolve it on `main`.
2. Resolve on **your branch** after `git merge origin/main`.
3. If it touches the other person's files, resolve it together over a quick call. The owner of the file decides.
4. Re-run `make test` before pushing.
5. Never `git push --force` to `main`.

### 7.6 Review rules (15 minutes, not a ceremony)
Reviewer checks: tests pass; no secrets; no edits outside the author's ownership without a note; `contracts/` unchanged or logged; the author's status message explains what changed for the reviewer. Approve quickly. Do not block on style.

### 7.7 Repository hygiene
`.gitignore` covers `.env`, `storage/`, `node_modules/`, `__pycache__/`, `.venv/`. Pre-commit runs ruff and gitleaks, with an extra gitleaks rule for `postgres://user:password@host` URLs because a Neon connection string is a credential. Only synthetic fixtures are committed. Rotate any key that ever lands in git. The **ownership guard** (`scripts/check_ownership.py`, technical doc §22.6) runs on pre-push and in CI for `a/*` and `b/*` branches and fails if a branch touches the other person's paths. This is the main protection against an AI session editing the wrong lane.

---

## 8. Rhythm, pairing sessions and communication

### 8.1 Daily rhythm
| When | What | Length |
|---|---|---|
| Start of day | Standup: yesterday, today, blockers. Merge `origin/main` into your branch. | 15 min |
| Midday | Sync: any contract changes, anything blocked, tomorrow's integration needs | 10 min |
| End of day | Push, then post a two-line status in chat: **done / blocked / tomorrow, plus "what changed for you"** | 5 min |

### 8.2 Pairing sessions (the only planned joint work)
| # | When | Length | Agenda | Output |
|---|---|---|---|---|
| 1 | Mon 09:00 | 90 min | Kickoff: repo, branches, freeze `contracts/` (§6), keys, ports, Neon project and branches (§15) | `contracts/` on `main` |
| 2 | Tue 17:00 | 90 min | **Integration:** replace `FakeRunService` with A's orchestrator; run Case A with ArmorIQ ON through the real API and UI | CP2 merge, M2 gate |
| 3 | Wed midday | 60 min | **Approvals seam:** B's approval API and UI with A's `request_supplier_send` and `send_supplier_message`, hash check, HOLD release | Two-key send works |
| 4 | Thu 15:30 | 90 min | **Arena and red-team:** live Arena runs, tune hostile documents until the model really attempts forbidden calls, capture traces | Evidence for the demo, Arena report |
| 5 | Fri afternoon | 2 h | **Script rehearsal and recording**, 2 to 3 takes | Video |
| 6 | Sat midday | 1 h | Fresh-clone check and submission | Submitted |
| 7 | Thu 18:00 | 15 min | **Flag decision:** enable only features whose tests are green | Demo build configuration |

### 8.3 Communication rules
- One channel for all project chat (shared group). Decisions are written in `docs/decisions.md`, not left in chat.
- **Blocked for more than 30 minutes? Say so.** Switch to a stub or pair for 30 minutes.
- Never change another person's directory silently. Send a message first: "I need X in your area, can you do it or can I?"

---

## 9. Joint tasks (done together, not split)

| ID | Task | Why together |
|---|---|---|
| C1 | Contracts and repo skeleton | Both depend on it |
| I1 | Integration of orchestrator and API | The main seam |
| I2 | Two-key send | Spans both lanes |
| I3 | Red-team session | Needs the agent (A) and the UI and ledger (B) |
| S3, S4 | Demo script and recording | Both narrate |
| S5 | Submission | Two sets of eyes on the checklist |

---

## 10. Interface change requests and the decision log

If you need a contract or the other person's area changed, post this in chat:

```
CHANGE REQUEST
What: (one line)
Why: (one line)
Impact on you: (files or behaviour)
Needed by: (time)
```

Rules:
- **Additive and non-breaking:** go ahead, post a one-line heads-up.
- **Breaking, or inside the other person's directory:** wait for a "yes". The owner may say "I'll do it" instead.
- Log every accepted change in `docs/decisions.md`: date, what, who agreed, files touched.
- The ArmorIQ spike may change tool signatures (for example if plans are fixed at the first response and we need composite tools). A posts the result to B at the Monday 13:00 sync; B updates `contracts/tools.py` for UI types if needed.

---

## 11. Rebalancing: spillover lists and trim levers

### 11.1 What limits you now (replaces the old capacity check)

With AI assistants, writing code is fast for both of you. What still limits the project:

| Limit | What to do |
|---|---|
| ArmorIQ and ADK unknowns (S1 to S12) | Day-1 spike; record verified snippets in `docs/vendor_notes.md` |
| Verification of AI-written code | Reserve about 40 percent of each day for running flows and reading diffs; test-first loop (technical doc §22.4) |
| Live-model behaviour | Arena runs 3× per attack; `ScriptedLlm` for deterministic coverage |
| OpenRouter limits (20 requests/min; `:free` 50 or 1,000 per day per **account**) | Own account and $10 credit each; DEV model on `:free`; Arena, live tests, recording and hosted demo on the paid STAGE model; rate limiter and budget guard (technical doc §23) |
| Neon free plan (100 CU-hours, 0.5 GB, 10 branches per project; cold start after 5 idle minutes) | Check usage on Wed and Fri, delete stale branches, pre-warm before recordings, upgrade the one project if compute hours run low (technical doc §24.8) |
| Integration between lanes | Contracts, stubs, checkpoint merges, pairing sessions |
| Fixed clock | Thu 18:00 flag decision, Fri 12:00 hard freeze |

### 11.2 Spillover: who takes what if one lane is behind

First move **showcase** items between lanes where the interface allows it; only then touch core items.
Use this list the moment a midday sync shows one person more than half a day behind.

| If A is behind, B takes | Hours |
|---|---|
| U7 lab page (UI part), S6 limitations text, T-E results table formatting | 3 to 5 |
| M7 recipient allowlist tests (API-level), T10 and T11 cross-project API tests | 3 |
| Writing the 10 red-team prompts and hostile document variants (A reviews) | 2 |

| If B is behind, A takes | Hours |
|---|---|
| P8 rate limits and CORS, D2 (Case B fixture, hostile PDF) | 3 to 4 |
| U8 mobile layout, T-F Playwright smoke test | 4 to 5 |
| S2 diagram, governance parts of README | 2 |

### 11.3 If something is at risk

Use the flag switch-off order in `plans.md` Level 6.3 (stability and verification, not hours). **Never switch off:** live ArmorIQ, a real blocked attempt, the ledger and canary proof, the policy matrix, RLS, the README, the recording.

---

## 12. Final merge and freeze procedure (CP5 and after)

1. **Thu 18:00:** flag decision (only features with green tests stay on). **Fri 12:00:** hard feature freeze for both lanes.
2. Both merge `origin/main` into their branches, run `make test` and `make test-live`.
3. First person opens the PR and merges; the second repeats step 2 and merges.
4. Tag `rc1`. Both do a **fresh clone** into a new directory and follow the README against a **new empty Neon project** (`make migrate`, `make seed`, `make up`, `make demo`).
5. Record the demo from the merged `main`, not from a personal branch.
6. **Sat:** after any fix, repeat the fresh-clone check. Submit with a safe margin before the official UTC deadline (IST is UTC+5:30).
7. After submission, only README typo fixes. No code changes.

---

## 13. Quick pre-merge checklist (print this)

- [ ] `git merge origin/main` done on my branch, conflicts resolved there
- [ ] `make test` passes (and `make test-live` for A before CP3 onwards)
- [ ] I did not edit the other person's directories, or I told them
- [ ] `contracts/` unchanged, or agreed and logged
- [ ] No secrets, no large files
- [ ] Status message posted: what changed for the other person
- [ ] After the merge: both run `git merge origin/main`
- [ ] If I touched migrations or `db/sql/`: `make promote-schema` done after the merge, and both of us ran `make db-reset`
- [ ] My env file points at my own Neon branch, and no connection string is in the diff

---

## 14. AI-assisted working agreement (both of you)

Full protocol: `technical_project.md` §22. The rules that matter for two people in parallel:

1. **One AI session per person per branch.** Two assistants editing the same files overwrite each other silently.
2. **Shared context.** Both load the same `AGENTS.md` (trust zones, ownership, commands, never-do list). Each also loads own lane file (`AGENTS.a.md` or `AGENTS.b.md`) listing the paths that lane may edit.
3. **Ownership guard on.** `scripts/check_ownership.py` runs on pre-push and in CI. If it fails, the AI touched the other lane: revert that part or send a change request (§10).
4. **Verified snippets only.** For ArmorIQ, ADK, FastMCP and `McpToolset`, the AI copies from `docs/vendor_notes.md`, not from memory. A is the owner of that file. Re-verify when versions change.
5. **Test-first for every tool.** Contract test → implementation → policy row → conformance cell → Arena attack if risky. No tool merges without all four.
6. **Read every diff** that touches `authz`, policies, the MCP pipeline, `contracts/` or anything in `agents/`. Use the review checklist in technical doc §22.5.
7. **Small commits, small PRs.** A bad AI edit should be cheap to revert. Revert a broken `main` first, debug on the branch second.
8. **Check every new dependency** (does it exist, is it the right one, pinned, not brand new). Never paste keys into prompts.
9. **Hostile fixtures stay away from your coding assistant.** `fixtures/hostile/` is on both machines' AI ignore lists; never ask an assistant to open or summarize those files.
10. **Own your OpenRouter key.** Each person uses their own key; quota is per account, so sharing one key shares one quota. Never paste keys into prompts or the repo.
11. **Flag everything new.** Each showcase feature merges behind `FEATURE_*`. Only the Thu 18:00 decision turns flags on for the demo build.
12. **Neon URLs are secrets.** Never paste a connection string or role password into a prompt, and never let an assistant run `db-reset`, migrations or ad hoc SQL against a branch that is not yours.

---

## 15. Database workflow (Neon)

Short version of technical doc §24. Read §24 once; this section is the daily routine.

### 15.1 Who does what

| | Person A | Person B |
|---|---|---|
| One time | Creates a Neon account, accepts B's invite, creates `dev-a` from `main` at CP0, runs spike S16 | Creates the Neon project (Postgres 16, `aws-ap-southeast-1`), invites A, creates `dev-b`, shares the role passwords once through a password manager |
| Writes | `db/sql/` (roles, RLS, triggers; idempotent) | Alembic migrations, seed, `DocumentStore`, Makefile targets |
| Env file points at | `dev-a` | `dev-b` |

### 15.2 Daily commands

```bash
git merge origin/main
make migrate     # applies new migrations, then db-init
make db-reset    # only if the merge brought migrations or db/sql changes, or your data is untrustworthy
make up          # api, mcp and web as native processes; no Docker
```

### 15.3 Rules

1. **Own branch only.** Your env file points at your branch. Never reset, migrate or run SQL against the other person's branch.
2. **`main` is golden.** It holds schema, roles and seed, and receives no application runs. It changes only through `make promote-schema`.
3. **Merged a PR with migrations or `db/sql/` changes?** You run `make promote-schema`, then both of you run `git merge origin/main` and `make db-reset`.
4. **Additive migrations only until CP5.** No drops, renames or type changes.
5. **Joint sessions** (I1 Tue 17:00, I2 Wed midday, I3 Thu 15:30) run on `integ`: reset it first (`ENV_FILE=.env.integ make db-reset`), then either of you can run the stack against it. Recording on Fri uses `demo`: reset, pre-warm, rehearse, record.
6. **Reset freely.** A branch with data you do not trust is cheaper to reset than to debug.
7. **Secrets.** Connection strings live only in env files (gitignored, on the AI ignore list). Passwords travel through the password manager.
