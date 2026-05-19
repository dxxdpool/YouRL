from app.core.database import test_db_connection
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    await test_db_connection()


@app.get("/")
async def root():
    return {"message": "YouRL Shortener API is running"}
