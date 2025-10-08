"""
Finnhub.io API Client
Pobiera dane finansowe fundamentalne dla stock scanner

FREE tier: 60 API calls/minute
Dokumentacja: https://finnhub.io/docs/api

OPTYMALIZACJE:
1. Redis cache (15 minut TTL) - zmniejsza API calls
2. Rate limiter (60 calls/min) - chroni przed przekroczeniem limitów
3. Exponential backoff - retry przy 429 error
"""
import finnhub
from typing import Optional, Dict, Callable, Any
import logging
import time
from ratelimit import limits, sleep_and_retry
from app.config import settings
from app.cache import cache

logger = logging.getLogger(__name__)


class FinnhubClient:
    """
    Client dla Finnhub.io API z rate limiting i cache.

    Finnhub przewaga nad FMP:
    - FREE tier DZIAŁA (60 calls/min vs FMP 403 Forbidden)
    - 117 metryk w JEDNYM calu (/stock/metric?metric=all)
    - Gwarantowane dane: ROE, ROIC, Debt/Equity, P/E, etc.
    - Oficjalny Python SDK

    OPTYMALIZACJE:
    - Rate limiter: Max 60 calls/min (automatyczne czekanie)
    - Redis cache: 15 min TTL (zmniejsza API calls)
    - Retry logic: Exponential backoff przy 429 errors
    """

    # Константы rate limiting
    CALLS_PER_MINUTE = 60  # FREE tier limit
    RATE_LIMIT_PERIOD = 60  # 60 sekund

    def __init__(self):
        """
        Inicjalizuje klienta Finnhub.

        Wymaga zmiennej środowiskowej FINNHUB_API_KEY w .env
        """
        self.api_key = settings.FINNHUB_API_KEY
        if not self.api_key:
            raise ValueError(
                "FINNHUB_API_KEY nie znaleziony w .env! "
                "Zarejestruj się na https://finnhub.io/register (FREE tier)"
            )

        # Inicjalizuj oficjalny klient Finnhub
        self.client = finnhub.Client(api_key=self.api_key)

    @sleep_and_retry
    @limits(calls=CALLS_PER_MINUTE, period=RATE_LIMIT_PERIOD)
    def _rate_limited_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Wrapper dla WSZYSTKICH Finnhub API calls z rate limiting.

        Automatycznie czeka jeśli przekroczony limit 60 calls/min.
        Decorator @sleep_and_retry powoduje że funkcja czeka zamiast rzucić error.

        Args:
            func: Funkcja Finnhub API do wywołania (np. self.client.quote)
            *args: Argumenty funkcji
            **kwargs: Keyword argumenty funkcji

        Returns:
            Wynik funkcji API

        Example:
            # Zamiast: self.client.quote("AAPL")
            # Używamy: self._rate_limited_call(self.client.quote, "AAPL")
        """
        logger.debug(f"[RATE LIMITER] Calling {func.__name__} with args={args}")
        return func(*args, **kwargs)

    def _make_request_with_retry(
        self,
        func: Callable,
        *args,
        max_retries: int = 3,
        **kwargs
    ) -> Optional[Any]:
        """
        Wywołuje API z retry logic i exponential backoff.

        Jeśli dostaniemy 429 (Too Many Requests), czekamy i próbujemy ponownie.
        Czasy oczekiwania: 1s, 2s, 4s (exponential backoff).

        Args:
            func: Funkcja API do wywołania
            *args: Argumenty funkcji
            max_retries: Max liczba prób (default 3)
            **kwargs: Keyword argumenty

        Returns:
            Wynik funkcji lub None jeśli wszystkie próby failed
        """
        for attempt in range(max_retries):
            try:
                # Użyj rate limiter wrapper
                return self._rate_limited_call(func, *args, **kwargs)

            except Exception as e:
                error_str = str(e)

                # 429 = Too Many Requests (rate limit exceeded)
                if "429" in error_str or "rate limit" in error_str.lower():
                    wait_time = 2 ** attempt  # 1s, 2s, 4s
                    logger.warning(
                        f"⚠ Rate limit hit! Retry {attempt + 1}/{max_retries} "
                        f"za {wait_time}s... (error: {error_str})"
                    )
                    time.sleep(wait_time)
                    continue

                # Inny błąd - rzuć error
                logger.error(f"API error: {error_str}")
                raise

        # Wszystkie próby failed
        logger.error(f"Max retries ({max_retries}) exceeded")
        return None

    @cache(ttl=900, key_prefix="finnhub")  # Cache 15 minut
    def get_fundamentals(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz WSZYSTKIE fundamentals w jednym API calu.

        OPTYMALIZACJE:
        - Cache: 15 minut TTL
        - Rate limiter: Max 60 calls/min
        - Retry: Exponential backoff przy 429

        Args:
            symbol: Symbol akcji (np. "AAPL")

        Returns:
            Dict z kluczami:
            - 'metric': Dict z 117 metrykami (roeTTM, roicTTM, totalDebtToEquity, etc.)
            - 'series': Dict z historical data (annual, quarterly)

        Example response:
        {
          "metric": {
            "roeTTM": 147.25,
            "roicTTM": 45.32,
            "totalDebtToEquity": 1.73,
            "peTTM": 28.5,
            "netMargin": 25.31,
            ... (117 total metrics)
          },
          "series": {
            "annual": {
              "revenue": [
                {"period": "2023-09-30", "v": 383285000000},
                {"period": "2022-09-24", "v": 394328000000}
              ]
            }
          }
        }
        """
        try:
            # Użyj rate-limited call z retry logic
            fundamentals = self._make_request_with_retry(
                self.client.company_basic_financials,
                symbol,
                'all'
            )

            if not fundamentals or 'metric' not in fundamentals:
                logger.warning(f"Finnhub: brak danych fundamentals dla {symbol}")
                return None

            return fundamentals

        except Exception as e:
            logger.error(f"Finnhub fundamentals error dla {symbol}: {e}")
            return None

    @cache(ttl=900, key_prefix="finnhub")  # Cache 15 minut
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz real-time quote (price, volume, etc.)

        OPTYMALIZACJE:
        - Cache: 15 minut TTL
        - Rate limiter: Max 60 calls/min
        - Retry: Exponential backoff przy 429

        Args:
            symbol: Symbol akcji (np. "AAPL")

        Returns:
            Dict z kluczami:
            - 'c': Current price
            - 'h': High price of the day
            - 'l': Low price of the day
            - 'o': Open price of the day
            - 'pc': Previous close price
            - 'v': Volume

        Example:
        {
          "c": 175.50,
          "h": 176.20,
          "l": 174.80,
          "o": 175.00,
          "pc": 174.50,
          "v": 50000000
        }
        """
        try:
            # Użyj rate-limited call z retry logic
            quote = self._make_request_with_retry(
                self.client.quote,
                symbol
            )

            if not quote or 'c' not in quote:
                logger.warning(f"Finnhub: brak danych quote dla {symbol}")
                return None

            return quote

        except Exception as e:
            logger.error(f"Finnhub quote error dla {symbol}: {e}")
            return None

    @cache(ttl=3600, key_prefix="finnhub")  # Cache 60 minut (zmienia się rzadko)
    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz company profile (market cap, industry, etc.)

        OPTYMALIZACJE:
        - Cache: 60 minut TTL (profile zmienia się bardzo rzadko)
        - Rate limiter: Max 60 calls/min
        - Retry: Exponential backoff przy 429

        Args:
            symbol: Symbol akcji (np. "AAPL")

        Returns:
            Dict z danymi firmy (marketCapitalization, industry, etc.)
        """
        try:
            # Użyj rate-limited call z retry logic
            profile = self._make_request_with_retry(
                self.client.company_profile2,
                symbol=symbol
            )

            if not profile:
                logger.warning(f"Finnhub: brak danych profile dla {symbol}")
                return None

            return profile

        except Exception as e:
            logger.error(f"Finnhub profile error dla {symbol}: {e}")
            return None
