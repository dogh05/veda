"""Rebuild the cache from the chain. The database is never the source of truth."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone

from psycopg.types.json import Jsonb

from .core.messages import message_hash
from .db import connect
from .hedera import mirror


def _ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    except ValueError:
        return None


def derive_state(events: list[dict]) -> tuple[str, str | None, int | None]:
    status = "submitted"
    token_id: str | None = None
    serial: int | None = None
    for item in events:
        event = item.get("event")
        if event == "extracted":
            status = "extracted"
        elif event == "validated":
            verdict = item.get("payload", {}).get("verdict")
            status = "validated" if verdict == "pass" else "failed"
        elif event == "sealed":
            status = "sealed"
            credential = item.get("payload", {}).get("credential", {})
            token_id = credential.get("token_id")
            serial = credential.get("serial")
    return status, token_id, serial


def sync_consensus(filing_id: str, messages: list[dict]) -> int:
    updated = 0
    with connect() as conn:
        for item in messages:
            ts = _ts(item.get("consensus_timestamp"))
            if ts is None:
                continue
            cursor = conn.execute(
                "UPDATE events SET consensus_ts = %s "
                "WHERE filing_id = %s AND hcs_sequence = %s",
                (ts, filing_id, item["sequence_number"]),
            )
            updated += cursor.rowcount
    return updated


def _known_topics(conn) -> dict[str, str]:
    known: dict[str, str] = {}
    for filing_id, topic_id in conn.execute(
        "SELECT id, topic_id FROM filings WHERE topic_id IS NOT NULL"
    ).fetchall():
        known[str(filing_id)] = topic_id
    row = conn.execute("SELECT value FROM _meta WHERE key = 'topics'").fetchone()
    if row:
        known.update(json.loads(row[0]))
    return known


def rebuild_cache() -> dict:
    with connect() as conn:
        known = _known_topics(conn)

    rebuilt = 0
    events_written = 0
    for filing_id, topic_id in known.items():
        try:
            messages = mirror.topic_messages(topic_id, attempts=3, delay=1.0)
        except Exception:  # noqa: BLE001 - skip unreachable topics
            continue
        if not messages:
            continue
        events = [item["message"] for item in messages]
        if events[0].get("event") != "filing_submitted":
            continue
        submitted = events[0].get("payload", {})
        try:
            period = date.fromisoformat(submitted["period"])
        except (KeyError, ValueError):
            continue
        status, token_id, serial = derive_state(events)

        with connect() as conn:
            existing = conn.execute(
                "SELECT unit, consolidation FROM filings WHERE id = %s",
                (filing_id,),
            ).fetchone()
            unit = existing[0] if existing else "TND"
            consolidation = existing[1] if existing else "individuel"
            conn.execute(
                "INSERT INTO filings (id, doc_sha256, issuer, period, sector, unit, "
                "consolidation, status, topic_id, token_id, serial) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET doc_sha256 = EXCLUDED.doc_sha256, "
                "issuer = EXCLUDED.issuer, period = EXCLUDED.period, "
                "sector = EXCLUDED.sector, status = EXCLUDED.status, "
                "topic_id = EXCLUDED.topic_id, token_id = EXCLUDED.token_id, "
                "serial = EXCLUDED.serial",
                (
                    filing_id,
                    submitted.get("doc_sha256", ""),
                    submitted.get("issuer", ""),
                    period,
                    events[0].get("sector", "industrial"),
                    unit,
                    consolidation,
                    status,
                    topic_id,
                    token_id,
                    serial,
                ),
            )
            conn.execute("DELETE FROM events WHERE filing_id = %s", (filing_id,))
            for item in messages:
                message = item["message"]
                conn.execute(
                    "INSERT INTO events (id, filing_id, hcs_sequence, event, actor, "
                    "role, payload, prev_hash, hash, consensus_ts) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        message.get("event_id"),
                        filing_id,
                        item["sequence_number"],
                        message.get("event"),
                        message.get("actor", ""),
                        message.get("role", ""),
                        Jsonb(message.get("payload", {})),
                        message.get("prev_hash", ""),
                        message_hash(message),
                        _ts(item.get("consensus_timestamp")),
                    ),
                )
                events_written += 1
        rebuilt += 1

    with connect() as conn:
        conn.execute(
            "INSERT INTO _meta (key, value) VALUES ('topics', %s) "
            "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
            (json.dumps(known),),
        )

    return {"rebuilt": rebuilt, "filings": rebuilt, "events": events_written}
