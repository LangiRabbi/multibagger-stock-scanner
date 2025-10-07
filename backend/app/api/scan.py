"""
Stock Scanner API endpoints
"""
from fastapi import APIRouter
from app.schemas.scan import ScanRequest, ScanResponse
from app.services.scanner import StockScanner

router = APIRouter(prefix="/api", tags=["Scanner"])


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
    # Wywolaj StockScanner service
    results = StockScanner.scan_stocks(
        symbols=request.symbols,
        min_volume=request.min_volume or 1000000,
        min_price_change_percent=request.min_price_change_percent
    )

    # Policz matches (akcje spelniajace kryteria)
    matches = sum(1 for r in results if r.meets_criteria)

    return ScanResponse(
        total_scanned=len(results),
        matches=matches,
        results=results
    )
