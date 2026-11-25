from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.config import settings
from db.db_helper import db_helper

from routers.auth import router as auth_router
from routers.categories import router as category_router
from routers.suppliers import router as supplier_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan
)
main_app.include_router(auth_router)
main_app.include_router(category_router)
main_app.include_router(supplier_router)

if __name__ == "__main__":
    uvicorn.run('main:main_app',
                host=settings.run_config.host,
                port=settings.run_config.port ,
                reload=settings.run_config.reload)