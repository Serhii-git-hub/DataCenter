from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
)

if __name__ == "main_app":
    uvicorn.run(main_app,
                host=settings.run_config.host,
                port=settings.run_config.port ,
                reload=settings.run_config.reload)