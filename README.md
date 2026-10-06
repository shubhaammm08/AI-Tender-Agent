# AI Tender Agent

An AI employee for government tendering. Upload your company information once. AI finds tenders you can bid on and prepares the complete bid for you.

Built for Indian MSMEs and GeM sellers (IT, contractors, equipment, electrical and medical suppliers).

## Workflow

Find → Analyze → Decide → Prepare → Verify → Approve → Track

A human approves every bid. The app never submits a bid by itself and never stores a digital signature token (DSC).

## Status

Phase 1 (GeM discovery, analysis, Bid/No-Bid score, document vault). See [ROADMAP](docs/ROADMAP.md).

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS |
| Backend | FastAPI (Python 3.12), SQLAlchemy, Alembic |
| Database | PostgreSQL + pgvector |
| Queue and cache | Redis + Celery |
| Files | S3-compatible storage (MinIO locally) |
| Browser automation | Playwright (separate worker) |
| Local run | Docker Compose |

## Quick start

```bash
cp .env.example .env        # fill in LLM and storage keys
docker compose up --build
# web: http://localhost:3000   api: http://localhost:8000/docs
docker compose exec api alembic upgrade head
```

## Project structure

```
apps/web           Next.js frontend
apps/api           FastAPI backend
apps/worker        Celery tasks (OCR, extraction, portal jobs)
packages/adapters  Portal adapters (gem first)
packages/rules     Eligibility rules
packages/schemas   Universal tender model
eval/              Labeled tenders and accuracy tests
infra/             docker-compose, env examples, IaC
docs/              Project documentation
```

## Documentation

| Doc | What it covers |
|---|---|
| [PRD](docs/PRD.md) | Problem, users, scope, metrics |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Layers, modules, data flow |
| [DATABASE](docs/DATABASE.md) | Tables and key SQL |
| [API](docs/API.md) | Endpoints and conventions |
| [AI_PIPELINE](docs/AI_PIPELINE.md) | OCR, extraction, rules, generation |
| [PORTAL_ADAPTERS](docs/PORTAL_ADAPTERS.md) | How to add a portal |
| [SECURITY](docs/SECURITY.md) | Isolation, encryption, DPDP |
| [DESIGN_SYSTEM](docs/DESIGN_SYSTEM.md) | White and green UI rules |
| [ROADMAP](docs/ROADMAP.md) | Phases |
| [TESTING_AND_EVAL](docs/TESTING_AND_EVAL.md) | Tests and accuracy targets |
| [DEPLOYMENT](docs/DEPLOYMENT.md) | Environments, CI/CD, monitoring |
| [AGENTS](AGENTS.md) | Rules for AI coding agents |
| [CONTRIBUTING](CONTRIBUTING.md) | Workflow for contributors |

## Disclaimer

The product helps prepare bids. It does not guarantee eligibility or a win. Users are responsible for checking the final bid before submission.
