from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.config import settings
from db.db_helper import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan
)

@main_app.get("/health")
async def health(session: AsyncSession = Depends(db_helper.session_getter)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": result.scalar()}

if __name__ == "__main__":
    uvicorn.run('main:main_app',
                host=settings.run_config.host,
                port=settings.run_config.port ,
                reload=settings.run_config.reload)