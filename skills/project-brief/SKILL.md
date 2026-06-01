---
name: project-brief
description: Use when someone is starting a new project, app, website, tool, SaaS, or product and its structure needs planning before any folders or code exist — triggers on "I want to build…", "I have an idea for an app", "starting a new project", "set up a workspace", "help me plan my product". Especially for non-technical builders who know their goal but not the tech: it researches the technical choices and asks only for plain-language confirmation, then writes a PROJECT-BRIEF.md that project-scaffold turns into a real folder structure. Use it for any new-project setup even if the user never says "brief".
allowed-tools: Read, Write, WebSearch, WebFetch, AskUserQuestion, Bash
---

# project-brief

## What this produces and why

This skill produces one file — `PROJECT-BRIEF.md` — that contains **everything the
`project-scaffold` skill needs to build the project's structure, with nothing missing.** It does
*not* build the application; it captures the structural decisions that make building it far
easier later.

The reason a brief exists as a separate step: the person with the idea usually isn't the person
who knows the tech. So this skill splits the work — it **asks the user only what only they can
know** (their goal, their users, what it must do) and **researches everything technical itself**
(stack, hosting, conventions), proposing sensible defaults in plain language. That way a
non-technical builder gets a complete, correct brief without being interrogated about things they
shouldn't have to know.

## The registry is the source of truth

Every project **type** (coding, content, client, business-opportunity) defines its own questions.
Read them from the registry — never invent questions.

**Registry location & lookup order.** The registry ships inside this plugin at
`${CLAUDE_PLUGIN_ROOT}/registry/`. For any registry file, check `~/.claude/icm/registry/<file>`
first — if it exists, use it (the user's override) — otherwise use `${CLAUDE_PLUGIN_ROOT}/registry/<file>`
(the bundled default).

- `<registry>/_index.md` — the Type Table (for classifying) + the format spec.
- `<registry>/<type>.md` — the chosen type's §3 "Brief question set".

Read only the index plus the one relevant type file.

## Process

### 1. Capture the goal in plain language
Ask what they want to build and who it's for — in their words. Note anything they volunteer
(tech preferences, constraints, examples); you'll skip researching whatever they already gave you.

**If they already have an existing codebase/repo** they want to add structure to (rather than a
brand-new idea), this is the wrong skill — hand off to **`adopt-project`**, which analyzes the repo
and writes the brief from what's already there. Use `project-brief` for projects starting from scratch.

### 2. Classify the type — and ALWAYS confirm
Read `_index.md`'s Type Table and match the user's description against the `match signals`.
- **Clear match** → confirm in one line: *"This looks like a **coding** project (you want to
  build software) — is that right?"* Proceed only after a yes.
- **Ambiguous / only weak signals** → present the plausible types as options and let them pick.
- **Never classify silently.** A wrong type means the wrong questions and the wrong structure, so
  the cheap confirmation up front saves a lot.
- If the matched type has `status: stub`, say so honestly: *"That type isn't fully set up yet — I
  can capture a basic brief, but the structure will be minimal. Want to proceed that way, or treat
  this as a `coding` project?"*

### 3. Load the type's question set
Read the type's registry file (`<registry>/<type>.md`, resolved per the lookup order above) and find
its §3 table. Each question has a `source` (`user-only` or `researchable`) and a `required` flag.

### 4. Ask the `user-only` questions
Ask these in plain language, conversationally. These are the things only the user knows: the goal,
the users, what it must do, hard constraints, things they already know they don't want. **Include the
`known_tools` question** — "Are there any tools, services, or systems you already know you want to
use?" — and capture whatever they name. Keep it light — don't turn it into a form.

**Don't let Avoid go empty.** `constraints` and `things_to_avoid` are guardrails — they keep future
sessions from wandering into the wrong tech, scope, or areas they shouldn't touch. `project-scaffold`
already adds generic baselines (scope, off-stack tech, secrets, unrelated refactors), so if the user
names none, **propose 2–4 PROJECT-SPECIFIC ones the baselines won't cover** (e.g. features to leave
out, areas/data to leave alone, budget or compliance limits) and confirm. A completely empty Avoid
usually means the brief missed something — treat it as a prompt to dig, not a pass.

### 5. Research the `researchable` gaps — propose, don't interrogate
**First, honor what they already chose.** Treat any `known_tools` answers (and other volunteered
preferences) as fixed constraints: research and propose defaults *around* them, and never propose an
alternative to a tool the user already said they want. If a `known_tools` choice already answers a
researchable field (e.g. they named a database), fill it from their answer and skip the search.

For each `researchable` question the user hasn't already answered:
- Do **one** focused web search (use the session's web tool — WebSearch/WebFetch, or whatever
  web/research tool is configured) to find the current sensible default for *this* kind of project.
- Propose **one** recommendation with a **one-sentence, jargon-free rationale**, and ask to confirm.
  Example: *"For saving the app's data I'd suggest **Supabase** — it gives you a database and user
  logins without running your own server. Good with you, or do you have something in mind?"*
- If they have a preference, use it. If they don't care, take your recommendation.

**Research discipline:** one search, one proposed default, plain rationale, confirm. Do **not**
present trade-off matrices or three competing options to a non-technical user — that just shifts
the burden back onto them, which is the whole thing we're avoiding. (If the user is clearly
technical and wants options, it's fine to offer them.)

### 6. Validation pass — the zero-missing-context guarantee
Before writing, check that **every `required: yes` field is filled.** If any is empty, go back and
ask or research it. This check is what lets `project-scaffold` build the whole structure without
guessing. (The `required` flags are the shared contract both skills rely on — see the registry's
`MAINTAINING.md`.)

### 7. Decide where the brief lives
The brief must sit at the project root, because that's where `project-scaffold` will look and build.
- If the user is already in the intended project folder, write it there.
- If there's no folder yet, ask for a path in plain terms (*"Where should this project live? e.g.
  `~/projects/tool-library`"*), create **only that one directory**, and write the brief inside it.
  Do not create any other folders — scaffolding is `project-scaffold`'s job.

### 8. Write `PROJECT-BRIEF.md`
Use this structure:

```markdown
# Project Brief: {app_name}

- **Type:** {type}
- **Created:** {date}

## Identity
- Goal: {goal}
- Users: {users}
- Platform: {platform}

## Structure Manifest
<!-- one entry per field in the type's question set, mapping 1:1 to the structure
     project-scaffold will build. Include every answered question by its id. -->
- {id}: {answer}
- ...

## Things to Avoid
- {constraints and things_to_avoid, as bullets}

## Reference Material to Seed (L3)
- {anything the user gave to start from; "none" if nothing}

## Provenance
- User-provided: {list of ids}
- Researched: {list of ids, with the one-line rationale for each}
```

The **Structure Manifest** is the important part: it's the field-by-field answer set that
`project-scaffold` maps directly onto folders and templates. Provenance is there so a human can see
later which choices were theirs versus researched defaults.

### 9. Offer the next step
Tell the user the brief is written, and offer: *"Want me to build the folder structure now?"* If
yes, that's the `project-scaffold` skill. Do **not** auto-run it — offer and wait.

## Idempotency
If a `PROJECT-BRIEF.md` already exists at the target location, read it, show what's already there,
and ask before overwriting. Never silently clobber an existing brief.

## What NOT to do
- Don't build the application or scaffold folders — this skill only produces the brief (plus,
  if needed, the single empty project root directory).
- Don't ask the user technical questions they likely can't answer — research those instead.
- Don't skip the type confirmation, and don't proceed with empty `required` fields.
