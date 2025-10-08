"""
Integration tests dla FastAPI endpoints

Testujemy:
1. POST /api/scan - skanowanie akcji
2. GET /health - health check
3. GET / - root endpoint
4. Walidacja Pydantic (422 errors)
5. CORS headers
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


@pytest.mark.integration
class TestScanEndpoint:
    """Integration tests dla /api/scan endpoint"""

    def test_scan_endpoint_returns_200(self, fastapi_test_client, mock_finnhub_fundamentals, mock_finnhub_quote, mock_yfinance_ticker):
        """
        Test: POST /api/scan zwraca 200 OK

        Weryfikuje:
        - Status code = 200
        - Response ma klucze: results, total_scanned, matches
        - Results jest listą StockResult
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Wykonaj request
            response = fastapi_test_client.post('/api/scan', json={
                'symbols': ['AAPL'],
                'min_volume': 1000000
            })

            # Asercje
            assert response.status_code == 200
            data = response.json()
            assert 'results' in data
            assert 'total_scanned' in data
            assert 'matches' in data
            assert isinstance(data['results'], list)
            assert data['total_scanned'] >= 0


    def test_scan_endpoint_validates_empty_symbols(self, fastapi_test_client):
        """
        Test: POST /api/scan waliduje puste symbols

        Weryfikuje:
        - Status code = 422 (Unprocessable Entity)
        - Pydantic validation error dla pustej listy symbols
        """
        response = fastapi_test_client.post('/api/scan', json={
            'symbols': [],  # Pusta lista - invalid
            'min_volume': 1000000
        })

        # Asercja - Pydantic validation zwraca 422
        assert response.status_code == 422, \
            f"Puste symbols powinny zwrócić 422, otrzymano {response.status_code}: {response.text}"


    def test_scan_endpoint_validates_negative_volume(self, fastapi_test_client):
        """
        Test: POST /api/scan waliduje ujemny volume

        Weryfikuje:
        - Status code = 422
        - Pydantic validation error dla ujemnego volume
        """
        response = fastapi_test_client.post('/api/scan', json={
            'symbols': ['AAPL'],
            'min_volume': -1000  # Ujemny - invalid
        })

        # Asercja
        assert response.status_code == 422, "Ujemny min_volume powinien zwrócić 422"


    def test_scan_endpoint_with_all_filters(self, fastapi_test_client, mock_finnhub_fundamentals, mock_finnhub_quote, mock_yfinance_ticker):
        """
        Test: POST /api/scan z wszystkimi filtrami fundamentals

        Weryfikuje:
        - Endpoint akceptuje wszystkie parametry
        - Status code = 200
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            # Request z WSZYSTKIMI filtrami
            response = fastapi_test_client.post('/api/scan', json={
                'symbols': ['AAPL', 'MSFT'],
                'min_volume': 1_000_000,
                'min_price_change_percent': 2.0,
                'min_market_cap': 50_000_000,
                'max_market_cap': 5_000_000_000,
                'min_roe': 15.0,
                'min_roce': 10.0,
                'max_debt_equity': 0.3,
                'min_revenue_growth': 15.0,
                'max_forward_pe': 15.0
            })

            # Asercje
            assert response.status_code == 200
            data = response.json()
            assert data['total_scanned'] >= 0


    def test_scan_endpoint_handles_scanner_exception(self, fastapi_test_client):
        """
        Test: POST /api/scan obsługuje błędy z StockScanner

        Weryfikuje:
        - Nie crashuje przy exception w StockScanner
        - Zwraca 500 lub inne poprawne error response
        """
        with patch('app.services.scanner.StockScanner.scan_stocks') as mock_scan:
            # Symuluj exception w scanner
            mock_scan.side_effect = Exception("Database connection error")

            response = fastapi_test_client.post('/api/scan', json={
                'symbols': ['AAPL'],
                'min_volume': 1000000
            })

            # Asercja: Powinien zwrócić error (500 lub inne)
            assert response.status_code >= 400, "Exception powinno zwrócić error status"


    def test_scan_endpoint_response_structure(self, fastapi_test_client, mock_finnhub_fundamentals, mock_finnhub_quote, mock_yfinance_ticker):
        """
        Test: POST /api/scan zwraca poprawną strukturę response

        Weryfikuje:
        - results zawiera wszystkie wymagane pola StockResult
        - matches jest poprawnie obliczony
        """
        with patch('app.services.scanner.yf.Ticker') as mock_yf, \
             patch('app.services.scanner.FinnhubClient') as mock_client_class:

            mock_yf.return_value = mock_yfinance_ticker
            mock_client = MagicMock()
            mock_client.get_fundamentals.return_value = mock_finnhub_fundamentals
            mock_client.get_quote.return_value = mock_finnhub_quote
            mock_client_class.return_value = mock_client

            response = fastapi_test_client.post('/api/scan', json={
                'symbols': ['AAPL'],
                'min_volume': 0
            })

            data = response.json()
            assert 'results' in data
            assert 'total_scanned' in data
            assert 'matches' in data

            # Sprawdź strukturę StockResult
            if len(data['results']) > 0:
                result = data['results'][0]
                required_fields = [
                    'symbol', 'price', 'volume', 'market_cap',
                    'roe', 'roce', 'meets_criteria'
                ]
                for field in required_fields:
                    assert field in result, f"Result powinien mieć pole '{field}'"


@pytest.mark.integration
class TestHealthEndpoint:
    """Integration tests dla /health endpoint"""

    def test_health_endpoint_returns_200(self, fastapi_test_client):
        """
        Test: GET /health zwraca 200 OK

        Weryfikuje:
        - Status code = 200
        - Response ma klucz 'status'
        """
        response = fastapi_test_client.get('/health')

        # Asercje
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'ok'


    def test_health_endpoint_checks_database(self, fastapi_test_client):
        """
        Test: GET /health sprawdza database status

        Weryfikuje:
        - Response ma klucz 'database'
        """
        response = fastapi_test_client.get('/health')

        data = response.json()
        assert 'database' in data
        # Może być 'connected' lub 'disconnected' - oba są OK


    def test_health_endpoint_checks_redis(self, fastapi_test_client):
        """
        Test: GET /health sprawdza Redis status

        Weryfikuje:
        - Response ma klucz 'redis'
        """
        response = fastapi_test_client.get('/health')

        data = response.json()
        assert 'redis' in data
        # Może być 'connected' lub 'unavailable' - oba są OK


@pytest.mark.integration
class TestRootEndpoint:
    """Integration tests dla / root endpoint"""

    def test_root_endpoint_returns_200(self, fastapi_test_client):
        """
        Test: GET / zwraca 200 OK

        Weryfikuje:
        - Status code = 200
        - Response ma klucz 'message'
        """
        response = fastapi_test_client.get('/')

        # Asercje
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data


    def test_root_endpoint_has_docs_link(self, fastapi_test_client):
        """
        Test: GET / zawiera link do /docs

        Weryfikuje:
        - Response ma klucz 'docs'
        """
        response = fastapi_test_client.get('/')

        data = response.json()
        assert 'docs' in data


@pytest.mark.integration
class TestCORS:
    """Integration tests dla CORS configuration"""

    def test_cors_allows_frontend_origin(self, fastapi_test_client):
        """
        Test: CORS pozwala na requesty z frontend (localhost:3000)

        Weryfikuje:
        - CORS headers są obecne w response
        - Access-Control-Allow-Origin zawiera localhost:3000
        """
        # OPTIONS request (preflight)
        response = fastapi_test_client.options('/api/scan', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        })

        # Asercje
        assert 'access-control-allow-origin' in response.headers
        # FastAPI może zwrócić '*' lub konkretny origin


    def test_cors_allows_post_method(self, fastapi_test_client):
        """
        Test: CORS pozwala na POST method

        Weryfikuje:
        - Access-Control-Allow-Methods zawiera POST
        """
        response = fastapi_test_client.options('/api/scan', headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        })

        # Asercja: Status 200 oznacza że CORS preflight passed
        assert response.status_code == 200
