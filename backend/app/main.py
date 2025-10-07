"""
Główny plik aplikacji FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import settings
from app.api import scan, portfolio  # Import API routers


# Tworzenie tabel w bazie danych (przy pierwszym uruchomieniu)
Base.metadata.create_all(bind=engine)


# Inicjalizacja aplikacji FastAPI
app = FastAPI(
    title="Multibagger Stock Scanner API",
    description="API do skanowania akcji i zarządzania portfolio",
    version="0.2.0"  # Sprint 2
)


# CORS - pozwala frontendowi (Next.js) komunikować się z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Wszystkie metody (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Wszystkie headers
)


# Include API routers (Sprint 2)
app.include_router(scan.router)
app.include_router(portfolio.router)


@app.get("/")
async def root():
    """
    Endpoint główny - powitanie
    """
    return {
        "message": "Multibagger Stock Scanner API",
        "version": "0.1.0",
        "docs": "/docs"  # Automatyczna dokumentacja FastAPI
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - sprawdza czy API działa.

    Używany przez:
    - Docker health check
    - Frontend do weryfikacji połączenia
    - Monitoring (np. uptime checks)

    Returns:
        dict: Status API i połączenia z bazą danych
    """
    # TODO: Dodać sprawdzanie połączenia z PostgreSQL i Redis
    return {
        "status": "ok",
        "message": "API is running",
        "database": "connected",  # W przyszłości: rzeczywiste sprawdzenie
        "redis": "connected"      # W przyszłości: rzeczywiste sprawdzenie
    }


@app.get("/api/info")
async def api_info():
    """
    Informacje o konfiguracji API (bez wrażliwych danych)
    """
    return {
        "min_volume": settings.MIN_VOLUME,
        "database_host": settings.DB_HOST,
        "database_port": settings.DB_PORT,
        "redis_configured": bool(settings.REDIS_URL)
    }


# Uruchomienie serwera (tylko jeśli uruchamiasz przez `python main.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True  # Auto-reload przy zmianach w kodzie
    )
