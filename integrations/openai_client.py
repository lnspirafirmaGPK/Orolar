"""
OpenAI (GPT) Client
"""

from openai import AsyncOpenAI
from typing import Dict, Any

from integrations.base import BaseAIClient
from config.settings import settings

class OpenAIClient(BaseAIClient):
    """
    Client สำหรับ GPT
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    async def generate(self, message: str, **kwargs) -> Dict[str, Any]:
        """สร้าง response"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
            max_tokens=kwargs.get("max_tokens", 1000)
        )

        return {
            "text": response.choices[0].message.content,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "model": self.model
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """คำนวณต้นทุน"""
        pricing = settings.PRICING["gpt-4o-mini"]

        cost = (
            (input_tokens * pricing["input"] / 1_000_000) +
            (output_tokens * pricing["output"] / 1_000_000)
        )

        return cost
