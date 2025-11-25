from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.device_history_schema import DeviceHistoryResponse
from app.services.device_history_service import DeviceHistoryService


router = APIRouter(prefix="/history", tags=["Device History"])

@router.get("/", response_model=List[DeviceHistoryResponse])
def get_all_histories(db: Session = Depends(get_db)):
    service = DeviceHistoryService(db)
    return service.get_all_histories()
