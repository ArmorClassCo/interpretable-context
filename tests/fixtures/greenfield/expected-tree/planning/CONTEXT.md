# planning

## What This Workspace Is
Where features get thought through before code. Specs say WHAT to build (one-off, L4);
architecture/ and decisions/ capture the stable reasoning (L3) that recurs across features.

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Write a feature spec | the goal, `architecture/` if it touches structure | `src/`, `docs/` |
| Record a decision (ADR) | the options considered | everything else |
| Revisit a past decision | the relevant `decisions/YYYY-MM-DD_*.md` | specs |

## Folder Structure
```
planning/
├── specs/          one spec per feature ({feature}-spec.md)
├── architecture/   stable design notes (data model, key flows)
└── decisions/      ADRs, dated
```

## The Process
1. New feature -> write `specs/{feature}-spec.md`: what, who it's for, what "done" looks like.
2. A choice with lasting consequences -> write an ADR in `decisions/`.
3. Specs are contracts, not code: they say WHAT and the acceptance criteria, not HOW.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| Web research | While speccing, to check current best practice | Validate an approach is still recommended |
| `superpowers:writing-plans` | Turning a spec into an executable plan | Structured implementation planning |

## What NOT to Do
- Don't put implementation code here — that's `src/`.
- Don't let a spec dictate line-by-line implementation; leave the builder room.
