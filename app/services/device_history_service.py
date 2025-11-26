from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.device_history_repository import DeviceHistoryRepository


class DeviceHistoryService:
    def __init__(self, db: Session):
        self.repository = DeviceHistoryRepository(db)

    def get_all_histories(self):
        return self.repository.get_all()
    def create_history(self, device_id: int, action_type: str, action_value: str, triggered_by: str):
        data = {
            "device_id": device_id,
            "action_type": action_type,
            "action_value": action_value,
            "triggered_by": triggered_by,
            "created_at": datetime.utcnow()
        }
        return self.repository.create(data)