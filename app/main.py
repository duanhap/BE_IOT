from fastapi import FastAPI
from app.routers.history_routes import router as history_router
from app.routers.temperature_routes import router as temperature_router
from app.routers.device_routes import router as device_router
from app.routers.voice_routes import router as voice_router
from app.mqtt.mqtt_service import start_mqtt, publish
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Cho phép tất cả domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(history_router)
app.include_router(temperature_router)
app.include_router(device_router)
app.include_router(voice_router)

@app.on_event("startup")
def startup_event():
    print("🚀 Starting HTTP API and MQTT Client...")
    start_mqtt()

@app.get("/")
def root():
    return {"message": "Smart Home API is running"}
