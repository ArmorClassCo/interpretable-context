# Project Brief: Notesy

- **Type:** coding
- **Origin:** brownfield (adopted from existing repo)
- **Created:** 2026-06-05

## Identity
- Goal: Capture and organize personal notes.
- Users: People who want quick personal notes.
- Platform: web

## Structure Manifest
- goal: Capture and organize personal notes.  [user]
- app_name: Notesy  [inferred-from-repo]
- users: People who want quick personal notes.  [user]
- platform: web  [inferred-from-repo]
- key_features: capture a note; organize notes; search notes  [user]
- frontend_stack: Next.js (React)  [inferred-from-repo]
- backend_stack: Next.js API routes (Node)  [inferred-from-repo]
- data_store: Postgres (Prisma)  [inferred-from-repo]
- hosting: Docker (self-hosted)  [inferred-from-repo]
- package_manager: npm  [inferred-from-repo]

## Existing Inventory
| Existing path | Maps to (ICM workspace / layer) | Notes |
|---------------|----------------------------------|-------|
| `src/app/`, `src/lib/` | src/ (L4 app code) | entry: src/app/page.tsx |
| `docs/architecture/` | planning/ → architecture (L3) | data-model.md |
| `docs/` | docs/ (L3/L4) | |
| `Dockerfile` | ops/ | root-level infra |
- Workspaces to ADD (absent in repo): planning/, ops/
- Directories left as-is: src/app, src/lib, docs/architecture

## Things to Avoid
### Hard (never cross)
- Don't modify the existing Dockerfile or build pipeline without recording an ADR.
### Soft (revisitable defaults)
- (none specific yet)

## Reference Material to Seed (L3)
- docs/architecture/data-model.md (existing)

## Provenance
- User-provided: goal, users, key_features
- Inferred from repo: app_name (package.json name), platform, frontend_stack (next/react in package.json), backend_stack, data_store (prisma dep + lib/db.ts), hosting (Dockerfile), package_manager (npm)
