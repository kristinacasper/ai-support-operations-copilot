from typing import Protocol


class AnalysisProvider(Protocol):
    """Contract implemented by any provider that proposes ticket analysis data."""

    def analyze(
        self,
        *,
        customer_email: str,
        message: str,
    ) -> dict[str, object]:
        """Return raw structured data. Validation happens outside the provider."""
        ...
