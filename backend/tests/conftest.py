"""
Shared fixtures dla pytest
Zawiera mock data dla Finnhub API, yfinance, oraz testowy client FastAPI
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
from fastapi.testclient import TestClient
import os

# Wyłącz Redis dla testów (używamy mock cache)
os.environ["REDIS_ENABLED"] = "false"


@pytest.fixture
def mock_finnhub_fundamentals():
    """
    Mock response dla Finnhub company_basic_financials (metric=all).

    UWAGA: Wartości są aproksymowane - testy używają pytest.approx() dla float.
    Zawiera 117 metryk fundamentalnych.
    """
    return {
        'metric': {
            'marketCapitalization': 3825259,  # w milionach USD (aktualne dane)
            'roeTTM': 154.92,                 # Return on Equity (%)
            'roicTTM': 56.99,                 # Return on Invested Capital (%)
            'peTTM': 38.38,                   # Price-to-Earnings ratio
            'totalDebt/totalEquityAnnual': 1.888,  # Debt/Equity ratio (zaokrąglone)
            'revenueGrowthTTMYoy': 5.97,      # Revenue Growth Year-over-Year (%)
        },
        'series': {
            'annual': {
                'roic': [
                    {'period': '2023-09-30', 'v': 0.5699},  # ROIC historyczny
                    {'period': '2022-09-30', 'v': 0.5123},
                ]
            }
        }
    }


@pytest.fixture
def mock_finnhub_quote():
    """
    Mock response dla Finnhub quote endpoint.

    UWAGA: Volume NIE jest dostępny w Finnhub FREE tier quote!
    Volume pobieramy z yfinance.
    Wartości aproksymowane - testy używają pytest.approx().
    """
    return {
        'c': 258.06,   # current price (aktualne dane)
        'h': 258.00,   # high price of the day
        'l': 254.00,   # low price of the day
        'o': 255.00,   # open price
        'pc': 254.50,  # previous close price
        'v': None      # Volume NIE jest w FREE tier!
    }


@pytest.fixture
def mock_yfinance_history():
    """
    Mock dla yfinance Ticker.history() - 30 dni danych.

    Zwraca DataFrame z kolumnami Close i Volume.
    Używany do obliczenia price_change_7d i price_change_30d.
    """
    # Symuluj 30 dni danych (Close price wzrasta z 250 do 256.48)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')

    # Ceny rosną liniowo od 250 do 256.48
    close_prices = [250.0 + (i * 0.216) for i in range(30)]

    # Volume około 50M dziennie
    volumes = [50_000_000 + (i * 100_000) for i in range(30)]

    return pd.DataFrame({
        'Close': close_prices,
        'Volume': volumes
    }, index=dates)


@pytest.fixture
def mock_yfinance_ticker(mock_yfinance_history):
    """
    Mock dla yfinance Ticker object.

    Returns:
        MagicMock: Mock który symuluje yf.Ticker("AAPL")
    """
    mock = MagicMock()
    mock.history.return_value = mock_yfinance_history
    return mock


@pytest.fixture
def mock_finnhub_client(mock_finnhub_fundamentals, mock_finnhub_quote):
    """
    Mock dla FinnhubClient class.

    Zwraca mock który symuluje wszystkie metody FinnhubClient:
    - get_fundamentals()
    - get_quote()
    """
    mock = MagicMock()
    mock.get_fundamentals.return_value = mock_finnhub_fundamentals
    mock.get_quote.return_value = mock_finnhub_quote
    return mock


@pytest.fixture
def fastapi_test_client():
    """
    Test client dla FastAPI app.

    Używany do integration tests endpoints.
    """
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_symbols():
    """Lista przykładowych symboli do testów"""
    return ["AAPL", "MSFT", "NVDA"]


@pytest.fixture
def invalid_symbol():
    """Niepoprawny symbol (nie istnieje na giełdzie)"""
    return "INVALID123"
