# ops

## What This Workspace Is
Getting the app running and keeping it healthy. Hosting: Docker (self-hosted). Covers the existing
root `Dockerfile`; reusable scripts live here.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Build / deploy | the root `Dockerfile`; CLAUDE.md Commands | `planning/specs/`, `docs/guides` |
| Add a reusable script | existing conventions | `src/` internals |

## What NOT to Do
- Don't hardcode secrets in the `Dockerfile` — reference the host's secret store (Docker (self-hosted)).
