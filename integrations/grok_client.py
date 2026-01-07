"""
xAI (Grok) Client
"""

from openai import AsyncOpenAI
from typing import Dict, Any

from integrations.base import BaseAIClient
from config.settings import settings

class GrokClient(BaseAIClient):
    """
    Client สำหรับ Grok (xAI)
    ใช้งานผ่าน OpenAI SDK แต่เปลี่ยน base_url
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        # Grok ใช้ OpenAI-compatible endpoint
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        self.model = "grok-beta"

    async def generate(self, message: str, **kwargs) -> Dict[str, Any]:
        """สร้าง response"""
        try:
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
        except Exception as e:
            raise Exception(f"Grok API Error: {str(e)}")

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """คำนวณต้นทุน"""
        # ราคาจาก settings
        pricing = settings.PRICING.get("grok-beta", {"input": 5.0, "output": 15.0})

        cost = (
            (input_tokens * pricing["input"] / 1_000_000) +
            (output_tokens * pricing["output"] / 1_000_000)
        )

        return cost
