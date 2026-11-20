from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from src.core.config import settings



class DataBaseHelper:
    def __init__(self ,
                 url: str,
                 echo: bool = False,
                 echo_pool: bool = False,
                 pool_size: int = 10 ,
                 max_overflow: int = 10) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url= url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

        self.session_factor = async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind = self.engine,
            expire_on_commit = False,
            autoflush = False,
            autocommit = False,
        )

        async def dispose()-> None:
            return await self.engine.dispose()

        async def session_getter() -> AsyncGenerator[AsyncSession, None]:
            async with self.session_factor() as session:
                yield session

db_helper = DataBaseHelper(
    url = settings.database_config.url,
    echo = settings.database_config.echo,
    echo_pool = settings.database_config.echo_pool,
    pool_size = settings.database_config.pool_size,
    max_overflow = settings.database_config.max_overflow
)

