# app/routes/device_control_route.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.device_service import DeviceService
from app.services.device_history_service import DeviceHistoryService
from app.mqtt.mqtt_service import publish

router = APIRouter(prefix="/device", tags=["Device Control"])

@router.post("/{device_id}/{action}/{action_type}")
def control_device(device_id: int, action: str,action_type: str ,db: Session = Depends(get_db)):
    """
    Điều khiển thiết bị qua MQTT + lưu lịch sử.
    action = on / off / set_value
    """

    device_service = DeviceService(db)
    history_service = DeviceHistoryService(db)

    device = device_service.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    action = action.lower()

    if action not in ["on", "off", "set_value"]:
        raise HTTPException(status_code=400, detail="Invalid action_type")

    # Publish MQTT (topic = device.name)
    publish(device.name, action)

    # Update device status/value
    device_service.update_status(device, action)

    # Save history
    history_service.create_history(
        device_id=device_id,
        action_type=action,
        action_value=None,  # nếu có giá trị thì truyền vào
        triggered_by=action_type
    )

    return {
        "message": f"Device {device.name} executed {action}",
        "topic": device.name,
        "action": action,
        "action_type": action_type
    }
