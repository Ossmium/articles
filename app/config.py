from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_DRIVER: str
    POSTGRES_CONN: str
    SECRET_KEY: str
    SECRET_ALGORITHM: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env-dev")


settings = Settings()
print(settings.POSTGRES_CONN, settings.POSTGRES_HOST)
