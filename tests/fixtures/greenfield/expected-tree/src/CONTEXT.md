# src

## What This Workspace Is
The application code. Frontend: Next.js (React). Backend: Next.js API routes (Node). Data: Supabase (Postgres).

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Implement a feature | the spec from `../planning/specs/`, this file's "Patterns" | `docs/`, `ops/` |
| Fix a bug | this file's **Known Gotchas** first; then the failing area; relevant architecture note | unrelated specs |
| Refactor | "Patterns We Follow"; affected files | `docs/` |

## Folder Structure
```
src/   application code; structure follows the Next.js (React) / Next.js API routes (Node) convention
```

## Patterns We Follow
- Build to the spec's acceptance criteria; verify before calling a feature done.
- A repeated, deterministic step becomes a script in `../ops/scripts/` + a CLAUDE.md Commands row — from then on code does it, not judgment.

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

> Baseline skills for this project type. If one isn't installed, install it: superpowers → https://github.com/obra/superpowers · Context7 MCP → https://github.com/upstash/context7

## What NOT to Do
- Don't add a dependency or service that contradicts the chosen stack or the brief's constraints.
- Don't bypass the spec — if scope changes, update the spec first.
- Don't refactor unrelated code as a side effect — keep each change scoped to its task.
