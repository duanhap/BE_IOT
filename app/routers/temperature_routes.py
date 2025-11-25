# app/routers/temperature_routes.py
from fastapi import APIRouter
from app.utils.mqtt_client import get_latest_temperature

router = APIRouter(prefix="/temperature", tags=["Temperature"])

@router.get("/")
def get_temperature():
    data = get_latest_temperature()
    if data is None:
        return {"message": "No temperature data yet"}
    return {"temperature": data}
