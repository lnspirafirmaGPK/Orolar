import asyncio
from core.resonance_engine import ResonanceEngine
from core.wisdom_vault import WisdomVault, SecretScroll
from core.aether_bus import AetherBus
from services.ai_router import AIRouter # เชื่อมกับ AI Router ที่เราสร้างไว้
from sqlalchemy.orm import Session
from models.user import User

class HarmonicOrolarKernel:
    """
    Integration Layer: เชื่อม Business Logic เข้ากับ Harmonic System
    """
    def __init__(self):
        self.bus = AetherBus()
        self.vault = WisdomVault()
        self.ai_router = AIRouter()
        self.signer = ResonanceEngine() # Helper for internal signing

        # เก็บ AI Router Logic ลงใน Vault (เป็นคัมภีร์)
        self.vault.store("ai_generation_protocol", SecretScroll(
            title="AI Generation Protocol",
            content=self.ai_router.generate_response,
            essence="The logic to converse with digital minds"
        ))

    async def execute_ai_request(self, db: Session, user: User, message: str, model: str):
        """
        Flow การทำงานผ่านระบบ Harmonic
        """
        # 1. สร้าง Signature (Internal)
        sig = self.signer.generate_signature(str(user.id))

        # 2. คำนวณ Purity (ง่ายๆ)
        purity = 1.0 if "hack" not in message.lower() else 0.0

        # 3. ขอ Access จาก Vault
        ai_function = self.vault.access(
            key="ai_generation_protocol",
            seeker_id=str(user.id),
            purity=purity,
            signature=sig
        )

        if not ai_function:
            raise ValueError("Resonance Failed: Access Denied to AI Protocol")

        # 4. เรียกใช้งานฟังก์ชันที่ได้มา
        result = await ai_function(db, user, message, model)

        # 5. Publish Event
        await self.bus.publish("AI_COMPLETED", {"user_id": user.id, "model": model})

        return result

# Singleton Instance
kernel = HarmonicOrolarKernel()
