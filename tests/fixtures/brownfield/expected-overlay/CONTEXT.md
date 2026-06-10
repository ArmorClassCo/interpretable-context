# Notesy — Task Router

CLAUDE.md (always loaded) has the folder map and naming. This file routes you to work.

## Task Routing
| Your Task | Go Here | You'll Also Need |
|-----------|---------|------------------|
| Plan a feature / write a spec | `planning/CONTEXT.md` | the goal + key features |
| Write or change app code | `src/CONTEXT.md` | the relevant existing module |
| Fix a bug / debug a failure | `src/CONTEXT.md` | its **Known Gotchas** + the debugging skill it names |
| Write user/developer docs | `docs/CONTEXT.md` | the feature it documents |
| Deploy / configure infra | `ops/CONTEXT.md` | hosting = Docker (self-hosted) |

## Workspace Summary
| Workspace | Covers (existing) |
|-----------|-------------------|
| `planning/` | New: specs + architecture/decisions (architecture mirrors `docs/architecture/`). |
| `src/` | Existing app code: `src/app/`, `src/lib/`. |
| `docs/` | Existing docs, including `docs/architecture/`. |
| `ops/` | The existing root `Dockerfile` + future scripts. |

## Cross-Workspace Flow
```
planning/specs  ->  src (implements the spec)  ->  docs (documents what shipped)
ops  <- builds/deploys src (Dockerfile)
```
