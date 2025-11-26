from sqlalchemy.orm import Session
from app.models.device_history import DeviceHistory


class DeviceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceHistory).all()
    def create(self, data: dict):
        history = DeviceHistory(**data)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_all_by_device(self, device_id: int):
        return self.db.query(DeviceHistory).filter(DeviceHistory.device_id == device_id).all()