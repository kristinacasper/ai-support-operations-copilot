from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class TicketCategory(str, Enum):
    BILLING = "BILLING"
    ACCOUNT_ACCESS = "ACCOUNT_ACCESS"
    TECHNICAL = "TECHNICAL"
    SUBSCRIPTION = "SUBSCRIPTION"
    GENERAL = "GENERAL"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ProposedAction(str, Enum):
    PROVIDE_INFORMATION = "PROVIDE_INFORMATION"
    INVESTIGATE_ACCOUNT = "INVESTIGATE_ACCOUNT"
    CREATE_REFUND_REQUEST = "CREATE_REFUND_REQUEST"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"


PROTECTED_ACTIONS = {ProposedAction.CREATE_REFUND_REQUEST}


class AnalysisPreviewRequest(BaseModel):
    customer_email: EmailStr
    message: str = Field(min_length=5, max_length=5000)

    model_config = ConfigDict(extra="forbid")


class TicketAnalysis(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    summary: str = Field(min_length=5, max_length=500)
    proposed_action: ProposedAction
    requires_approval: bool
    knowledge_query: str = Field(min_length=2, max_length=200)
    response_draft: str = Field(min_length=5, max_length=2000)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def enforce_protected_action_approval(self) -> "TicketAnalysis":
        if self.proposed_action in PROTECTED_ACTIONS and not self.requires_approval:
            raise ValueError(
                "Protected actions must explicitly require human approval."
            )
        return self
