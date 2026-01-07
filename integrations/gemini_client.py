"""
Google Gemini Client
"""

import google.generativeai as genai
from typing import Dict, Any

from integrations.base import BaseAIClient
from config.settings import settings

class GeminiClient(BaseAIClient):
    """
    Client สำหรับ Gemini
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate(self, message: str, **kwargs) -> Dict[str, Any]:
        """สร้าง response"""

        response = await self.model.generate_content_async(message)

        # Gemini ไม่ให้ token count โดยตรง ต้องประมาณ
        input_tokens = len(message.split()) * 1.3  # ประมาณการ
        output_tokens = len(response.text.split()) * 1.3

        return {
            "text": response.text,
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "model": "gemini-1.5-flash"
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """คำนวณต้นทุน"""
        pricing = settings.PRICING["gemini-flash"]

        cost = (
            (input_tokens * pricing["input"] / 1_000_000) +
            (output_tokens * pricing["output"] / 1_000_000)
        )

        return cost
