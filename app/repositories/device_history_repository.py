from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.device_history import DeviceHistory


class DeviceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceHistory).all()

    def get_paginated(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        query = self.db.query(DeviceHistory)
        total = query.count()
        items = query.order_by(DeviceHistory.created_at.desc()).offset(offset).limit(page_size).all()
        return items, total

    def create(self, data: dict):
        history = DeviceHistory(**data)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_all_by_device(self, device_id: int):
        return self.db.query(DeviceHistory).filter(DeviceHistory.device_id == device_id).all()