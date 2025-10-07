"""
Portfolio API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.portfolio import PortfolioItemCreate, PortfolioItemUpdate, PortfolioItemResponse
from app.services.portfolio import PortfolioService

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])


# MOCK USER ID (w Sprint 3 bedzie authentication)
MOCK_USER_ID = 1


@router.get("", response_model=List[PortfolioItemResponse])
async def get_portfolio(db: Session = Depends(get_db)):
    """
    Pobierz wszystkie pozycje portfolio uzytkownika.

    **Response:**
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "symbol": "AAPL",
            "entry_price": 150.00,
            "quantity": 10.0,
            "notes": "Long term hold",
            "added_at": "2025-10-07T12:00:00Z"
        }
    ]
    ```
    """
    items = PortfolioService.get_all(db, user_id=MOCK_USER_ID)
    return items


@router.get("/{item_id}", response_model=PortfolioItemResponse)
async def get_portfolio_item(item_id: int, db: Session = Depends(get_db)):
    """
    Pobierz pojedyncza pozycje portfolio po ID.
    """
    item = PortfolioService.get_by_id(db, item_id=item_id, user_id=MOCK_USER_ID)
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return item


@router.post("", response_model=PortfolioItemResponse, status_code=201)
async def create_portfolio_item(
    item: PortfolioItemCreate,
    db: Session = Depends(get_db)
):
    """
    Dodaj nowa akcje do portfolio.

    **Request:**
    ```json
    {
        "symbol": "AAPL",
        "entry_price": 150.00,
        "quantity": 10,
        "notes": "Long term hold"
    }
    ```
    """
    new_item = PortfolioService.create(db, user_id=MOCK_USER_ID, item=item)
    return new_item


@router.put("/{item_id}", response_model=PortfolioItemResponse)
async def update_portfolio_item(
    item_id: int,
    updates: PortfolioItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Edytuj istniejaca pozycje portfolio.

    **Request (partial update):**
    ```json
    {
        "notes": "Updated notes"
    }
    ```
    """
    updated_item = PortfolioService.update(
        db,
        item_id=item_id,
        user_id=MOCK_USER_ID,
        updates=updates
    )
    if not updated_item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return updated_item


@router.delete("/{item_id}", status_code=204)
async def delete_portfolio_item(item_id: int, db: Session = Depends(get_db)):
    """
    Usun pozycje z portfolio.
    """
    success = PortfolioService.delete(db, item_id=item_id, user_id=MOCK_USER_ID)
    if not success:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return None
