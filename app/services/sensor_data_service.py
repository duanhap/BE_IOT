# app/services/sensor_data_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.sensor_data_repository import SensorDataRepository

class SensorDataService:
    def __init__(self, db: Session):
        self.repository = SensorDataRepository(db)

    def save_sensor_data(self, temperature: float, humidity: float):
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "created_at": datetime.utcnow()
        }
        return self.repository.create(data)

    def get_all_sensor_data(self):
        return self.repository.get_all()

    def get_latest_sensor_data(self):
        return self.repository.get_latest()
    def get_latest_sensor_data(self, limit: int = 20):
        return self.repository.get_latest(limit)