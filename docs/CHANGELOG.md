# Changelog

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
