# src

## What This Workspace Is
The application code. Frontend: Next.js (React). Backend: Next.js API routes (Node). Data: Supabase (Postgres).

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Implement a feature | the spec from `../planning/specs/`, this file's "Patterns" | `docs/`, `ops/` |
| Fix a bug | the failing area; relevant architecture note | unrelated specs |
| Refactor | "Patterns We Follow"; affected files | `docs/` |

## Folder Structure
```
src/   application code; structure follows the Next.js (React) / Next.js API routes (Node) convention
```

## Patterns We Follow
- Build to the spec's acceptance criteria; verify before calling a feature done.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| `superpowers:test-driven-development` | Before writing feature code | Tests first |
| `superpowers:systematic-debugging` | On any bug or unexpected behavior | Root-cause before fixing |
| Context7 MCP | Need current library docs mid-build | Fetch accurate API usage |

## What NOT to Do
- Don't add a dependency or service that contradicts the chosen stack or the brief's constraints.
- Don't bypass the spec — if scope changes, update the spec first.
- Don't refactor unrelated code as a side effect — keep each change scoped to its task.
