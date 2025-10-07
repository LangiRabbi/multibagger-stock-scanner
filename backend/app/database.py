"""
Konfiguracja bazy danych (SQLAlchemy)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# Silnik SQLAlchemy - odpowiada za połączenie z PostgreSQL
engine = create_engine(
    settings.database_url,
    echo=True,  # Loguje wszystkie zapytania SQL (pomocne przy debugowaniu)
    pool_pre_ping=True  # Sprawdza połączenie przed użyciem
)

# SessionLocal - fabryka sesji (sesja = "rozmowa" z bazą danych)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - klasa bazowa dla wszystkich modeli
Base = declarative_base()


def get_db():
    """
    Dependency injection dla FastAPI.
    Tworzy sesję bazy danych i zamyka ją po zakończeniu requestu.

    Użycie w endpoincie:
    @app.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
