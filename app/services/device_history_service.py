from sqlalchemy.orm import Session
from app.repositories.device_history_repository import DeviceHistoryRepository


class DeviceHistoryService:
    def __init__(self, db: Session):
        self.repository = DeviceHistoryRepository(db)

    def get_all_histories(self):
        return self.repository.get_all()
