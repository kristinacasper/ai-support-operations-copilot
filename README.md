# AI Support Operations Copilot

Portfolio-grade Python application for exploring safe, human-controlled AI support operations.

## Status

**In development — Milestone 3B adapter implementation complete; live OpenAI API smoke test pending.**

The current version provides a working FastAPI backend, ticket persistence, workflow states, synthetic customer records, a local knowledge base, read-only retrieval tools, strict structured analysis validation, a deterministic mock provider, an OpenAI Responses API adapter, automated tests, and GitHub Actions CI.

## Project Goal

Build a small but realistic support-operations copilot that can:

- receive and persist support tickets,
- classify and summarize requests with structured AI output,
- retrieve customer and knowledge-base context,
- propose next actions and response drafts,
- separate read-only tools from protected write tools,
- require explicit human approval before sensitive state-changing actions,
- keep an audit trail,
- fail safely when required information is missing or invalid.

## Current Architecture

```text
Client
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
AnalysisProvider interface
  ├─ MockAnalysisProvider (default for local dev + CI)
  └─ OpenAIAnalysisProvider (Responses API)
  ↓
Strict TicketAnalysis validation
  ↓
Read-only tool layer
  ├─ Customer lookup
  └─ Knowledge-base search
  ↓
SQLAlchemy
  ↓
SQLite
```

Protected write tools are intentionally not available to the AI yet.

## Structured Analysis Contract

Provider output must validate as `TicketAnalysis`:

```text
category
priority
summary
proposed_action
requires_approval
knowledge_query
response_draft
```

Extra fields are rejected.

Protected actions such as `CREATE_REFUND_REQUEST` must have:

```text
requires_approval = true
```

That rule is enforced by application validation rather than trusted to the model.

## OpenAI Adapter

The OpenAI adapter uses the Responses API with strict JSON Schema structured output.

The application remains provider-agnostic: the rest of the workflow depends on the `AnalysisProvider` interface rather than on OpenAI-specific code.

Normal development and CI use the mock provider, so automated tests do not make paid external API calls.

### Provider configuration

Copy `.env.example` to `.env` and keep the default mock provider while developing:

```text
ANALYSIS_PROVIDER=mock
```

To enable the real adapter locally:

```text
ANALYSIS_PROVIDER=openai
OPENAI_API_KEY=your_private_key_here
OPENAI_MODEL=gpt-6-luna
```

`OPENAI_MODEL` is configurable without code changes. Never commit a real `.env` file or API key.

A live provider smoke test is intentionally treated as separate evidence and is not run automatically in CI.

## Current API

### `GET /health`
Returns service health, environment, and selected analysis provider.

### `POST /tickets`
Creates and persists a validated support ticket.

Example request:

```json
{
  "customer_email": "mark@example.com",
  "message": "I was charged twice and I need help."
}
```

New tickets begin with the workflow state `NEW`.

### `GET /customers/lookup?email=...`
Returns a synthetic demo customer by email. The lookup is read-only and case-insensitive.

### `GET /knowledge/search?q=...`
Searches active local knowledge-base articles. The search is read-only and returns at most 10 results.

### `POST /analysis/preview`
Runs structured ticket analysis without persisting analysis results and without executing actions.

With the default configuration this uses the deterministic mock provider. With `ANALYSIS_PROVIDER=openai`, the same endpoint uses the OpenAI adapter and then validates the returned data again with Pydantic.

## Demo Data

Only synthetic portfolio data is seeded automatically.

Example demo customer:

```text
mark@example.com
```

Example knowledge topics:

- duplicate charge handling,
- password reset guidance,
- simulated refund-request policy.

No real customer records are used.

## Read vs. Write Boundary

The current tool layer contains only read-only functions:

```text
get_customer_by_email()
search_knowledge_base()
```

These functions retrieve context but do not modify system state.

Protected write tools will be introduced later and will require explicit human approval before execution.

## Workflow States

```text
NEW
→ ANALYZING
→ READY_FOR_REVIEW
→ AWAITING_APPROVAL
→ APPROVED
→ ACTION_EXECUTED
→ RESOLVED
```

Failure state: `FAILED`

## Safety Principles

- Customer text is treated as untrusted input.
- Provider output is schema-constrained and validated again by Pydantic.
- AI cannot choose arbitrary application fields.
- AI is not allowed to execute arbitrary tools.
- Read-only and state-changing tools remain explicitly separated.
- Protected writes require human approval.
- Real secrets belong in `.env`, which is ignored by Git.
- CI uses mocks and does not require an API key.
- Public portfolio evidence uses synthetic or sanitized data.
- No real refunds, payments, or customer-account changes are performed by this portfolio prototype.

## Technology

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- OpenAI Python SDK / Responses API
- pytest
- GitHub Actions

Planned: allow-listed tool/function calling, human approval, audit logging, and a simple UI.

## Project Structure

```text
app/
├── main.py
├── config.py
├── ai/
│   ├── factory.py
│   ├── provider.py
│   ├── mock_provider.py
│   └── openai_provider.py
├── db/
│   ├── session.py
│   └── seed.py
├── models/
│   ├── customer.py
│   ├── knowledge.py
│   └── ticket.py
├── schemas/
│   ├── analysis.py
│   ├── customer.py
│   ├── knowledge.py
│   └── ticket.py
├── services/
│   ├── analysis_service.py
│   ├── customer_service.py
│   ├── knowledge_service.py
│   └── ticket_service.py
└── tools/
    └── read_tools.py

tests/
├── test_analysis_api.py
├── test_analysis_schema.py
├── test_analysis_service.py
├── test_health.py
├── test_openai_provider.py
├── test_provider_factory.py
├── test_read_tools.py
├── test_reference_api.py
├── test_ticket_api.py
└── test_ticket_schema.py
```

## Local Setup

```bash
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then run:

```bash
uvicorn app.main:app --reload
```

Open the generated API documentation at:

```text
http://127.0.0.1:8000/docs
```

Run tests with:

```bash
python -m pytest -q
```

## Development Roadmap

1. Backend foundation and ticket persistence — **complete**
2. Customer model, local knowledge base, and read-only retrieval tools — **complete**
3. Strict provider-agnostic structured analysis pipeline — **complete**
4. OpenAI Responses API adapter — **code complete; live smoke test pending**
5. Allow-listed orchestrator tool use
6. Proposed-action policy
7. Human approval workflow
8. Protected write tools
9. Audit logging and failure handling
10. Expanded automated tests
11. Portfolio evidence and case study

## Portfolio Context

This is a portfolio prototype designed to demonstrate progression from workflow automation toward coded AI application engineering. It is not presented as a production customer-support platform.
