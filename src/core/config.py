
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class RunConfig(BaseModel):
    port: int = 8000
    host: str = "127.0.0.1"
    reload: bool = False

class DataBaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_nested_delimiter='__'
    )
    run_config: RunConfig = RunConfig()
    database_config: DataBaseConfig


settings = Settings()