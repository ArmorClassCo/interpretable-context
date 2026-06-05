# docs

## What This Workspace Is
User- and developer-facing documentation: API reference, how-to guides, changelog.
Downstream of `src/` — documents what actually shipped.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Document an API | the relevant `../src/` code | `planning/`, `ops/` |
| Write a how-to guide | the feature; the goal for tone | architecture internals |
| Update changelog | what changed this release | everything else |

## Folder Structure
```
docs/
├── api/         endpoint / interface reference
├── guides/      task-oriented how-tos
└── changelog.md dated, user-visible changes
```

## The Process
- Document after a feature is verified, not before.
- Guides are task-oriented ("How to reset a password"), not exhaustive.

## What NOT to Do
- Don't duplicate architecture rationale here — link to `planning/decisions/`.
