from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeArticle


def search_knowledge_base(
    db: Session,
    query: str,
    limit: int = 5,
) -> list[KnowledgeArticle]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    terms = [term for term in dict.fromkeys(normalized.split()) if len(term) >= 2]
    if not terms:
        return []

    conditions = []
    for term in terms:
        pattern = f"%{term}%"
        conditions.extend(
            [
                KnowledgeArticle.title.ilike(pattern),
                KnowledgeArticle.topic.ilike(pattern),
                KnowledgeArticle.content.ilike(pattern),
            ]
        )

    statement = (
        select(KnowledgeArticle)
        .where(
            KnowledgeArticle.active.is_(True),
            or_(*conditions),
        )
        .order_by(KnowledgeArticle.id)
        .limit(max(1, min(limit, 10)))
    )
    return list(db.scalars(statement).all())
