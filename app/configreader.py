from typing import Optional

from pydantic import BaseModel, BaseSettings, PostgresDsn, RedisDsn, validator


class Telegram(BaseModel):
    token: str
    fsm_storage: str
    webhook_path: str

    @validator("fsm_storage")
    def validate_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
        return v


class Discord(BaseModel):
    token: str
    prefix: str


class Storages(BaseModel):
    redis_dsn: Optional[RedisDsn]
    postgres_dsn: PostgresDsn

    
class Fondy(BaseModel):
    merchant_id: str
    secret_key: str
    lifetime: int
    webhook_path: str


class Files(BaseModel):
    presentation: str


class Webhook(BaseModel):
    enable: bool
    domain: str


class WebApp(BaseModel):
    host: str
    port: int


class Config(BaseSettings):
    telegram: Telegram
    discord: Discord
    storages: Storages
    fondy: Fondy
    files: Files
    webhook: Webhook
    webapp: WebApp

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
