from fastapi import APIRouter
from app.mqtt.mqtt_handler import get_latest_data  # lấy từ handler mới

router = APIRouter(prefix="/temperature", tags=["Temperature"])

@router.get("/")
def get_temperature():
    data = get_latest_data("temperature")
    if data is None:
        return {"message": "No temperature data yet"}
    return {"temperature": data}
