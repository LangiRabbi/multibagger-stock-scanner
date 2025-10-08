"""
Konfiguracja aplikacji (ustawienia środowiskowe)
"""
import os
import logging
from pydantic_settings import BaseSettings
from typing import Optional

# Logger dla ostrzeżeń konfiguracji
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Ustawienia aplikacji wczytywane z zmiennych środowiskowych (.env)

    Pydantic BaseSettings automatycznie wczytuje zmienne z pliku .env
    jeśli jest on w katalogu głównym projektu.
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

    def validate_api_keys(self) -> None:
        """
        Waliduje czy wymagane API keys są ustawione.

        Wyświetla ostrzeżenie (nie error) jeśli brakuje kluczy,
        bo może to być środowisko dev bez dostępu do API.
        """
        if not self.FINNHUB_API_KEY:
            logger.warning(
                "⚠️  FINNHUB_API_KEY nie jest ustawiony w .env!\n"
                "   Stock Scanner NIE BĘDZIE działał bez tego klucza.\n"
                "   Zarejestruj się BEZPŁATNIE: https://finnhub.io/register\n"
                "   Następnie dodaj do .env: FINNHUB_API_KEY=twoj_klucz"
            )
        else:
            logger.info(f"✅ FINNHUB_API_KEY załadowany: {self.FINNHUB_API_KEY[:10]}...")

    class Config:
        """
        Konfiguracja Pydantic BaseSettings

        env_file określa skąd wczytywać zmienne środowiskowe.
        Pydantic automatycznie mapuje zmienne z .env na pola klasy.
        """
        env_file = ".env"
        # case_sensitive = False oznacza że FINNHUB_API_KEY i finnhub_api_key są tym samym
        case_sensitive = False


# Singleton - jedna instancja ustawień dla całej aplikacji
settings = Settings()

# Automatyczna walidacja przy imporcie
settings.validate_api_keys()
