from fastapi import FastAPI
from app.db.session import engine, Base
from app.db import models

app = FastAPI()

Base.metadata.create_all(bind=engine)