"""
Unit tests dla Redis cache

Testujemy:
1. Cache decorator cache'uje wyniki
2. Cache TTL działa (wygasanie po X sekund)
3. clear_cache() usuwa klucze
4. Cache działa bez Redis (graceful degradation)
"""
import pytest
from unittest.mock import patch, MagicMock
from app.cache import RedisCache, cache, clear_finnhub_cache
import time


@pytest.mark.unit
class TestRedisCache:
    """Unit tests dla RedisCache class"""

    def test_redis_cache_initialization_success(self):
        """
        Test: RedisCache inicjalizuje się poprawnie gdy Redis działa

        Weryfikuje:
        - client nie jest None
        - is_available() zwraca True
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()

            # Asercje
            assert cache_instance.client is not None
            assert cache_instance.is_available() == True


    def test_redis_cache_initialization_failure(self):
        """
        Test: RedisCache gracefully handle Redis connection failure

        Weryfikuje:
        - Nie crashuje gdy Redis nie działa
        - client = None
        - is_available() zwraca False
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            # Symuluj ConnectionError
            mock_redis.side_effect = Exception("Connection refused")

            cache_instance = RedisCache()

            # Asercje
            assert cache_instance.client is None
            assert cache_instance.is_available() == False


    def test_cache_get_hit(self):
        """
        Test: cache.get() zwraca dane gdy klucz istnieje (CACHE HIT)

        Weryfikuje:
        - Zwraca dict z danymi
        - Deserializuje JSON
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            # Mock Redis GET - zwraca JSON string
            mock_client.get.return_value = '{"symbol": "AAPL", "price": 256.48}'
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()
            result = cache_instance.get("finnhub:get_quote:AAPL")

            # Asercje
            assert result is not None
            assert result['symbol'] == "AAPL"
            assert result['price'] == 256.48


    def test_cache_get_miss(self):
        """
        Test: cache.get() zwraca None gdy klucz nie istnieje (CACHE MISS)

        Weryfikuje:
        - Zwraca None
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_client.get.return_value = None  # Klucz nie istnieje
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()
            result = cache_instance.get("nonexistent_key")

            # Asercja
            assert result is None


    def test_cache_set(self):
        """
        Test: cache.set() zapisuje dane w Redis

        Weryfikuje:
        - Wywołuje Redis.setex() z TTL
        - Serializuje do JSON
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()
            data = {"symbol": "AAPL", "price": 256.48}
            result = cache_instance.set("finnhub:get_quote:AAPL", data, ttl=900)

            # Asercje
            assert result == True
            # Sprawdź że setex został wywołany z JSON
            mock_client.setex.assert_called_once()
            call_args = mock_client.setex.call_args
            assert call_args[0][0] == "finnhub:get_quote:AAPL"
            assert call_args[0][1] == 900  # TTL
            assert '"symbol": "AAPL"' in call_args[0][2]  # JSON string


    def test_cache_delete(self):
        """
        Test: cache.delete() usuwa klucz z Redis

        Weryfikuje:
        - Wywołuje Redis.delete()
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()
            result = cache_instance.delete("finnhub:get_quote:AAPL")

            # Asercje
            assert result == True
            mock_client.delete.assert_called_once_with("finnhub:get_quote:AAPL")


    def test_cache_clear_pattern(self):
        """
        Test: clear_pattern() usuwa wszystkie klucze pasujące do wzorca

        Weryfikuje:
        - Wywołuje Redis.keys(pattern)
        - Wywołuje Redis.delete(*keys)
        - Zwraca liczbę usuniętych kluczy
        """
        with patch('app.cache.redis.Redis.from_url') as mock_redis:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            # Mock Redis.keys() - zwraca 3 klucze
            mock_client.keys.return_value = [
                "finnhub:get_quote:AAPL",
                "finnhub:get_quote:MSFT",
                "finnhub:get_fundamentals:AAPL"
            ]
            # Mock Redis.delete() - zwraca liczbę usuniętych
            mock_client.delete.return_value = 3
            mock_redis.return_value = mock_client

            cache_instance = RedisCache()
            deleted_count = cache_instance.clear_pattern("finnhub:*")

            # Asercje
            assert deleted_count == 3
            mock_client.keys.assert_called_once_with("finnhub:*")
            mock_client.delete.assert_called_once()


@pytest.mark.unit
class TestCacheDecorator:
    """Unit tests dla @cache decorator"""

    def test_cache_decorator_caches_result(self):
        """
        Test: @cache decorator cache'uje wynik funkcji

        Weryfikuje:
        - Pierwsze wywołanie wykonuje funkcję
        - Drugie wywołanie zwraca z cache (funkcja nie jest wykonana)
        """
        call_count = 0

        with patch('app.cache.redis_cache') as mock_cache:
            # Setup mock cache
            mock_cache.is_available.return_value = True
            mock_cache.get.side_effect = [None, {"result": 20}]  # Pierwsza: MISS, druga: HIT
            mock_cache.set.return_value = True

            @cache(ttl=60, key_prefix="test")
            def expensive_function(x):
                nonlocal call_count
                call_count += 1
                return {"result": x * 2}

            # Pierwsze wywołanie - cache miss
            result1 = expensive_function(10)
            assert result1 == {"result": 20}
            assert call_count == 1

            # Drugie wywołanie - cache hit
            result2 = expensive_function(10)
            assert result2 == {"result": 20}
            assert call_count == 1  # Nie zwiększyło się! Funkcja nie była wykonana


    def test_cache_decorator_generates_correct_key(self):
        """
        Test: @cache decorator generuje poprawny cache key

        Weryfikuje:
        - Key format: "{prefix}:{function_name}:{args}"
        - Przykład: "finnhub:get_quote:AAPL"
        """
        with patch('app.cache.redis_cache') as mock_cache:
            mock_cache.is_available.return_value = True
            mock_cache.get.return_value = None
            mock_cache.set.return_value = True

            @cache(ttl=60, key_prefix="finnhub")
            def get_quote(self, symbol):
                return {"symbol": symbol, "price": 100.0}

            # Wywołaj funkcję
            dummy_self = object()
            get_quote(dummy_self, "AAPL")

            # Sprawdź że cache.get został wywołany z poprawnym kluczem
            mock_cache.get.assert_called()
            call_args = mock_cache.get.call_args[0][0]
            assert "finnhub:get_quote:AAPL" in call_args


    def test_cache_decorator_respects_ttl(self):
        """
        Test: @cache decorator używa podanego TTL

        Weryfikuje:
        - cache.set() jest wywołany z TTL parametrem
        """
        with patch('app.cache.redis_cache') as mock_cache:
            mock_cache.is_available.return_value = True
            mock_cache.get.return_value = None
            mock_cache.set.return_value = True

            @cache(ttl=1800, key_prefix="test")
            def test_function():
                return {"data": "test"}

            test_function()

            # Sprawdź że cache.set został wywołany z TTL=1800
            mock_cache.set.assert_called()
            call_args = mock_cache.set.call_args[0]
            ttl = call_args[2] if len(call_args) > 2 else mock_cache.set.call_args[1].get('ttl')
            assert ttl == 1800


    def test_cache_decorator_handles_redis_unavailable(self):
        """
        Test: @cache decorator działa gdy Redis nie jest dostępny

        Weryfikuje:
        - Nie crashuje
        - Funkcja jest wykonana normalnie
        - Wynik jest zwrócony (bez cache'owania)
        """
        with patch('app.cache.redis_cache') as mock_cache:
            mock_cache.is_available.return_value = False
            mock_cache.get.return_value = None

            @cache(ttl=60, key_prefix="test")
            def test_function(x):
                return x * 2

            # Wykonaj funkcję - powinna działać mimo braku Redis
            result = test_function(5)

            # Asercja
            assert result == 10


@pytest.mark.unit
class TestCacheUtilities:
    """Unit tests dla utility functions"""

    def test_clear_finnhub_cache(self):
        """
        Test: clear_finnhub_cache() usuwa wszystkie cache Finnhub

        Weryfikuje:
        - Wywołuje clear_pattern("finnhub:*")
        - Zwraca liczbę usuniętych kluczy
        """
        with patch('app.cache.redis_cache') as mock_cache:
            mock_cache.is_available.return_value = True
            mock_cache.clear_pattern.return_value = 10

            deleted_count = clear_finnhub_cache()

            # Asercje
            assert deleted_count == 10
            mock_cache.clear_pattern.assert_called_once_with("finnhub:*")
