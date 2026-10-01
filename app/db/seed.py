from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.knowledge import KnowledgeArticle


DEMO_CUSTOMERS = [
    {
        "name": "Mark Demo",
        "email": "mark@example.com",
        "account_status": "active",
    },
    {
        "name": "Lina Demo",
        "email": "lina@example.com",
        "account_status": "active",
    },
]

DEMO_KNOWLEDGE_ARTICLES = [
    {
        "title": "Duplicate charge handling",
        "topic": "billing",
        "content": (
            "If a customer reports being charged twice, verify the account and transaction context first. "
            "Do not promise a refund automatically. Prepare the case for human review when a refund-related "
            "action may be required."
        ),
    },
    {
        "title": "Password reset guidance",
        "topic": "account_access",
        "content": (
            "For password-reset requests, provide the approved reset steps and avoid requesting passwords, "
            "security codes, or other secrets from the customer."
        ),
    },
    {
        "title": "Refund request policy for the demo system",
        "topic": "refunds",
        "content": (
            "The portfolio demo never performs real refunds. A refund-related recommendation may only create "
            "a simulated request after explicit human approval."
        ),
    },
]


def seed_demo_data(db: Session) -> None:
    changed = False

    for item in DEMO_CUSTOMERS:
        exists = db.scalar(select(Customer).where(Customer.email == item["email"]))
        if exists is None:
            db.add(Customer(**item, is_demo=True))
            changed = True

    for item in DEMO_KNOWLEDGE_ARTICLES:
        exists = db.scalar(
            select(KnowledgeArticle).where(KnowledgeArticle.title == item["title"])
        )
        if exists is None:
            db.add(KnowledgeArticle(**item, active=True))
            changed = True

    if changed:
        db.commit()
