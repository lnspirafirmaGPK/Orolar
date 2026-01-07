"""
AI Router Service (Updated)
รองรับ Grok และใช้ UsageTracker
"""
from typing import Dict, Any
from sqlalchemy.orm import Session

from integrations.anthropic_client import AnthropicClient
from integrations.openai_client import OpenAIClient
from integrations.gemini_client import GeminiClient
from integrations.grok_client import GrokClient # New Import

from models.user import User
from services.usage_tracker import UsageTracker # New Import
from config.settings import settings

class AIRouter:
    def __init__(self):
        self.clients = {}

        # Initialize all clients if keys exist
        if settings.ANTHROPIC_API_KEY:
            self.clients["claude"] = AnthropicClient(settings.ANTHROPIC_API_KEY)
        if settings.OPENAI_API_KEY:
            self.clients["gpt"] = OpenAIClient(settings.OPENAI_API_KEY)
        if settings.GEMINI_API_KEY:
            self.clients["gemini"] = GeminiClient(settings.GEMINI_API_KEY)
        if settings.GROK_API_KEY:
            self.clients["grok"] = GrokClient(settings.GROK_API_KEY)

    async def generate_response(
        self,
        db: Session,
        user: User,
        message: str,
        model: str = "claude"
    ) -> Dict[str, Any]:

        # 1. Validate Model Availability
        if model not in self.clients:
            raise ValueError(f"Model '{model}' not configured or available")

        client = self.clients[model]

        # 2. Check Balance (Estimation)
        estimated_cost = 0.01 # Minimum buffer
        if user.balance < estimated_cost:
            raise ValueError(f"Insufficient balance. Please top up.")

        try:
            # 3. Call AI
            result = await client.generate(message)

            # 4. Calculate Actual Cost
            actual_cost = client.calculate_cost(
                result["input_tokens"],
                result["output_tokens"]
            )

            # 5. Track Usage & Billing (using Service)
            UsageTracker.record_usage(
                db=db,
                user=user,
                model=result["model"],
                input_tokens=result["input_tokens"],
                output_tokens=result["output_tokens"],
                cost=actual_cost
            )

            return {
                "text": result["text"],
                "cost": actual_cost,
                "model": result["model"],
                "balance_remaining": user.balance
            }

        except Exception as e:
            raise Exception(f"AI Generation Failed: {str(e)}")
