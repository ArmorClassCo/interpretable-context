# Project Brief: ToolShare

- **Type:** coding
- **Created:** 2026-06-05

## Identity
- Goal: Let neighbors lend and borrow tools.
- Users: Local residents who occasionally need a tool; main action is to list a tool or request a borrow.
- Platform: web

## Structure Manifest
- goal: Let neighbors lend and borrow tools.  [user]
- app_name: ToolShare  [user]
- users: Local residents who occasionally need a tool; main action is to list a tool or request a borrow.  [user]
- platform: web  [user]
- key_features: list a tool; browse nearby tools; request a borrow; confirm a return; basic profile  [user]
- frontend_stack: Next.js (React)  [user-confirmed-default]
- backend_stack: Next.js API routes (Node)  [user-confirmed-default]
- data_store: Supabase (Postgres)  [user-confirmed-default]
- auth: Supabase Auth (email magic link)  [assumed-default]
- hosting: Vercel  [user-confirmed-default]
- package_manager: npm  [assumed-default]

## Things to Avoid
### Hard (never cross)
- Don't add payments or checkout in v1.
- Don't store exact home addresses — neighborhood-level location only.
### Soft (revisitable defaults)
- Prefer not to add a native mobile app until the web app is validated.

## Reference Material to Seed (L3)
- none

## Provenance
- User-provided: goal, app_name, users, platform, key_features
- User-confirmed defaults: frontend_stack, backend_stack, data_store, hosting
- Assumed defaults: auth, package_manager
