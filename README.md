# AI Support Operations Copilot

Portfolio-grade Python application for exploring safe, human-controlled AI support operations.

## Status

**In development — foundation phase.**

The current version establishes the backend structure, ticket persistence, workflow states, validation, and initial automated tests. LLM integration and controlled tool calling will be added in later milestones.

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

## Current Foundation

```text
Client
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
Service layer
  ↓
SQLAlchemy
  ↓
SQLite
```

Planned next layer:

```text
Validated ticket
  ↓
LLM structured analysis
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
- Read-only and state-changing tools will remain explicitly separated.
- Protected writes will require human approval.
- Real secrets belong in `.env`, which is ignored by Git.
- Public portfolio evidence must use synthetic or sanitized data.
- No real refunds, payments, or customer-account changes are performed by this portfolio prototype.

## Technology

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- pytest

Planned: structured LLM output, tool/function calling, human approval, audit logging, and a simple UI.

## Project Structure

```text
app/
├── main.py
├── config.py
├── db/
│   └── session.py
├── models/
│   └── ticket.py
├── schemas/
│   └── ticket.py
├── services/
│   └── ticket_service.py
└── tools/

tests/
├── test_health.py
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

Open the automatically generated API documentation at:

```text
http://127.0.0.1:8000/docs
```

Run tests with:

```bash
python -m pytest -q
```

## Development Roadmap

1. Backend foundation and ticket persistence — **current milestone**
2. Customer and knowledge-base models
3. Structured LLM analysis
4. Read-only tool layer
5. Proposed-action policy
6. Human approval workflow
7. Protected write tools
8. Audit logging and failure handling
9. Expanded automated tests
10. Portfolio evidence and case study

## Portfolio Context

This is a portfolio prototype designed to demonstrate progression from workflow automation toward coded AI application engineering. It is not presented as a production customer-support platform.
