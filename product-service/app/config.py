from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/productdb"
    SERVICE_NAME: str = "product-service"
    PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()