# ADR: Gate HSK promotion with a level exam

Date: 2026-08-01
Slug: level-exam-promotion-gate
Status: Accepted
Supersedes: promotion decision in 2026-07-31-progressive-hsk-ai-paths
Related spec: docs/specs/hsk-level-exams/Specification.md

## Context

The current path promotes a learner immediately after a five-lesson checkpoint score of at least
80% and vocabulary retention of at least 70%. That checkpoint measures one Day, not the breadth of
an HSK level, so it is too narrow to be the final promotion signal.

## Decision

Checkpoint and retention remain prerequisites. Once both thresholds are met, the learner must also
pass a server-scored 20-question level exam covering vocabulary, grammar, reading and listening.
Passing requires at least 80% overall and at least 60% in every skill. HSK 1–5 passes unlock the next
level; an HSK 6 pass completes the journey. Failed exams never reset learning progress.
The immutable exam is derived from the five lessons just completed, so it stays aligned with learned
content and does not require another AI request.

## Consequences

- Promotion has broader evidence than a single checkpoint.
- Learners get skill-specific remediation before retrying.
- Daily-path generation must expose an exam-required state instead of auto-promoting.
- The server must persist immutable exam snapshots, attempts and results.
- The quality of the exam depends on the reviewed or AI-generated source lessons.
