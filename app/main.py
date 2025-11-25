from fastapi import FastAPI
from app.routers.history_routes import router as history_router
from app.routers.temperature_routes import router as temperature_router
from app.utils.mqtt_client import start_mqtt


app = FastAPI()

app.include_router(history_router)
app.include_router(temperature_router)

@app.on_event("startup")
def startup_event():
    print("🚀 Starting HTTP API and MQTT Client...")
    start_mqtt()


@app.get("/")
def root():
    return {"message": "Smart Home API is running"}
