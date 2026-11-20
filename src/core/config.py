from pydantic import BaseModel
from pydantic_settings import BaseSettings

class RunConfig(BaseModel):
    port: int = 8080
    host: str = "127.0.0.1"
    reload: bool = False

class DataBaseConfig(BaseModel):
    url: str = 'postgresql+asyncpg://serhii:serhii2006@localhost:5433/datacenter'
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_pool_size: int = 10
    max_overflow: int = 10

class Settings(BaseSettings):
    run_config: RunConfig = RunConfig()
    database_config: DataBaseConfig = DataBaseConfig()


settings = Settings()