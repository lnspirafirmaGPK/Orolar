import asyncio
from typing import Dict, List, Callable, Any

class AetherBus:
    """
    Event Layer: ระบบประสาทสื่อสาร
    """
    def __init__(self):
        self._channels: Dict[str, List[Callable]] = {}

    def subscribe(self, channel: str, handler: Callable):
        if channel not in self._channels:
            self._channels[channel] = []
        self._channels[channel].append(handler)

    async def publish(self, channel: str, payload: Any):
        if channel in self._channels:
            async def safe_handler(handler, data):
                try:
                    await handler(data)
                except Exception as e:
                    print(f"[Bus Error]: {e}")
            tasks = [safe_handler(h, payload) for h in self._channels[channel]]
            await asyncio.gather(*tasks)
