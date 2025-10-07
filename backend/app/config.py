"""
Konfiguracja aplikacji (ustawienia środowiskowe)
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Ustawienia aplikacji wczytywane z zmiennych środowiskowych (.env)
    """
    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "multibagger"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433  # Port zmieniony na 5433 bo lokalny postgres zajmuje 5432

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # API
    PORT: int = 8000
    MIN_VOLUME: int = 1000000

    # API Keys
    # Finnhub.io - WYMAGANE dla stock scanner fundamentals
    # FREE tier: 60 calls/min, 117 metrics w jednym calu
    FINNHUB_API_KEY: str = ""

    # Inne API Keys (opcjonalne)
    ALPHA_VANTAGE_API_KEY: str = ""

    @property
    def database_url(self) -> str:
        """
        Tworzy URL połączenia do PostgreSQL
        Format: postgresql://user:password@host:port/database
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


# Singleton - jedna instancja ustawień dla całej aplikacji
settings = Settings()
