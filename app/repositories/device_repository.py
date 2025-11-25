# app/repositories/device_repository.py

from sqlalchemy.orm import Session
from app.models.device import Device

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, device_id: int):
        return self.db.query(Device).filter(Device.id == device_id).first()

    def update(self, device: Device):
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def get_all(self):
        return self.db.query(Device).all()
