# Implementation Plan: Phiên học từ vựng đầu tiên

Spec: docs/specs/first-vocabulary-session/Specification.md

## Approach

### Approaches considered

1. **Two Vercel projects in one monorepo — recommended.** `frontend/` and `backend/` build
   independently, use explicit environment configuration and can be verified separately.
   The cost is CORS and two deployment URLs.
2. **One Vercel project with multiple Services.** Provides one domain and coordinated routing,
   but adds a newer deployment abstraction and couples release configuration before the MVP
   needs it.
3. **FastAPI serves the Angular build.** Provides one process locally, but couples Python
   deployment to frontend assets and works against independent framework build/deploy flows.

The plan uses approach 1. Angular is a standalone client-side application. FastAPI exposes a
versioned lesson endpoint and owns all AI interaction. Frontend session state keeps ratings
and review cards in `sessionStorage`, matching the MVP's anonymous, same-browser scope.

The AI boundary uses an adapter interface. The first adapter uses the official OpenAI Python
SDK with a configurable model and structured output validated against the same lesson schema
returned by the API. Missing configuration, refusal, timeout, provider error or schema
failure selects a validated built-in HSK 1 lesson. No live AI call is required for local use
or automated tests.

Vercel deployment uses two projects configured with root directories `frontend` and
`backend`. Angular builds static browser assets; FastAPI exports a recognized ASGI `app`
entrypoint. Local Angular requests under `/api` are proxied to Uvicorn.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/app.py` | Export the FastAPI ASGI application for Vercel discovery. | API boundary |
| `backend/hsk_api/main.py` | Construct the application, middleware and routers. | FR-16, FR-18 |
| `backend/hsk_api/config.py` | Validate server-only environment configuration. | FR-14, FR-18 |
| `backend/hsk_api/models/lesson.py` | Define validated lesson and vocabulary-card contracts. | FR-3, FR-4 |
| `backend/hsk_api/content/default_lesson.py` | Own the controlled five-card HSK 1 fallback lesson. | FR-3, FR-4, FR-15 |
| `backend/hsk_api/adapters/base.py` | Define the lesson generator boundary. | FR-14 |
| `backend/hsk_api/adapters/openai_lessons.py` | Generate structured lesson content without exposing credentials. | FR-14, FR-15, FR-18 |
| `backend/hsk_api/services/lessons.py` | Select generated content or fallback and report its source. | FR-14, FR-15 |
| `backend/hsk_api/routers/health.py` | Expose a deployment health signal. | Deployment verification |
| `backend/hsk_api/routers/lessons.py` | Expose the versioned recommended-lesson contract. | FR-1–FR-4, FR-14–FR-18 |
| `backend/tests/` | Verify models, fallback, adapter error handling and HTTP contract. | Backend FR coverage |
| `backend/pyproject.toml` | Declare Python version, runtime and test tooling. | Build/test |
| `backend/requirements.txt` | Provide Vercel-compatible production dependencies. | Deployment |
| `frontend/src/app/core/models/lesson.ts` | Represent the backend lesson contract in the client. | FR-3, FR-4 |
| `frontend/src/app/core/services/lesson-api.service.ts` | Load the recommended lesson from `/api`. | FR-1, FR-14–FR-16 |
| `frontend/src/app/core/services/study-session.service.ts` | Own current card, ratings, results and session persistence. | FR-7–FR-13 |
| `frontend/src/app/features/dashboard/` | Present the recommended lesson and HSK path entry. | `learning-dashboard.md` |
| `frontend/src/app/features/lesson-overview/` | Present lesson scope and start action. | `lesson-overview.md` |
| `frontend/src/app/features/study/` | Present flip-card reveal/rating flow. | `flip-card-study.md` |
| `frontend/src/app/features/results/` | Present summary, review and return actions. | `session-results.md` |
| `frontend/src/app/app.routes.ts` | Define the prototype's screen sequence as routes. | Prototype transitions |
| `frontend/src/styles.scss` | Define responsive visual tokens and shared presentation. | All wireframes |
| `frontend/proxy.conf.json` | Proxy local `/api` requests to FastAPI. | Local integration |
| `frontend/src/environments/` | Supply production API base URL without secrets. | Deployment |
| `frontend/src/**/*.spec.ts` | Verify components, services, transitions and states. | Frontend FR coverage |
| `frontend/e2e/` | Verify the complete learner journey against a running system. | AC-1–AC-10 |
| `.env.example` | Document safe server/client environment variable names only. | FR-18 |
| `README.md` | Document local startup, tests and Vercel configuration. | Handoff |

## API Contract

- `GET /api/health` returns service status without configuration secrets.
- `GET /api/v1/lessons/recommended?level=1&size=5` returns one validated lesson.
- Response contains lesson identity, HSK level, Vietnamese title/goal, estimated minutes,
  exactly five cards and `source` (`ai` or `fallback`).
- Each card contains stable identity, simplified Chinese, pinyin, Sino-Vietnamese reading,
  Vietnamese meaning, Chinese example and Vietnamese example translation.
- Provider failures are not surfaced as learner-blocking HTTP failures when fallback is
  available.

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1 | Dashboard component test plus journey E2E verifies recommended lesson and start action. |
| FR-2 | Lesson overview component test verifies goal, count, duration and learning supports. |
| FR-3 | Backend schema/fallback tests and frontend contract test assert exactly five cards. |
| FR-4 | Backend validation tests assert every required card field; study component renders them. |
| FR-5 | Study component test asserts answer content is hidden before reveal. |
| FR-6 | Study component test asserts answer and two rating actions appear after reveal. |
| FR-7 | Session service/component tests reject rating before reveal. |
| FR-8 | Study component test verifies current/total progress for each card. |
| FR-9 | Session service tests verify exactly one advance per accepted rating. |
| FR-10 | Session service and results component tests verify counts and review list. |
| FR-11 | Results-to-review route test verifies only unremembered cards are included. |
| FR-12 | Router/component test verifies return to dashboard. |
| FR-13 | Session service test reconstructs state from browser session storage. |
| FR-14 | Lesson service test with a successful fake generator and adapter contract test. |
| FR-15 | Parameterized backend tests cover missing key, timeout, provider error and invalid schema. |
| FR-16 | Component/service tests cover loading, empty, error and populated states. |
| FR-17 | Component tests assert Vietnamese labels for primary controls and explanations. |
| FR-18 | Config/API tests and built-asset scan assert the test secret never appears. |

## Risks / Open Questions

- OpenAI model availability and cost can change; model name remains server configuration and
  fallback keeps the learner flow available.
- AI-generated Vietnamese and HSK correctness needs a future content-evaluation suite; MVP
  enforces schema and HSK level but cannot prove pedagogical correctness automatically.
- Separate Vercel preview domains require explicit CORS configuration.
- Browser-session persistence intentionally does not meet long-term retention metrics; that
  belongs to the later progress epic.
- A real production deploy requires the user's Vercel account/project authorization and
  environment secrets; readiness can be proven locally without exposing those secrets.

## Related ADRs

- docs/adr/2026-07-30-ai-generated-lessons.md
- docs/adr/2026-07-30-fastapi-angular-vercel.md
- docs/adr/2026-07-30-separate-vercel-projects.md
- docs/adr/2026-07-30-lesson-api-contract.md

## Official Platform References

- Angular local setup and build: https://angular.dev/tools/cli/setup-local
- Angular deployment: https://angular.dev/tools/cli/deployment
- FastAPI deployment concepts: https://fastapi.tiangolo.com/deployment/
- FastAPI on Vercel: https://vercel.com/docs/frameworks/backend/fastapi
- Vercel monorepos: https://vercel.com/docs/monorepos
- OpenAI structured outputs: https://developers.openai.com/api/docs/guides/structured-outputs
