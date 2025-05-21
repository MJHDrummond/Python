from fastapi import FastAPI
from app.db import models, engine
from app.api.routes import router as api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "NYC Analytics API is running!"}