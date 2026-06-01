from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurante Pro-Max - Notification API"
    ENVIRONMENT: str = "development"
    DESCRIPTION: str = 'Microsserviço de notificação'
    VERSION: str = '0.1.0'

    DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

 