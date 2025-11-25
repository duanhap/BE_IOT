from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import database
from datetime import datetime


class VoiceHistory(database.Base):
    __tablename__ = "VoiceHistory"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    raw = Column(String, nullable=False)
    device_id = Column(Integer, ForeignKey("Device.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    action_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    # Relationship
    device = relationship("Device", back_populates="voice_histories")

    def to_dict(self):
        return {
            "id": self.id,
            "raw": self.raw,
            "device_id": self.device_id,
            "action_name": self.action_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }
