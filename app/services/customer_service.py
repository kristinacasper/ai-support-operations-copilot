from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_customer_by_email(db: Session, email: str) -> Customer | None:
    normalized = email.strip().lower()
    statement = select(Customer).where(func.lower(Customer.email) == normalized)
    return db.scalar(statement)
