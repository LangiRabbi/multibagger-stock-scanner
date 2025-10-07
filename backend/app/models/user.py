"""
Model użytkownika (tabela 'users')
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    Tabela użytkowników aplikacji.

    Relacje:
    - user.portfolio_items -> lista pozycji w portfolio użytkownika
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Email użytkownika (unikalny - nie może być duplikatów)
    email = Column(String, unique=True, index=True, nullable=False)

    # Zahaszowane hasło (NIGDY nie przechowujemy plain text!)
    hashed_password = Column(String, nullable=False)

    # Data utworzenia konta (automatycznie ustawiana)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacja: jeden user -> wiele portfolio_items
    portfolio_items = relationship("PortfolioItem", back_populates="user")
