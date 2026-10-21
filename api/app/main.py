"""Veda API — skeleton (Step 3). Health only; Hedera logic arrives in Step 4."""
import os

import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

VERSION = "0.1.0"
DATABASE_URL = os.environ.get("DATABASE_URL", "")

app = FastAPI(title="Veda API", version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_db() -> str:
    if not DATABASE_URL:
        return "not_configured"
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return "ok"
    except Exception:
        return "error"


@app.get("/health")
@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok", "db": check_db(), "version": VERSION}
