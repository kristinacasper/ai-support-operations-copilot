from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.session import Base
from app.models.customer import Customer
from app.models.knowledge import KnowledgeArticle
from app.tools.read_tools import get_customer_by_email, search_knowledge_base


def make_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_customer_lookup_is_read_only_and_case_insensitive() -> None:
    with make_session() as db:
        db.add(
            Customer(
                name="Demo User",
                email="demo@example.com",
                account_status="active",
                is_demo=True,
            )
        )
        db.commit()

        result = get_customer_by_email(db, "DEMO@example.com")

        assert result is not None
        assert result["name"] == "Demo User"
        assert result["account_status"] == "active"
        assert result["is_demo"] is True


def test_knowledge_search_returns_only_active_matches() -> None:
    with make_session() as db:
        db.add_all(
            [
                KnowledgeArticle(
                    title="Duplicate charge handling",
                    topic="billing",
                    content="Verify billing context before proposing a refund-related action.",
                    active=True,
                ),
                KnowledgeArticle(
                    title="Old billing note",
                    topic="billing",
                    content="Deprecated billing instructions.",
                    active=False,
                ),
            ]
        )
        db.commit()

        results = search_knowledge_base(db, "billing")

        assert len(results) == 1
        assert results[0]["title"] == "Duplicate charge handling"
        assert results[0]["active"] is True
