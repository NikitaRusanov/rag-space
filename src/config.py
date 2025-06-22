from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class EmbeddingConfig(BaseModel):
    model_name: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    embeddings: EmbeddingConfig


settings = Settings()
