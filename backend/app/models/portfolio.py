"""
Model pozycji w portfolio (tabela 'portfolio_items')
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class PortfolioItem(Base):
    """
    Tabela przechowująca akcje zapisane w portfolio użytkownika.

    Przykład:
    - User #1 dodał AAPL po cenie $150, ilość 10 akcji, notatka "Long term hold"
    """
    __tablename__ = "portfolio_items"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key -> users.id (który użytkownik dodał tę pozycję)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Symbol akcji (np. AAPL, TSLA, MSFT)
    symbol = Column(String, nullable=False, index=True)

    # Cena wejścia (po jakiej cenie użytkownik "zapamiętał" akcję)
    entry_price = Column(Float, nullable=False)

    # Ilość akcji (opcjonalne, domyślnie 0 = tracking tylko)
    quantity = Column(Float, default=0.0)

    # Notatki użytkownika (np. "Waiting for Q3 earnings")
    notes = Column(Text, nullable=True)

    # Data dodania
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacja: wiele portfolio_items -> jeden user
    user = relationship("User", back_populates="portfolio_items")
