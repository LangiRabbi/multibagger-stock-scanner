"""
Stock Scanner API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.schemas.scan import ScanRequest, ScanResponse
from app.services.scanner import StockScanner
import logging

router = APIRouter(prefix="/api", tags=["Scanner"])
logger = logging.getLogger(__name__)


@router.post("/scan", response_model=ScanResponse)
async def scan_stocks(request: ScanRequest):
    """
    Skanuje akcje wedlug kryteriow.

    **Przyklad request:**
    ```json
    {
        "symbols": ["AAPL", "MSFT", "TSLA", "GOOGL"],
        "min_volume": 1000000,
        "min_price_change_percent": 2.0
    }
    ```

    **Przyklad response:**
    ```json
    {
        "total_scanned": 4,
        "matches": 2,
        "results": [
            {
                "symbol": "AAPL",
                "price": 175.50,
                "volume": 50000000,
                "price_change_7d": 3.5,
                "price_change_30d": 8.2,
                "meets_criteria": true
            }
        ]
    }
    ```
    """
    try:
        # Wywolaj StockScanner service z WSZYSTKIMI parametrami
        results = StockScanner.scan_stocks(
            symbols=request.symbols,
            min_volume=request.min_volume or 1_000_000,
            min_price_change_percent=request.min_price_change_percent,
            # === FUNDAMENTALS ===
            min_market_cap=request.min_market_cap,
            max_market_cap=request.max_market_cap,
            min_roe=request.min_roe,
            min_roce=request.min_roce,
            max_debt_equity=request.max_debt_equity,
            min_revenue_growth=request.min_revenue_growth,
            max_forward_pe=request.max_forward_pe
        )

        # Policz matches (akcje spelniajace kryteria)
        matches = sum(1 for r in results if r.meets_criteria)

        return ScanResponse(
            total_scanned=len(results),
            matches=matches,
            results=results
        )

    except ValueError as e:
        # Blad walidacji danych (np. nieprawidlowy symbol)
        logger.error(f"Validation error podczas skanowania: {e}")
        raise HTTPException(
            status_code=422,
            detail=f"Nieprawidlowe dane wejsciowe: {str(e)}"
        )

    except Exception as e:
        # Ogolny blad (API timeout, network error, itp.)
        logger.error(f"Nieoczekiwany blad podczas skanowania akcji: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Nie udalo sie przetworzyc skanowania: {str(e)}"
        )
