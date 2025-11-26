from datetime import datetime
from math import ceil
from sqlalchemy.orm import Session
from app.repositories.device_history_repository import DeviceHistoryRepository
from app.schemas.device_history_schema import DeviceHistoryResponse


class DeviceHistoryService:
    def __init__(self, db: Session):
        self.repository = DeviceHistoryRepository(db)

    def get_all_histories(self):
        return self.repository.get_all()

    def get_paginated_histories(self, page: int = 1, page_size: int = 10):
        items, total = self.repository.get_paginated(page, page_size)
        total_pages = ceil(total / page_size) if page_size > 0 else 0
        # Convert items to response schema with device names
        formatted_items = []
        for item in items:
            item_dict = {
                "id": item.id,
                "device_id": item.device_id,
                "action_type": item.action_type,
                "action_value": item.action_value,
                "triggered_by": item.triggered_by,
                "created_at": item.created_at,
                "device_name": item.device.name if item.device else None,
                "device_name_vn": item.device.name_vn if item.device else None
            }
            formatted_items.append(DeviceHistoryResponse(**item_dict))
        return {
            "items": formatted_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    def create_history(self, device_id: int, action_type: str, action_value: str, triggered_by: str):
        data = {
            "device_id": device_id,
            "action_type": action_type,
            "action_value": action_value,
            "triggered_by": triggered_by,
            "created_at": datetime.utcnow()
        }
        return self.repository.create(data)