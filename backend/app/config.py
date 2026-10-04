from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "PolicyLens AI"
    environment: str = "development"

    mongodb_uri: str
    mongodb_db: str

    openrouter_api_key: str
    openrouter_embedding_model: str
    openrouter_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()