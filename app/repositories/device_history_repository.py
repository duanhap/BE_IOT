from sqlalchemy.orm import Session
from app.models.device_history import DeviceHistory


class DeviceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceHistory).all()
