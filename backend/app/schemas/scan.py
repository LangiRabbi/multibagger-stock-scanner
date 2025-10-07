"""
Pydantic schemas dla Stock Scanner
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ScanRequest(BaseModel):
    """
    Request body dla POST /api/scan

    Przyklad:
    {
        "symbols": ["AAPL", "MSFT", "TSLA"],
        "min_volume": 1000000,
        "min_price_change_percent": 2.0
    }
    """
    symbols: List[str] = Field(
        ...,
        description="Lista symboli akcji do skanowania (np. ['AAPL', 'MSFT'])",
        example=["AAPL", "MSFT", "TSLA"]
    )
    min_volume: Optional[int] = Field(
        1000000,
        description="Minimalny wolumen (domyslnie 1M)",
        example=1000000
    )
    min_price_change_percent: Optional[float] = Field(
        None,
        description="Minimalny % zmiana ceny (7 dni). Np. 2.0 = +2%",
        example=2.0
    )


class StockResult(BaseModel):
    """
    Pojedynczy wynik skanowania (jedna akcja)
    """
    symbol: str = Field(..., description="Symbol akcji", example="AAPL")
    price: float = Field(..., description="Aktualna cena", example=175.50)
    volume: int = Field(..., description="Wolumen z ostatniego dnia", example=50000000)
    price_change_7d: Optional[float] = Field(None, description="Zmiana ceny 7 dni (%)", example=3.5)
    price_change_30d: Optional[float] = Field(None, description="Zmiana ceny 30 dni (%)", example=8.2)
    meets_criteria: bool = Field(..., description="Czy akcja spelnia kryteria", example=True)


class ScanResponse(BaseModel):
    """
    Response dla POST /api/scan

    Przyklad:
    {
        "total_scanned": 3,
        "matches": 2,
        "results": [...]
    }
    """
    total_scanned: int = Field(..., description="Ilosc przeskanowanych akcji")
    matches: int = Field(..., description="Ilosc akcji spelniajacych kryteria")
    results: List[StockResult] = Field(..., description="Lista wynikow")
