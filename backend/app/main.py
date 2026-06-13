from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import test_db_connection
from app.core.redis import close_redis, initialize_redis
from app.modules.auth.router import router as auth_router
from app.modules.urls.public_router import router as public_url_router
from app.modules.urls.router import router as url_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await test_db_connection()
    await initialize_redis()

    yield

    await close_redis()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(url_router)
app.include_router(public_url_router)


@app.get("/")
async def root():
    return {"message": "YouRL Shortener API is running"}
