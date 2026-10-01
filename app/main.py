from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.ai.factory import build_analysis_provider
from app.config import settings
from app.db.seed import seed_demo_data
from app.db.session import Base, SessionLocal, engine, get_db
from app.models.customer import Customer  # noqa: F401 - registers model metadata
from app.models.knowledge import KnowledgeArticle  # noqa: F401 - registers model metadata
from app.models.ticket import Ticket  # noqa: F401 - registers model metadata
from app.schemas.analysis import AnalysisPreviewRequest, TicketAnalysis
from app.schemas.customer import CustomerRead
from app.schemas.knowledge import KnowledgeArticleRead
from app.schemas.ticket import TicketCreate, TicketRead
from app.services.analysis_service import analyze_ticket_preview
from app.services.customer_service import get_customer_by_email
from app.services.knowledge_service import search_knowledge_base
from app.services.ticket_service import create_ticket


analysis_provider = build_analysis_provider(settings)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data(db)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.4.0",
    description="Portfolio-grade AI support operations copilot foundation.",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "provider-adapter-ready",
        "analysis_provider": settings.analysis_provider,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
        "analysis_provider": settings.analysis_provider,
    }


@app.post(
    "/tickets",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def create_support_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
) -> TicketRead:
    return create_ticket(db, payload)


@app.get("/customers/lookup", response_model=CustomerRead)
def customer_lookup(
    email: EmailStr,
    db: Session = Depends(get_db),
) -> CustomerRead:
    customer = get_customer_by_email(db, str(email))
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/knowledge/search", response_model=list[KnowledgeArticleRead])
def knowledge_search(
    q: str = Query(min_length=2, max_length=200),
    limit: int = Query(default=5, ge=1, le=10),
    db: Session = Depends(get_db),
) -> list[KnowledgeArticleRead]:
    return search_knowledge_base(db, q, limit=limit)


@app.post("/analysis/preview", response_model=TicketAnalysis)
def analysis_preview(payload: AnalysisPreviewRequest) -> TicketAnalysis:
    """Run structured analysis without persisting or executing actions."""
    return analyze_ticket_preview(
        analysis_provider,
        customer_email=str(payload.customer_email),
        message=payload.message,
    )
