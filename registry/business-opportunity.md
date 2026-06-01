---
type: business-opportunity
version: 0
shape: pipeline
status: stub
match_signals:
  - business idea
  - opportunity
  - market
  - validate
  - go-to-market
  - monetize
  - startup
  - venture
  - business model
---

# Registry Type: business-opportunity   (STUB)

> Recognized by the classifier but **not fully built**. Completing it = filling the TODO
> sections below following the FORMAT SPEC in `_index.md`. No skill code changes needed once
> filled. Until then, `project-brief` tells the user this type isn't fully set up and offers to
> proceed minimally or pick a completed type.

## 1. Identity  (consumed by: project-brief)
Evaluate and develop a business idea or opportunity — moving from a raw idea through research,
validation, a business model, and a go-to-market plan. Use when the deliverable is a decision /
plan about a venture, not a built product (if they want to BUILD the product, that's `coding`).

## 2. Match signals  (consumed by: project-brief)
Strong: business idea, opportunity, market, validate, go-to-market, monetize, startup, venture,
business model. Weak/ambiguous: "platform" / "app idea" (could be `coding` if they want it built) —
confirm whether they want to evaluate the opportunity or build the product.

## 3. Brief question set  (consumed by: project-brief)
TODO: complete this type. Minimum rows to define before use:

| id | prompt | source | required | maps_to |
|----|--------|--------|----------|---------|
| `idea` | "What's the idea, in a sentence or two?" | user-only | yes | CLAUDE.md identity |
| `customer` | "Who has the problem you'd solve?" | user-only | yes | research stage |
| `unknowns` | "What are you most unsure about?" | user-only | yes | validation stage |
<!-- TODO: add market-size, competition, monetization, GTM, naming, etc. -->

## 4. Folder tree  (consumed by: project-scaffold, session-learnings)
TODO: complete this type. Sketch (pipeline shape):
```
{venture}/
├── CLAUDE.md   (L0)
├── CONTEXT.md  (L1)
├── .icm/ ...
└── stages/
    ├── CONTEXT.md              (L1/L2 pipeline router)
    ├── 01_research/           (L4)
    ├── 02_validation/         (L4)
    ├── 03_business-model/     (L4)
    └── 04_go-to-market/       (L4)
```

## 5. Layer map        TODO: complete this type.
## 6. CLAUDE.md template (L0)   TODO: complete this type. (Map-only, NO routing table.)
## 7. CONTEXT.md templates       TODO: complete this type. (Root router + stage router + per-stage L2.)
## 8. Naming conventions         TODO: complete this type.
## 9. Learning-routing rules     TODO: complete this type.
## 10. Existing-repo mapping (brownfield)  (consumed by: adopt-project, project-scaffold overlay)
TODO: complete this type. (How existing research/validation docs map onto the pipeline stages — without moving files.)
