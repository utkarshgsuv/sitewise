# Sitewise: Level-wise Plans (Team of 2, parallel build)

**Event:** ArmorIQ Flow State 2026 · **Updated:** Mon 12 Oct 2026 · **Deadline:** Sat 17 Oct 2026 (confirm exact UTC cutoff today)
**Companions:** `technical_project.md` (all technical decisions; §numbers refer to it) · `team_distribution.md` (who owns what, git workflow, seams)
**Database (updated Mon 12 Oct):** one Neon project with a golden `main` branch and one branch per person. No Docker in the dev loop (`make up` runs native processes). Details: `technical_project.md` §24 and `team_distribution.md` §15.

**Two people, called Person A and Person B throughout.**
- **Person A = Governance and Agents lead:** ArmorIQ, Google ADK agents, MCP tool server, policies, ledger and audit, security tests, red-team.
- **Person B = Platform and Product lead:** schema, API, auth, ingestion and extraction, approvals API, frontend, fixtures, README and demo packaging.

Every task below carries an **Owner** (A, B or Both). The two lanes are designed so each of you can work all day without waiting for the other, using agreed **contracts** and **stubs** (Level 2.3).

| Level | Question it answers |
|---|---|
| 0 | What are we trying to achieve and what counts as winning? |
| 1 | What are the milestones, exit gates and merge checkpoints? |
| 2 | Which workstreams exist, who owns them, and where do the two lanes meet? |
| 3 | What does each person do each day? |
| 4 | What are the concrete tasks, owners and acceptance criteria? |
| 5 | How do we know each stage is truly done (gates, demo, submission)? |
| 6 | What if a risk hits? What gets cut, in what order? |
| 7 | What happens after the hackathon? |

**Assumption:** the build starts today (Mon 12 Oct). The brief's Sunday scaffold day is merged into today. If either of you already did some of it, bank the time as buffer for Thu and Fri.

**Build method (updated):** both of you build with AI coding assistants, so typing speed is not the constraint and the plan targets the **best version possible**, not the minimum. What stays slow is verification, the ArmorIQ unknowns, live-model behaviour, integration and the fixed clock. The plan is organized around those (see Level 4C and `technical_project.md` §22). The core demo is protected by a stability rule (Level 0.7).


---

## Level 0: North Star

### 0.1 Goal
Build **Sitewise**, a governed AI project desk where a Google ADK agent turns a site discrepancy report into an evidence-backed issue, task and supplier draft, and where **ArmorIQ stops the agent from crossing its authority boundary before any side effect happens**.

### 0.2 What the judges must see
1. **Useful work:** "100 bags ordered, 92 counted" → agent reads the PO, compares, creates an issue, assigns a task, drafts a supplier message.
2. **Boundary holding:** a hostile instruction makes the agent *really attempt* a forbidden action → ArmorIQ blocks it → audit pane shows `BLOCK`, `executed = no`, canary table empty.

### 0.3 Definition of Done (whole project)
- [ ] Happy path runs end to end with **live ArmorIQ** and a **live OpenRouter-served model** (STAGE tier).
- [ ] At least one forbidden action genuinely attempted by the agent and blocked or held before execution.
- [ ] Audit pane shows actor, proposed action, decision, reason, executed yes/no.
- [ ] Independent proof: ArmorIQ trace plus MCP ledger (no row) plus canary table (empty).
- [ ] Test matrix T01 to T20 passes (live tests included).
- [ ] README with architecture, setup, policies, limitations and the recorded demo.
- [ ] Both branches merged to `main`, fresh-clone setup verified, submitted before the official UTC deadline.

### 0.4 Non-negotiables
- No fake tool calls in the recording. No mock governance in the final demo.
- Synthetic data only. No real payments, suppliers or credentials.
- Agents never decide identity, approvals or completion.
- One workflow. New ideas go to the Level 7 parking lot.
- **No one edits the other person's directories without telling them** (team_distribution.md §3).

### 0.5 Priority tiers

| Tier | Meaning | Examples |
|---|---|---|
| **Core** (every P0 and P1 in Level 4) | Required. The submission stands on this. | Happy path, boundary demo, hold and two-key approval, Case B, cross-project, idempotency, lab page, mobile layout, Playwright, recording |
| **Showcase** (X1 to X16 in Level 4B) | We build these. Each sits behind a feature flag and is enabled in the demo only when its tests are green. | Attack Arena, policy matrix, tamper-evident ledger, RLS, supplier reply loop, RFI scenario, digest, Hindi and voice, evidence pack, replay, hosted demo, PWA |
| **Stretch** (X17, X18, X14, P2 items) | Only if everything above is stable. | Quote comparison, WhatsApp sandbox, ADK multi-agent composition, `FollowUpAgent` extras |

With AI-assisted building, treat **all P1 items as required** and P2 items as Showcase or Stretch.

### 0.6 Demo story split
Person B tells the **first half** (problem, upload, extraction, issue, approval screen). Person A tells the **second half** (hostile document, real attempt, ArmorIQ block, audit, canary). Both know the whole flow.

### 0.7 Best-version scope and the stability rule

Every extra feature must strengthen one of three claims:

| Claim | What the judge should conclude |
|---|---|
| **Useful** | A contractor's real work gets easier, end to end, including supplier replies, RFIs, languages and voice. |
| **Governed** | The agent provably cannot exceed its authority: ArmorIQ plus tool validation plus database isolation, and every attack is covered. |
| **Provable** | Anyone can verify the claims: Arena report, policy matrix, ledger chain, replay, evidence pack. |

**Stability rule (this is what protects the demo):**
1. The core demo is flawless before any showcase feature is enabled in the demo build.
2. Every showcase feature is behind a `FEATURE_*` flag. **Thu 18:00:** enable only the flags whose tests are green.
3. A new tool always arrives with a policy row, a conformance-matrix cell, contract tests and (if risky) an Arena attack. No tool, no merge.
4. No breaking contract changes after Wed evening.

**Extended Definition of Done**
- [ ] Arena report: every attack run 3 times live with `executed = 0` and canary unchanged, on **at least two different models**.
- [ ] Policy matrix verified live for all personas and tools.
- [ ] Ledger chain verifies; evidence pack shows the chain head.
- [ ] RLS test shows zero cross-project rows even from raw SQL.
- [ ] Hosted demo reachable (or deliberately switched off with the local path documented).

---

## Level 1: Milestones and Merge Checkpoints

AI-assisted building lets you compress the core and spend the saved time on showcase features and verification.

| ID | Milestone | Target | Exit gate | Merge checkpoint |
|---|---|---|---|---|
| **M0** | Spikes done (A) and schema pushed (B) | Mon 12 Oct, ~13:00 | A: ArmorIQ plus ADK hello-world shows ALLOW, HOLD (released in console), BLOCK; S1 to S15 answered or scheduled; **DEV and STAGE models chosen by qualification** (technical doc §23.7). B: Neon project and branches created, schema, models and contracts on `main`; VISION model chosen. A: S16 (Neon roles, RLS, latency) answered. | **CP0:** B's schema and `contracts/` on `main` and promoted to Neon `main` (`make promote-schema`); A creates `dev-a` from it and merges `main` |
| **M1** | Skeleton, data, auth, AI context | Mon EOD | `make up` runs everything (native processes against your own Neon branch, no Docker). Seed loads. Persona login works. Upload stores a file (a `document_blobs` row). `AGENTS.md`, `OWNERSHIP.yaml` and the ownership guard are in place. | **CP1:** both merge |
| **M2** | Governed happy path | Tue, after the integration session | Extraction → confirm → investigate → record works with ArmorIQ **ON** through the real API. Ledger rows written. | **CP2:** Tue EOD |
| **M3** | Core complete | Wed midday | One real BLOCK and one real HOLD. Per-persona policies. Two-key send works. Audit pane v1. RLS on. | (no separate merge) |
| **M3b** | Showcase wave 1 | Wed EOD | Ledger chain, policy matrix, supplier portal loop, evidence pack, Mailpit channel, Case B, mobile layout. | **CP3:** Wed EOD |
| **M4** | Showcase wave 2 and hardening | Thu EOD | Arena (15+ attacks × 3 live runs), RFI, digest, Hindi and voice, replay, hosted demo working, T01 to T38 results table. **Flag decision at 18:00.** | **CP4:** Thu EOD |
| **M5** | Demo-ready | Fri EOD (hard freeze 12:00) | Polish, README, recording reviewed by an outsider, fresh-clone and hosted smoke tests. | **CP5:** final merge, tag `rc1` |
| **M6** | Submitted | Sat 17 Oct, target before midday IST | Fresh-clone test, tests re-run, submission fields verified. | Fixes only, on `main` by agreement |

**Rules:** `main` is demo-able at the end of every day. Merge at every checkpoint, then both merge `main` back into their branches. Showcase features land disabled; flags are decided on Thursday at 18:00.

---

## Level 2: Workstreams, Owners and Seams

### 2.1 Workstreams

| WS | Name | Owner | Main output |
|---|---|---|---|
| WS0 | Contracts and repo skeleton | **Both** (kickoff, ~90 min) | `contracts/` package, repo, branches, CI, `.env.example` |
| WS1 | Platform: Neon DB, auth, authz, API, SSE, uploads | **B** | Running api against Neon, `authz.py` |
| WS2 | Data and domain: fixtures, seed, state machine, approval hashing | **B** | Seed, fixtures, `domain/state.py`, `domain/approvals.py` |
| WS3 | Ingestion and extraction | **B** | Source-linked, confidence-scored facts plus confirmation flow |
| WS7a | Frontend: login, intake, review, issue, approvals | **B** | Main product UI |
| WS9a | README, diagram, packaging | **B** (A contributes governance sections) | README and diagram |
| WS6 | ArmorIQ governance | **A** | Spike results, wiring, policies, fail-closed |
| WS5 | MCP tool server | **A** | All tools, canary, idempotency, ledger writes |
| WS4 | ADK agents and orchestrator | **A** | Stage agents, circuit breaker, attempt logging |
| WS2b | Comparison engine, DB roles, RLS and triggers | **A** | `domain/compare.py`, `db/sql/*.sql` |
| WS7b | Frontend: audit pane, lab page | **A** | `/audit`, `/lab` |
| WS8 | Testing and red-team | **A** (governance tests) and **B** (extraction, e2e, API) | Test matrix T01 to T20 |
| WS9b | Demo script, recording, submission | **Both** | Video, checklist, submission |

### 2.1b Showcase workstreams (best-version scope)

| WS | Name | Owner | Main output |
|---|---|---|---|
| WS10 | Governance showcase: X1 Arena, X2 policy matrix, X3 ledger chain, X9 RLS, X10 replay, X14, X17 | **A** | `/arena`, `/policy`, `/replay`, chain verify, RLS policies |
| WS11 | Workflow showcase (agent side): X5 evidence stage, X6 RFI tools and retrieval, X7 FollowUpAgent | **A** | New agents and tools, each with policy rows and tests |
| WS12 | Product showcase: X4 evidence pack, X5 supplier portal, X6 spec ingestion and RFI UI, X7 digest UI, X8 Hindi and voice, X12 PWA, X13 email channel | **B** | The extra user-facing features |
| WS13 | Delivery: X11 hosted demo, X15 extraction eval, X18 sandbox | **B** (A supports with ArmorIQ and MCP hosting) | Public demo URL, eval report |
| WS14 | AI-assisted process: AI1 to AI4 | **Both** | `AGENTS.md`, ownership guard, verified-snippet registry |

### 2.2 Who is on the critical path
- **A:** ArmorIQ spike (Mon) → tools and stage agents (Tue) → policies and holds (Wed) → real attack (Thu). A's lane is the riskiest because of the unknowns in S3, S4, S7.
- **B:** schema (Mon) → extraction and API (Tue) → approvals and issue UI (Wed). B's lane is more predictable but larger in UI work.
- **Interdependence is deliberately small** and handled by contracts and stubs, not by waiting.

### 2.3 Seams: where the lanes meet, and the stub that removes waiting

| # | Seam | Producer → Consumer | Contract form | Stub so the consumer is never blocked | Due |
|---|---|---|---|---|---|
| 1 | DB schema and models | B → A | SQLAlchemy models plus Alembic | A codes pure logic first; builds tools after CP0 | Mon 13:00 |
| 2 | `authz.authorize(actor, action, resource)` | B → A (MCP) | Function signature in `contracts/` | Stub that implements the permission matrix in memory | Mon 13:00 stub, Tue real |
| 3 | `RunService.start_run(...)` plus `RunEvent` stream | A → B (API/SSE) | Protocol in `contracts/` | B uses `FakeRunService` that replays canned events | Tue morning (stub), Tue EOD (real) |
| 4 | `EventBus.publish(run_id, event)` | B → A (orchestrator) | Protocol | A uses an in-memory list bus in tests | Tue |
| 5 | Confirmed facts (`FactsRepository`) | B → A (stage input) | Protocol plus `ExtractionResult` model | A uses fixture JSON for Case A facts | Tue |
| 6 | Approvals: table, `payload_hash(draft)` | B → A (MCP send tool) | Table columns plus function in `domain/approvals.py` | A tests the send tool with a hand-inserted approval row | Wed morning |
| 7 | Audit data (`agent_tool_attempts`, `action_ledger`) | A → B/UI | Tables plus `/audit` router (A-owned file) | A owns the whole chain; B only links the nav | Wed |
| 8 | Run-context JWT | A → A | Mint in agents, verify in MCP | Internal to A | n/a |
| 9 | Seed and fixtures | B → A | `seed/` modules, fixed UUIDs in `contracts/` | A adds `seed/a_governance.py` (auto-loaded) | Mon EOD |
| 9a | Document bytes | B (`DocumentStore`, `document_blobs`) → A (`read_document`) | Protocol in `contracts/protocols.py` (add at kickoff) | `InMemoryDocumentStore` in `tests/` | Mon 13:00 (protocol), Tue (real) |
| 9b | Neon project, branches, role passwords | B → A | Variable names in `.env.example`; rules in technical doc §24 | None needed before CP0 (spike and comparison engine are pure code), then branch `dev-a` | Mon 13:00 |

### 2.4 New seams for the showcase features

| # | Seam | Producer → Consumer | Contract | Stub |
|---|---|---|---|---|
| 10 | Supplier replies | B (portal, `supplier_replies`, tokens) → A (`attach_supplier_evidence`) | Table plus models in `contracts/tools.py` | A inserts a reply row by hand |
| 11 | Spec chunks | B (ingestion, embeddings) → A (`search_project_specs`) | `spec_chunks` table | A seeds a few chunks (keyword fallback) |
| 12 | Chain verification | A (`verify_chain(project_id)`) → B (evidence pack, UI badge) | Protocol in `contracts/protocols.py` | Stub returns `valid` |
| 13 | Digest | A (`Digest` model) → B (UI, TTS) | Pydantic model in `contracts/` | Fixture JSON |
| 14 | Language | B (`lang`) → A (agent output language) | Optional `lang` claim in run-context (**add at kickoff, additive**) | Default `en` |
| 15 | Hosting | B ↔ A | Env var list, MCP URL, ArmorIQ constraints from S4 | n/a |

---

## Level 3: Day-by-Day Plan (two lanes, AI-accelerated)

"Together" blocks are the scheduled pairing sessions. Everything else runs in parallel. Plan **about 40 percent of every day for verification** (running flows, reading AI-written diffs, tuning prompts), not only for generating code.

### Mon 12 Oct: Kickoff, spike, skeleton (M0, M1)
| Block | Person A (Governance and Agents) | Person B (Platform and Product) | Together |
|---|---|---|---|
| 09:00 to 10:30 | n/a | n/a | **Kickoff:** repo, branches, freeze `contracts/` (include the `lang` claim), keys (ArmorIQ for A; **each of you creates an OpenRouter account and buys the one-time $10 credit**, technical doc §23); **Neon:** B creates the project (Postgres 16, region `aws-ap-southeast-1`), invites A as collaborator, creates `dev-b`, and shares the role passwords once through a password manager (technical doc §24); add `DocumentStore` to the frozen `contracts/protocols.py`; **AI1 to AI3:** `AGENTS.md`, `OWNERSHIP.yaml` plus guard, `vendor_notes.md` skeleton |
| Morning | **G1 to G4, S11 to S16:** ArmorIQ install, hello-world FastMCP (allow / hold / block) under ADK **with `LiteLlm` and OpenRouter**, answer S1 to S16 (S16 is the 30-minute Neon check, technical doc §24.9); **L1 to L3:** model factory, model qualification (afternoon), rate limiter. Record **verified snippets** in `vendor_notes.md` | **P1, P2, N1, N2:** Neon branches, Makefile plus `Procfile.dev` (native `make up`), schema, models, Alembic, `DocumentStore` (Mailpit and Jaeger are optional binaries via `make tools`); **L4:** PDF-to-image rasterization and vision qualification (afternoon) | n/a |
| ~13:00 | **M0 report** to B (anything changing tool signatures?) | **CP0:** schema, models and contracts on `main` | 10-minute sync |
| Afternoon | **D4** comparison engine, **M1** MCP skeleton plus run-token middleware, **P3** DB roles (created by SQL), triggers and **RLS policies (X9)** in `db/sql/`, idempotent, run by `make db-init` | **P4** auth, **P5** `authz.py`, **P6** upload, **D1, D2, D3** fixtures (Case A, Case B, hostile PDF, Project B quotes) and seed | n/a |
| Evening | **C3** fixture facts for A's stage input | **U1** shell and login, **C2** `FakeRunService` | **CP1:** both merge, `make up` on a clean clone against your own Neon branch, tag `m1` |

### Tue 13 Oct: Governed happy path (M2)
| Block | Person A | Person B | Together |
|---|---|---|---|
| Morning | **M2, M3** MCP pipeline plus read and compute tools, **G6** `run_stage()` | **E1, E2, E3** extraction (text layer, vision agent, cross-check), **P7** runs endpoint and SSE with the fake service | n/a |
| Early afternoon | **A1 to A4** prompts, stage agents, orchestrator, attempt logger, **M4** write tools | **E4** confirmation API, **D5, D6** state machine and approval hashing, **U2, U3** intake timeline and extraction review | n/a |
| 17:00 | n/a | n/a | **Integration session (I1, 90 min):** swap `FakeRunService` for the real orchestrator, Case A with ArmorIQ ON |
| Evening | **G7** per-persona policies, **M6** forbidden stubs plus canary, **A5** circuit breaker, **G8** fail-closed and startup guard | **U4** issue detail, approvals API (approve, reject), resolve endpoint (human-only), outbox | **CP2** merge, tag `m2` |

### Wed 14 Oct: Core complete, showcase wave 1 (M3, M3b)
| Block | Person A | Person B | Together |
|---|---|---|---|
| Morning | **M5** send tools, **U6** audit pane, **A6** `ScriptedLlm`, **T-B1**, **T24** RLS test | **U5** approvals screen, **E5** Case B flow, **U8** mobile layout, i18n scaffolding | n/a |
| Midday | n/a | n/a | **Approvals seam (I2, 60 min):** two-key send end to end. **M3 gate** |
| Afternoon | **X3** hash-chained ledger plus verify endpoint, **X2** policy matrix and live test, **X5 (agent side)** `EvidenceAgent`, `attach_supplier_evidence`, `request_site_confirmation` | **X5 (portal)** supplier portal and tokens, **X13** Mailpit channel, **X4** evidence pack PDF (against the chain-verify stub) | n/a |
| Evening | **T22, T23, T26, T27** | **T25, T33** | **CP3** merge, tag `m3` (M3b) |

### Thu 15 Oct: Showcase wave 2 and hardening (M4)
| Block | Person A | Person B | Together |
|---|---|---|---|
| Morning | **X1** Arena catalogue (15+ attacks) and runner, **T-C, T-D1** | **X6 (ingestion)** spec chunks, embeddings, pgvector, RFI UI, **X8** Hindi UI and drafts with back-translation | n/a |
| Afternoon | **X6 (tools)** `search_project_specs`, `draft_rfi`, `send_rfi`, **X7** `FollowUpAgent`, **X10** run replay page, Arena `/arena` page | **X8** voice notes and TTS digest, **X15** extraction eval harness, **X11** hosted deploy (VM, Caddy, `hosted` Neon branch, budget cap), **T-F** Playwright | n/a |
| 15:30 to 17:00 | n/a | n/a | **Red-team and Arena session (I3):** live Arena runs, tune hostile documents until the model really attempts forbidden calls, capture traces |
| 18:00 | n/a | n/a | **Flag decision:** enable only features whose tests are green. **CP4** merge, tag `m4`, data model frozen |

### Fri 16 Oct: Stabilize, polish, record (M5)
| Block | Person A | Person B | Together |
|---|---|---|---|
| Morning (to 12:00) | Final Arena run and report, rerun policy matrix, **X16** property tests (own modules), **X17** and **X14** only if stable, **S6** limitations | Hosted demo smoke test, **X12** PWA, **X16** property tests (own modules), README, diagram, polish | **Hard feature freeze 12:00** |
| Afternoon | `docs/governance.md`, `docs/arena_report.md`, trace links (**G9**) | README final, fresh-clone test, hosted demo reset script | **Rehearsal and recording (S3, S4)** from merged `main` |
| Evening | n/a | n/a | **CP5** final merge, tag `rc1`, outsider follows README |

### Sat 17 Oct: Buffer and submit (M6)
| Block | Person A | Person B | Together |
|---|---|---|---|
| Morning | Rerun `make test-live`, confirm the recording shows live ArmorIQ | Fresh-clone setup after the last commit, hosted demo check | n/a |
| Midday | n/a | n/a | **S5** verify submission fields and the UTC deadline (IST is UTC+5:30), **submit** |

**Daily rituals:** 15-minute standup, 10-minute midday sync, two-line end-of-day status (done, blocked, tomorrow, what changed for you). Merge `main` into your branch every morning, then `make migrate` (or `make db-reset` if the merge brought migrations or `db/sql/` changes). Details in `team_distribution.md` §8, §14 and §15.

---

## Level 4: Task Backlog (with owners)

Estimates here are human-pace ideal hours; with AI assistance treat them as upper bounds and read Levels 4B and 4C for the extended scope. IDs go in commit messages (e.g. `G6: run_stage with fresh agent`).

### WS0: Contracts and repo (Both)
| ID | Pri | Task | Owner | Est | Acceptance |
|---|---|---|---|---|---|
| C1 | P0 | Kickoff: repo, branches, CI skeleton, `contracts/` package frozen (team_distribution.md §6), ports and env agreed | Both | 1.5 each | `contracts/` on `main`; both can run an empty `make up` |

### WS6: ArmorIQ (A)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| G1 | P0 | ArmorIQ account and key; install SDK with `google-adk` extra | 1 | `import ArmorIQADK` works; key only in `.env` |
| G2 | P0 | Hello-world: FastMCP with `ok_tool`, `hold_tool`, `block_tool` under an ADK agent with scope | 3 | ALLOW, HOLD released in console, BLOCK observed |
| G3 | P0 | S3: plan semantics with a dependent-call repro | 2 | Written answer; design fallback chosen |
| G4 | P0 | S4 to S7: proxy vs callback, mapping, callback coexistence, headers | 3 | Each answered with evidence |
| G5 | P1 | S8 to S10: policies, HOLD timeout, latency | 2 | Documented |
| G6 | P0 | `run_stage()` per §8.3, fresh agent per run | 3 | Runs under scope; uninstall in `finally` |
| G7 | P0 | Per-persona policies in console plus mirror in `policies/` | 2 | Repo table equals console |
| G8 | P0 | Fail-closed behaviour, startup guard, governance badge signal | 2 | T20 passes; demo mode refuses mock |
| G9 | P1 | Trace link capture in `agent_tool_attempts` | 2 | Audit row links to ArmorIQ trace |

### WS5: MCP tool server (A)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| M1 | P0 | FastMCP app, streamable HTTP, run-token middleware | 3 | Missing or expired token refused |
| M2 | P0 | Standard execution pipeline (§9.2) as helper | 3 | Used by every tool |
| M3 | P0 | Read and compute tools | 4 | Contract tests incl. wrong project |
| M4 | P0 | `create_issue`, `assign_task`, `draft_supplier_message`, `notify_manager` | 5 | Idempotent; ledger row in same transaction |
| M5 | P0 | `request_supplier_send`, `send_supplier_message` (simulated outbox) | 4 | Needs valid approval; atomic consume |
| M6 | P0 | Forbidden stubs plus canary, flag-gated exposure | 2 | Canary empty after denial |
| M7 | P1 | Recipient allowlist and lookalike test | 1 | T15 passes |

### WS4: ADK agents (A)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| A1 | P0 | Prompts (shared rules §8.5) for investigator and recorder | 3 | Prompt hashes stored |
| A2 | P0 | `InvestigatorAgent`, `RecorderAgent` with tool filters | 4 | Normal mode exposes only stage tools |
| A3 | P0 | Orchestrator implementing `RunService`; pause and resume | 4 | Pauses on clarification, resumes after confirm |
| A4 | P0 | Attempt-logger plugin writing via `runtime/` repo | 3 | Every tool attempt has a row |
| A5 | P0 | Circuit breaker after BLOCK | 2 | T17 passes |
| A6 | P1 | `ScriptedLlm` for deterministic tests | 3 | CI drives tool calls without a live model |
| A7 | P2 | `FollowUpAgent` digest | 3 | Only if P0 and P1 are done |

### WS2b and WS7b: A's domain, SQL and UI pieces
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| D4 | P0 | Comparison engine plus unit map (`domain/compare.py`, pure Python) | 3 | 100 vs 92 gives an 8-bag discrepancy; unit mismatch gives clarification |
| P3 | P0 | DB roles `app_rw` and `mcp_rw` (created with SQL as NOBYPASSRLS, never in the Neon console), append-only triggers and RLS in `db/sql/`, idempotent, run by `make db-init` | 3 | `mcp_rw` cannot UPDATE ledger; triggers reject UPDATE/DELETE; a second `db-init` changes nothing |
| U6 | P0 | Audit pane and `/audit` router (§12.2) | 4 | Executed yes/no comes from the ledger |
| U7 | P1 | Lab page for hostile documents; governance badge | 3 | Runs adversarial flow |

### WS1: Platform (B)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| P1 | P0 | Repo, Makefile and `Procfile.dev` (native `make up`, no Docker), `.env.example`, pre-commit with gitleaks (plus a rule for `postgres://user:password@host` URLs) | 3 | `make up` from clean clone against your own Neon branch |
| P2 | P0 | Schema, models, migrations per §6.2 (including `document_blobs`); additive-only after CP0 | 4 | Migrations apply on Neon; constraints present |
| P4 | P0 | Demo auth, JWT cookie, `/me`, membership lookups | 3 | Roles from DB, never from token |
| P5 | P0 | `authz.py` with the permission matrix as data | 3 | Unit tests per role and action |
| P6 | P0 | Upload endpoint with validation, `DocumentStore` (Postgres blobs), sha256 | 3 | Rejects wrong type and oversize |
| P7 | P0 | Runs endpoint and SSE (calls `RunService`) | 3 | Events stream to a test client |
| P8 | P1 | Rate limits, CORS lock, structured logging | 2 | Config present |
| C2 | P0 | `FakeRunService` and canned SSE events for UI development | 2 | UI runs without A's orchestrator |

### WS2: Data and domain (B)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| D1 | P0 | Fixture generator: PO, challan, invoice, Case A | 3 | Reproducible files |
| D2 | P1 | Case B blurry challan, hostile PDF, Project B quotes | 2 | Files exist and are used by tests |
| D3 | P0 | Seed script (auto-loads `seed/*.py`), fixtures loaded as blobs, run against `main` by `promote-schema` | 2 | `make seed` repeatable and under 10 s; `make db-reset` back to golden state in under a minute |
| D5 | P0 | State machine with transition table (`domain/state.py`) | 2 | Illegal transitions rejected |
| D6 | P0 | Payload hashing and approval service (`domain/approvals.py`) | 3 | Edit changes hash and invalidates approval |

### WS3: Extraction (B)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| E1 | P0 | PDF text-layer extraction with page references | 3 | Fields with page numbers |
| E2 | P0 | `ExtractionAgent` (no tools, JSON validated by Pydantic with one repair retry; no reliance on ADK `output_schema`) | 4 | Returns a valid `ExtractionResult` for image and PDF |
| E3 | P0 | Cross-check, confidence rules, critical-field gate | 3 | Image-sourced numbers always need confirmation |
| E4 | P0 | Confirmation API and persistence (`FactsRepository`) | 2 | Only confirmed facts feed stages |
| E5 | P1 | Case B path ends in NEEDS_CLARIFICATION | 2 | T05 passes |

### WS7a: Frontend (B)
| ID | Pri | Task | Est | Acceptance |
|---|---|---|---|---|
| U1 | P0 | Next.js shell, login persona picker, typed API client, nav with placeholders for `/audit` and `/lab` | 3 | Login for every persona |
| U2 | P0 | Project page: intake, upload, run timeline | 5 | Live SSE events |
| U3 | P0 | Extraction review with source and confirm | 4 | Uncertainty is clearly visible |
| U4 | P0 | Issue detail (evidence pack, comparison table, draft, state) | 4 | Sources shown per fact |
| U5 | P0 | Approvals screen with exact payload and approvals API | 3 | Recipient, project and final text shown |
| U8 | P1 | Mobile-friendly layout | 2 | Usable at phone width |
| U9 | P2 | Voice note (ElevenLabs) | 4 | Never at the cost of P0 and P1 |

### WS8: Testing
| ID | Pri | Task | Owner | Est | Acceptance |
|---|---|---|---|---|---|
| T-A | P0 | Test harness, fixtures, markers (`live`, `redteam`) | B (A adds markers) | 2 | `make test` runs |
| T-B1 | P0 | T01 to T04, T07 | A | 3 | Green |
| T-B2 | P0 | T05, T06 | B | 1 | Green |
| T-C | P0 | T08 to T13 (injection, cross-project, PO, plan) | A | 5 | Green incl. live |
| T-D1 | P0 | T14 to T17, T19, T20 | A | 4 | Green |
| T-D2 | P0 | T18 (human-only resolve) | B | 1 | Green |
| T-E | P1 | 10-prompt red-team set and results table | A | 3 | Table in README |
| T-F | P1 | Playwright smoke test | B | 3 | Full flow passes |

### WS9: Demo and submission
| ID | Pri | Task | Owner | Est | Acceptance |
|---|---|---|---|---|---|
| S1 | P0 | README: architecture, setup, tool surface, policies, limitations | B (A writes governance sections) | 4 | Fresh-clone review passes |
| S2 | P0 | Architecture diagram (from §2.1) | B | 1 | In README |
| S3 | P0 | 3-minute script plus rehearsal | Both | 1 each | Timed under 3:00 |
| S4 | P0 | Recording: real attempt, real block, trace plus ledger plus canary | Both | 2 each | Reviewed by an outsider |
| S5 | P0 | Submission checklist and final verification | Both | 1 each | All boxes ticked |
| S6 | P1 | Honest limitations (adversarial flags, simulated send) | A | 1 | Present in README |

### WS-LLM: LLM access (OpenRouter through ADK `LiteLlm`)

| ID | Pri | Task | Owner | Size | Acceptance |
|---|---|---|---|---|---|
| L1 | P0 | `agents/model_factory.py`: tiers (DEV, STAGE, VISION), provider switch, OpenRouter preferences, model id recorded per run | A | S | One agent runs on OpenRouter and on Gemini by changing env only |
| L2 | P0 | `make model-qualify`: tool-call validity, stop-after-BLOCK, loop cap, JSON validity, latency, cost; run on 3 DEV and 3 STAGE candidates | A | M | Report committed; DEV and STAGE models chosen and logged in `docs/decisions.md` |
| L3 | P0 | `agents/llm_guard.py`: RPM token bucket, concurrency limit, backoff (max 3), 402 handling, daily counter | A | S | 429 and 402 produce clear run events; no retry storms |
| L4 | P0 | PDF-to-image rasterization, vision qualification on fixtures, JSON validate-and-repair wrapper for extraction | B | M | VISION model chosen; false-accept after confirmation gate is 0 |
| L5 | P1 | Arena runs on two different models; report shows model id per run | A | S | `executed = 0` on both |
| L6 | P1 | Separate OpenRouter key and spending limit for the hosted demo, wired to `LLM_DAILY_BUDGET` | B | S | Budget cap enforced (T34) |
| L7 | P1 | Embeddings through OpenRouter or LiteLLM; STT choice (ElevenLabs or audio-capable model) | B | S | Spike S15 answered; X6 and X8 unblocked |

### WS-DB: Neon (shared cloud Postgres, technical doc §24)

| ID | Pri | Task | Owner | Size | Acceptance |
|---|---|---|---|---|---|
| N1 | P0 | Create the Neon project (Postgres 16, `aws-ap-southeast-1`), invite A, create `dev-b` (then `dev-a` at CP0); `.env.example` variables; role passwords shared via a password manager | B | S | Both can run `make up` against their own branch; no secrets in the repo |
| N2 | P0 | Makefile targets `migrate`, `db-init`, `db-reset`, `promote-schema` with the branch-name and host guards; `PgDocumentStore` and `InMemoryDocumentStore` | B | M | `db-reset` refuses `main` and mismatched hosts; a branch returns to golden state in under a minute |
| N3 | P0 | Spike S16: SQL-created roles obey forced RLS, `SET LOCAL`, pgvector, branch reset keeps roles, latency from Bengaluru | A | S | Results in `docs/spike_results.md`; any failure becomes a change request the same day |
| N4 | P1 | CI: short-lived Neon branch per run for contract and integration tests | B | S | CI green; branches deleted after each run |
| N5 | P1 | README "Bring your own database" section (free Neon project or any Postgres 16 with pgvector); fresh-clone path on a throwaway Neon project | B | S | An outsider follows it end to end (M5) |

### Integration tasks (Both)
| ID | Pri | Task | When | Acceptance |
|---|---|---|---|---|
| I1 | P0 | Swap `FakeRunService` for the real orchestrator; run Case A | Tue evening | M2 gate |
| I2 | P0 | Two-key send across A's MCP tools and B's approval API | Wed midday | M3 gate |
| I3 | P0 | Joint red-team session on the live agent | Thu afternoon | M4 gate |
| I4 | P0 | Merge checkpoints CP0 to CP5 (team_distribution.md §7) | see Level 1 | `main` green after each |

### Level 4B: Showcase and stretch backlog (best-version scope)

Size: S under half a day, M about a day, L more than a day (with AI assistance). Every item merges behind its flag and brings its own tests (see `technical_project.md` §21.17).

| ID | Feature | Owner | Size | Flag | Acceptance |
|---|---|---|---|---|---|
| X1 | **Attack Arena:** catalogue of 15+ attacks, runner (3 live runs each), `/arena`, auto-generated `arena_report.md` | A | L | `FEATURE_ARENA` | T21: `executed = 0`, canary unchanged |
| X2 | **Policy conformance matrix** and `/policy` page | A | M | on | T22: every persona × tool cell matches |
| X3 | **Tamper-evident ledger:** hash chain, `verify_chain`, audit badge | A | M | `FEATURE_CHAIN` | T23 |
| X9 | **Row-Level Security** on all project tables | A | M | on | T24 |
| X10 | **Replay page** plus OpenTelemetry to Jaeger | A | M | `FEATURE_REPLAY` | Any past run steps through call, decision, result, ledger row |
| X5a | **Evidence stage:** `EvidenceAgent`, `attach_supplier_evidence`, `request_site_confirmation` | A | M | `FEATURE_PORTAL` | T26, T27 |
| X6a | **RFI tools:** `search_project_specs`, `draft_rfi`, `send_rfi` (HOLD) | A | M | `FEATURE_RFI` | T27, T28, T29 |
| X7a | **FollowUpAgent:** digest and `draft_reminder` | A | M | `FEATURE_DIGEST` | T30 |
| X14 | **ADK multi-agent composition** (only if S11 is positive) | A | M | `FEATURE_MULTIAGENT` | Enforcement unchanged, tests green |
| X17 | **Quote comparison** with need-to-know | A | M | `FEATURE_QUOTES` | T38 |
| X16a | **Property tests** for `compare`, tools, hashing of ledger | A | S | tests | T36 |
| X4 | **Evidence pack PDF** | B | M | `FEATURE_EVIDENCE` | T33 |
| X5b | **Supplier portal** (token, upload, reply) and UI | B | M | `FEATURE_PORTAL` | T25 |
| X6b | **Spec ingestion**, embeddings, pgvector, RFI issue UI | B | L | `FEATURE_RFI` | T28 |
| X7b | **Digest UI** and optional spoken digest | B | S | `FEATURE_DIGEST` | Digest displays and plays |
| X8 | **Hindi/English** UI and drafts with back-translation, **voice notes** (STT), TTS digest | B | L | `FEATURE_HI`, `FEATURE_VOICE` | T31, T32 |
| X11 | **Hosted demo:** VM with native processes (Compose only if deploy-only), Caddy, `hosted` Neon branch, rate limits, budget cap, reset, kill switch | B | L | n/a | T34 |
| X12 | **PWA** with offline capture queue | B | M | `FEATURE_PWA` | T35 |
| X13 | **Email channel to Mailpit** | B | S | `FEATURE_EMAIL` | Approved message arrives in the local sink only |
| X15 | **Extraction evaluation** with 30 labelled synthetic documents | B | M | tests | T37 |
| X16b | **Property tests** for `authz`, state machine, approval hashing | B | S | tests | T36 |
| X18 | **WhatsApp sandbox** to a team-owned number | B | M | `FEATURE_WA_SANDBOX` | Allowlist enforced; never a supplier |

### Level 4C: AI-assisted process tasks (Both)

| ID | Pri | Task | Owner | Acceptance |
|---|---|---|---|---|
| AI1 | P0 | `AGENTS.md` (trust zones, ownership, commands, never-do list), `AGENTS.a.md`, `AGENTS.b.md` | Both (Mon kickoff) | Both AI sessions load the same constraints |
| AI2 | P0 | `OWNERSHIP.yaml` plus `scripts/check_ownership.py` in pre-push and CI | Both | Guard fails when a branch touches the other lane |
| AI3 | P0 | `docs/vendor_notes.md`: verified ArmorIQ and ADK snippets with versions and dates | A | AI copies from here, not memory |
| AI4 | P1 | Add `fixtures/hostile/` to AI-tool ignore lists | Both | Confirmed on both machines |

### Where the time goes (with AI assistance)

| Activity | Speed with AI | Plan for |
|---|---|---|
| Writing endpoints, UI, tools, tests | Fast | Run the code and read every diff |
| ArmorIQ and ADK unknowns | **Not faster** (facts, not code) | Day-1 spike, verified-snippet registry |
| AI inventing SDK calls | Risk | Never trust memory for SDK APIs |
| Live-model attack behaviour | **Not faster** (nondeterministic) | Arena 3× per attack, `ScriptedLlm` for coverage |
| Integration of two lanes | Moderate | Contracts, stubs, checkpoint merges |
| Hosted demo, keys, recording | Fixed clock | Start Thursday, rehearse Friday |

---

## Level 5: Quality Gates, Demo and Submission

### 5.1 Gate checklists
**M0 (A and B):** A: hello-world shows ALLOW, HOLD, BLOCK; spike answers recorded; stage-scope design confirmed. B: schema, models, contracts on `main`.
**M1:** `make up` from a clean clone against your own Neon branch · seed loads · login works · upload stores file · DB role tests pass · both branches merged.
**M2:** Case A runs end to end with live ArmorIQ through the real API · issue, task, draft created · ledger rows · SSE timeline shows each tool call.
**M3 (core complete, Wed midday):** one real BLOCK and one real HOLD visible · two-key send works · audit pane shows attempts joined to ledger · RLS test passes (T24).
**M3b (CP3, Wed EOD):** ledger chain verifies (T23) · policy matrix passes live (T22) · supplier portal loop works (T25 to T27) · evidence pack generated (T33) · email sink receives the approved message · Case B and mobile layout done.
**M4 (CP4, Thu EOD):** results for T01 to T38 recorded · Arena report shows `executed = 0` for every attack across 3 live runs (T21) · a real hostile run where the model attempted the forbidden tool · canary empty · flags decided at 18:00 · Neon quota checked, `demo` and `hosted` branches created from `main`.
**M5:** outsider follows README (including creating their own throwaway Neon project) · recording reviewed · gitleaks clean · ownership guard green · hosted demo smoke test passes (or it is switched off and the local path is documented).
**M6:** fresh-clone test after the final commit, against a new empty Neon project · live tests rerun · submission fields verified.

### 5.2 Merge gate (before every checkpoint merge)
- [ ] `make test` passes on your branch after merging `main` into it.
- [ ] You did not change the other person's directories (or you told them and they agreed).
- [ ] `contracts/` unchanged, or the change was agreed and logged in `docs/decisions.md`.
- [ ] No secrets (`gitleaks` clean), no large files.
- [ ] Your status message lists what changed for the other person.

### 5.3 Demo script (target 2:50)
| Time | Show | Narrator | Proof point |
|---|---|---|---|
| 0:00 | Problem: a delivery mismatch buried in chats | B | Clear user, not a chatbot |
| 0:20 | Upload PO, challan, invoice; "100 ordered, 92 counted" | B | Source-linked extraction, uncertainty visible |
| 0:55 | Confirm critical fields | B | Human stays in control |
| 1:00 | Run: reads, compare, issue, task | B | Governed calls, "ArmorIQ LIVE" badge |
| 1:40 | Supplier draft plus approval screen | B | Human approves external communication |
| 2:00 | Hostile document processed | A | Agent really attempts a forbidden call |
| 2:30 | ArmorIQ trace, audit `BLOCK`, executed = no, canary empty | A | Boundary held technically |
| 2:50 | One-line close | Both | Useful and bounded |

### 5.3b Optional extended tour (60 to 90 seconds, if the rules allow a longer video or a separate clip)

Hosted URL working → Arena report with `executed = 0` → ledger chain "verified" → evidence pack PDF for the issue → policy matrix → replay of the blocked run. Keep the 2:50 core script first and unchanged.

### 5.4 Demo credibility checklist
- [ ] Forbidden tool is in the registry and callable in principle.
- [ ] Decision shown from ArmorIQ **and** the app ledger, not from model text.
- [ ] Canary table shown empty after the denial.
- [ ] No fake tool call. If the model did not attempt it, we strengthened the document and re-ran.
- [ ] Adversarial flags disclosed in README.

### 5.5 Submission checklist
- [ ] Repository on `main` with setup instructions and architecture diagram
- [ ] README: workflow, tool surface, permissions, ArmorIQ integration, limitations
- [ ] Recording shows success **and** the attempted boundary crossing
- [ ] Tests: permitted read/create/draft, unplanned tool call, denied tool, cross-project, idempotent retry
- [ ] No keys, Neon connection strings, supplier data or confidential documents committed; README shows how a judge brings their own database (free Neon project or any Postgres 16 with pgvector)
- [ ] Official requirements and exact UTC deadline verified in the organizer channel
- [ ] Submitted at least a few hours early

---

## Level 6: Risks, Contingencies and Cut-line

### 6.1 Technical risks
| ID | Risk | Likelihood | Signal | Mitigation | Fallback |
|---|---|---|---|---|---|
| R1 | Plan semantics (S3): plan fixed at first model response, so dependent calls are blocked | Medium | G3 shows blocked second-step calls | Stage-scoped intent already planned | Natural keys, composite tools such as `create_issue_with_task`, more stages |
| R2 | ArmorIQ needs MCP behind its proxy (public URL) | Medium | S4 | Tunnel or small cloud deploy | Callback mode with local MCP as in the docs |
| R3 | Model never attempts the forbidden call in the live run | Medium | Thursday red-team shows refusals | Stronger hostile doc, adversarial flags (§17.3), several variants | Labelled "deterministic replay" clip with `ScriptedLlm` as supporting evidence only |
| R4 | Our plugin conflicts with ArmorIQ callbacks | Low-Medium | S6 | Ledger and canary are primary proof | Rely on ArmorIQ audit plus ledger join |
| R5 | Headers or identity do not reach MCP through the governed path | Medium | S7 | Use ArmorIQ-injected IAM context | Per-request MCP instance or signed context outside LLM args |
| R6 | HOLD release in console is clumsy in the live demo | Medium | S9 | Pre-stage approver, rehearse | Record hold and release as a separate clip |
| R7 | SDK or package version drift | Medium | Import or signature errors | One package, one pinned version | Ask organizers which version the cookbook expects |
| R8 | OpenRouter limits or latency (`:free`: 20 requests/min, 50 or 1,000 per day) | Medium | 429s, 402s, slow stages | One-time $10 credit on each account, rate limiter (L3), cache by sha256, paid STAGE model for anything important | Second account or key per person, Gemini fallback provider (`LLM_PROVIDER=gemini`), pre-warm before recording |
| R9 | OCR misreads fixture | Medium | Wrong quantity in tests | Confirmation gate, two-pass check | Cleaner fixtures; Case B stays the intentional ambiguity |
| R10 | Scope creep | High | New ideas appear | Level 7 parking lot | Say no until M6 |
| R11 | Deadline timezone mistake | Low | n/a | Check UTC cutoff today; IST = UTC+5:30 | Submit with a large margin |
| R12 | Secret leakage | Low | gitleaks hit | pre-commit hook, `.env` only | Rotate keys immediately |
| R19 | AI invents or misuses SDK calls (ArmorIQ, ADK, FastMCP) | High | Code looks right, fails live; signatures differ from docs | Verified-snippet registry (`vendor_notes.md`), spike tests | Re-run the spike snippet, read the official docs |
| R20 | Breadth hurts core stability | Medium | Core demo flaky after merging showcase work | Feature flags, stability rule, Thu 18:00 flag decision | Switch flags off, keep the core |
| R21 | Hosted demo abused or expensive | Medium | LLM spend spikes, strange traffic | Rate limits, daily budget cap, `DEMO_READONLY` kill switch | Local-only demo with recorded video |
| R22 | Your own coding assistant is tricked by hostile fixtures | Low to Medium | Assistant follows text from a fixture | Ignore list for `fixtures/hostile/`, never open them with an assistant | Review diffs, rotate keys |
| R23 | AI-written code adds a second path to a side effect | Medium | Tool without policy row, direct DB call in `agents/` | Review checklist (§22.5), T19, policy matrix, RLS | Fix and add a regression test |
| R24 | Free-tier quota exhausted mid-day (shared account, Arena or tests drain it) | High | 429s, daily cap reached | Own account per person, $10 credit, DEV on `:free` and STAGE on paid, daily counter with 80 percent warning | Switch to STAGE model for the rest of the day |
| R25 | Model is unreliable at tool calling, or ADK-on-LiteLLM bug (loops, dropped schemas) | Medium | Loops, malformed calls, runs hitting caps | Qualification suite (L2), no `output_schema`, flat tool results, non-streaming, tool-call caps | Choose another model; use Gemini fallback provider |
| R26 | A free model disappears or changes behaviour | Medium | Sudden 404 or different outputs | Models only via env vars; requalify when changed; record model id per run | Switch DEV to another qualified model |
| R27 | ArmorIQ plan capture misbehaves with `LiteLlm` responses (S13) | Medium | Plan empty or calls wrongly blocked | Test in the Monday spike with the chosen STAGE model | Try another model, or Gemini fallback provider, and report the finding |
| R28 | Neon cold start or a network hiccup breaks a stage or a recording take | Medium | First request after idle is slow, connect timeouts | `pool_pre_ping`, connect retries, warm-up `SELECT 1` at run start, pre-warm before recording (technical doc §19, §24.5) | Retry the take; upgrade the plan and disable scale-to-zero on `hosted` if needed |
| R29 | Neon free quota (100 CU-hours, 0.5 GB, 10 branches) runs out | Low to Medium | Console usage page; compute suspended at the limit | Check Wed and Fri, delete stale branches, create `integ`, `demo` and `hosted` only when needed, short expiry on CI branches | Upgrade the single project (usage-based), or fall back to local Postgres |
| R30 | Roles with BYPASSRLS make RLS look enforced when it is not | Medium | T24 passes when run as the owner, or app roles were created in the console | Create roles with SQL (NOBYPASSRLS); T24 connects as `app_rw` and `mcp_rw`; S16 on Monday | Fix `db/sql/`, re-run `db-init` and T24 |
| R31 | Two people write to one branch, or the wrong branch gets reset | Medium | Missing rows, surprise resets, canary not empty | One branch each, `db-reset` guards (branch name and host), golden `main` receives no application runs | `make db-reset` on your own branch and re-seed |
| R32 | Neon unreachable (outage, venue network) on demo or submission day | Low | Connection errors | Everything is scripted, so any Postgres 16 with pgvector works by changing three URLs | Local Postgres (install, or a one-off `docker run` of a pgvector image), then `make migrate` and `make seed` |

### 6.2 Team risks
| ID | Risk | Signal | Mitigation | Fallback |
|---|---|---|---|---|
| R13 | Merge conflicts at checkpoints | Conflict markers in shared files | Directory ownership, auto-discovered routers and seeds, daily `merge main` | Resolve together in a screen share; never force-push `main` |
| R14 | Contract drift (one side changes a signature silently) | Integration fails at CP2 or CP3 | `contracts/` change requires the other person's OK and a line in `docs/decisions.md` | Revert to the last agreed contract |
| R15 | One person blocked by the other | Waiting more than 30 minutes | Stubs (Level 2.3), message early | Switch to a stub, or pair for 30 minutes |
| R16 | One lane finishes early or falls behind | Midday sync shows imbalance | Spillover lists (team_distribution.md §11) | Move tasks per the list, update owners |
| R17 | Verification bottleneck: more code than we can check | Untested merges, red CI, unread diffs | 40 percent verification budget, test-first loop (§22.4), small PRs | Switch showcase flags off and pause new features until green |
| R18 | Both branches only meet at the end | No checkpoint merges | CP0 to CP5 are mandatory | n/a |

### 6.3 What gets switched off first if something is at risk

Writing code is no longer the limit, so this list is about **stability and verification**, not hours. Everything below is a feature flag. Switch off from the top.

1. X18 WhatsApp sandbox
2. X17 quote comparison
3. X14 ADK multi-agent composition
4. X12 PWA
5. X8 voice notes (keep Hindi text if stable)
6. X7 digest
7. X6 RFI scenario
8. X5 supplier portal loop
9. X4 evidence pack
10. X10 replay page (keep OpenTelemetry)
11. X1 Arena UI (**keep the runner script and report**)

**Never switch off:** live ArmorIQ, a real blocked attempt, the ledger and canary proof, the policy matrix, RLS, the README, the recording.

### 6.4 Slip rules
- **Core not green by Wed midday (M3):** freeze all showcase work; both people work only on the core until it is green.
- **Thu 18:00 stability line:** a showcase feature without green tests is switched off for the demo build. It is not rushed.
- **Fri 12:00 hard freeze:** no new features, fixes only.
- **A merge breaks `main`:** revert it first, debug on the branch second.

---

## Level 7: After the Hackathon

### 7.1 Parking lot (do not touch before M6)
WhatsApp to real suppliers · production connectors (Powerplay, Tally and similar) · multi-tenant admin console · retention and consent workflows · formal security review · change-order evidence scenario · native mobile apps · any payment rails.

### 7.2 Validation plan
| Step | Action | Success signal |
|---|---|---|
| 1 | Interview 5 to 10 contractors (owner, PM, site supervisor, store, accountant); ask them to retell the last delivery or site issue that went wrong | Pain is real and recurring |
| 2 | Map what they use today (WhatsApp, Excel, Powerplay, ERP) and what stays manual | Clear gap between inputs and their tracker |
| 3 | Test trust: what may the agent do alone, what must a human approve? | Approval boundaries match our policy defaults |
| 4 | Pilot with redacted or synthetic documents, 1 company, 1 project, 1 workflow | Weekly submissions without hand-holding |
| 5 | Measure time from signal to owned issue, extraction accepted without edits, follow-up completion, zero unauthorized side effects | Baseline versus after |

### 7.3 Roadmap (condensed)
Pilot v1 (2 to 3 real projects, manual import, mobile intake) → Pilot v2 (verified messaging, reminders, connectors) → Production (tenant isolation, security review, DPDP Act review, retention, monitoring) → Expansion (RFIs, submittals, change-order evidence, quote comparison), each with its own permission and safety review.

---

## Quick reference: critical paths

```
A:  ArmorIQ spike (Mon) → MCP tools + agents (Tue) → core boundaries (Wed AM) → chain, matrix, evidence stage (Wed PM)
    → Arena, RFI, digest, replay (Thu) → final Arena report + governance docs (Fri)
B:  schema + auth + fixtures (Mon) → extraction + API + UI (Tue) → approvals + portal + evidence pack (Wed)
    → RFI ingestion, voice, Hindi, hosted demo (Thu) → PWA, README, polish (Fri)
Both: kickoff + AI setup (Mon) · integration (Tue 17:00) · approvals seam (Wed midday) · Arena session (Thu 15:30)
      · flag decision (Thu 18:00) · freeze (Fri 12:00) · record (Fri) · submit (Sat)
```

If anything on your path is at risk, say so immediately and apply Level 6.