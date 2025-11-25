from fastapi import FastAPI
from app.routers.history_routes import router as history_router
from app.routers.light_routes import router as light_router

app = FastAPI()

app.include_router(history_router)
app.include_router(light_router)
