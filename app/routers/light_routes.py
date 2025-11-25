from fastapi import APIRouter, HTTPException

from app.schemas.light_schema import LightToggleRequest, LightToggleResponse
from app.utils import mqtt_client


router = APIRouter(prefix="/light", tags=["Light Control"])


@router.post(
    "/publish",
    response_model=LightToggleResponse,
    summary="Publish arbitrary payload to the light topic via MQTT",
)
async def publish_light(payload: LightToggleRequest):
    try:
        mqtt_client.publish("light", payload.message, qos=1)
        return {"topic": "light", "payload": payload.message, "status": "published"}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

