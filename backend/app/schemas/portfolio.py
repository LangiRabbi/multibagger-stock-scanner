"""
Pydantic schemas dla Portfolio
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PortfolioItemCreate(BaseModel):
    """
    Request body dla POST /api/portfolio (dodawanie nowej pozycji)

    Przyklad:
    {
        "symbol": "AAPL",
        "entry_price": 150.00,
        "quantity": 10,
        "notes": "Long term hold"
    }
    """
    symbol: str = Field(..., description="Symbol akcji", example="AAPL")
    entry_price: float = Field(..., description="Cena wejscia", example=150.00)
    quantity: float = Field(0.0, description="Ilosc akcji", example=10.0)
    notes: Optional[str] = Field(None, description="Notatki", example="Long term hold")


class PortfolioItemUpdate(BaseModel):
    """
    Request body dla PUT /api/portfolio/{id} (edycja pozycji)
    """
    entry_price: Optional[float] = Field(None, description="Nowa cena wejscia")
    quantity: Optional[float] = Field(None, description="Nowa ilosc")
    notes: Optional[str] = Field(None, description="Nowe notatki")


class PortfolioItemResponse(BaseModel):
    """
    Response dla GET /api/portfolio (pojedyncza pozycja)

    Przyklad:
    {
        "id": 1,
        "user_id": 1,
        "symbol": "AAPL",
        "entry_price": 150.00,
        "quantity": 10.0,
        "notes": "Long term hold",
        "added_at": "2025-10-07T12:00:00Z"
    }
    """
    id: int
    user_id: int
    symbol: str
    entry_price: float
    quantity: float
    notes: Optional[str]
    added_at: datetime

    class Config:
        from_attributes = True  # Pozwala konwersje z SQLAlchemy model -> Pydantic
