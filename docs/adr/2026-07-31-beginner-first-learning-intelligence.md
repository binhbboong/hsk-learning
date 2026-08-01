# ADR: Beginner-first learning intelligence

Date: 2026-07-31
Slug: beginner-first-learning-intelligence
Status: Superseded by 2026-08-01-optional-placement-test (entry-level decision only)
Related spec: docs/specs/learning-intelligence-operations/Specification.md

## Context

HSK Learning is explicitly for Vietnamese beginners. The next increment adds adaptive content
operations, pronunciation feedback, progress insights and content administration. A placement test
would add friction and contradict the requested beginner-first entry point. AI-generated content
also needs observable quality and cost boundaries.

## Decision

Every new learner starts at HSK 1, difficulty 1, without a placement test. Adaptation happens only
from evidence collected while learning.

AI paths pass deterministic scope, completeness and repetition checks before release. Content that
does not pass remains in a review queue; an authorized administrator can edit, approve or reject it.
Generation is limited by configurable daily account and system quotas, and usage is recorded.

Pronunciation feedback separates recognized-content confidence from syllable and tone observations,
shows Vietnamese correction guidance, and never presents itself as an official HSK score or a
teacher replacement.

## Consequences

- Onboarding stays immediate and predictable for beginners.
- Advanced learners are intentionally not placed into a higher starting level.
- Adaptation becomes evidence-based after learning begins.
- Some generated days may wait for review instead of being released.
- Operators gain a review workflow and usage visibility, with additional administration overhead.
- Acoustic feedback remains assistive and must communicate uncertainty.
