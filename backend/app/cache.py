"""
Redis cache decorator dla Finnhub API calls

PROBLEM: Finnhub API ma limit 60 calls/minute (FREE tier)
ROZWIĄZANIE: Cache responses w Redis przez 15 minut (900s)

Każdy scan robi 2 API calls per symbol:
- get_quote(): Real-time price
- get_fundamentals(): 131 metryk fundamentalnych

Z cache: 5 symboli = 0 API calls (po pierwszym scan)
Bez cache: 5 symboli = 10 API calls
"""
import redis
import json
import functools
import logging
from typing import Callable, Any, Optional, Dict
from app.config import settings

# Logger dla cache operations
logger = logging.getLogger(__name__)


class RedisCache:
    """
    Wrapper dla Redis client z connection pooling.

    Connection pool optymalizuje wydajność - używa jednego połączenia Redis
    zamiast tworzyć nowe przy każdym request.
    """

    def __init__(self):
        """
        Inicjalizuje Redis client z connection pool.

        Parametry:
        - decode_responses=True: Automatycznie konwertuj bytes -> str
        - socket_connect_timeout=2: Max 2s na połączenie
        - socket_timeout=2: Max 2s na operacje read/write
        """
        try:
            self.client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Test połączenia
            self.client.ping()
            logger.info(f"✓ Redis połączony: {settings.REDIS_URL}")
        except redis.ConnectionError as e:
            logger.warning(f"⚠ Redis niedostępny: {e}. Cache wyłączony.")
            self.client = None
        except Exception as e:
            logger.error(f"❌ Redis error: {e}. Cache wyłączony.")
            self.client = None

    def is_available(self) -> bool:
        """
        Sprawdza czy Redis jest dostępny.

        Returns:
            True jeśli Redis działa, False w przeciwnym razie
        """
        if not self.client:
            return False

        try:
            self.client.ping()
            return True
        except Exception:
            return False

    def get(self, key: str) -> Optional[Dict]:
        """
        Pobiera wartość z cache.

        Args:
            key: Klucz cache (np. "finnhub:get_quote:AAPL")

        Returns:
            Dict z danymi jeśli znaleziono, None jeśli brak w cache lub błąd
        """
        if not self.is_available():
            return None

        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"[CACHE HIT] {key}")
                return json.loads(value)
            else:
                logger.debug(f"[CACHE MISS] {key}")
                return None
        except Exception as e:
            logger.error(f"Redis GET error dla {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 900) -> bool:
        """
        Zapisuje wartość w cache z TTL (Time To Live).

        Args:
            key: Klucz cache
            value: Wartość do zapisania (będzie zserializowana do JSON)
            ttl: Czas życia w sekundach (default 900s = 15 minut)

        Returns:
            True jeśli zapisano, False jeśli błąd
        """
        if not self.is_available():
            return False

        try:
            self.client.setex(key, ttl, json.dumps(value))
            logger.debug(f"[CACHE SET] {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Redis SET error dla {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Usuwa klucz z cache.

        Args:
            key: Klucz do usunięcia

        Returns:
            True jeśli usunięto, False jeśli błąd
        """
        if not self.is_available():
            return False

        try:
            self.client.delete(key)
            logger.debug(f"[CACHE DELETE] {key}")
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error dla {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """
        Usuwa wszystkie klucze pasujące do wzorca.

        Args:
            pattern: Wzorzec Redis (np. "finnhub:*" usuwa wszystkie cache Finnhub)

        Returns:
            Liczba usuniętych kluczy
        """
        if not self.is_available():
            return 0

        try:
            keys = self.client.keys(pattern)
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"[CACHE CLEAR] Usunięto {deleted} kluczy: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Redis CLEAR error dla {pattern}: {e}")
            return 0


# Singleton - jedna instancja RedisCache dla całej aplikacji
redis_cache = RedisCache()


def cache(ttl: int = 900, key_prefix: str = "finnhub"):
    """
    Decorator cache'ujący wynik funkcji w Redis.

    Automatycznie generuje cache key z:
    - key_prefix (np. "finnhub")
    - Nazwa funkcji (np. "get_quote")
    - Argumenty funkcji (np. symbol="AAPL")

    Cache key format: "{prefix}:{function_name}:{arg1}:{arg2}"
    Przykład: "finnhub:get_quote:AAPL"

    Args:
        ttl: Time To Live w sekundach (default 900s = 15 minut)
        key_prefix: Prefix dla cache key (default "finnhub")

    Usage:
        @cache(ttl=900)
        def get_quote(self, symbol: str):
            return self.client.quote(symbol)

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        """
        Wrapper decorator.

        Args:
            func: Funkcja do cache'owania

        Returns:
            Wrapped function z cache logic
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            Wrapper function z cache logic.

            1. Generuje cache key z argumentów funkcji
            2. Sprawdza czy wynik jest w cache (GET)
            3. Jeśli HIT: zwraca z cache
            4. Jeśli MISS: wywołuje funkcję, zapisuje w cache (SET), zwraca wynik

            Args:
                *args: Positional arguments funkcji
                **kwargs: Keyword arguments funkcji

            Returns:
                Wynik funkcji (z cache lub nowo obliczony)
            """
            # Generuj cache key z argumentów
            # args[0] to self (dla metod klasy), args[1:] to prawdziwe argumenty
            # Dla get_quote(self, symbol="AAPL"): key = "finnhub:get_quote:AAPL"
            cache_args = list(args[1:])  # Pomiń self
            cache_args.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])

            # Bezpieczne generowanie klucza (tylko string/int/float)
            safe_args = []
            for arg in cache_args:
                if isinstance(arg, (str, int, float)):
                    safe_args.append(str(arg))

            cache_key = f"{key_prefix}:{func.__name__}:{':'.join(safe_args)}"

            # Sprawdź cache
            cached_value = redis_cache.get(cache_key)
            if cached_value is not None:
                logger.info(f"✓ Cache HIT: {cache_key}")
                return cached_value

            # Cache MISS - wywołaj funkcję
            logger.info(f"⊗ Cache MISS: {cache_key} - wywołuję API...")
            result = func(*args, **kwargs)

            # Zapisz w cache (tylko jeśli wynik nie jest None/pusty)
            if result:
                redis_cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


# === UTILITY FUNCTIONS ===


def clear_finnhub_cache() -> int:
    """
    Usuwa WSZYSTKIE cache Finnhub.

    Użyteczne gdy:
    - Chcesz wymusić świeże dane z API
    - Po deploy nowej wersji z zmienioną logiką

    Returns:
        Liczba usuniętych kluczy
    """
    return redis_cache.clear_pattern("finnhub:*")


def get_cache_stats() -> Dict[str, Any]:
    """
    Zwraca statystyki Redis cache.

    Returns:
        Dict z info o cache (memory usage, keys count, etc.)
    """
    if not redis_cache.is_available():
        return {"status": "unavailable", "error": "Redis nie jest dostępny"}

    try:
        info = redis_cache.client.info("stats")
        keyspace = redis_cache.client.info("keyspace")

        return {
            "status": "available",
            "total_connections": info.get("total_connections_received", 0),
            "total_commands": info.get("total_commands_processed", 0),
            "keys_finnhub": len(redis_cache.client.keys("finnhub:*")),
            "keyspace": keyspace
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
