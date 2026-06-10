# ops

## What This Workspace Is
Getting the app running and keeping it healthy. Hosting: Docker (self-hosted). Covers the existing
root `Dockerfile`; reusable scripts live here.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Build / deploy | the root `Dockerfile`; CLAUDE.md Commands | `planning/specs/`, `docs/guides` |
| Add a reusable script | existing conventions | `src/` internals |
| Investigate an incident | this file's **Known Gotchas** first; relevant architecture note | docs |

## Known Gotchas
<!-- Diagnostic memory for deploy & infra quirks: symptom → likely cause → fix/check.
     session-learnings appends recurring gotchas below this line -->
- None recorded yet.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| Context7 MCP | Configuring Docker (self-hosted) or any infra service | Current docs for the hosting platform / CLI |

> Baseline tools for this project type. If Context7 MCP isn't installed, install it: https://github.com/upstash/context7

## What NOT to Do
- Don't hardcode secrets in the `Dockerfile` — reference the host's secret store (Docker (self-hosted)).
