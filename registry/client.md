---
type: client
version: 0
shape: workspace
status: stub
match_signals:
  - client
  - engagement
  - retainer
  - deliverable
  - account
  - agency
  - stakeholder
  - consulting
---

# Registry Type: client   (STUB)

> Recognized by the classifier but **not fully built**. Completing it = filling the TODO
> sections below following the FORMAT SPEC in `_index.md`. No skill code changes needed once
> filled. Until then, `project-brief` tells the user this type isn't fully set up and offers to
> proceed minimally or pick a completed type.

## 1. Identity  (consumed by: project-brief)
Manage deliverables for an external client / engagement. Use when the work is organized around
one or more clients, each with intake, deliverables, and communications, plus shared templates.

## 2. Match signals  (consumed by: project-brief)
Strong: client, engagement, retainer, deliverable, account, agency, stakeholder, consulting.
Weak/ambiguous: "project for X" (could be `coding`) — confirm.

## 3. Brief question set  (consumed by: project-brief)
TODO: complete this type. Minimum rows to define before use:

| id | prompt | source | required | maps_to |
|----|--------|--------|----------|---------|
| `practice` | "What do you do for clients, in a sentence?" | user-only | yes | CLAUDE.md identity |
| `clients` | "Which client(s) are we setting up first?" | user-only | yes | clients/* folders |
| `deliverables` | "What do you typically deliver?" | user-only | yes | templates; deliverables folders |
<!-- TODO: add confidentiality rules, review process, naming, etc. -->

## 4. Folder tree  (consumed by: project-scaffold, session-learnings)
TODO: complete this type. Sketch (workspace shape):
```
{practice}/
├── CLAUDE.md   (L0)
├── CONTEXT.md  (L1)
├── .icm/ ...
├── clients/
│   └── {client}/  CONTEXT.md(L2) · intake/(L4) · deliverables/(L4) · communications/(L4)
├── templates/     CONTEXT.md(L2) · proposals/(L3) · reports/(L3) · emails/(L3)
└── business-dev/  CONTEXT.md(L2) · pipeline/(L4) · outreach/(L4) · case-studies/(L4)
```

## 5. Layer map        TODO: complete this type.
## 6. CLAUDE.md template (L0)   TODO: complete this type. (Map-only, NO routing table.)
## 7. CONTEXT.md templates       TODO: complete this type. (Root router + per-workspace L2.)
## 8. Naming conventions         TODO: complete this type.
## 9. Learning-routing rules     TODO: complete this type.
## 10. Existing-repo mapping (brownfield)  (consumed by: adopt-project, project-scaffold overlay)
TODO: complete this type. (How an existing client/deliverables folder set maps onto the workspaces — without moving files.)

> Note: client work has a hard **confidentiality** rule (never cross-reference one client's
> info in another's workspace). Bake that into §6/§7 when completing this type.
