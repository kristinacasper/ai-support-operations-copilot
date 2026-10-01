class MockAnalysisProvider:
    """Deterministic provider used to test the structured-analysis pipeline safely."""

    def analyze(
        self,
        *,
        customer_email: str,
        message: str,
    ) -> dict[str, object]:
        normalized = message.lower()

        if "charged twice" in normalized or "duplicate charge" in normalized:
            return {
                "category": "BILLING",
                "priority": "HIGH",
                "summary": "Customer reports a possible duplicate charge.",
                "proposed_action": "CREATE_REFUND_REQUEST",
                "requires_approval": True,
                "knowledge_query": "duplicate charge refund policy",
                "response_draft": (
                    "Thanks for flagging this. I have prepared the case for review. "
                    "Any refund-related action requires human approval before it can be submitted."
                ),
            }

        if "password" in normalized or "login" in normalized or "access" in normalized:
            return {
                "category": "ACCOUNT_ACCESS",
                "priority": "MEDIUM",
                "summary": "Customer reports an account-access problem.",
                "proposed_action": "INVESTIGATE_ACCOUNT",
                "requires_approval": False,
                "knowledge_query": "password reset account access",
                "response_draft": (
                    "Thanks for the details. I have prepared the account-access issue "
                    "for investigation and will use the approved support guidance."
                ),
            }

        return {
            "category": "GENERAL",
            "priority": "LOW",
            "summary": "Customer submitted a general support request.",
            "proposed_action": "PROVIDE_INFORMATION",
            "requires_approval": False,
            "knowledge_query": "general support guidance",
            "response_draft": (
                "Thanks for contacting support. I have summarized your request and "
                "prepared it for review."
            ),
        }
