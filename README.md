# Veda — Financial Document Analysis & Blockchain Traceability

Veda is a team-built prototype that turns financial statement PDFs into structured data, consistency checks, financial ratios, and Excel reports, with a Hedera-based audit trail.

**Winner — Hedera Cross Campus Challenge 2026, ISGT Edition.** Our team qualified for the international final.

## Why we built it

Financial information is often published as PDFs, making analysis time-consuming and difficult to trace back to the source. Veda explores a workflow that connects document extraction, repeatable calculations, and verifiable records for financial analysts and other stakeholders.

## What the prototype includes

- PDF extraction with source page references using PyMuPDF.
- Accounting consistency checks and deterministic financial ratio calculations.
- Excel report generation.
- Role-based workflows for issuers, brokers, verifiers, and administrators.
- Hedera integration for recording events and verifying document-related evidence.

## Team project & personal contribution

Veda was developed collaboratively for the Hedera Cross Campus Challenge. The award and international qualification belong to the team.

My main contribution focused on the Python/FastAPI backend and PDF extraction, with additional contributions to the frontend and Hedera integration.

## Technology stack

| Area | Technologies |
| --- | --- |
| Backend | Python, FastAPI |
| PDF extraction and reports | PyMuPDF, openpyxl |
| Frontend | React, Vite, CSS |
| Database | PostgreSQL |
| Blockchain | Hedera, Hiero Python SDK |
| Local deployment | Docker Compose, nginx |

## Prototype scope

This repository contains a hackathon prototype, not a production service. The current PDF extraction implementation uses deterministic parsing; AI-assisted extraction described in the original project plan should not be read as an implemented feature. PDF layout coverage is limited and extracted values should be reviewed against the source document.

Hedera records provide traceability and integrity evidence; they do not independently certify that a financial statement or its analysis is correct.

## Run locally

Requirements: Git, Docker with Docker Compose, and a configured Hedera testnet account for on-chain operations.

```bash
git clone https://github.com/dogh05/veda.git
cd veda
cp .env.example .env
```

Set your own `HEDERA_OPERATOR_ID`, `HEDERA_OPERATOR_KEY`, and `JWT_SECRET` in `.env`. Do not commit credentials. The Compose configuration also accepts `POSTGRES_PASSWORD`.

```bash
docker compose up --build
```

- Web interface: http://localhost:8080
- API health: http://localhost:8000/health

The interface can start locally, but on-chain actions require working Hedera testnet credentials and network access.

## Interface

| Route | Purpose |
| --- | --- |
| `/login` | Sign-in and demo access for four roles |
| `/depots` | Filing registry and role-specific overview |
| `/depots/:id` | Filing details, ratios, HCS evidence, and verification |
| `/depots/nouveau` | Submission, extraction, and sealing workflow |
| `/verification` | Review workspace for analysts and auditors |
| `/operations` | System status and administrator cache rebuild |
| `/compte` | Profile, password, and theme settings |

The selected theme is saved in the browser. JWT sessions are stored in `sessionStorage` and expire after one hour by default.

## Demo accounts

These are local demonstration accounts only. Shared demo password: `demo1234`.

| Email | Role |
| --- | --- |
| issuer@lilas.tn | issuer |
| broker@veda.tn | broker |
| verifier@veda.tn | verifier |
| admin@veda.tn | admin |

Replace demo credentials and development defaults before considering any public deployment.

## Repository layout

| Directory | Contents |
| --- | --- |
| `api/` | FastAPI backend, extraction, calculations, Hedera integration, and tests |
| `web/` | React frontend and nginx configuration |
| `db/` | PostgreSQL initialization scripts |
| `docs/` | Original project plan and technical contracts |
| `scripts/` | Supporting utilities |
| `spike/` | Early Hedera integration experiments |

## Technical documentation

- [Original project plan](docs/PLAN.md) — design intent and planned scope; some items may differ from the implementation.
- [Technical contracts](docs/contracts.md)
- [French contract summary](docs/CONTRATS_RESUME_FR.md)
- [Changelog](docs/CHANGELOG.md)
