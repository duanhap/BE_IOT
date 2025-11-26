from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.database import database
from datetime import datetime


class SensorData(database.Base):
    __tablename__ = "SensorData"

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
