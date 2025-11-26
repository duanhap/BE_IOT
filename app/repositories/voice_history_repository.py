from sqlalchemy.orm import Session
from app.models.voice_history import VoiceHistory


class VoiceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(VoiceHistory).all()
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
