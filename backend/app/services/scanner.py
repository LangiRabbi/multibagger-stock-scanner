"""
Stock Scanner Service - HYBRID: yfinance (price changes) + Finnhub (fundamentals)
"""
import yfinance as yf
from typing import List, Optional
import logging
from app.schemas.scan import StockResult
from app.database import SessionLocal
from app.models.scan import ScanResult as ScanResultModel
from app.services.finnhub_client import FinnhubClient

# Logger dla error handling
logger = logging.getLogger(__name__)


class StockScanner:
    """
    Serwis do skanowania akcji wedlug kryteriow MULTIBAGGER.

    Hybrid approach:
    - yfinance: Price Changes 7d/30d (historical data)
    - Finnhub API: Fundamentals + Real-time Price/Volume (117 metrics w 1 calu!)
    """

    @staticmethod
    def scan_stocks(
        symbols: List[str],
        min_volume: int = 1_000_000,
        min_price_change_percent: Optional[float] = None,
        # === NOWE PARAMETRY FUNDAMENTALS ===
        min_market_cap: Optional[int] = 50_000_000,        # min 50M (small cap)
        max_market_cap: Optional[int] = 5_000_000_000,     # max 5B (mid cap)
        min_roe: Optional[float] = 15.0,                   # min 15% ROE
        min_roce: Optional[float] = 10.0,                  # min 10% ROCE
        max_debt_equity: Optional[float] = 0.3,            # max 30% zadluzenie
        min_revenue_growth: Optional[float] = 15.0,        # min 15% wzrost przychodow
        max_forward_pe: Optional[float] = 15.0             # max P/E = 15 (tanie)
    ) -> List[StockResult]:
        """
        Skanuje liste akcji i zwraca te ktore spelniaja kryteria MULTIBAGGER.

        Args:
            symbols: Lista symboli (np. ["AAPL", "MSFT"])
            min_volume: Minimalny wolumen (domyslnie 1M)
            min_price_change_percent: Minimalna zmiana ceny w % (7 dni)
            min_market_cap: Min kapitalizacja (50M = small cap)
            max_market_cap: Max kapitalizacja (5B = mid cap)
            min_roe: Minimalny ROE w % (15% = dobre)
            min_roce: Minimalny ROCE w % (10% = efektywne)
            max_debt_equity: Max zadluzenie (0.3 = 30% max)
            min_revenue_growth: Min wzrost przychodow YoY % (15% = growth)
            max_forward_pe: Max forward P/E (15 = nie przewartosciowane)

        Returns:
            Lista StockResult z akcjami + fundamentals
        """
        results = []

        # Inicjalizuj Finnhub client raz dla wszystkich symboli
        finnhub = FinnhubClient()

        for symbol in symbols:
            try:
                # === PRICE CHANGES Z YFINANCE (historical data) ===
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo")

                if hist.empty:
                    logger.warning(f"Brak danych historycznych dla {symbol}")
                    continue

                # Oblicz zmiane ceny 7 dni
                price_change_7d = None
                if len(hist) >= 7:
                    current_price_hist = float(hist["Close"].iloc[-1])
                    price_7d_ago = float(hist["Close"].iloc[-7])
                    price_change_7d = ((current_price_hist - price_7d_ago) / price_7d_ago) * 100

                # Oblicz zmiane ceny 30 dni
                price_change_30d = None
                if len(hist) >= 30:
                    current_price_hist = float(hist["Close"].iloc[-1])
                    price_30d_ago = float(hist["Close"].iloc[-30])
                    price_change_30d = ((current_price_hist - price_30d_ago) / price_30d_ago) * 100
                elif len(hist) > 1:
                    current_price_hist = float(hist["Close"].iloc[-1])
                    price_first = float(hist["Close"].iloc[0])
                    price_change_30d = ((current_price_hist - price_first) / price_first) * 100

                # === REAL-TIME PRICE/VOLUME Z FINNHUB ===
                quote = finnhub.get_quote(symbol)
                if not quote:
                    logger.warning(f"Brak danych quote Finnhub dla {symbol}")
                    continue

                current_price = quote.get('c', 0)  # current price
                current_volume = int(quote.get('v', 0))  # volume

                # === FUNDAMENTALS Z FINNHUB (1 API call!) ===
                fundamentals = finnhub.get_fundamentals(symbol)

                if not fundamentals or 'metric' not in fundamentals:
                    logger.warning(f"Brak danych fundamentals Finnhub dla {symbol} - pomijamy")
                    continue

                # Metrics dict - zawiera 117 metryk!
                metrics = fundamentals['metric']

                # === POBIERZ METRYKI BEZPOŚREDNIO ===

                # Market Cap
                market_cap = metrics.get('marketCapitalization', 0)

                # ROE (Return on Equity) - Finnhub zwraca już w % (nie decimal!)
                roe = metrics.get('roeTTM', 0)

                # ROIC (Return on Invested Capital) - podobne do ROCE
                roce = metrics.get('roicTTM', 0)

                # Debt/Equity
                debt_equity = metrics.get('totalDebtToEquity', 999)

                # P/E Ratio TTM
                forward_pe = metrics.get('peTTM', 999)

                # === REVENUE GROWTH z historical data ===
                # series zawiera historical annual/quarterly data
                revenue_growth = 0
                if 'series' in fundamentals and 'annual' in fundamentals['series']:
                    revenue_series = fundamentals['series']['annual'].get('revenue', [])

                    # Oblicz YoY growth z ostatnich 2 lat
                    if len(revenue_series) >= 2:
                        latest_revenue = revenue_series[0].get('v', 0)
                        prev_revenue = revenue_series[1].get('v', 1)

                        if prev_revenue > 0:
                            revenue_growth = ((latest_revenue - prev_revenue) / prev_revenue) * 100

                # === SPRAWDZ WSZYSTKIE KRYTERIA ===
                meets_criteria = True

                # Kryterium 1: Volume
                if current_volume < min_volume:
                    meets_criteria = False

                # Kryterium 2: Price change (jesli podane)
                if min_price_change_percent is not None and price_change_7d is not None:
                    if price_change_7d < min_price_change_percent:
                        meets_criteria = False

                # === NOWE KRYTERIA FUNDAMENTALS ===

                # Kryterium 3: Market Cap (musi byc w zakresie)
                if min_market_cap is not None and max_market_cap is not None:
                    if not (min_market_cap <= market_cap <= max_market_cap):
                        meets_criteria = False

                # Kryterium 4: ROE (min 15%)
                if min_roe is not None and roe < min_roe:
                    meets_criteria = False

                # Kryterium 5: ROCE (min 10%)
                if min_roce is not None and roce < min_roce:
                    meets_criteria = False

                # Kryterium 6: Debt/Equity (max 0.3 = 30%)
                if max_debt_equity is not None and debt_equity > max_debt_equity:
                    meets_criteria = False

                # Kryterium 7: Revenue Growth (min 15%)
                if min_revenue_growth is not None and revenue_growth < min_revenue_growth:
                    meets_criteria = False

                # Kryterium 8: Forward P/E (max 15)
                if max_forward_pe is not None and forward_pe > max_forward_pe:
                    meets_criteria = False

                # Dodaj wynik z WSZYSTKIMI danymi (cenowe + fundamentals)
                results.append(StockResult(
                    symbol=symbol,
                    price=round(current_price, 2),
                    volume=current_volume,
                    price_change_7d=round(price_change_7d, 2) if price_change_7d else None,
                    price_change_30d=round(price_change_30d, 2) if price_change_30d else None,
                    # === NOWE POLA ===
                    market_cap=market_cap,
                    roe=round(roe, 2),
                    roce=round(roce, 2),
                    debt_equity=round(debt_equity, 3) if debt_equity != 999 else None,
                    revenue_growth=round(revenue_growth, 2),
                    forward_pe=round(forward_pe, 2) if forward_pe != 999 else None,
                    meets_criteria=meets_criteria
                ))

            except Exception as e:
                # Jesli blad (np. symbol nie istnieje) - pomijamy
                logger.error(f"Error scanning {symbol}: {e}")
                continue

        # === ZAPISZ WYNIKI DO BAZY DANYCH ===
        db = SessionLocal()
        try:
            for result in results:
                # Stworz nowy rekord w tabeli scan_results
                scan_record = ScanResultModel(
                    symbol=result.symbol,
                    price=result.price,
                    volume=result.volume,
                    # criteria_met to JSON - zapisujemy wszystkie kryteria
                    criteria_met={
                        "volume": result.volume,
                        "price_change_7d": result.price_change_7d,
                        "market_cap": result.market_cap,
                        "roe": result.roe,
                        "roce": result.roce,
                        "debt_equity": result.debt_equity,
                        "revenue_growth": result.revenue_growth,
                        "forward_pe": result.forward_pe
                    },
                    # Fundamentals w osobnych kolumnach
                    market_cap=result.market_cap,
                    roe=result.roe,
                    roce=result.roce,
                    debt_equity=result.debt_equity,
                    revenue_growth=result.revenue_growth,
                    forward_pe=result.forward_pe,
                    price_change_7d=result.price_change_7d,
                    price_change_30d=result.price_change_30d,
                    meets_criteria=result.meets_criteria
                )
                db.add(scan_record)

            db.commit()
            logger.info(f"Zapisano {len(results)} wynikow skanowania do bazy danych")

        except Exception as e:
            logger.error(f"Blad zapisu do bazy danych: {e}")
            db.rollback()
        finally:
            db.close()

        return results
