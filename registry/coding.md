---
type: coding
version: 6
shape: workspace
status: complete
match_signals:
  - app
  - application
  - website
  - web app
  - mobile app
  - api
  - backend
  - service
  - saas
  - dashboard
  - tool
  - build software
  - feature
  - bug
  - refactor
  - frontend
  - fullstack
---

# Registry Type: coding

> Consumed by all three skills. Edit THIS file to change how coding projects are
> **classified** (project-brief), **scaffolded** (project-scaffold), and **maintained**
> (session-learnings). The three stay in sync because they read this one file.
> See `../MAINTAINING.md`.

## 1. Identity  (consumed by: project-brief)

A **coding** project builds a software application — a web app, mobile app, API / back-end
service, CLI, or similar. The work is **not a linear assembly line**: planning, source code,
docs, and operations are worked on in parallel and revisited continuously. So the structure is
**parallel named workspaces**, not numbered pipeline stages.

**Use this type when** the user wants to build, ship, or maintain software — even if they
describe it in plain terms ("I want an app that lets people book tennis courts").

## 2. Match signals  (consumed by: project-brief classifier)

**Strong:** app, application, website, web app, mobile app, API, backend, service, SaaS,
dashboard, tool, "build software", feature, bug, deploy, frontend, backend, fullstack.

**Weak / ambiguous (confirm, don't assume):** "platform" / "system" (could be
business-opportunity), "automation" (could be business-opportunity), "content tool" (could be
content). When only weak signals are present, present type options rather than single-confirm.

## 3. Brief question set  (consumed by: project-brief)

Ask `user-only` questions in plain language. For `researchable` rows the user hasn't already
answered, run **one** scoped web search, propose **one** sensible default with a one-sentence
plain-language rationale, and ask to confirm. Skip anything already volunteered. The
`required: yes` rows define the validation contract that BOTH project-brief (final validation)
and project-scaffold (re-validation) check.

| id | prompt (plain language) | source | required | maps_to |
|----|-------------------------|--------|----------|---------|
| `goal` | "In one or two sentences, what should this app do for people?" | user-only | yes | CLAUDE.md → What This Is; PROJECT-BRIEF Identity |
| `app_name` | "What do you want to call it? (a working name is fine)" | user-only | yes | project root dir name; CLAUDE.md title |
| `users` | "Who will use it, and what's the main thing they'll do?" | user-only | yes | CLAUDE.md → What This Is; planning scope |
| `platform` | "Is this a website, a mobile app, or something else?" | user-only | yes | tech choices; src/CONTEXT.md; CLAUDE.md Commands |
| `key_features` | "List the 3–5 most important things it must do at launch." | user-only | yes | planning/specs seeds; Structure Manifest |
| `known_tools` | "Are there any tools, services, or systems you already know you want to use? (a database, Stripe, a framework, an existing account, etc.)" | user-only | no | planning/architecture; CLAUDE.md → Avoid (as fixed choices); a "Skills & Tools" row in the most relevant workspace CONTEXT.md; **constrains the researchable fields below** |
| `frontend_stack` | "What to build the screens with." | researchable | yes | src/CONTEXT.md Patterns; CLAUDE.md Commands; planning/architecture |
| `backend_stack` | "Where the data and logic live (server / database / login)." | researchable | yes | src/CONTEXT.md; planning/architecture; CLAUDE.md Commands |
| `data_store` | "Where the app's data is saved." | researchable | yes | planning/architecture; ops/CONTEXT.md |
| `auth` | "Do people need to log in? How?" | researchable | no | planning/architecture; src/CONTEXT.md |
| `hosting` | "Where it runs once it's live." | researchable | no | ops/CONTEXT.md; CLAUDE.md Commands (deploy) |
| `package_manager` | "(derived from the stack) how dependencies are installed." | researchable | no | CLAUDE.md → Commands table |
| `constraints` | "Any hard limits? (budget, no-code preference, must use X, deadlines)" | user-only | no | CLAUDE.md → Avoid; PROJECT-BRIEF constraints |
| `things_to_avoid` | "Anything you already know you do NOT want?" | user-only | no | CLAUDE.md → Avoid |
| `reference_material` | "Any examples, docs, or brand assets to start from?" | user-only | no | references / planning/architecture (L3) seeds |

> **Research rule:** `researchable` answers are proposals, not interrogations. Example —
> "For saving data I suggest **Supabase**, so you don't have to run your own server or build
> login from scratch. Good with you, or do you have something in mind?" One default, plain
> rationale, confirm. No trade-off matrices for non-technical users.

> **`known_tools` is a hard constraint, not a suggestion.** Whatever the user names here, research
> *around* it — never propose an alternative. If it already answers a `researchable` field (a named
> database fills `data_store`, a named framework fills `frontend_stack`/`backend_stack`), fill that
> field from their answer and skip the search.

> **Avoid & constraints should rarely be empty — they are guardrails, not paperwork.** The Avoid
> section keeps future sessions from wandering into the wrong tech, scope, or areas they shouldn't
> touch. So `constraints` / `things_to_avoid` being empty is a **smell that the brief is
> underspecified**, not a normal pass. The scaffold already adds generic baselines (scope, off-stack
> tech, secrets, unrelated refactors), so when the user names none, **propose 2–4 PROJECT-SPECIFIC
> ones the baselines don't cover** and confirm — e.g. features or integrations to deliberately leave
> out, areas/data to leave alone, budget or compliance limits. There needn't be many, but there
> should almost always be *something specific to this project*.

## 4. Folder tree  (consumed by: project-scaffold, session-learnings)

Layer annotations in parentheses. `{app_name}` and other `{slots}` are filled from the brief.

```
{app_name}/
├── CLAUDE.md                     (L0)  THE MAP — always loaded
├── CONTEXT.md                    (L1)  THE ROUTER — loaded on navigation
├── .icm/
│   ├── manifest.md               (—)   type, registry_version, shape, created
│   ├── LEARNINGS-INBOX.md        (—)   session-learnings review/audit list (starts empty)
│   └── README.md                 (—)   "marks an ICM-managed project"
├── planning/
│   ├── CONTEXT.md                (L2)  workspace contract
│   ├── specs/                    (L4)  one spec per feature ({feature}-spec.md)
│   ├── architecture/             (L3)  stable design notes (data model, key flows)
│   └── decisions/                (L3)  ADRs — YYYY-MM-DD_title.md
├── src/
│   ├── CONTEXT.md                (L2)  workspace contract + "Patterns We Follow"
│   └── (application code)        (L4)
├── docs/
│   ├── CONTEXT.md                (L2)  workspace contract
│   ├── api/                      (L4)
│   ├── guides/                   (L4)
│   └── changelog.md              (L4)
└── ops/
    ├── CONTEXT.md                (L2)  workspace contract
    ├── deploy/                   (L3/L4) deploy config (stable) + run artifacts
    ├── monitoring/               (L4)
    └── scripts/                  (L3)  reusable project scripts
```

## 5. Layer map  (consumed by: project-scaffold, session-learnings)

| Layer | Role | Paths |
|-------|------|-------|
| L0 | Identity / "where am I" — always loaded | `CLAUDE.md` |
| L1 | Router / "where do I go" — loaded on navigation | `CONTEXT.md` (root) |
| L2 | Workspace contract / "what do I do here" | `planning/CONTEXT.md`, `src/CONTEXT.md`, `docs/CONTEXT.md`, `ops/CONTEXT.md` |
| L3 | Stable recurring reference (the factory) | `planning/architecture/`, `planning/decisions/`, `ops/scripts/`, stable `ops/deploy/`, the "Patterns We Follow" section of `src/CONTEXT.md` |
| L4 | One-off working artifacts (the product) | `src/` code, `planning/specs/`, `docs/api/`, `docs/guides/`, `docs/changelog.md`, `ops/monitoring/` output |

> session-learnings (§9) keys off this map: a learning that belongs in **L3** is kept; one that
> only concerns **L4** is discarded.

## 6. CLAUDE.md template (L0)  (consumed by: project-scaffold)

> THE MAP. Always loaded → every line costs tokens in every conversation. Keep < 200 lines.
> Identity, folder tree, naming, commands, avoid, current state. **NO routing table** (that
> lives in CONTEXT.md). Fill `{slots}` from the brief. For the **Commands** table, derive the
> actual command from the stack the brief gives you (e.g. `package_manager: npm` → install =
> `npm install`; a Next.js frontend → start locally = `npm run dev`). If a command is genuinely
> unknowable from the brief (often the test command, sometimes deploy), write `TBD` and keep the
> row — don't delete it; the row tells future sessions the command still needs filling in.
> **Avoid has two parts and must never be empty.** Emit it as **HARD constraints** (real user
> guardrails — never cross) and **SOFT defaults** (researched/assumed defaults, revisitable as the
> project matures; each carries a date + provenance so a capable future session can tell a real limit
> from a default it may revisit — the ARA §7.4 "don't over-constrain a capable agent" lesson). The
> brief's HARD `things_to_avoid` / `constraints` render under Hard (plus the secrets baseline);
> researched/assumed defaults and the rest of the baseline floor (scope / off-stack tech / unrelated
> refactors) render under Soft. **De-dupe:** if a brief-specific avoid already covers a baseline, keep
> only the specific one. If the brief carries no specifics at all, emit just the baselines AND note the
> brief looks underspecified on guardrails.

```markdown
# {app_name} — Project Map

## What This Is
{goal}
Built for: {users}. Platform: {platform}.

## Folder Structure
{folder_tree_from_§4_without_layer_annotations}

## Naming Conventions
| Thing | Pattern | Example |
|-------|---------|---------|
| Feature spec | `planning/specs/{feature}-spec.md` | `booking-flow-spec.md` |
| Decision (ADR) | `planning/decisions/YYYY-MM-DD_{title}.md` | `2026-06-01_pick-supabase.md` |
| Guide | `docs/guides/{slug}.md` | `local-setup.md` |
| Script | `ops/scripts/{verb}-{noun}.sh` | `seed-db.sh` |

## Commands
| Do this | Run |
|---------|-----|
| Install dependencies | {package_manager_install_cmd} |
| Start locally | {frontend_dev_cmd} |
| Run tests | {test_cmd} |
| Deploy | {deploy_cmd_or_TBD} |

## Avoid
<!-- HARD = user guardrails (never cross). SOFT = researched/assumed defaults, revisitable as the
     project matures — each carries a date + provenance. NEVER leave Avoid empty. De-dupe: if a
     brief-specific avoid already covers a baseline, keep only the specific one. -->

### Hard constraints (never cross)
{each HARD thing_to_avoid / constraint from the brief as a bullet}
- Don't hard-code secrets or keys — use the host's secret store ({hosting}).

### Soft defaults (revisit as the project matures)
{each SOFT thing_to_avoid from the brief as a bullet — default, {created_date}, provenance: assumed-default}
- Stay within the agreed launch scope; don't add features beyond the current `planning/specs/` without writing a spec first. — default, {created_date}, provenance: scaffold-baseline
- Don't introduce tech or services outside the chosen stack ({frontend_stack} / {backend_stack} / {data_store}) without recording an ADR in `planning/decisions/`. — default, {created_date}, provenance: scaffold-baseline
- Don't refactor or modify areas unrelated to the current task — keep changes scoped. — default, {created_date}, provenance: scaffold-baseline
<!-- session-learnings appends earned anti-patterns below this line, as Soft defaults -->

## Current State
- Project scaffolded {created_date}. Nothing built yet.
<!-- session-learnings appends persistent state changes below this line -->

## Maintenance
When a chunk of work looks finished, consider running the `session-learnings` skill to
capture any reusable learnings into this project's context files.
```

> The "Maintenance" footer is what lets the agent reliably *offer* session-learnings at task
> completion (CLAUDE.md is always loaded). Keep it — it is the hook-free trigger.

## 7. CONTEXT.md templates  (consumed by: project-scaffold)

> **Skills & Tools is a curated baseline, not an inventory of what happens to be installed.** The
> skills these templates name are this type's recommended defaults — **emit the rows even when a
> skill isn't currently installed**. After generating, `project-scaffold` checks availability and
> prompts the user to install anything missing (the install links ship in the table footnotes, so
> they survive into the generated files). To change the baseline, override this file via
> `~/.claude/icm/registry/coding.md`. Also render **one extra row per brief `known_tools` entry**
> in the most relevant workspace's table (a payments service → `src/`; a deploy/infra tool →
> `ops/`), naming its MCP server or CLI when one exists.
>
> **Known Gotchas is the workspace's diagnostic memory** — `symptom → likely cause → fix/check`.
> Diagnostic tasks (fixing a bug, investigating an incident) load it BEFORE reasoning from
> scratch, and session-learnings appends to it over time (§9 `gotcha`). It ships in `src/` and
> `ops/` — the workspaces with recurring diagnostic work.

### 7a. Root CONTEXT.md (L1) — THE ROUTER

> Router only. Task → workspace table, workspace summary, cross-workspace flow. ~30–50 lines.
> **NO folder map, NO naming rules** (those live in CLAUDE.md).

```markdown
# {app_name} — Task Router

CLAUDE.md (always loaded) has the folder map and naming. This file routes you to work.

## Task Routing
| Your Task | Go Here | You'll Also Need |
|-----------|---------|------------------|
| Plan a feature / write a spec | `planning/CONTEXT.md` | the goal + key features |
| Write or change app code | `src/CONTEXT.md` | the relevant spec from `planning/specs/` |
| Fix a bug / debug a failure | `src/CONTEXT.md` | its **Known Gotchas** + the debugging skill it names |
| Record an architecture decision | `planning/CONTEXT.md` | — |
| Write user/developer docs | `docs/CONTEXT.md` | the feature it documents |
| Deploy / configure infra / scripts | `ops/CONTEXT.md` | hosting = {hosting} |

## Workspace Summary
| Workspace | Purpose |
|-----------|---------|
| `planning/` | Decide what to build and why. Specs (L4) + architecture & decisions (L3). |
| `src/` | The application code. Conventions live in its CONTEXT.md. |
| `docs/` | API docs, guides, changelog. |
| `ops/` | Deploy, monitoring, reusable scripts. |

## Cross-Workspace Flow
\```
planning/specs  →  src (implements the spec)  →  docs (documents what shipped)
planning/architecture & decisions  ↘ inform every workspace (load on demand)
ops  ← consumes src build output for deploy
\```
```

### 7b. planning/CONTEXT.md (L2)

```markdown
# planning

## What This Workspace Is
Where features get thought through before code. Specs say WHAT to build (one-off, L4);
architecture/ and decisions/ capture the stable reasoning (L3) that recurs across features.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Write a feature spec | the goal, `architecture/` if it touches structure | `src/`, `docs/` |
| Record a decision (ADR) | the options considered | everything else |
| Revisit a past decision | the relevant `decisions/YYYY-MM-DD_*.md` | specs |

## Folder Structure
\```
planning/
├── specs/          ← one spec per feature ({feature}-spec.md)
├── architecture/   ← stable design notes (data model, key flows)
└── decisions/      ← ADRs, dated
\```

## The Process
1. New feature → write `specs/{feature}-spec.md`: what, who it's for, what "done" looks like.
2. A choice with lasting consequences → write an ADR in `decisions/`.
3. Specs are contracts, not code: they say WHAT and the acceptance criteria, not HOW.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| Web research | While speccing, to check current best practice | Validate an approach is still recommended |
| `superpowers:writing-plans` | Turning a spec into an executable plan | Structured implementation planning |

> Baseline skills for this project type. If one isn't installed, install it: superpowers → https://github.com/obra/superpowers

## What NOT to Do
- Don't put implementation code here — that's `src/`.
- Don't let a spec dictate line-by-line implementation; leave the builder room.
```

### 7c. src/CONTEXT.md (L2)

```markdown
# src

## What This Workspace Is
The application code. Frontend: {frontend_stack}. Backend: {backend_stack}. Data: {data_store}.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Implement a feature | the spec from `../planning/specs/`, this file's "Patterns" | `docs/`, `ops/` |
| Fix a bug | this file's **Known Gotchas** first; then the failing area; relevant architecture note | unrelated specs |
| Refactor | "Patterns We Follow"; affected files | `docs/` |

## Folder Structure
\```
src/   ← application code; structure follows {frontend_stack}/{backend_stack} convention
\```

## Patterns We Follow
- Build to the spec's acceptance criteria; verify before calling a feature done.
- A repeated, deterministic step becomes a script in `../ops/scripts/` + a CLAUDE.md Commands row — from then on code does it, not judgment.
<!-- session-learnings appends recurring conventions below this line -->

## Known Gotchas
<!-- Diagnostic memory: symptom → likely cause → fix/check. Check BEFORE debugging from scratch.
     session-learnings appends recurring gotchas below this line -->
- None recorded yet.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| `superpowers:test-driven-development` | Before writing feature code | Tests first |
| `superpowers:systematic-debugging` | On any bug or unexpected behavior | Root-cause before fixing — after checking **Known Gotchas** above |
| Context7 MCP | Need current library docs mid-build | Fetch accurate API usage |
{plus one row per src-relevant known_tools entry from the brief — the tool, when to reach for it, purpose}

> Baseline skills for this project type. If one isn't installed, install it: superpowers → https://github.com/obra/superpowers · Context7 MCP → https://github.com/upstash/context7

## What NOT to Do
- Don't add a dependency or service that contradicts the chosen stack or the brief's constraints{constraints_inline_if_any}.
- Don't bypass the spec — if scope changes, update the spec first.
- Don't refactor unrelated code as a side effect — keep each change scoped to its task.
```

### 7d. docs/CONTEXT.md (L2)

```markdown
# docs

## What This Workspace Is
User- and developer-facing documentation: API reference, how-to guides, changelog.
Downstream of `src/` — documents what actually shipped.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Document an API | the relevant `../src/` code | `planning/`, `ops/` |
| Write a how-to guide | the feature; the goal for tone | architecture internals |
| Update changelog | what changed this release | everything else |

## Folder Structure
\```
docs/
├── api/         ← endpoint / interface reference
├── guides/      ← task-oriented how-tos
└── changelog.md ← dated, user-visible changes
\```

## The Process
- Document after a feature is verified, not before.
- Guides are task-oriented ("How to reset a password"), not exhaustive.

## What NOT to Do
- Don't duplicate architecture rationale here — link to `planning/decisions/`.
```

### 7e. ops/CONTEXT.md (L2)

```markdown
# ops

## What This Workspace Is
Getting the app running and keeping it healthy. Hosting: {hosting}. Reusable scripts (L3) live
here; per-run output (L4) does too.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Deploy | `deploy/` config; CLAUDE.md Commands | `planning/specs/`, `docs/guides` |
| Add a reusable script | existing `scripts/` for conventions | `src/` internals |
| Investigate an incident | this file's **Known Gotchas** first; `monitoring/`; relevant architecture note | docs |

## Folder Structure
\```
ops/
├── deploy/      ← deployment configuration (stable) + run artifacts
├── monitoring/  ← logs, alerts, dashboards config
└── scripts/     ← reusable project scripts ({verb}-{noun}.sh)
\```

## The Process
- Reusable operational steps become a script in `scripts/`, then a row in CLAUDE.md Commands.
- One-off run output stays in `monitoring/` and is not promoted.

## Known Gotchas
<!-- Diagnostic memory for deploy & infra quirks: symptom → likely cause → fix/check.
     session-learnings appends recurring gotchas below this line -->
- None recorded yet.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| Context7 MCP | Configuring {hosting} or any infra service | Current docs for the hosting platform / CLI |
{plus one row per ops-relevant known_tools entry from the brief — the tool, when to reach for it, purpose}

> Baseline tools for this project type. If Context7 MCP isn't installed, install it: https://github.com/upstash/context7

## What NOT to Do
- Don't hardcode secrets in `deploy/` — reference the host's secret store ({hosting}).
```

## 8. Naming conventions  (consumed by: project-scaffold, session-learnings)

| Thing | Pattern | Example |
|-------|---------|---------|
| Feature spec | `planning/specs/{feature}-spec.md` | `booking-flow-spec.md` |
| ADR / decision | `planning/decisions/YYYY-MM-DD_{title}.md` | `2026-06-01_pick-supabase.md` |
| Guide | `docs/guides/{slug}.md` | `local-setup.md` |
| API doc | `docs/api/{resource}.md` | `bookings.md` |
| Script | `ops/scripts/{verb}-{noun}.sh` | `seed-db.sh` |
| Changelog entry | dated heading in `docs/changelog.md` | `## 2026-06-01` |

## 9. Learning-routing rules  (consumed by: session-learnings)

Apply the **recurrence test** first: does the learning touch something **recurring / L3 /
factory**? Keep it. Else (purely L4 / one-off) **DISCARD** it. Then route survivors:

| Category | Recurrence test (keep if YES) | Destination file → section | Insert format |
|----------|-------------------------------|----------------------------|---------------|
| new-convention | Will this pattern recur in future code? | `src/CONTEXT.md` → "Patterns We Follow" | `- {pattern}: {one-line why}` |
| thing-to-avoid | Will this mistake / anti-pattern recur? | `CLAUDE.md` → "Avoid" → **Soft defaults** (never Hard — that's user-authored) | `- {avoid X} — {short reason} ({date}, provenance: learned)` |
| current-state-update | Persistent state change (not transient)? | `CLAUDE.md` → "Current State" | `- {what changed} ({date})` |
| decision | A real, lasting technical decision? | new `planning/decisions/YYYY-MM-DD_{title}.md` | ADR (Context / Decision / Consequences) |
| command | Reusable project command **not already in the Commands table**? | `CLAUDE.md` → "Commands" table | table row: `\| {do this} \| {cmd} \|` |
| gotcha | Integration quirk that will bite again? | nearest relevant `*/CONTEXT.md` → "Known Gotchas" (create the section if absent; remove a "None recorded yet." placeholder on first insert; CLAUDE.md → Avoid → Soft if cross-cutting) | `- {symptom} → {likely cause} → {fix or what to check} ({date})` |
| dependency-stale | A dependency / version fact that recurs? | `CLAUDE.md` → "Current State" or `src/CONTEXT.md` Patterns | `- {dep} pinned/updated to {ver} ({date}) — {why}` |
| (one-off) | Fails the recurrence test (only this run) | — | **DISCARD** (do not stage) |

> Every staged/applied entry must carry: the learning, its category, the destination
> file + section, the EXACT insert text above, and the recurrence justification.

## 10. Existing-repo mapping (brownfield)  (consumed by: adopt-project, project-scaffold overlay)

Used when adopting an **existing** codebase: recognize what's already there and map it onto this
type's ICM layers **without moving, renaming, or rewriting any file**. The ICM layer is *added on
top* — `CLAUDE.md` describes where things are; the `CONTEXT.md` routers point at the existing dirs.

### Infer the researchable §3 fields from the repo (no web search needed)
| Signal in the repo | Fills |
|--------------------|-------|
| `package.json` deps: react / next / vue / svelte / angular | `frontend_stack` |
| `package.json` deps: express / fastify / nest; or `requirements.txt`/`pyproject.toml`, `go.mod`, `Gemfile` | `backend_stack` |
| Lockfile: `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `poetry.lock` | `package_manager` |
| `prisma/`, `drizzle*`, `supabase/`, `*.sql`, `DATABASE_URL` in `.env.example` | `data_store` |
| `next-auth`, `@clerk/*`, `passport`, supabase-auth usage | `auth` |
| `Dockerfile`, `vercel.json`, `netlify.toml`, `fly.toml`, `.github/workflows/*deploy*` | `hosting` |

Record each inferred value **with its evidence**; if a field can't be inferred, mark it for the user.

### Map existing directories → ICM workspace / layer (point at them; don't move)
| Found in repo | Maps to |
|---------------|---------|
| `src/`, `app/`, `lib/`, `pages/`, `components/`, `server/`, `api/` | the **`src/`** workspace (L4 app code) |
| `docs/`, `README.md`, `wiki/` | the **`docs/`** workspace (L3/L4) |
| `docs/architecture/`, `adr/`, `decisions/`, `rfcs/`, `design/` | **`planning/`** → architecture & decisions (L3) |
| `specs/`, `requirements/`, roadmap docs | **`planning/specs/`** (L4) |
| `infra/`, `deploy/`, `ops/`, `terraform/`, `Dockerfile`, `.github/workflows/`, `k8s/` | the **`ops/`** workspace |
| `test/`, `tests/`, `__tests__/`, `*.test.*`, `*.spec.*` | note the test setup in `src/CONTEXT.md` "Patterns We Follow" |
| build/config: `vite.config*`, `next.config*`, `tsconfig*`, `Makefile` | reference in `CLAUDE.md` Commands; leave in place |

### Rules
- **Never** create / move / modify existing source. If a workspace home is genuinely absent (often
  `planning/`), add just that one and leave the rest pointing at the real dirs.
- A repo dir that doesn't fit a workspace is fine — list it in `CLAUDE.md`'s folder map as-is.
- **Multiple code dirs map to the ONE `src/` workspace.** If `src/` and `app/` (or `lib/`, `server/`,
  `pages/`) all hold application code, they all map to the single `src/` workspace — list each in the
  manifest's `workspace → existing-dir` map and in `src/CONTEXT.md`. Don't invent a second code workspace.
- **A workspace whose artifacts live elsewhere still gets its contract, but no empty placeholders.**
  If infra lives at the repo root (`Dockerfile`, `.github/workflows/`), create `ops/` only to hold its
  `CONTEXT.md` (pointing at those real paths). Do NOT create empty placeholder subdirs (`ops/deploy/`,
  `ops/monitoring/`, `docs/api/`, …) that don't correspond to anything actually in the repo.
- The brief's **"Existing Inventory"** section records this mapping (found dir → workspace/layer)
  for the user to confirm before `project-scaffold` overlays the structure.
