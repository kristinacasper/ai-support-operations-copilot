# AI Support Operations Copilot

Portfolio-grade Python application for exploring safe, human-controlled AI support operations.

## Status

**In development — Milestone 2 complete: customer context + knowledge retrieval.**

The current version provides a working FastAPI backend, ticket persistence, workflow states, synthetic customer records, a local knowledge base, read-only retrieval tools, validation, automated tests, and GitHub Actions CI. Structured LLM analysis is the next milestone.

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
Service layer
  ↓
Read-only tool layer
  ├─ Customer lookup
  └─ Knowledge-base search
  ↓
SQLAlchemy
  ↓
SQLite
```

Planned next layer:

```text
Validated ticket
  ↓
Structured LLM analysis
  ↓
Allow-listed read tools
  ↓
Proposed action
  ↓
Human approval gate for protected writes
  ↓
Action execution + audit log
```

## Current API

### `GET /health`
Returns a simple service-health response.

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
- AI will not be allowed to execute arbitrary tools.
- Read-only and state-changing tools remain explicitly separated.
- Protected writes will require human approval.
- Real secrets belong in `.env`, which is ignored by Git.
- Public portfolio evidence uses synthetic or sanitized data.
- No real refunds, payments, or customer-account changes are performed by this portfolio prototype.

## Technology

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- pytest
- GitHub Actions

Planned: structured LLM output, tool/function calling, human approval, audit logging, and a simple UI.

## Project Structure

```text
app/
├── main.py
├── config.py
├── db/
│   ├── session.py
│   └── seed.py
├── models/
│   ├── customer.py
│   ├── knowledge.py
│   └── ticket.py
├── schemas/
│   ├── customer.py
│   ├── knowledge.py
│   └── ticket.py
├── services/
│   ├── customer_service.py
│   ├── knowledge_service.py
│   └── ticket_service.py
└── tools/
    └── read_tools.py

tests/
├── test_health.py
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
3. Structured LLM analysis — **next**
4. Allow-listed orchestrator tool use
5. Proposed-action policy
6. Human approval workflow
7. Protected write tools
8. Audit logging and failure handling
9. Expanded automated tests
10. Portfolio evidence and case study

## Portfolio Context

This is a portfolio prototype designed to demonstrate progression from workflow automation toward coded AI application engineering. It is not presented as a production customer-support platform.
