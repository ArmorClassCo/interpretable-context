# ops

## What This Workspace Is
Getting the app running and keeping it healthy. Hosting: Vercel. Reusable scripts (L3) live
here; per-run output (L4) does too.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Deploy | `deploy/` config; CLAUDE.md Commands | `planning/specs/`, `docs/guides` |
| Add a reusable script | existing `scripts/` for conventions | `src/` internals |
| Investigate an incident | this file's **Known Gotchas** first; `monitoring/`; relevant architecture note | docs |

## Folder Structure
```
ops/
├── deploy/      deployment configuration (stable) + run artifacts
├── monitoring/  logs, alerts, dashboards config
└── scripts/     reusable project scripts ({verb}-{noun}.sh)
```

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
| Context7 MCP | Configuring Vercel or any infra service | Current docs for the hosting platform / CLI |

> Baseline tools for this project type. If Context7 MCP isn't installed, install it: https://github.com/upstash/context7

## What NOT to Do
- Don't hardcode secrets in `deploy/` — reference the host's secret store (Vercel).
