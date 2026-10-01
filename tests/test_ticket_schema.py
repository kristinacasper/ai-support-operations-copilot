import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketCreate


def test_valid_ticket_payload() -> None:
    ticket = TicketCreate(
        customer_email="mark@example.com",
        message="I was charged twice and I need help.",
    )

    assert str(ticket.customer_email) == "mark@example.com"


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TicketCreate(
            customer_email="not-an-email",
            message="I need help with my account.",
        )
