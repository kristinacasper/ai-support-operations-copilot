from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import Base, engine, get_db
from app.models.ticket import Ticket  # noqa: F401 - registers model metadata
from app.schemas.ticket import TicketCreate, TicketRead
from app.services.ticket_service import create_ticket


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Portfolio-grade AI support operations copilot foundation.",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "foundation-ready",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
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
