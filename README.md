# AI Support Operations Copilot

Portfolio-grade Python application for exploring safe, human-controlled AI support operations.

## Status

**In development — Milestone 3A complete: strict structured analysis with a controlled mock provider.**

The current version provides a working FastAPI backend, ticket persistence, workflow states, synthetic customer records, a local knowledge base, read-only retrieval tools, strict AI-analysis schemas, a provider abstraction, a deterministic mock provider, validation tests, and GitHub Actions CI.

A real LLM provider has **not** been connected yet. The analysis pipeline is intentionally tested first without API keys or provider-specific code.

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
Pydantic request validation
  ↓
Service layer
  ├─ Ticket persistence
  ├─ Customer lookup
  ├─ Knowledge-base search
  └─ Structured analysis validation
       ↓
   Provider interface
       ↓
   Controlled mock provider
       ↓
   TicketAnalysis schema
       ↓
   Reject invalid output
```

Reference data is stored through SQLAlchemy + SQLite.

Planned next layer:

```text
Validated ticket
  ↓
Real LLM provider adapter
  ↓
Strict TicketAnalysis output
  ↓
Allow-listed read tools
  ↓
Proposed action policy
  ↓
Human approval gate for protected writes
  ↓
Action execution + audit log
```

## Structured Analysis Contract

The provider is not allowed to return arbitrary free-form data to downstream code. Provider output must validate against `TicketAnalysis`.

```text
TicketAnalysis
├── category
├── priority
├── summary
├── proposed_action
├── requires_approval
├── knowledge_query
└── response_draft
```

Unknown fields are rejected.

Protected actions are validated by deterministic application rules. For example:

```text
CREATE_REFUND_REQUEST
→ requires_approval must be true
```

The provider cannot override that rule.

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

### `POST /analysis/preview`
Runs structured analysis through the controlled mock provider.

Example request:

```json
{
  "customer_email": "mark@example.com",
  "message": "I was charged twice and I need help."
}
```

Example structured result:

```json
{
  "category": "BILLING",
  "priority": "HIGH",
  "summary": "Customer reports a possible duplicate charge.",
  "proposed_action": "CREATE_REFUND_REQUEST",
  "requires_approval": true,
  "knowledge_query": "duplicate charge refund policy",
  "response_draft": "Thanks for flagging this. I have prepared the case for review. Any refund-related action requires human approval before it can be submitted."
}
```

This preview endpoint does **not** persist the analysis and does **not** execute any action.

## Why a Mock Provider First?

The mock provider is intentional, not a substitute for the final LLM integration.

It lets the project test:

- the provider interface,
- strict structured output,
- enum validation,
- rejection of unexpected fields,
- protected-action rules,
- API behavior,
- CI coverage,

before introducing network calls, API keys, model variability, or provider-specific SDKs.

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

The analysis preview proposes actions but executes nothing.

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
- Provider output must pass strict Pydantic validation.
- Unexpected structured-output fields are rejected.
- Protected actions require deterministic approval rules.
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

Planned: real LLM provider integration, tool/function calling, human approval, audit logging, and a simple UI.

## Project Structure

```text
app/
├── ai/
│   ├── provider.py
│   └── mock_provider.py
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
3. Structured analysis contract + mock provider — **complete**
4. Real LLM provider adapter — **next**
5. Allow-listed orchestrator tool use
6. Proposed-action policy
7. Human approval workflow
8. Protected write tools
9. Audit logging and failure handling
10. Expanded portfolio evidence and case study

## Portfolio Context

This is a portfolio prototype designed to demonstrate progression from workflow automation toward coded AI application engineering. It is not presented as a production customer-support platform.
