from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurante Pro-Max - Payment API"
    ENVIRONMENT: str = "development"
    DESCRIPTION: str = 'Microsserviço de pagamento'
    VERSION: str = '0.1.0'


    DATABASE_URL: str

    ORDER_API_URL: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

 