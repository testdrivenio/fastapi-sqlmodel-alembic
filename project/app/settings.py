import os
from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any, Union

class Settings(BaseSettings):    
    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
    DATABASE_PORT: Union[int, str] = os.environ.get("DATABASE_PORT")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")
    ASYNC_DATABASE_URI: Optional[
        Any
    ] = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")
