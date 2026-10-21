"""Event payload builders (contracts v1.0, section 1.2)."""
from __future__ import annotations


def filing_submitted_payload(
    *,
    issuer: str,
    period: str,
    doc_sha256: str,
    mime: str,
    pages: int,
    source_url: str | None = None,
) -> dict:
    return {
        "issuer": issuer,
        "period": period,
        "doc_sha256": doc_sha256,
        "mime": mime,
        "pages": pages,
        "source_url": source_url,
    }
