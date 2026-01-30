from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- DB ----
    DATABASE_URL: str

    # ---- storage/media ----
    MEDIA_DIR: str = "media"

    # ---- web admin auth ----
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_JWT_SECRET: str
    ADMIN_JWT_EXPIRES_MINUTES: int = 1440

    BOT_ADMIN_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    @property
    def bot_admin_token(self) -> str:
        return self.BOT_ADMIN_TOKEN
    
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def media_dir(self) -> str:
        # код в storage.py читает settings.media_dir
        return self.MEDIA_DIR


settings = Settings()
