import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resolve.ai"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_PLEASE_CHANGE_ME_TO_A_LONG_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./aiops.db"

    # AI Engine (OpenRouter)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "openai/gpt-oss-120b:free"
    FALLBACK_MODELS: list[str] = [
        "google/gemini-1.5-pro",
        "meta-llama/llama-3-8b-instruct:free"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
