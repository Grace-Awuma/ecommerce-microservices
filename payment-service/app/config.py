from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/paymentdb"
    SERVICE_NAME: str = "payment-service"
    PORT: int = 8002

    class Config:
        env_file = ".env"


settings = Settings()
