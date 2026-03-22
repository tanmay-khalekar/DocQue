from fastapi import FastAPI
from app.db.session import engine, Base
from app.db import models
from app.api.routes import symptom

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(symptom.router)