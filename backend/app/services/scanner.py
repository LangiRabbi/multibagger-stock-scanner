"""
Stock Scanner Service - skanowanie akcji z yfinance
"""
import yfinance as yf
from typing import List, Optional
from app.schemas.scan import StockResult


class StockScanner:
    """
    Serwis do skanowania akcji wedlug kryteriow.
    Uzywamy yfinance (FREE API) do pobierania danych.
    """

    @staticmethod
    def scan_stocks(
        symbols: List[str],
        min_volume: int = 1000000,
        min_price_change_percent: Optional[float] = None
    ) -> List[StockResult]:
        """
        Skanuje liste akcji i zwraca te ktore spelniaja kryteria.

        Args:
            symbols: Lista symboli (np. ["AAPL", "MSFT"])
            min_volume: Minimalny wolumen
            min_price_change_percent: Minimalna zmiana ceny w % (7 dni)

        Returns:
            Lista StockResult z akcjami
        """
        results = []

        for symbol in symbols:
            try:
                # Pobierz dane z yfinance
                ticker = yf.Ticker(symbol)

                # Historia ostatnich 30 dni (aby obliczyc price_change)
                hist = ticker.history(period="1mo")

                if hist.empty:
                    # Brak danych dla tego symbolu - pomijamy
                    continue

                # Aktualna cena (ostatni Close)
                current_price = float(hist["Close"].iloc[-1])

                # Wolumen z ostatniego dnia
                current_volume = int(hist["Volume"].iloc[-1])

                # Oblicz zmiane ceny 7 dni
                price_change_7d = None
                if len(hist) >= 7:
                    price_7d_ago = float(hist["Close"].iloc[-7])
                    price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100

                # Oblicz zmiane ceny 30 dni
                price_change_30d = None
                if len(hist) >= 30:
                    price_30d_ago = float(hist["Close"].iloc[-30])
                    price_change_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100
                elif len(hist) > 1:
                    # Jesli mniej niz 30 dni, uzyj pierwszego dostepnego
                    price_first = float(hist["Close"].iloc[0])
                    price_change_30d = ((current_price - price_first) / price_first) * 100

                # Sprawdz kryteria
                meets_criteria = True

                # Kryterium 1: Volume
                if current_volume < min_volume:
                    meets_criteria = False

                # Kryterium 2: Price change (jesli podane)
                if min_price_change_percent is not None and price_change_7d is not None:
                    if price_change_7d < min_price_change_percent:
                        meets_criteria = False

                # Dodaj wynik
                results.append(StockResult(
                    symbol=symbol,
                    price=round(current_price, 2),
                    volume=current_volume,
                    price_change_7d=round(price_change_7d, 2) if price_change_7d else None,
                    price_change_30d=round(price_change_30d, 2) if price_change_30d else None,
                    meets_criteria=meets_criteria
                ))

            except Exception as e:
                # Jesli blad (np. symbol nie istnieje) - pomijamy
                print(f"Error scanning {symbol}: {e}")
                continue

        return results
