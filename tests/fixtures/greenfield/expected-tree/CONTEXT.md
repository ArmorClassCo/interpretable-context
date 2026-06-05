# ToolShare — Task Router

CLAUDE.md (always loaded) has the folder map and naming. This file routes you to work.

## Task Routing
| Your Task | Go Here | You'll Also Need |
|-----------|---------|------------------|
| Plan a feature / write a spec | `planning/CONTEXT.md` | the goal + key features |
| Write or change app code | `src/CONTEXT.md` | the relevant spec from `planning/specs/` |
| Record an architecture decision | `planning/CONTEXT.md` | — |
| Write user/developer docs | `docs/CONTEXT.md` | the feature it documents |
| Deploy / configure infra / scripts | `ops/CONTEXT.md` | hosting = Vercel |

## Workspace Summary
| Workspace | Purpose |
|-----------|---------|
| `planning/` | Decide what to build and why. Specs (L4) + architecture & decisions (L3). |
| `src/` | The application code. Conventions live in its CONTEXT.md. |
| `docs/` | API docs, guides, changelog. |
| `ops/` | Deploy, monitoring, reusable scripts. |

## Cross-Workspace Flow
```
planning/specs  ->  src (implements the spec)  ->  docs (documents what shipped)
planning/architecture & decisions  inform every workspace (load on demand)
ops  <- consumes src build output for deploy
```
