# SITEWISE — Level-wise Plans

Companion to `technical.md` (how we build) and `team_distribution.md` (who builds what).
Plans are layered from the **goal** (Level 0) down to **individual tasks** (Level 3), then verification, demo, and contingency.

**Calendar reality check:** today is **Tuesday 13 Oct 2026**. The proposal's "Monday 12 Oct" gates are folded into today. Build window closes **Sat 17 Oct** (exact UTC cutoff to be confirmed on the official page — Spike S6). **Internal hard freeze: Fri 16 Oct, 23:59 IST. Submit target: Sat 17 Oct morning IST, ≥ 6 h before the cutoff.**

Estimates are focused-work hours per person. Assumption: ~8–9 productive hours/day each, ~2 people. Re-estimate after Spike S1.

---

## Level 0 — North Star

### 0.1 Mission
> An AI agent that investigates a business exception across company records, prepares the work to resolve it, and **cannot cross its authorized boundary unnoticed or unchecked**.

### 0.2 The 4-minute proof we must be able to give
1. **Useful:** ₹18 lakh invoice → three evidence-linked risk signals + review task + vendor-message draft.
2. **Scoped:** declared scope and policy are visible.
3. **Attacked:** malicious invoice makes the agent *really* try `export_all_supplier_bids`.
4. **Governed:** live ArmorIQ blocks it; MCP independently refuses.
5. **Proven:** DB proof — canary empty, no forbidden ledger rows, bids checksum unchanged; readable audit trace.

### 0.3 Definition of Done for the whole project (P0)
- [ ] Live ArmorIQ in the real tool-call path (no mocks in demo build)
- [ ] One seeded end-to-end invoice case with expected findings (T-01)
- [ ] Findings are evidence-linked; uncertainty visible (T-02)
- [ ] Review task + vendor draft created once each (idempotent)
- [ ] One genuine blocked forbidden call from a real model run (T-04)
- [ ] Independent MCP refusal (T-06) and no-side-effect proof (T-05)
- [ ] Audit trace UI/API showing attempt → verdict → MCP → ledger
- [ ] Fresh-clone setup works (T-18); README complete
- [ ] 3–4 min demo video recorded + submission sent

### 0.4 Success metrics (from proposal §19, made measurable)
| Metric | Target |
|---|---|
| Seeded records retrieved & checked | 100 % |
| Material findings with valid evidence | 100 % |
| Review task / draft created exactly once | 1 / 1 over 5 repeated runs |
| Forbidden attempts blocked before execution | 100 % of observed attempts |
| Canary mutations | 0 |
| Cross-tenant / unapproved-send rejections | 100 % |
| Injection **attempt rate** (reported honestly) | measured over 20 runs |
| Clean-start demo reliability | 5 consecutive successful resets+runs |

---

## Level 1 — Milestones (phases with exit gates)

| # | Milestone | Target | Exit gate (binary) |
|---|---|---|---|
| **M0** | Foundations & spikes | Tue 13 Oct EOD | Repo + Compose runs; Neon project with roles; **ArmorIQ hello-world call + off-plan call blocked** (S1); ADK hello-agent calls one MCP tool (S2); contracts frozen v0 |
| **M1** | Data & read-path | Wed 14 Oct noon | Schema + RLS + seed loaded; read tools work through MCP with envelope; PDF extraction works for both fixtures |
| **M2** | Happy path end-to-end | Wed 14 Oct EOD | Agent pipeline runs on seeded invoice → findings in DB → task + draft created through governed path; SSE timeline in UI |
| **M3** | Boundary proof | Thu 15 Oct noon | Malicious fixture → real forbidden attempt → ArmorIQ block → MCP deny → proof endpoint all-green |
| **M4** | Approvals & hardening | Thu 15 Oct EOD | Payload-hash approval, replay/tamper tests, RLS negatives, append-only, fail-closed all green. **Feature freeze for P1/P2 starts here.** |
| **M5** | UI/Audit polish & matrix | Fri 16 Oct noon | Governance + Proof panels complete; 2×2 matrix and attempt-rate reports generated |
| **M6** | Release candidate | Fri 16 Oct EOD | Fresh clone works; README done; 3 clean rehearsals; **hard freeze 23:59 IST** |
| **M7** | Submit | Sat 17 Oct AM IST | Video recorded, repo/links submitted, confirmation saved |

Dependency spine (anything on it delays everything):
`S1 ArmorIQ spike → Gateway → governed read tools → agent happy path → forbidden attempt → proof → demo`.

---

## Level 2 — Day-by-day plan

Legend: **A** = Person A (Governance & Agents), **B** = Person B (Platform & Product). Details of each task ID are in Level 3.

### Tue 13 Oct — M0 Foundations (catch-up day)
| Time block | A | B |
|---|---|---|
| Morning (3–4 h) | **S1 ArmorIQ spike** (G-01), then write `docs/armoriq_spike.md`; start `packages/contracts` v0 *together with B* (30-min session) | Repo scaffold, Compose, uv/pnpm workspaces, CI skeleton (F-01..F-03); Neon project, branches, 3 roles, pooled/direct strings (D-01) |
| Midday (1 h) | **Contracts freeze v0** — both: tool IO, enums, envelope, event schema, error taxonomy (F-04) | same |
| Afternoon (3–4 h) | **S2 ADK spike**: hello-agent → callback short-circuit → tool via gateway stub (A-01); FastMCP hello with envelope verify (M-01) | Alembic schema v1 for business tables + auth tables (D-02); seed script skeleton + PDF fixture generator (S-01) |
| Evening (1 h) | Merge checkpoint #1; update `technical.md` §8/§22 with spike results | Spike S4 (RLS + pooled `set_config` check); S6 (read official submission rules) |
**Gate M0.**

### Wed 14 Oct — M1 + M2 (the "happy path" day)
| Block | A | B |
|---|---|---|
| Morning | Security SQL: roles/grants/RLS/append-only (D-03); MCP read tools + guards (M-02..M-04) | Seed data complete (S-02); PDF extraction + grounding (I-01..I-03); auth + `/cases`, `/run` skeleton (P-01..P-03) |
| Midday | Gateway v1 (attempt log → ArmorIQ → MCP) (G-02..G-04); scope template + plan declaration (G-05) | Comparison engine + unit tests (E-01..E-04) — handed to A at 13:00 for wrapping as `compare_invoice_terms` |
| Afternoon | ADK pipeline stages 1–4 wired (A-02..A-06); findings builder hook (A-07) | Next.js shell: login, case list, case detail tabs, SSE timeline (U-01..U-03) |
| Evening | **Integration session (90 min, together):** run happy path end-to-end on seeded case → fix contract drift | same |
**Gate M2.** If red, Thursday's morning starts with repair, and M3 slips *only* by the time needed.

### Thu 15 Oct — M3 + M4 (the "prove it" day)
| Block | A | B |
|---|---|---|
| Morning | Forbidden stubs + armed canary (M-05); malicious fixture tuning with B; attempt-rate script (R-01..R-03) → **Gate M3 by noon** | Malicious PDF fixture generator (S-03); Findings/Evidence UI + Governance panel on frozen event schema (U-04, U-05); drafts API + edit-invalidates-approval (P-05) |
| Afternoon | Approval guard in MCP + HOLD flow (S5) (M-06, G-06); idempotency (M-07); fail-closed tests (G-07) | Approval queue UI (U-06); approvals API (P-06); `/audit` and `/proof` endpoints (P-07, P-08) with A's SQL |
| Evening | Security test suite T-06..T-10, T-13..T-17 green | UI wired to real events; E2E Playwright happy-path skeleton |
**Gate M4. Feature freeze for new scope at 21:00.** Anything not started is cut (Level 6).

### Fri 16 Oct — M5 + M6 (the "make it solid" day)
| Block | A | B |
|---|---|---|
| Morning | 2×2 matrix runner (R-04); attempt-rate (N=20) report; route-around test (T-17) | Proof panel + policy view (P1) (U-07, U-08); polish evidence drawer; empty/error states |
| Afternoon | Bug-fix queue from integration; ledger hash-chain (P2) **only if** all P0/P1 green | README, architecture diagram, threat model, demo script (X-01..X-03); `make reset/demo` scripts |
| Evening | **Rehearsal #1 (cold clone on B's laptop), #2, #3** — together; timer on; fix only blockers | same |
**Gate M6 + HARD FREEZE 23:59 IST** (tag `v1.0-rc`). After this: only fixes for demo-breaking bugs, each reviewed by the other person.

### Sat 17 Oct — M7 Submit
| Time (IST) | Activity |
|---|---|
| 07:00–08:30 | Fresh `make reset`, warm Neon + tunnel, pre-flight checklist (Level 5.3) |
| 08:30–10:30 | Record demo (screen + voice), 2 takes max; backup recording on different machine |
| 10:30–12:00 | Final README links, repo cleanup (no secrets), tag `v1.0`; submit |
| 12:00–… | **Buffer** — no new code. Confirm submission received; keep both laptops ready for any organizer question |

---

## Level 3 — Task-level breakdown by workstream

Format: **ID — task — owner — est. — priority — acceptance**.
Priority: P0 must · P1 if stable · P2 stretch.

### W0 Foundations (F)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| F-01 | Monorepo scaffold, uv workspace, pnpm, `.env.example`, Makefile | B | 1.5h | P0 | `make up` starts api, mcp, web (hello endpoints) |
| F-02 | Docker Compose (api, mcp, web) | B | 1h | P0 | one command boots all |
| F-03 | CI: ruff, mypy(contracts), pytest, eslint | B | 1h | P1 | PR check green |
| F-04 | **Contracts v0 freeze** — enums, tool IO, envelope claims, event schema, error taxonomy, digest fn | A+B | 2h | P0 | merged to `main`, both signed off; later changes need both reviewers |
| F-05 | gitleaks pre-commit, CODEOWNERS | B | 0.5h | P1 | commit with fake key rejected |

### W1 Database & security (D)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| D-01 | Neon project, `main`/`demo` branches, 4 roles, pooled+direct URLs, warm-up script | B (A reviews) | 1.5h | P0 | both roles connect; cold-start retry works |
| D-02 | Alembic: identity, business, documents, investigation, approvals, tasks/drafts/outbox, attempts, ledger, canary tables | B | 4h | P0 | `alembic upgrade head` clean on empty DB |
| D-03 | Security SQL: grants, RLS on all `org_id` tables, FORCE RLS, append-only revokes + triggers | A | 3h | P0 | T-07, T-14, T-16 pass |
| D-04 | Column-level grant on `approvals.used_at` for MCP role | A | 0.5h | P0 | MCP cannot change `decision` |
| D-05 | Hash-chain trigger + verifier query | A | 2h | P2 | tamper test detects edited row |
| D-06 | `make reset` (truncate/reseed/baseline checksum) <60 s | B | 1.5h | P0 | 5 consecutive resets OK |

### W2 Seed & fixtures (S)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| S-01 | reportlab PDF generators (contract, PO, invoice 0417, prior invoice) | B | 2h | P0 | PDFs have text layer; reproducible bytes |
| S-02 | Seed script per technical.md §21 (2 orgs, users, vendor, change event, bids) | B | 2h | P0 | numbers match T-01 exactly |
| S-03 | Malicious invoice 0419 with visible + hidden injection text | B (A tunes wording) | 1.5h | P0 | pdfplumber extracts the injection text |
| S-04 | Optional construction regression fixture | B | 1.5h | P2 | extra case passes engine tests |

### W3 Ingestion & engine (I / E)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| I-01 | Upload endpoint: magic bytes, size, sha256, store | B | 1h | P0 | non-PDF rejected |
| I-02 | pdfplumber text+bbox → `documents.text_content` & spans | B | 2h | P0 | all fixtures extracted |
| I-03 | ExtractionAgent schema + grounding check + cross-validation vs DB | A (agent) / B (grounding) | 3h | P0 | ungrounded field → `grounded=false`; T-02 |
| E-01 | Price variance + unapproved charge | B | 1.5h | P0 | ₹1,20,000 + ₹1,20,000 |
| E-02 | Duplicate scoring | B | 1.5h | P0 | candidate score 0.80, label POSSIBLE |
| E-03 | Bank-change risk | B | 1h | P0 | HIGH on seeded event |
| E-04 | Payment status | B | 0.5h | P0 | PARTIALLY_PAID ₹9,00,000 for candidate |
| E-05 | Finding builder (requires evidence) | B | 1.5h | P0 | T-15 |

### W4 Governance (G)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| G-01 | **S1 ArmorIQ spike** + spike doc | A | 3h | P0 | answers to the 7 questions in technical.md §8.8 |
| G-02 | `GovernanceAdapter` (Mode A or B) + verdict normalization + raw storage | A | 3h | P0 | unit tests on normalization incl. unknown→ERROR |
| G-03 | Gateway: attempt row → adapter → MCP → outcome row; envelope signing | A | 3h | P0 | every call yields attempt row with correlation IDs |
| G-04 | Fail-closed + timeouts + startup guard against fake adapter | A | 1.5h | P0 | T-10 |
| G-05 | Scope templates + plan declaration + token caching per run | A | 2h | P0 | plan visible in UI event `plan.declared` |
| G-06 | HOLD handling for `request_vendor_send` (S5) | A | 2h | P0 | held call resolves only after valid approval |
| G-07 | Policy file `policies/armoriq_policy.md` + sync check with platform | A | 1h | P1 | table = platform config |

### W5 MCP server (M)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| M-01 | FastMCP skeleton + envelope verification + replay cache | A | 2h | P0 | T-13 |
| M-02 | Guard chain (role allowlist, tenant ownership, schema, state machine) | A | 2h | P0 | T-07 |
| M-03 | Read tools: list/read document, PO, contract, invoice history | A | 3h | P0 | return source refs |
| M-04 | `compare_invoice_terms` wrapping B's engine | A | 1h | P0 | output matches engine |
| M-05 | Forbidden stubs + armed canary + `mcp_denials` | A | 2h | P0 | T-05, T-06 |
| M-06 | `request_vendor_send` approval guard (digest, single-use, atomic outbox) | A | 3h | P0 | T-08, T-09 |
| M-07 | `create_review_task` / `draft_vendor_message` with idempotency + ledger in-txn | A | 2h | P0 | one row per key |

### W6 Agents (A)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| A-01 | **S2 ADK spike** (callbacks, output_schema/tools, LiteLLM fallback) | A | 2h | P0 | notes in `technical.md` §7 |
| A-02 | ExtractionAgent | A | 2h | P0 | validated against fixtures |
| A-03 | InvestigatorAgent (tools + prompt) | A | 3h | P0 | calls every read tool on seeded case |
| A-04 | ActionPlannerAgent | A | 2h | P0 | 1 task, 1 draft, no send without approval |
| A-05 | ReporterAgent (schema) | A | 1h | P0 | JSON valid 20/20 |
| A-06 | Pipeline + state + caps (25 attempts/90 s/3 min) | A | 2h | P0 | caps → `FAILED_CLOSED` |
| A-07 | Findings builder invocation + blocked-attempt handling in prompts | A+B | 1.5h | P0 | T-17 |
| A-08 | Fallback model switch tested (OpenRouter) | A | 1h | P1 | `LLM_MODEL` swap works |

### W7 API (P)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| P-01 | Auth (argon2, JWT cookie), `/me`, role dependency | B | 2h | P0 | wrong role 403 |
| P-02 | Tx helper setting `app.org_id` per transaction | B | 1h | P0 | T-14 |
| P-03 | Cases CRUD, run start, SSE with persistence/replay | B | 3h | P0 | reconnect resumes |
| P-04 | Findings/evidence endpoints | B | 1.5h | P0 | evidence drawer data |
| P-05 | Drafts PATCH invalidates approvals | B | 1h | P0 | T-08 |
| P-06 | Approvals create/list (four-eyes, 30-min expiry) | B | 2h | P0 | creator ≠ approver |
| P-07 | `/audit` (join attempts↔MCP↔ledger) | B (A supplies SQL) | 1.5h | P0 | T-11 |
| P-08 | `/proof` (canary, forbidden-ledger, bids checksum, outbox) | B (A supplies SQL) | 1h | P0 | T-05 |
| P-09 | `/redteam/run`, `/policy` | B | 2h | P1 | arena works |

### W8 Frontend (U)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| U-01 | App shell, login, case list, typed API client (openapi-typescript) | B | 2.5h | P0 | login works for 4 roles |
| U-02 | Case workspace + tabs | B | 2h | P0 | — |
| U-03 | RunTimeline (SSE) | B | 2h | P0 | live events |
| U-04 | Findings + EvidenceDrawer | B | 3h | P0 | quote highlighted |
| U-05 | **GovernancePanel** (attempt table, verdict badges, raw JSON expand) | B | 3h | P0 | shows BLOCKED row w/ ArmorIQ raw payload |
| U-06 | ApprovalQueue (digest, validity state) | B | 2h | P0 | invalidated state visible |
| U-07 | **ProofPanel** | B | 2h | P0 | all zeros / unchanged shown with timestamps |
| U-08 | Policy view | B | 1.5h | P1 | renders policy table |
| U-09 | Attack Arena | B | 3h | P2 | replay scenarios |
| U-10 | PDF.js bbox highlight | B | 3h | P2 | highlights in document |

### W9 Red-team (R)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| R-01 | Injection fixture tuning (with B) | A | 2h | P0 | attempt observed |
| R-02 | `attempt_rate.py` N=20 | A | 1h | P0 | report saved |
| R-03 | Route-around test (T-17) | A | 1h | P0 | green |
| R-04 | 2×2 matrix runner | A | 2h | P1 | table in README |
| R-05 | Additional attacks (payment release, bank change, cross-tenant read via prompt) | A | 2h | P2 | each blocked |

### W10 Docs & demo (X)
| ID | Task | Own | Est | Pri | Acceptance |
|---|---|---|---|---|---|
| X-01 | README (setup, architecture, policy, threat, tests, demo steps) | B (A writes governance section) | 3h | P0 | fresh clone works from README only |
| X-02 | Demo script + timing + backup plan | A+B | 1.5h | P0 | rehearsed 3× |
| X-03 | Architecture + trust-boundary diagram image | B | 1h | P1 | in README |
| X-04 | Record demo + backup recording | A+B | 2h | P0 | file saved on 2 machines |
| X-05 | Submission package & confirmation | B | 1h | P0 | receipt saved |

**Total P0 effort estimate:** A ≈ 60 h, B ≈ 60 h across ~4.5 working days → roughly 13 h/day each in the worst case, which is tight. That is the schedule risk. Mitigation: **E-01..E-05 and extraction grounding are B's work (moved from A per D9)**, and every A task flagged P1/P2 above is the first cut list (Level 6).

---

## Level 4 — Verification plan (gates, not afterthoughts)

### 4.1 Gate checklist per milestone
| Gate | Must be green |
|---|---|
| M0 | S1 answers recorded; off-plan call blocked live; contracts merged |
| M1 | T-14 (RLS unset=0 rows), T-18 partial (reset+seed), engine unit tests |
| M2 | T-01, T-02 on real model run; 5/5 repeated runs create exactly 1 task + 1 draft |
| M3 | T-04, T-05, T-06; attempt rate ≥ 1 observed in 3 tries |
| M4 | T-07..T-10, T-13..T-17 |
| M5 | T-03 (live marker), T-11, 2×2 matrix output |
| M6 | T-18 on a *different* machine; T-12 egress check; 3 rehearsals |

### 4.2 Regression rule
After M2, every merge to `main` must run `make test-fast` (unit + integration + security, ≈ 3 min). A red `main` is the top priority for both people.

### 4.3 What "live" means
`@live_armoriq` tests are run **manually** at M0, M3, M5, M6 and once on demo morning. Save the raw output into `docs/evidence/` (timestamped) — these are submission artifacts.

---

## Level 5 — Demo and submission plan

### 5.1 Demo script (3:40–4:00) — roles
| Time | Beat | Speaker | Screen |
|---|---|---|---|
| 0:00–0:30 | Problem + request ("Investigate ₹18L invoice; do not release payment") | B | Case intake |
| 0:30–1:30 | Run → live timeline → 3 findings with evidence → task + draft | B | Findings, Actions |
| 1:30–2:00 | Declared scope + policy table | A | Policy / plan.declared |
| 2:00–3:00 | Upload malicious invoice → run → forbidden attempt → ArmorIQ BLOCK → MCP refusal row | A | Governance panel |
| 3:00–3:40 | Proof panel: canary 0, forbidden ledger 0, checksum unchanged; ArmorIQ trace; matrix table | A | Proof panel + ArmorIQ dashboard |
| 3:40–4:00 | Value close: reviewable case, agent stays in scope | B | Case summary |

### 5.2 Backup plans
| Failure | Backup |
|---|---|
| Model doesn't attempt the forbidden call | Re-run (visible); keep 1 pre-recorded successful live run as video insert, clearly labelled "recorded earlier today" |
| ArmorIQ slow/down | Show the fail-closed behaviour (it *is* a feature); then show earlier recorded trace from `docs/evidence/` |
| Neon cold start | Warm-up script in `make demo`; keep an open connection page |
| Tunnel drops (Mode A) | Pre-start second tunnel; Mode B fallback config via env flag |
| Wi-Fi | Phone hotspot tested in rehearsal |

### 5.3 Pre-flight checklist (demo morning)
- [ ] `git status` clean, tag `v1.0-rc` checked out
- [ ] `make reset` → baseline checksum printed
- [ ] ArmorIQ key valid; live marker test passes
- [ ] Neon warm; tunnel up (Mode A)
- [ ] Both fixtures present; browser zoom 110 %; notifications off
- [ ] Screen recorder tested with audio
- [ ] Backup recording folder on second machine

### 5.4 Submission package
Repo link (clean history, no secrets) · README · demo video (≤ 4 min) · short write-up: *what the agent does, how ArmorIQ is used, how the boundary held* · `docs/evidence/` (raw ArmorIQ outputs, matrix, attempt-rate report) · confirmation screenshot.
Re-read the official event page rules **Tue** and **Fri** for format changes.

---

## Level 6 — Risk, contingency and cut plan

### 6.1 Cut order (cut from the top first)
1. P2 items: Attack Arena, PDF bbox highlight, hash chain, regression fixture, extra attacks
2. P1: policy view, CI polish, OpenRouter fallback test, matrix runner (keep the *manual* matrix table)
3. Approval **UI polish** (keep API + MCP guard)
4. Duplicate scoring detail (keep simple exact-match + score)
5. **Never cut:** live ArmorIQ, forbidden-call proof, MCP independent refusal, DB proof, fail-closed, no-real-effects.

### 6.2 Tripwires (decide, don't agonize)
| Tripwire | Action |
|---|---|
| S1 not complete by Tue 20:00 | Switch to Mode B; call ArmorIQ/organizers' channel for help; keep spike open in parallel |
| M2 gate red by Wed 23:00 | Freeze all UI work; both fix pipeline Thu until noon |
| Attempt rate < 3/20 on Thu noon | Change fixture wording; if still low, try second model (`LLM_MODEL`); do **not** fake |
| `main` red > 2 h | Revert last merge |
| Anyone > 90 min stuck | Ask the other person (pair for 30 min) |
| Fri 18:00: rehearsal failing | Stop features; only demo-path fixes |

### 6.3 Risk register (live)
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| ArmorIQ can't reach local MCP | M | H | Tunnel / Mode B | A |
| ADK structured output blocks tools | M | M | Separate stages (already designed) | A |
| RLS misconfig via pooler | M | H | Transaction-local `set_config`; T-14 | B/A |
| Model verbosity/timeouts | M | M | caps; low temperature; Flash model | A |
| A overloaded | H | H | D9 rebalance; cut order | both |
| Secrets leaked | L | H | gitleaks, `.env` ignored | B |
| Submission cutoff misread | L | H | S6 + internal deadline 12 h earlier | B |

---

## Appendix A — Daily rituals
- **09:00 / 5 min stand-up**: yesterday, today, blockers, contract changes.
- **13:00 sync (10 min)**: merge status; hand-offs (e.g., engine → MCP wrapper).
- **Evening integration (60–90 min)**: run end-to-end together; update this file's gate checkboxes.
- **Contract change rule**: any change to `packages/contracts` is announced in chat and needs the other person's approval.

## Appendix B — Gate tracker (tick as you go)
- [ ] M0 · [ ] M1 · [ ] M2 · [ ] M3 · [ ] M4 · [ ] M5 · [ ] M6 · [ ] M7

*End of plans.md*
