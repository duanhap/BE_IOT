from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.device_history_schema import PaginationResponse


class VoiceHistoryBase(BaseModel):
    raw: str
    action_name: Optional[str] = None


class VoiceHistoryResponse(VoiceHistoryBase):
    id: int
    device_id: Optional[int] = None
    device_name: Optional[str] = None
    device_name_vn: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

