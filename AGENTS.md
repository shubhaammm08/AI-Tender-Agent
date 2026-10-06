# AGENTS.md

Rules for AI coding agents (Antigravity, Claude Code, Cursor) working in this repo.

## Before you code

1. Read `docs/ARCHITECTURE.md`, `docs/DATABASE.md` and the doc for the area you touch.
2. For any task larger than one file, write a short plan and wait for approval.
3. Work on Phase 1 scope only unless told otherwise (see `docs/ROADMAP.md`).

## Hard rules

- A human approves every bid. Never add code that submits a bid automatically.
- Never store, log or transmit DSC private keys or tokens.
- Every table has `tenant_id`. Every query filters by it. Add a test for each new query path.
- Eligibility is decided by code in `packages/rules`, never by the LLM. The LLM extracts and explains.
- Every extracted requirement stores source file, page, clause and confidence.
- Every AI output writes an `audit_log` entry (model, prompt version, sources, actor).
- Never log document contents or personal data.
- Call LLMs only through `LLMClient`. Do not import a provider SDK elsewhere.
- Portal parsers are versioned. Do not edit an old version in place when a portal changes. Add a new one.

## Commands

| Task | Command |
|---|---|
| Start everything | `docker compose up --build` |
| API tests | `docker compose exec api pytest` |
| Web tests | `pnpm --filter web test` |
| E2E | `pnpm --filter web playwright test` |
| Migrations | `docker compose exec api alembic revision --autogenerate -m "msg"` then `alembic upgrade head` |
| Eval | `python eval/run_eval.py` |
| Lint | `ruff check . && pnpm lint` |

## Code style

- Python: type hints, ruff, small functions, no hidden global state.
- TypeScript: strict mode, no `any`, server components by default.
- Comments only where intent is not obvious.
- No new dependency without a one-line reason in the PR.

## Definition of done

Tests pass, migration included, docs updated, no secrets in code, audit entries added for AI actions.
