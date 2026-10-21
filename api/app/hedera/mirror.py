"""Hedera reader: Mirror Node REST (trustless path)."""
from __future__ import annotations

import base64
import json
import time
import urllib.request

from ..config import settings


def _get(path: str, attempts: int = 12, delay: float = 1.5):
    base = settings.mirror_url.rstrip("/")
    url = path if path.startswith("http") else f"{base}{path}"
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - retry on indexing lag
            last_error = exc
            time.sleep(delay)
    raise RuntimeError(f"mirror request failed: {path}: {last_error}")


def _fetch_topic(topic_id: str) -> list[dict]:
    messages: list[dict] = []
    path = f"/api/v1/topics/{topic_id}/messages?order=asc&limit=100"
    while path:
        data = _get(path)
        for item in data.get("messages", []):
            raw = base64.b64decode(item["message"]).decode("utf-8")
            messages.append(
                {
                    "consensus_timestamp": item.get("consensus_timestamp"),
                    "sequence_number": item.get("sequence_number"),
                    "message": json.loads(raw),
                }
            )
        path = data.get("links", {}).get("next")
    return messages


def topic_messages(
    topic_id: str,
    expected_min: int | None = None,
    attempts: int = 20,
    delay: float = 1.5,
) -> list[dict]:
    """Read all messages; if expected_min is set, wait for mirror indexing."""
    messages: list[dict] = []
    for _ in range(attempts):
        messages = _fetch_topic(topic_id)
        if expected_min is None or len(messages) >= expected_min:
            return messages
        time.sleep(delay)
    return messages


def nft(token_id: str, serial: int) -> dict:
    data = _get(f"/api/v1/tokens/{token_id}/nfts/{serial}")
    if isinstance(data, dict) and "nfts" in data:
        items = data["nfts"]
        return items[0] if items else {}
    return data


def nft_metadata_bytes(token_id: str, serial: int) -> bytes:
    raw = nft(token_id, serial).get("metadata", "")
    return base64.b64decode(raw)
