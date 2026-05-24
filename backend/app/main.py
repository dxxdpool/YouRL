import app.models
from app.core.database import test_db_connection
from app.modules.auth.router import router as auth_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await test_db_connection()


@app.get("/")
async def root():
    return {"message": "YouRL Shortener API is running"}
