from typing import Dict, Any, Optional, Union, Callable
from dataclasses import dataclass
from core.resonance_engine import ResonanceEngine, HarmonicState

@dataclass
class SecretScroll:
    title: str
    content: Union[str, Callable, bytes, dict]
    essence: str

class WisdomVault:
    """
    Storage Layer: เก็บ Logic และ Data สำคัญ
    """
    def __init__(self):
        self._storage: Dict[str, SecretScroll] = {}
        self.resonance_gate = ResonanceEngine()

    def store(self, key: str, scroll: SecretScroll):
        self._storage[key] = scroll

    def access(self, key: str, seeker_id: str, purity: float, signature: str) -> Optional[Any]:
        try:
            state = self.resonance_gate.analyze_vibration(seeker_id, purity, signature)
            if state == HarmonicState.RESONANCE:
                scroll = self._storage.get(key)
                return scroll.content if scroll else None
            return None
        except Exception as e:
            print(f"Vault Error: {e}")
            return None
