"""
Financial Modeling Prep (FMP) API Client
Pobiera dane finansowe z oficjalnych SEC filings

Free tier: 250 requests/day
Dokumentacja: https://site.financialmodelingprep.com/developer/docs
"""
import os
import requests
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class FMPClient:
    """
    Client dla Financial Modeling Prep API.

    Używamy FMP zamiast yfinance dla fundamentals, bo:
    - Gwarantowane dane z SEC filings
    - Kompletne pola (EBIT, Total Assets, ROE, etc.)
    - Stabilne API z SLA
    """

    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self):
        """
        Inicjalizuje klienta FMP.

        Wymaga zmiennej środowiskowej FMP_API_KEY w .env
        """
        self.api_key = os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FMP_API_KEY nie znaleziony w .env! "
                "Zarejestruj się na https://site.financialmodelingprep.com/developer/docs/pricing"
            )

    def get_income_statement(self, symbol: str, limit: int = 1) -> Optional[Dict]:
        """
        Pobierz Income Statement (rachunek zysków i strat).

        Args:
            symbol: Symbol akcji (np. "AAPL")
            limit: Liczba okresów (domyślnie 1 = ostatni kwartał)

        Returns:
            Dict z danymi lub None jeśli błąd

        Pola w response:
        - operatingIncome (EBIT alternative)
        - revenue
        - netIncome
        - costOfRevenue
        """
        url = f"{self.BASE_URL}/income-statement/{symbol}"
        params = {"limit": limit, "apikey": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"FMP Income Statement: brak danych dla {symbol}")
                return None

            return data[0] if isinstance(data, list) else data

        except requests.exceptions.HTTPError as e:
            logger.error(f"FMP HTTP error dla {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"FMP Income Statement error dla {symbol}: {e}")
            return None

    def get_balance_sheet(self, symbol: str, limit: int = 1) -> Optional[Dict]:
        """
        Pobierz Balance Sheet (bilans).

        Args:
            symbol: Symbol akcji (np. "AAPL")
            limit: Liczba okresów (domyślnie 1 = ostatni kwartał)

        Returns:
            Dict z danymi lub None jeśli błąd

        Pola w response:
        - totalAssets
        - totalCurrentLiabilities
        - totalDebt
        - totalStockholdersEquity
        """
        url = f"{self.BASE_URL}/balance-sheet-statement/{symbol}"
        params = {"limit": limit, "apikey": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"FMP Balance Sheet: brak danych dla {symbol}")
                return None

            return data[0] if isinstance(data, list) else data

        except requests.exceptions.HTTPError as e:
            logger.error(f"FMP HTTP error dla {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"FMP Balance Sheet error dla {symbol}: {e}")
            return None

    def get_key_metrics(self, symbol: str) -> Optional[Dict]:
        """
        Pobierz Key Metrics TTM (Trailing Twelve Months).

        TTM = suma ostatnich 4 kwartałów (najbardziej aktualne dane)

        Args:
            symbol: Symbol akcji (np. "AAPL")

        Returns:
            Dict z danymi lub None jeśli błąd

        Pola w response:
        - marketCapTTM
        - roeTTM (Return on Equity)
        - peRatioTTM (P/E)
        - revenueGrowthTTM
        - debtToEquityTTM
        """
        url = f"{self.BASE_URL}/key-metrics-ttm/{symbol}"
        params = {"apikey": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"FMP Key Metrics: brak danych dla {symbol}")
                return None

            return data[0] if isinstance(data, list) else data

        except requests.exceptions.HTTPError as e:
            logger.error(f"FMP HTTP error dla {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"FMP Key Metrics error dla {symbol}: {e}")
            return None
