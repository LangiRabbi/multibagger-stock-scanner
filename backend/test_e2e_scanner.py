"""
End-to-end test Stock Scanner z prawdziwymi danymi (yfinance + Finnhub)

Ten test używa PRAWDZIWYCH API calls:
- yfinance: Pobiera historyczne dane cenowe (zmiany 7d/30d)
- Finnhub API: Pobiera fundamentals (ROE, ROCE, Market Cap, etc.)

UWAGA: Test wykonuje prawdziwe API calls do Finnhub (zużywa limity FREE tier: 60 calls/min)
"""
import logging
from typing import List
from app.services.scanner import StockScanner
from app.schemas.scan import StockResult

# Konfiguruj logging aby zobaczyć szczegóły
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator(title: str) -> None:
    """
    Wyświetla separator z tytułem dla czytelności outputu.

    Args:
        title: Tytuł sekcji
    """
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_stock_result(result: StockResult) -> None:
    """
    Wyświetla szczegółowe dane dla jednej akcji w czytelnym formacie.

    Args:
        result: Wynik skanowania dla jednej akcji
    """
    print(f"\n[STOCK] {result.symbol}")
    print("-" * 40)

    # Dane cenowe (z yfinance + Finnhub)
    print(f"Cena aktualna:      ${result.price:,.2f}")
    print(f"Zmiana 7 dni:       {result.price_change_7d:+.2f}%" if result.price_change_7d else "   Brak danych")
    print(f"Zmiana 30 dni:      {result.price_change_30d:+.2f}%" if result.price_change_30d else "   Brak danych")
    print(f"Wolumen:            {result.volume:,}")

    # Fundamentals (z Finnhub)
    print(f"\nFUNDAMENTALS:")
    print(f"   Market Cap:         ${result.market_cap:,}")
    print(f"   ROE (zwrot):        {result.roe:.2f}%")
    print(f"   ROCE (efektywnosc): {result.roce:.2f}%")

    if result.debt_equity is not None:
        print(f"   Debt/Equity:        {result.debt_equity:.3f}")
    else:
        print(f"   Debt/Equity:        Brak danych")

    print(f"   Revenue Growth:     {result.revenue_growth:.2f}%")

    if result.forward_pe is not None:
        print(f"   P/E Ratio:          {result.forward_pe:.2f}")
    else:
        print(f"   P/E Ratio:          Brak danych")

    # Czy spełnia kryteria multibagger
    if result.meets_criteria:
        print(f"\n[OK] SPELNIA kryteria multibagger!")
    else:
        print(f"\n[SKIP] NIE SPELNIA kryteriow multibagger")


def test_scanner_5_symbols() -> None:
    """
    Test główny: skanuje 5 najpopularniejszych akcji amerykańskich.

    Sprawdza:
    1. Czy dla każdego symbolu zwrócono wynik
    2. Czy dane cenowe są poprawne (price > 0, volume > 0)
    3. Czy fundamentals są pobierane z Finnhub (market_cap > 0, ROE/ROCE nie None)
    4. Czy wszystkie pola są wypełnione
    """
    print_separator("E2E TEST: Stock Scanner - yfinance + Finnhub")

    # Lista 5 znanych symboli (duże spółki tech)
    symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "TSLA"]

    logger.info(f"[SCAN] Skanowanie {len(symbols)} symboli: {', '.join(symbols)}")
    logger.info("   yfinance: Volume + Price Changes (7d, 30d)")
    logger.info("   Finnhub: 131 metryk fundamentalnych")

    # Wywołaj scanner (PRAWDZIWE API calls!)
    # UWAGA: Każdy symbol = ~2-3 Finnhub API calls (quote + fundamentals + profile)
    results: List[StockResult] = StockScanner.scan_stocks(
        symbols=symbols,
        min_volume=0,  # Wyłącz filtrowanie aby zobaczyć wszystkie wyniki
        min_price_change_percent=None,  # Wyłącz filtr zmian cen
        min_market_cap=None,  # Wyłącz wszystkie filtry
        max_market_cap=None,
        min_roe=None,
        min_roce=None,
        max_debt_equity=None,
        min_revenue_growth=None,
        max_forward_pe=None,
        save_to_db=False  # NIE zapisuj do bazy (test dziala bez PostgreSQL)
    )

    # === WERYFIKACJE ===
    print_separator("WERYFIKACJA WYNIKÓW")

    # Test 1: Liczba wyników
    assert len(results) == 5, f"[ERROR] Oczekiwano 5 wynikow, otrzymano {len(results)}"
    print(f"[OK] Test 1 PASSED: Zwrocono {len(results)}/5 wynikow")

    # Test 2-6: Weryfikacja każdego wyniku
    errors = []

    for i, result in enumerate(results, 1):
        print(f"\n--- Weryfikacja #{i}: {result.symbol} ---")

        # Test 2: Cena > 0
        if result.price <= 0:
            errors.append(f"{result.symbol}: price = {result.price} (powinno byc > 0)")
        else:
            print(f"[OK] Price: ${result.price:.2f}")

        # Test 3: Volume > 0
        if result.volume <= 0:
            errors.append(f"{result.symbol}: volume = {result.volume} (powinno byc > 0)")
        else:
            print(f"[OK] Volume: {result.volume:,}")

        # Test 4: Market Cap > 0
        if result.market_cap <= 0:
            errors.append(f"{result.symbol}: market_cap = {result.market_cap} (brak danych Finnhub)")
        else:
            print(f"[OK] Market Cap: ${result.market_cap:,}")

        # Test 5: ROE nie None (może być 0 ale nie None)
        if result.roe is None:
            errors.append(f"{result.symbol}: ROE = None (brak danych Finnhub)")
        else:
            print(f"[OK] ROE: {result.roe:.2f}%")

        # Test 6: ROCE nie None (może być 0 ale nie None)
        if result.roce is None:
            errors.append(f"{result.symbol}: ROCE = None (brak danych Finnhub)")
        else:
            print(f"[OK] ROCE: {result.roce:.2f}%")

    # Podsumowanie błędów
    if errors:
        print_separator("[ERROR] TESTY FAILED - ZNALEZIONE BLEDY")
        for error in errors:
            print(f"  * {error}")
        raise AssertionError(f"Znaleziono {len(errors)} bledow w danych")

    # === WYŚWIETL SZCZEGÓŁOWE WYNIKI ===
    print_separator("SZCZEGÓŁOWE WYNIKI SKANOWANIA")

    for result in results:
        print_stock_result(result)

    # === PODSUMOWANIE ===
    print_separator("[SUCCESS] WSZYSTKIE TESTY PASSED!")

    print(f"\n[SUMMARY] PODSUMOWANIE:")
    print(f"   * Przeskanowano: {len(results)} symboli")
    print(f"   * Dane cenowe: yfinance (volume, price changes)")
    print(f"   * Fundamentals: Finnhub API (ROE, ROCE, Market Cap, etc.)")
    print(f"   * Wszystkie dane poprawnie pobrane!")

    # Policz ile spełnia kryteria
    meets_criteria_count = sum(1 for r in results if r.meets_criteria)
    print(f"\n   [INFO] Akcje spelniajace kryteria multibagger: {meets_criteria_count}/{len(results)}")

    if meets_criteria_count > 0:
        print(f"\n   [MULTIBAGGERS] Znalezione:")
        for r in results:
            if r.meets_criteria:
                print(f"      * {r.symbol}")


if __name__ == "__main__":
    """
    Uruchomienie testu:
    1. cd backend
    2. python test_e2e_scanner.py

    UWAGA: Test używa prawdziwego Finnhub API (FREE tier: 60 calls/min)
    """
    try:
        test_scanner_5_symbols()
        print("\n" + "=" * 80)
        print("  [SUCCESS] E2E TEST ZAKONCZONY SUKCESEM!")
        print("=" * 80 + "\n")
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"  [FAILED] E2E TEST FAILED: {e}")
        print("=" * 80 + "\n")
        raise
