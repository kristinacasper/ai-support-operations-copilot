from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.ticket import TicketStatus


class TicketCreate(BaseModel):
    customer_email: EmailStr
    message: str = Field(min_length=5, max_length=5000)


class TicketRead(BaseModel):
    id: int
    customer_email: EmailStr
    message: str
    category: str | None
    priority: str | None
    summary: str | None
    proposed_action: str | None
    response_draft: str | None
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
