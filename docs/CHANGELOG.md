# Changelog

## 1.2 — 2026-10-21

- Added `POST /filings/{id}/seal` (issuer/admin): deterministic Excel report,
  HFS metadata with compact extracted values, one NFT serial per
  `(issuer, period)`, and the `sealed` event.
- HFS properties now include `report_sha256` and `values` (≤ 4096 bytes).
- `GET /filings/{id}/report.xlsx` returns the same deterministic bytes that
  were anchored at seal time.
- Cache rebuild rehydrates sealed values/ratios from the HFS file and recomputes
  ratios, so `POST /system/rebuild` no longer depends on local-only data for
  sealed filings.
- Added `report_hash_match` to the verifier.
- Mirror reader reassembles HCS chunked messages (`chunk_info`) so the hash
  chain survives messages above 1024 bytes.
- The Excel report is byte-deterministic (fixed core properties and zip
  timestamps); the download hash equals the anchored `report_sha256`.
- Validation details are compact so a passing `validated` event fits in one
  1024-byte HCS message.

## 1.1 — 2026-10-21

- Added `POST /filings/{id}/extract` (issuer/admin): re-uploads the PDF,
  verifies `doc_sha256`, runs the deterministic extractor, writes `extracted`
  and `validated` events, and returns the verdict + checks.
- `extracted.model` is now `deterministic:pymupdf` (no model produces figures).
- Added `variation_stocks` to the line-item registry (section 7).
- Ratio engine (`section 8`) and the seven coherence checks are implemented
  with tolerance `max(1 dinar, 0.01 %)`.

## 1.0 — frozen

- Initial HCS envelope, NFT/HFS schema, verification algorithm, API, database,
  and French line-item registry.
