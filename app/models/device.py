from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database.database import database
from datetime import datetime



class Device(database.Base):
    __tablename__ = "Device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=True)
    status = Column(Enum("on", "off"), default="off", nullable=False)
    value = Column(String(50), nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    histories = relationship("DeviceHistory", back_populates="device", cascade="all, delete-orphan")
    voice_histories = relationship("VoiceHistory", back_populates="device")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "status": self.status,
            "value": self.value,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
