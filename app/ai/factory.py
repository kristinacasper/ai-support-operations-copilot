from app.ai.mock_provider import MockAnalysisProvider
from app.ai.openai_provider import OpenAIAnalysisProvider
from app.ai.provider import AnalysisProvider
from app.config import Settings


def build_analysis_provider(settings: Settings) -> AnalysisProvider:
    provider_name = settings.analysis_provider.strip().lower()

    if provider_name == "mock":
        return MockAnalysisProvider()

    if provider_name == "openai":
        return OpenAIAnalysisProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    raise ValueError(
        f"Unsupported ANALYSIS_PROVIDER '{settings.analysis_provider}'. "
        "Allowed values: mock, openai."
    )
