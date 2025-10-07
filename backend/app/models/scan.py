"""
Model wyników skanowania (tabela 'scan_results')
"""
from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, JSON
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

    # === FUNDAMENTALS (nowe kolumny) ===

    # Market Cap (kapitalizacja) - używamy BigInteger bo może być > 2B
    market_cap = Column(BigInteger, nullable=True)

    # ROE (Return on Equity) - zwrot z kapitału w %
    roe = Column(Float, nullable=True)

    # ROCE (Return on Capital Employed) - efektywność kapitału w %
    roce = Column(Float, nullable=True)

    # Debt/Equity - zadłużenie (niższe = lepsze)
    debt_equity = Column(Float, nullable=True)

    # Revenue Growth - wzrost przychodów YoY w %
    revenue_growth = Column(Float, nullable=True)

    # Forward P/E - wycena forward (niższe = tańsze)
    forward_pe = Column(Float, nullable=True)

    # Zmiana ceny 7 dni (%)
    price_change_7d = Column(Float, nullable=True)

    # Zmiana ceny 30 dni (%)
    price_change_30d = Column(Float, nullable=True)

    # Czy akcja spełnia wszystkie kryteria
    meets_criteria = Column(Boolean, default=False, nullable=False)
