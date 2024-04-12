from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_URL: str
    REDIS_URL: str
    PREFIX_URL: str
    SUPERUSER_HEADER: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
