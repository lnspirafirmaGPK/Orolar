"""
Anthropic (Claude) Client
"""

import anthropic
from typing import Dict, Any

from integrations.base import BaseAIClient
from config.settings import settings

class AnthropicClient(BaseAIClient):
    """
    Client สำหรับ Claude
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    async def generate(self, message: str, **kwargs) -> Dict[str, Any]:
        """สร้าง response"""

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            messages=[{"role": "user", "content": message}]
        )

        return {
            "text": response.content[0].text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "model": self.model
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """คำนวณต้นทุน"""
        pricing = settings.PRICING["claude-sonnet"]

        cost = (
            (input_tokens * pricing["input"] / 1_000_000) +
            (output_tokens * pricing["output"] / 1_000_000)
        )

        return cost
