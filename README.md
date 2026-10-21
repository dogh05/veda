# Veda — Dépôts financiers vérifiés

Trust layer for financial filings: AI extracts, code validates, Hedera seals.
See `docs/PLAN.md` and `docs/contracts.md`.

## Run

```bash
docker compose up --build
```

- Web: http://localhost:8080
- API health: http://localhost:8000/health

## Layout

```
api/    FastAPI (backend, Hedera client, ratios)
web/    React (Vite) + nginx
db/     Postgres init scripts (cache, rebuildable from chain)
docs/   plan + contracts
spike/  Day-1 Hedera spike (already passed)
```
