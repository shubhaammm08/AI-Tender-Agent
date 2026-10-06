# Architecture

A modular monolith with background workers. Split into services only when a module needs separate scaling.

## Layers

| Layer | Responsibility | Tech |
|---|---|---|
| Web | Dashboard, tender view, vault, approvals | Next.js |
| API | Auth, tenants, business logic, billing | FastAPI |
| Portal adapters | Fetch and normalize tenders | Playwright, HTTP |
| Document pipeline | OCR, file classification, BOQ parsing | Document AI / Surya, pandas |
| AI layer | Extraction, explanation, generation | LLM + RAG behind `LLMClient` |
| Rule engine | Eligibility and Bid/No-Bid score | Plain Python in `packages/rules` |
| Workflow | Long jobs, retries, reminders | Celery (Temporal later) |
| Notifications | WhatsApp, email, in-app | WhatsApp Cloud API |
| Storage | Data, vectors, files | PostgreSQL + pgvector, S3 |
| Cache | Rate limits, dedupe | Redis |
| Audit | Append-only action log | `audit_log` with hash chain |

## Modules (inside apps/api)

`auth`, `tenants`, `profile`, `portals`, `documents`, `vault`, `ai`, `rules`, `bids`, `reminders`, `audit`, `billing`.

Modules talk through service interfaces, not by reading each other's tables.

## Data flow

```
Portal adapter -> UniversalTender -> tenders (+ versions)
   -> download docs -> classify -> OCR / parse -> chunks + embeddings
   -> LLM extraction -> requirements (cited)
   -> rule engine (profile + vault) -> match score + reasons
   -> LLM explanation -> dashboard / WhatsApp
   -> (Phase 3) generate bid docs -> verify -> human approval -> audit
```

## Key decisions

| Decision | Reason |
|---|---|
| Modular monolith | Faster to build and debug for a small team |
| PostgreSQL + pgvector | Relational data and vectors in one store |
| Rules decide, LLM reads and explains | Auditable and testable decisions |
| Adapters per portal | Portals change independently |
| Human approval gate | Legal safety and user trust |
| DSC signing stays on user's machine | Hardware tokens cannot be used from a cloud server |

## Scaling notes

- Run workers on separate queues: `portals`, `ocr`, `llm`, `notify`.
- Cache OCR output and embeddings by file hash.
- Use cheaper models for classification, stronger ones for extraction and drafting.
- Add read replicas and partition `audit_log` by month when volume grows.
