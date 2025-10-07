"""
Finnhub.io API Client
Pobiera dane finansowe fundamentalne dla stock scanner

FREE tier: 60 API calls/minute
Dokumentacja: https://finnhub.io/docs/api
"""
import finnhub
from typing import Optional, Dict
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class FinnhubClient:
    """
    Client dla Finnhub.io API.

    Finnhub przewaga nad FMP:
    - FREE tier DZIAŁA (60 calls/min vs FMP 403 Forbidden)
    - 117 metryk w JEDNYM calu (/stock/metric?metric=all)
    - Gwarantowane dane: ROE, ROIC, Debt/Equity, P/E, etc.
    - Oficjalny Python SDK
    """

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

    def get_fundamentals(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz WSZYSTKIE fundamentals w jednym API calu.

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
            # company_basic_financials(symbol, metric)
            # metric='all' zwraca wszystkie 117 metryk
            fundamentals = self.client.company_basic_financials(symbol, 'all')

            if not fundamentals or 'metric' not in fundamentals:
                logger.warning(f"Finnhub: brak danych fundamentals dla {symbol}")
                return None

            return fundamentals

        except Exception as e:
            logger.error(f"Finnhub fundamentals error dla {symbol}: {e}")
            return None

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz real-time quote (price, volume, etc.)

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
            quote = self.client.quote(symbol)

            if not quote or 'c' not in quote:
                logger.warning(f"Finnhub: brak danych quote dla {symbol}")
                return None

            return quote

        except Exception as e:
            logger.error(f"Finnhub quote error dla {symbol}: {e}")
            return None

    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz company profile (market cap, industry, etc.)

        Args:
            symbol: Symbol akcji (np. "AAPL")

        Returns:
            Dict z danymi firmy (marketCapitalization, industry, etc.)
        """
        try:
            profile = self.client.company_profile2(symbol=symbol)

            if not profile:
                logger.warning(f"Finnhub: brak danych profile dla {symbol}")
                return None

            return profile

        except Exception as e:
            logger.error(f"Finnhub profile error dla {symbol}: {e}")
            return None
