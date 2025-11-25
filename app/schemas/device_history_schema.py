from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DeviceHistoryBase(BaseModel):
    action_type: str
    action_value: Optional[str]
    triggered_by: str


class DeviceHistoryResponse(DeviceHistoryBase):
    id: int
    device_id: int
    created_at: datetime

    class Config:
        orm_mode = True
