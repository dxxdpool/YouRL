from app.core.database import test_db_connection
from app.core.redis import close_redis, initialize_redis
from app.modules.auth.router import router as auth_router
from app.modules.urls.public_router import router as public_url_router
from app.modules.urls.router import router as url_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router)
app.include_router(url_router)
app.include_router(public_url_router)


@app.on_event("startup")
async def startup():
    await test_db_connection()
    await initialize_redis()


@app.on_event("shutdown")
async def shutdown():
    await close_redis()


@app.get("/")
async def root():
    return {"message": "YouRL Shortener API is running"}
