"""
Model wyników skanowania (tabela 'scan_results')
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func

from app.database import Base


class ScanResult(Base):
    """
    Tabela przechowująca wyniki skanów akcji.

    Każdy rekord = jedna akcja która przeszła kryteria w danym dniu.

    Przykład:
    - symbol: "AAPL"
    - scan_date: 2025-10-07
    - criteria_met: {"volume": 50000000, "rsi": 65, "price_change_7d": 12.5}
    - price: 175.50
    - volume: 50000000
    """
    __tablename__ = "scan_results"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Symbol akcji
    symbol = Column(String, nullable=False, index=True)

    # Data skanu
    scan_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Spełnione kryteria (JSON - elastyczna struktura)
    # Przykład: {"volume": 50M, "rsi": 65, "ma_50_cross": true}
    criteria_met = Column(JSON, nullable=False)

    # Cena w momencie skanu
    price = Column(Float, nullable=False)

    # Wolumen w momencie skanu
    volume = Column(Integer, nullable=False)
