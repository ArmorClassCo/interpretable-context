---
type: content
version: 0
shape: pipeline
status: stub
match_signals:
  - blog
  - article
  - newsletter
  - video
  - post
  - content
  - publish
  - editorial
  - writing
  - podcast
---

# Registry Type: content   (STUB)

> Recognized by the classifier but **not fully built**. Completing it = filling the TODO
> sections below following the FORMAT SPEC in `_index.md`. No skill code changes needed once
> filled. Until then, `project-brief` tells the user this type isn't fully set up and offers to
> proceed minimally or pick a completed type.

## 1. Identity  (consumed by: project-brief)
Produce written or media content through a publishing pipeline (idea → draft → edit → publish).
Use when the user wants to create and ship content regularly.

## 2. Match signals  (consumed by: project-brief)
Strong: blog, article, newsletter, video, post, content, publish, editorial, writing, podcast.
Weak/ambiguous: "content tool" (could be `coding`) — confirm.

## 3. Brief question set  (consumed by: project-brief)
TODO: complete this type. Minimum rows to define before use:

| id | prompt | source | required | maps_to |
|----|--------|--------|----------|---------|
| `goal` | "What are you publishing, and for whom?" | user-only | yes | CLAUDE.md identity |
| `cadence` | "How often do you publish?" | user-only | yes | pipeline stage sizing |
| `channels` | "Where does it go out?" | user-only | yes | output stage |
<!-- TODO: add voice/style, formats, research/sourcing, naming, etc. -->

## 4. Folder tree  (consumed by: project-scaffold, session-learnings)
TODO: complete this type. Sketch (pipeline shape):
```
{project}/
├── CLAUDE.md   (L0)
├── CONTEXT.md  (L1)
├── .icm/ ...
└── stages/
    ├── CONTEXT.md           (L1/L2 pipeline router)
    ├── 01_ideas/            (L4)
    ├── 02_drafts/           (L4)
    ├── 03_edit/             (L4)
    └── 04_published/        (L4)
```

## 5. Layer map  (consumed by: project-scaffold, session-learnings)
TODO: complete this type.

## 6. CLAUDE.md template (L0)  (consumed by: project-scaffold)
TODO: complete this type. (Map-only, < 200 lines, NO routing table.)

## 7. CONTEXT.md templates  (consumed by: project-scaffold)
TODO: complete this type. (Root router L1 + a stage-router + per-stage L2 contracts.)

## 8. Naming conventions  (consumed by: project-scaffold, session-learnings)
TODO: complete this type.

## 9. Learning-routing rules  (consumed by: session-learnings)
TODO: complete this type. (category → recurrence test → destination → insert format + DISCARD.)

## 10. Existing-repo mapping (brownfield)  (consumed by: adopt-project, project-scaffold overlay)
TODO: complete this type. (Which files reveal the researchable fields, and how existing folders map onto the pipeline stages — without moving files.)
