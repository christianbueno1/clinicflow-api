from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_name: str

    debug: bool = False
    api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.database_user,
            password=self.database_password,
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
