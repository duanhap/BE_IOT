from datetime import datetime
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class DeviceHistoryBase(BaseModel):
    action_type: str
    action_value: Optional[str]
    triggered_by: str


class DeviceHistoryResponse(DeviceHistoryBase):
    id: int
    device_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
