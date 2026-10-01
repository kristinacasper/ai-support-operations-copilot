from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate


def create_ticket(db: Session, payload: TicketCreate) -> Ticket:
    ticket = Ticket(
        customer_email=str(payload.customer_email),
        message=payload.message,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
