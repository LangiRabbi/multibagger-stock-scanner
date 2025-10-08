"""
Pydantic schemas dla Stock Scanner
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class ScanRequest(BaseModel):
    """
    Request body dla POST /api/scan - z kryteriami MULTIBAGGER

    Przyklad (wszystkie parametry opcjonalne poza symbols):
    {
        "symbols": ["AAPL", "MSFT", "TSLA"],
        "min_volume": 1000000,
        "min_market_cap": 50000000,
        "max_market_cap": 5000000000,
        "min_roe": 15.0,
        "min_roce": 10.0,
        "max_debt_equity": 0.3,
        "min_revenue_growth": 15.0,
        "max_forward_pe": 15.0
    }
    """
    symbols: List[str] = Field(
        ...,
        min_length=1,
        description="Lista symboli akcji do skanowania (np. ['AAPL', 'MSFT']). Musi zawierac co najmniej 1 symbol.",
        example=["AAPL", "MSFT", "TSLA"]
    )
    min_volume: Optional[int] = Field(
        1000000,
        ge=0,
        description="Minimalny wolumen (domyslnie 1M). Musi byc >= 0.",
        example=1000000
    )
    min_price_change_percent: Optional[float] = Field(
        None,
        description="Minimalny % zmiana ceny (7 dni). Np. 2.0 = +2%",
        example=2.0
    )

    # === NOWE PARAMETRY FUNDAMENTALS ===
    min_market_cap: Optional[int] = Field(
        50_000_000,
        description="Min kapitalizacja (50M = small cap)",
        example=50_000_000
    )
    max_market_cap: Optional[int] = Field(
        5_000_000_000,
        description="Max kapitalizacja (5B = mid cap)",
        example=5_000_000_000
    )
    min_roe: Optional[float] = Field(
        15.0,
        description="Min ROE % (15% = dobre)",
        example=15.0
    )
    min_roce: Optional[float] = Field(
        10.0,
        description="Min ROCE % (10% = efektywne)",
        example=10.0
    )
    max_debt_equity: Optional[float] = Field(
        0.3,
        description="Max Debt/Equity (0.3 = 30% max zadluzenie)",
        example=0.3
    )
    min_revenue_growth: Optional[float] = Field(
        15.0,
        description="Min wzrost przychodow YoY % (15% = growth)",
        example=15.0
    )
    max_forward_pe: Optional[float] = Field(
        15.0,
        description="Max Forward P/E (15 = nie przewartosciowane)",
        example=15.0
    )

    @field_validator('symbols')
    @classmethod
    def validate_symbols_not_empty(cls, v: List[str]) -> List[str]:
        """
        Walidator sprawdzający czy lista symbols nie jest pusta.

        Args:
            v: Lista symboli akcji

        Returns:
            Lista symboli jeśli walidacja przejdzie

        Raises:
            ValueError: Jeśli lista jest pusta
        """
        if not v or len(v) == 0:
            raise ValueError('symbols list cannot be empty')
        return v


class StockResult(BaseModel):
    """
    Pojedynczy wynik skanowania (jedna akcja) + fundamentals
    """
    symbol: str = Field(..., description="Symbol akcji", example="AAPL")
    price: float = Field(..., description="Aktualna cena", example=175.50)
    volume: int = Field(..., description="Wolumen z ostatniego dnia", example=50000000)
    price_change_7d: Optional[float] = Field(None, description="Zmiana ceny 7 dni (%)", example=3.5)
    price_change_30d: Optional[float] = Field(None, description="Zmiana ceny 30 dni (%)", example=8.2)

    # === FUNDAMENTALS ===
    market_cap: Optional[int] = Field(None, description="Market Cap (kapitalizacja)", example=2500000000)
    roe: Optional[float] = Field(None, description="ROE - Return on Equity (%)", example=25.5)
    roce: Optional[float] = Field(None, description="ROCE - Return on Capital Employed (%)", example=18.3)
    debt_equity: Optional[float] = Field(None, description="Debt/Equity ratio", example=0.25)
    revenue_growth: Optional[float] = Field(None, description="Revenue Growth YoY (%)", example=22.1)
    forward_pe: Optional[float] = Field(None, description="Forward P/E ratio", example=12.5)

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
