# app/api/sensor_data_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.sensor_data_service import SensorDataService

router = APIRouter(prefix="/sensordata", tags=["SensorData"])

@router.get("/latest/{limit}")
def get_latest_sensor_data(limit: int, db: Session = Depends(get_db)):
    service = SensorDataService(db)
    records = service.get_latest_sensor_data(limit=limit)
    return [r.to_dict() for r in records]
