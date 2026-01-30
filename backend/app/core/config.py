from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(validation_alias="DATABASE_URL")
    
    bot_admin_token: str = Field(default="dev-bot-admin-token", validation_alias="BOT_ADMIN_TOKEN")

    # JWT
    jwt_secret: str = Field(default="dev-secret-change-me", validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALG")
    jwt_exp_minutes: int = Field(default=60 * 24, validation_alias="JWT_EXP_MIN")

    # Admin credentials (для MVP — позже можно вынести в таблицу админов)
    admin_username: str = Field(default="admin", validation_alias="ADMIN_USER")
    admin_password: str = Field(default="admin", validation_alias="ADMIN_PASS")

        # Media storage (локально)
    media_dir: str = Field(default="/code/storage", validation_alias="MEDIA_DIR")
    public_base_url: str = Field(default="http://localhost:8000", validation_alias="PUBLIC_BASE_URL")


settings = Settings()
