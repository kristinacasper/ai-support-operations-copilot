from sqlalchemy.orm import Session

from app.services.customer_service import get_customer_by_email as _get_customer_by_email
from app.services.knowledge_service import search_knowledge_base as _search_knowledge_base


def get_customer_by_email(db: Session, email: str) -> dict[str, object] | None:
    """Read-only customer lookup exposed to the future orchestrator."""
    customer = _get_customer_by_email(db, email)
    if customer is None:
        return None

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "account_status": customer.account_status,
        "is_demo": customer.is_demo,
    }


def search_knowledge_base(
    db: Session,
    query: str,
    limit: int = 5,
) -> list[dict[str, object]]:
    """Read-only knowledge retrieval exposed to the future orchestrator."""
    articles = _search_knowledge_base(db, query, limit=limit)
    return [
        {
            "id": article.id,
            "title": article.title,
            "topic": article.topic,
            "content": article.content,
            "active": article.active,
        }
        for article in articles
    ]
