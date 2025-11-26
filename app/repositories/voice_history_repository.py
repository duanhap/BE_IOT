from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.voice_history import VoiceHistory


class VoiceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(VoiceHistory).options(joinedload(VoiceHistory.device)).filter(
            VoiceHistory.raw != ""
        ).all()
    
    def get_paginated(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        query = self.db.query(VoiceHistory).options(joinedload(VoiceHistory.device)).filter(
            VoiceHistory.raw != ""
        )
        total = query.count()
        items = query.order_by(VoiceHistory.created_at.desc()).offset(offset).limit(page_size).all()
        return items, total
    
    def create(self, data: dict):
        history = VoiceHistory(**data)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history
    
    def update(self, history_id: int, data: dict):
        obj = self.db.query(VoiceHistory).get(history_id)
        for k, v in data.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj
