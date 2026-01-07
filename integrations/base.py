"""
Base AI Client Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIClient(ABC):
    """
    Base class สำหรับ AI clients ทั้งหมด
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def generate(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        สร้าง response จาก AI

        Returns:
            {
                "text": str,
                "input_tokens": int,
                "output_tokens": int,
                "model": str
            }
        """
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """คำนวณต้นทุน"""
        pass
