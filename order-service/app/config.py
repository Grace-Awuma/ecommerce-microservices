from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/orderdb"
    PRODUCT_SERVICE_URL: str = "http://localhost:8000"
    PAYMENT_SERVICE_URL: str = "http://localhost:8002"
    SERVICE_NAME: str = "order-service"
    PORT: int = 8001

    class Config:
        env_file = ".env"

settings = Settings()