# AI Pipeline

Principle: the LLM reads and explains. Code decides.

## Stages

| # | Stage | Tool | Output |
|---|---|---|---|
| 1 | Collect files | Adapter | PDFs, ZIPs, Excel |
| 2 | Classify files | Small LLM or rules | NIT, BOQ, GCC, SCC, annexure, corrigendum |
| 3 | Read text | Layout-aware OCR (Document AI, Azure DI, Surya) | Text with page numbers and tables |
| 4 | Parse BOQ | pandas / openpyxl | Item table (no LLM) |
| 5 | Chunk and embed | pgvector | Searchable chunks with page and clause |
| 6 | Extract requirements | LLM, JSON schema output | `requirements` rows with citations |
| 7 | Score | Rule engine | Score, decision, reasons |
| 8 | Explain | LLM | Plain-language summary |
| 9 | Generate documents | LLM + templates + RAG | Draft bid files (Phase 3) |
| 10 | Verify | Rules + LLM | Inconsistency report |

## Requirement schema

```json
{
  "type": "turnover | experience | certification | document | technical_spec | emd | other",
  "label": "Average annual turnover",
  "value": { "amount": 5000000, "currency": "INR", "years": 3 },
  "mandatory": true,
  "msme_relaxation": true,
  "source": { "file": "NIT.pdf", "page": 4, "clause": "3.1" },
  "confidence": 0.93
}
```

Reject any output without a source. Send low-confidence items (under 0.7) to a review list.

## Rule engine

- Lives in `packages/rules`. Pure functions, fully unit tested.
- Inputs: requirements, company profile, vault documents, current date.
- Encodes India-specific logic: MSME and startup relaxations, Make in India classes, certificate validity, EMD exemption.
- Output per requirement: `met | not_met | missing | expired | unknown`.
- Decision: any mandatory `not_met` gives Skip. Mandatory `missing` or `expired` gives Check. Otherwise Bid.

## Corrigendums

Store each as a new tender version with a diff. Re-run extraction and scoring on the changed clauses, then alert the user ("Deadline extended, turnover limit relaxed").

## RAG for past bids

Chunk past bid documents by section. Retrieve the top matches for the new tender's requirement, then draft with the sources listed. Never mix chunks across tenants.

## Prompt management

- Keep prompts in `apps/api/ai/prompts/` with a version string (`extract_requirements_v3`).
- Save the version, model name and source chunk ids with every output.
- Change a prompt only after the eval set shows no regression.

## Cost control

- Cache OCR and embeddings by file SHA-256.
- Use a small model for classification and a stronger one for extraction and drafting.
- Limit analyses per plan. Track cost per tender in the database.

## Languages

Test OCR and extraction on Hindi and regional-language tenders early. Mark language and confidence on each file.
