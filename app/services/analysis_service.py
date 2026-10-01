from app.ai.provider import AnalysisProvider
from app.schemas.analysis import TicketAnalysis


def analyze_ticket_preview(
    provider: AnalysisProvider,
    *,
    customer_email: str,
    message: str,
) -> TicketAnalysis:
    """Validate provider output before any downstream workflow can use it."""
    raw_analysis = provider.analyze(
        customer_email=customer_email,
        message=message,
    )
    return TicketAnalysis.model_validate(raw_analysis)
