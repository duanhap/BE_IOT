# app/services/device_service.py

from sqlalchemy.orm import Session
from app.repositories.device_repository import DeviceRepository

class DeviceService:
    def __init__(self, db: Session):
        self.repo = DeviceRepository(db)

    def get_by_id(self, device_id: int):
        return self.repo.get_by_id(device_id)

    def update_status(self, device, action: str):
        if action in ["on", "off"]:
            device.status = action
            device.value = None
        self.repo.update(device)
        return device
