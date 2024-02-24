from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str

    algorithm: str
    secret_key: str
    access_token_expire_minutes: int = 30

    telegram_bot_base_url: str

    class Config:
        env_prefix = ''
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
