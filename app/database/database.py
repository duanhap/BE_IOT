# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
# Tải biến môi trường từ file .env
load_dotenv()
DB_URL = os.getenv("DB_URL")

class Database:
    def __init__(self, url):
        self.engine = create_engine(url, echo=True,     connect_args={"init_command": "SET time_zone = '+07:00'"})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self):
        return self.SessionLocal()

# instance global
database = Database(DB_URL)

def get_db():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()