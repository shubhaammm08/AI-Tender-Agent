# Deployment

## Environments

| Env | Purpose | Hosting |
|---|---|---|
| Local | Development | Docker Compose |
| Staging | Testing with sample data | Small cloud instance |
| Production | Customers | AWS Mumbai (ap-south-1) or Azure Central India |

## Services

| Service | Notes |
|---|---|
| web | Next.js container |
| api | FastAPI container, 2 or more replicas |
| worker | Celery workers per queue: portals, ocr, llm, notify |
| playwright | Isolated container per job, no shared sessions |
| postgres | Managed PostgreSQL with pgvector |
| redis | Managed Redis |
| storage | S3 bucket with versioning and encryption |

## Environment variables (`.env.example`)

| Variable | Purpose |
|---|---|
| DATABASE_URL | PostgreSQL connection |
| REDIS_URL | Redis connection |
| S3_ENDPOINT, S3_BUCKET, S3_ACCESS_KEY, S3_SECRET_KEY | File storage |
| LLM_PROVIDER, LLM_API_KEY, LLM_MODEL_EXTRACT, LLM_MODEL_SMALL | LLM settings |
| OCR_PROVIDER, OCR_API_KEY | OCR service |
| WHATSAPP_TOKEN, WHATSAPP_PHONE_ID | Alerts |
| JWT_SECRET | Auth |
| SENTRY_DSN | Error tracking |

## CI/CD (GitHub Actions)

1. Lint and type-check
2. Unit and integration tests
3. Build images and scan them
4. Run the eval set on AI changes
5. Deploy to staging, run E2E
6. Manual approval, deploy to production
7. Run Alembic migrations before the new version starts

## Monitoring

| What | Tool |
|---|---|
| Errors | Sentry |
| Metrics and dashboards | Prometheus + Grafana or a managed equivalent |
| Adapter health | Dashboard of tenders found per portal per day |
| Queue depth and job failures | Celery metrics, alert on backlog |
| LLM cost per tender | Stored in the database, daily report |

## Backups and recovery

- Daily encrypted database backups, 30-day retention.
- Versioned object storage.
- Restore drill every quarter.
- Document the recovery steps and target time.

## Release checklist

- [ ] Migrations tested on a copy of production data
- [ ] Feature flags set for new AI features
- [ ] Rollback plan written
- [ ] Alerts confirmed working
