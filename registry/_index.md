# ICM Structure Registry — Index

This directory is the **single source of truth** for four skills:
`project-brief`, `adopt-project`, `project-scaffold`, and `session-learnings`.
Each project **type** has exactly one file here. To change how a type is classified,
scaffolded, or maintained, edit **that one file** — all the skills read it, so they stay
in sync automatically. See `MAINTAINING.md` (beside this file) for the interdependency contract.

> **Where this registry lives.** It ships bundled inside the `interpretable-context` plugin at
> `${CLAUDE_PLUGIN_ROOT}/registry/`. Skills resolve any registry file with a **user-override-first**
> lookup: use `~/.claude/icm/registry/<file>` if it exists, otherwise the bundled copy. That lets a
> user customize or add a type locally without editing the plugin (and survive plugin updates).

> ICM = Interpretable Context Methodology: folder structure *is* the agent's architecture.
> Five layers — L0 `CLAUDE.md` (identity/map), L1 `CONTEXT.md` (routing), L2 workspace/stage
> `CONTEXT.md` (contract), L3 reference material (stable, recurring — "the factory"),
> L4 working artifacts (per-run, one-off — "the product").

---

## How the skills use this directory

1. **`project-brief`** reads the **Type Table** below to classify a new project, then loads
   that one type's file for its **Brief question set** (§3).
2. **`adopt-project`** (existing-repo path) classifies via the **Type Table**, then loads that
   type's **Brief question set** (§3) and its **existing-repo mapping** (§10) to inventory the repo.
3. **`project-scaffold`** reads the declared `type` from a project's `PROJECT-BRIEF.md`, then
   loads that one type's file for the **folder tree** (§4), **layer map** (§5),
   **templates** (§6–7), and — for brownfield overlays — the **existing-repo mapping** (§10).
4. **`session-learnings`** reads `.icm/manifest.md` for the project's `type`, then loads that
   one type's file for its **learning-routing rules** (§9).

**Load only the one relevant type file, on demand.** Never read all of them; never force-load
a type file with `@`-embeds. (This is the deliberate, justified exception to "skills are
self-contained" — a shared registry is what keeps the three skills interdependent-by-design.)

---

## Type Table — the classifier's lookup

| type | shape | status | one-line identity | match signals |
|------|-------|--------|-------------------|---------------|
| `coding` | workspace | complete | Build a software application (web / mobile / API / CLI). | app, application, website, web app, mobile app, API, backend, service, SaaS, dashboard, tool, "build software", feature, bug, deploy, frontend, fullstack |
| `content` | pipeline | stub | Produce written/media content through a publishing pipeline. | blog, article, newsletter, video, post, content, publish, editorial, writing, podcast |
| `client` | workspace | stub | Manage deliverables for an external client / engagement. | client, engagement, retainer, deliverable, account, agency, stakeholder, consulting |
| `business-opportunity` | pipeline | stub | Evaluate / develop a business idea or opportunity. | business idea, opportunity, market, validate, go-to-market, monetize, startup, venture |

`status: stub` types are **recognizable but not fully built**. When the classifier lands on a
stub, `project-brief` must tell the user the type isn't fully set up yet and offer to either
proceed minimally or treat it as the closest `complete` type (usually `coding`).

---

## Registry-file FORMAT SPEC — follow this exactly when adding or editing a type

Every type file MUST contain these sections, in this order:

| # | Section | Consumed by | Required contents |
|---|---------|-------------|-------------------|
| FM | Frontmatter | all | `type` (kebab-case, == filename stem), `version` (integer, bump on any change), `shape` (`workspace` \| `pipeline`), `match_signals` (list), `status` (`complete` \| `stub`) |
| 1 | Identity | project-brief | What this type is; when to use it (plain language) |
| 2 | Match signals | project-brief | Strong signals + weak/ambiguous ones (confirm-don't-assume) for the classifier |
| 3 | Brief question set | project-brief | Markdown table, columns: `id`, `prompt` (plain language), `source` (`user-only` \| `researchable`), `required` (yes/no), `maps_to` (target structure slot/file). **The `required: yes` rows ARE the validation contract for BOTH project-brief (final check) and project-scaffold (re-check) — now also machine-checked by `icm validate` (the `maps_to` binding) and `icm lint`.** |
| 4 | Folder tree | project-scaffold, session-learnings | Exact tree to create, layer-annotated, with `{slots}` filled from the brief |
| 5 | Layer map | project-scaffold, session-learnings | Table mapping every path to L0/L1/L2/L3/L4 |
| 6 | CLAUDE.md template (L0) | project-scaffold | Map-only template with `{slots}`; keep < 200 lines; **NO routing table**. Its **Avoid** section must be authored as **`### Hard constraints`** (user guardrails, incl. the secrets baseline) + **`### Soft defaults`** (researched/assumed defaults & the scope/off-stack/refactor baselines — each carrying a date + provenance, revisitable: ARA §7.4), and is **never empty** (see "Avoid is a guardrail" below). |
| 7 | CONTEXT.md templates | project-scaffold | Root router (L1, **NO folder map**) + one per workspace/stage (L2): What-this-is / What-to-load (Load + Skip) / Folder / Process / Skills & Tools / What-NOT-to-do |
| 8 | Naming conventions | project-scaffold, session-learnings | File-naming patterns table |
| 9 | Learning-routing rules | session-learnings | Table: category → recurrence test → destination file+section → insert format; plus an explicit **DISCARD** row for one-offs. A `thing-to-avoid` routes to `CLAUDE.md` → Avoid → **Soft defaults** (never Hard), with date + `provenance: learned`. |
| 10 | Existing-repo mapping (brownfield) | adopt-project, project-scaffold (overlay) | How to recognize an existing repo's parts and map them onto this type's ICM layers **without moving files**: which files reveal the researchable fields, and which existing dirs map to which workspace/layer |

### Avoid is a guardrail, not paperwork (applies to every type)
The L0 `CLAUDE.md` **Avoid** section steers every future session away from the wrong tech, scope, or
areas it shouldn't touch. So it should **almost never be empty**: each type's §6 template defines a
small set of **baseline avoids** (scope, off-stack tech, secrets, unrelated refactors) that always
render, and `project-brief` / `adopt-project` **propose project-specific avoids/constraints the
baselines don't already cover** when the user names none (de-dupe overlaps — keep the specific one).
Treat an empty Avoid as a sign the brief missed something — dig, don't pass.

### Validation & provenance (`icm lint` / `icm validate`)
The structure is **machine-checked** — and mechanically, not by LLM judgment (ARA found mechanical
checks catch ~100% of injected defects vs ~22% for an LLM-judged check):
- **`icm lint`** validates each type file against this FORMAT SPEC (`status: complete` strictly,
  `status: stub` leniently — a stub passes, its TODO sections are reported as info). Run it after
  editing a type: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/icm" lint --type <type> --strict`.
- **`icm validate project <dir>`** validates a scaffolded/overlaid project: no unfilled `{slots}`,
  the L0/L1 split, every router target resolves, every required field's value landed (the `maps_to`
  binding), the manifest is well-formed, and — brownfield — that **no pre-existing file was modified**
  (re-hashing `.icm/baseline.json`). `project-scaffold` runs it in a generate→validate→fix loop.

Both are **registry-driven** — they parse the type file and never hardcode a type — so completing a
stub or adding a type needs **no validator change** (the same property as "No skill code changes" below).

**Provenance vocabulary** (used by the brief's Structure Manifest and the Avoid Hard/Soft split):
`user` · `user-confirmed-default` · `assumed-default` · `inferred-from-repo` (brownfield) · `learned`
(session-learnings) · `scaffold-baseline` (a §6 template baseline avoid).

### The layer split (do not violate)
- **`CLAUDE.md` (L0) = THE MAP.** Always loaded → every line costs tokens in every conversation.
  Identity, folder tree, naming, commands, avoid, current-state. Keep < 200 lines. **No routing tables.**
- **Root `CONTEXT.md` (L1) = THE ROUTER.** Loaded on navigation. Task→workspace table, workspace
  summary, cross-workspace flow. ~30–50 lines. **No folder map, no naming rules.**
- **Workspace `CONTEXT.md` (L2) = THE CONTRACT.** What this workspace is, what to load/skip,
  its process, its skills, what not to do.

### Shape conventions
- **`workspace`** → parallel **named** folders (e.g. `coding`: planning/src/docs/ops). Root
  `CONTEXT.md` routes by task → workspace.
- **`pipeline`** → sequential **numbered** stages `NN_*` (e.g. `01_ideas/ → 02_drafts/ → …`),
  usually under a `stages/` folder with its own stage-router `CONTEXT.md`. Each stage's output
  feeds the next. The folder SHAPE differs; the L0–L4 PRINCIPLES are identical.

---

## Adding a new type — checklist

1. Copy an existing file (or a stub) to `registry/<new-type>.md` (bundled), or to
   `~/.claude/icm/registry/<new-type>.md` to add it just for yourself.
2. Fill all 10 sections + frontmatter following the FORMAT SPEC above.
3. Add a row to the **Type Table** (type, shape, status, identity, match signals).
4. Set `status: complete` and `version: 1` when the type is fully usable.
5. **No skill code changes are needed** — the skills pick up the new file automatically.

When you change an existing type's structure, also update its §3 questions and §9
learning-routing in the **same file** (they live together so they can't drift). Bump `version`.
