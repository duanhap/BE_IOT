# app/repositories/sensor_data_repository.py
from sqlalchemy.orm import Session
from app.models.sensor_data import SensorData

class SensorDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict):
        record = SensorData(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_all(self):
        return self.db.query(SensorData).all()

    def get_latest(self):
        return self.db.query(SensorData).order_by(SensorData.id.desc()).first()
    def get_latest(self, limit: int = 20):
        return (
            self.db.query(SensorData)
            .order_by(SensorData.created_at.desc())
            .limit(limit)
            .all()
        )
