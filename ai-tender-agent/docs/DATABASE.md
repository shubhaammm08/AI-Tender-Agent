# Database

PostgreSQL 16 with `pgvector`. Every tenant-owned table has `tenant_id` and Row-Level Security enabled.

## Tables

| Table | Purpose | Key fields |
|---|---|---|
| tenants | Customer organization | name, plan, created_at |
| users | People in a tenant | tenant_id, email, role |
| company_profile | Facts used for matching | gstin, pan, udyam_no, turnover, categories, states |
| documents | Vault files | type, file_key, issued_on, expires_on, version |
| tenders | One row per portal tender | portal, portal_tender_id, title, buyer, closes_at, emd, status |
| tender_versions | Original and corrigendums | tender_id, version, diff, fetched_at |
| tender_files | Files of a tender | tender_id, kind, file_key, sha256 |
| requirements | Extracted rules | tender_id, type, value, mandatory, file, page, clause, confidence |
| matches | Tenant-to-tender result | tenant_id, tender_id, score, decision, reasons |
| bids | A bid in progress | tenant_id, tender_id, status, approved_by |
| bid_documents | Generated files | bid_id, kind, content_key, model, prompt_version, sources |
| price_history | Award data | item, buyer, state, l1_price, awarded_on |
| audit_log | Append-only actions | tenant_id, actor, action, entity, before, after, prev_hash, hash |
| reminders | Deadlines and alerts | tenant_id, tender_id, due_at, channel, sent_at |

## Core SQL

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE tenders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  portal text NOT NULL,
  portal_tender_id text NOT NULL,
  title text NOT NULL,
  buyer text,
  state text,
  category text,
  estimated_value numeric,
  emd numeric,
  closes_at timestamptz,
  status text NOT NULL DEFAULT 'open',
  current_version int NOT NULL DEFAULT 1,
  UNIQUE (portal, portal_tender_id)
);

CREATE TABLE requirements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tender_id uuid NOT NULL REFERENCES tenders(id),
  version int NOT NULL,
  type text NOT NULL,          -- turnover | experience | certification | document | spec | emd
  value jsonb NOT NULL,
  mandatory boolean NOT NULL DEFAULT true,
  source_file uuid,
  page int,
  clause text,
  confidence real
);

CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  type text NOT NULL,
  file_key text NOT NULL,
  issued_on date,
  expires_on date,
  version int NOT NULL DEFAULT 1
);

CREATE TABLE audit_log (
  id bigserial PRIMARY KEY,
  tenant_id uuid NOT NULL,
  actor text NOT NULL,         -- user id or 'ai'
  action text NOT NULL,
  entity text NOT NULL,
  detail jsonb,
  prev_hash text,
  hash text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON documents
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Rules

- Never update or delete `audit_log` rows. Revoke UPDATE and DELETE for the app role.
- Use migrations (Alembic) for every change.
- Index `tenders(closes_at)`, `matches(tenant_id, score)`, `documents(tenant_id, expires_on)`.
- Embeddings live in a `chunks` table with an `ivfflat` or `hnsw` index.
