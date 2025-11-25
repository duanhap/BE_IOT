from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.database import database
from datetime import datetime


class DeviceHistory(database.Base):
    __tablename__ = "DeviceHistory"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("Device.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    action_type = Column(Enum("on", "off", "set_value"), nullable=False)
    action_value = Column(String(50), nullable=True)
    triggered_by = Column(Enum("dashboard", "voice", "other"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    device = relationship("Device", back_populates="histories")

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "action_type": self.action_type,
            "action_value": self.action_value,
            "triggered_by": self.triggered_by,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
