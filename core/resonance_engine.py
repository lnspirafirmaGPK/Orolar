import hashlib
import hmac
import os
from enum import Enum

class HarmonicState(Enum):
    SILENCE = "SILENCE"
    DISSONANCE = "DISSONANCE"
    RESONANCE = "RESONANCE"

class ResonanceEngine:
    """
    Security Layer: ตรวจสอบความสั่นพ้องของเจตจำนง
    """
    def __init__(self):
        self._cosmic_salt = os.getenv("COSMIC_SALT", "The_Lonely_Dawn_DEFAULT_DEV_SALT")

    def analyze_vibration(self, sender_id: str, intent_purity: float, provided_signature: str) -> HarmonicState:
        # 1. Purity Check
        if intent_purity < 0.8:
            return HarmonicState.DISSONANCE

        # 2. Signature Verification
        expected_sig = self.generate_signature(sender_id)
        if not hmac.compare_digest(expected_sig, provided_signature):
            return HarmonicState.DISSONANCE

        return HarmonicState.RESONANCE

    def generate_signature(self, content: str) -> str:
        raw = f"{content}:{self._cosmic_salt}"
        return hashlib.sha256(raw.encode()).hexdigest()
