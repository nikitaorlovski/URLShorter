from contextlib import asynccontextmanager

import redis
import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from database.config import settings
from database.database import create_tables
from routers.redirects import router as redirect_router
from routers.urls import router as url_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_tables()
        print("✅ Database tables created")
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )
        redis_client.ping()
        print(f"✅ Redis connected to {settings.REDIS_HOST}:{settings.REDIS_PORT}")

        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        print("✅ Cache initialized")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        raise
    yield
    redis_client.close()
    print("✅ Redis connection closed")


app = FastAPI(lifespan=lifespan)

app.include_router(url_router)
app.include_router(redirect_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
