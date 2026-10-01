from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    account_status: str
    is_demo: bool

    model_config = ConfigDict(from_attributes=True)
