from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.device_history_schema import DeviceHistoryResponse, PaginationResponse
from app.services.device_history_service import DeviceHistoryService


router = APIRouter(prefix="/history", tags=["Device History"])

@router.get("/", response_model=PaginationResponse[DeviceHistoryResponse])
def get_all_histories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(10, ge=1, le=100, description="Số item mỗi trang")
):
    service = DeviceHistoryService(db)
    return service.get_paginated_histories(page=page, page_size=page_size)

