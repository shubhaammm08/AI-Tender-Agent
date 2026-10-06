# Testing and Evaluation

## Test layers

| Layer | Tool | What it covers |
|---|---|---|
| Unit | pytest | Rule engine, parsers, schema validation |
| Integration | pytest + test DB | API routes, tenant isolation, audit chain |
| Adapter | Saved HTML samples | Each parser version |
| E2E | Playwright | Sign in, view tender, upload document, approve |
| Eval | `eval/run_eval.py` | Extraction accuracy on labeled tenders |
| Security | Tenant isolation suite, dependency scan | Cross-tenant access, known CVEs |

## Evaluation set

- Start with 50 real tenders, grow to 100 or more.
- Mix categories, states, scanned and digital PDFs, ZIPs, and at least 10 corrigendums.
- Label each requirement: type, value, mandatory, page, clause.
- Store labels as JSON next to the file in `eval/data/`. Remove personal data first.

## Metrics

| Metric | Target |
|---|---|
| Recall on mandatory requirements | 95% or higher |
| Precision on requirements | 90% or higher |
| Citation correct (right page and clause) | 95% or higher |
| Decision agreement with expert (Bid / Check / Skip) | 90% or higher |
| Median analysis time per tender | Under 3 minutes |
| Cost per analyzed tender | Tracked and under plan budget |

## Rules

- Run the eval on every prompt, model or OCR change. Block the change if a metric drops.
- Keep a changelog of eval scores in `eval/RESULTS.md`.
- Write a unit test for every rule in the rule engine, including MSME relaxations.
- Every bug found in production becomes a test case.

## Must-have tests

- Tenant A cannot read tenant B's tenders, documents, bids or audit log.
- Audit log rows cannot be updated or deleted, and the hash chain verifies.
- A tender without a source citation is rejected by the extractor.
- A bid cannot reach "submitted" without an approval record.
