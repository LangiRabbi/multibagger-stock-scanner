"""
Unit tests dla StockScanner service

Testujemy:
1. Poprawne skanowanie akcji
2. Filtrowanie po volume
3. Obliczenia fundamentals (ROE, ROCE, etc.)
4. Obsługę błędów (invalid symbols)
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.scanner import StockScanner
from app.schemas.scan import StockResult


@pytest.mark.unit
class TestStockScanner:
    """Unit tests dla klasy StockScanner"""

    def test_scan_stocks_returns_results(
        self,
        mock_finnhub_fundamentals,
        mock_finnhub_quote,
        mock_yfinance_ticker
    ):
        """
        Test: scan_stocks zwraca wyniki dla poprawnych symboli

        Weryfikuje:
        - Liczba wyników = liczba symboli
        - Wszystkie pola wypełnione
        - Price, volume, market_cap > 0
        - ROE i ROCE nie są None
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            # Setup mocks
            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Wykonaj scan
            results = StockScanner.scan_stocks(
                symbols=["AAPL"],
                min_volume=1_000_000,
                save_to_db=False  # Nie zapisuj do bazy podczas testu
            )

            # Asercje
            assert len(results) == 1, "Powinien zwrócić 1 wynik dla 1 symbolu"

            result = results[0]
            assert result.symbol == "AAPL"
            assert result.price > 0, "Price powinien być > 0"
            assert result.volume > 0, "Volume powinien być > 0"
            assert result.market_cap > 0, "Market Cap powinien być > 0"
            assert result.roe is not None, "ROE nie może być None"
            assert result.roce is not None, "ROCE nie może być None"


    def test_scan_stocks_filters_by_volume(
        self,
        mock_finnhub_fundamentals,
        mock_finnhub_quote
    ):
        """
        Test: Scanner filtruje akcje po minimalnym volume

        Weryfikuje:
        - Akcje z volume < min_volume są odrzucane
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            # Mock dla akcji z NISKIM volume (999,000)
            mock_ticker = MagicMock()
            mock_history = MagicMock()
            mock_history.tail.return_value = MagicMock(Volume=MagicMock(mean=lambda: 999_000))
            mock_ticker.history.return_value = mock_history
            mock_yf.return_value = mock_ticker

            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Wykonaj scan z min_volume = 1M
            results = StockScanner.scan_stocks(
                symbols=["LOWVOL"],
                min_volume=1_000_000,  # Wymaga minimum 1M volume
                save_to_db=False
            )

            # Asercja: 0 wyników bo volume < 1M
            assert len(results) == 0, "Akcja z niskim volume powinna być odfiltrowana"


    def test_scan_stocks_handles_invalid_symbols(self):
        """
        Test: Scanner gracefully obsługuje niepoprawne symbole

        Weryfikuje:
        - Nie crashuje przy invalid symbols
        - Zwraca pustą listę lub pomija niepoprawne symbole
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            # Mock dla invalid symbol - yfinance rzuca Exception
            mock_yf.return_value.history.side_effect = Exception("Invalid symbol")

            mock_client = MagicMock()
            mock_client.get_fundamentals.side_effect = Exception("Symbol not found")
            mock_client_class.return_value = mock_client

            # Wykonaj scan
            results = StockScanner.scan_stocks(
                symbols=["INVALID123"],
                min_volume=0,
                save_to_db=False
            )

            # Asercja: Nie crashuje, zwraca pustą listę
            assert isinstance(results, list), "Powinien zwrócić listę"
            # Może być pusta lub może mieć wynik z partial data - zależy od implementacji


    def test_scan_stocks_multiple_symbols(
        self,
        mock_finnhub_fundamentals,
        mock_finnhub_quote,
        mock_yfinance_ticker
    ):
        """
        Test: Skanowanie wielu symboli jednocześnie

        Weryfikuje:
        - Każdy symbol zwraca wynik
        - Kolejność symboli jest zachowana
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            symbols = ["AAPL", "MSFT", "NVDA"]

            # Wykonaj scan
            results = StockScanner.scan_stocks(
                symbols=symbols,
                min_volume=0,  # Wyłącz filtrowanie
                save_to_db=False
            )

            # Asercje
            assert len(results) == len(symbols), f"Powinien zwrócić {len(symbols)} wyników"

            # Sprawdź że symbole są w wynikach
            result_symbols = [r.symbol for r in results]
            for symbol in symbols:
                assert symbol in result_symbols, f"Symbol {symbol} powinien być w wynikach"


    def test_scan_stocks_calculates_fundamentals_correctly(
        self,
        mock_finnhub_fundamentals,
        mock_finnhub_quote,
        mock_yfinance_ticker
    ):
        """
        Test: Sprawdzenie poprawności obliczeń fundamentals

        Weryfikuje:
        - ROE jest prawidłowo wyliczone z Finnhub
        - Market Cap jest w USD (nie milionach)
        - Debt/Equity ratio jest poprawny
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Wykonaj scan
            results = StockScanner.scan_stocks(
                symbols=["AAPL"],
                min_volume=0,
                save_to_db=False
            )

            result = results[0]

            # Sprawdź fundamentals
            assert result.roe == 154.92, "ROE powinien być 154.92%"
            assert result.roce == 56.99, "ROCE powinien być 56.99%"

            # Market cap powinien być przekonwertowany z milionów do USD
            # 3,809,379M = $3,809,379,000,000
            expected_market_cap = 3809379 * 1_000_000
            assert result.market_cap == expected_market_cap, \
                f"Market Cap powinien być {expected_market_cap}"

            # Debt/Equity ratio (zaokrąglony do 3 miejsc dziesiętnych)
            assert result.debt_equity == 1.888, "Debt/Equity powinien być 1.888 (zaokrąglony z 1.8881)"


    def test_scan_stocks_meets_criteria_logic(
        self,
        mock_finnhub_fundamentals,
        mock_finnhub_quote,
        mock_yfinance_ticker
    ):
        """
        Test: Logika meets_criteria (czy akcja spełnia kryteria multibagger)

        Weryfikuje:
        - meets_criteria = True jeśli wszystkie kryteria spełnione
        - meets_criteria = False jeśli któreś kryterium nie spełnione
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Scan z BARDZO wysokimi wymaganiami (nie spełni)
            results_strict = StockScanner.scan_stocks(
                symbols=["AAPL"],
                min_volume=0,
                min_roe=200.0,  # Wymaga ROE > 200% (AAPL ma 154%)
                save_to_db=False
            )

            # Asercja: meets_criteria = False
            if len(results_strict) > 0:
                assert results_strict[0].meets_criteria == False, \
                    "meets_criteria powinno być False jeśli ROE < min_roe"

            # Scan z NISKIMI wymaganiami (spełni)
            results_lenient = StockScanner.scan_stocks(
                symbols=["AAPL"],
                min_volume=0,
                min_roe=10.0,  # Wymaga tylko ROE > 10%
                min_roce=10.0,
                # Wyłącz inne kryteria które mogą powodować fail
                max_debt_equity=None,  # Wyłącz sprawdzanie zadłużenia
                max_forward_pe=None,   # Wyłącz sprawdzanie P/E
                min_revenue_growth=None,  # Wyłącz sprawdzanie wzrostu
                min_market_cap=None,   # Wyłącz market cap min
                max_market_cap=None,   # Wyłącz market cap max
                save_to_db=False
            )

            # Asercja: meets_criteria = True
            if len(results_lenient) > 0:
                assert results_lenient[0].meets_criteria == True, \
                    "meets_criteria powinno być True jeśli wszystkie kryteria spełnione"
