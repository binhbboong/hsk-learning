# ADR: Optional adaptive HSK placement test

Date: 2026-08-01
Slug: optional-placement-test
Status: Accepted
Supersedes: 2026-07-31-beginner-first-learning-intelligence (entry-level decision only)
Related spec: docs/specs/hsk-placement-test/Specification.md

## Context

The beginner-first entry keeps onboarding simple, but learners with prior Chinese knowledge must
repeat HSK 1 content. The product now needs an optional, low-friction way to recommend a starting
level while preserving the safe default and all existing learning progress.

## Decision

New learners may take a server-scored, adaptive 20-question placement test across vocabulary,
grammar, listening and pronunciation, or skip it and start HSK 1. Before meaningful learning
progress exists, a learner may accept or override the recommended HSK 1–6 starting level. A higher
starting level is applied only after its first five-lesson daily path has been prepared successfully.

Retakes after learning are advisory and never reset progress. Placement activity does not affect
lesson completion, checkpoints, SRS, retention metrics or streaks. Audio is analyzed ephemerally.

## Consequences

- Beginner onboarding remains one click away through “Start HSK 1”.
- Experienced learners can avoid clearly unsuitable beginner material.
- The server needs durable attempt state, a reviewed question bank and scoring governance.
- Applying HSK 2–6 depends on successful path generation and must fail atomically.
- Placement confidence may be lower when pronunciation cannot be assessed.
- Analytics must distinguish placement evidence from ongoing learning evidence.
