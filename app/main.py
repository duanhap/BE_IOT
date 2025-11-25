from fastapi import FastAPI
from app.routers.history_routes import router as history_router

app = FastAPI()

app.include_router(history_router)
