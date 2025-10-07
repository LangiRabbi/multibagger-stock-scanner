"""
Test: Sprawdź WSZYSTKIE endpointy Finnhub na FREE tier
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.config import settings
import finnhub

client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)
symbol = "AAPL"

print("=" * 80)
print("FINNHUB - ALL ENDPOINTS TEST (FREE TIER)")
print("=" * 80)

# 1. Quote
print("\n1️⃣ QUOTE (Real-time)")
try:
    quote = client.quote(symbol)
    print(f"   ✅ Response: {quote}")
    print(f"   Volume (v): {quote.get('v', 'NOT FOUND')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Candles (OHLCV data - może mieć volume?)
print("\n2️⃣ CANDLES (OHLCV)")
try:
    import time
    end = int(time.time())
    start = end - 86400  # 1 dzień temu
    candles = client.stock_candles(symbol, 'D', start, end)
    print(f"   ✅ Response keys: {candles.keys() if candles else 'None'}")
    if candles and 'v' in candles:
        print(f"   Volume data: {candles['v']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Company Profile (market cap?)
print("\n3️⃣ COMPANY PROFILE")
try:
    profile = client.company_profile2(symbol=symbol)
    print(f"   ✅ Market Cap: {profile.get('marketCapitalization', 'NOT FOUND')}")
    print(f"   Share Outstanding: {profile.get('shareOutstanding', 'NOT FOUND')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Basic Financials (już testowane, ale dla pewności)
print("\n4️⃣ BASIC FINANCIALS (metric=all)")
try:
    fundamentals = client.company_basic_financials(symbol, 'all')
    metrics = fundamentals.get('metric', {})
    print(f"   ✅ Total metrics: {len(metrics)}")
    print(f"   ROE: {metrics.get('roeTTM', 'NOT FOUND')}")
    print(f"   Debt/Equity: {metrics.get('totalDebt/totalEquityAnnual', 'NOT FOUND')}")
    print(f"   Revenue Growth: {metrics.get('revenueGrowthTTMYoy', 'NOT FOUND')}")

    # ROIC z series
    series = fundamentals.get('series', {}).get('annual', {})
    roic = series.get('roic', [])
    if roic:
        print(f"   ROIC (from series): {roic[0].get('v', 0) * 100:.2f}%")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Financials (income statement, balance sheet)
print("\n5️⃣ FINANCIALS (Income Statement)")
try:
    financials = client.financials(symbol, 'ic', 'annual')  # ic = income statement
    print(f"   ✅ Response: {financials}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 6. Financials Reported (może mieć więcej danych?)
print("\n6️⃣ FINANCIALS REPORTED")
try:
    reported = client.financials_reported(symbol=symbol, freq='annual')
    print(f"   ✅ Response keys: {reported.keys() if reported else 'None'}")
    if reported and 'data' in reported:
        print(f"   Data entries: {len(reported['data'])}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("PODSUMOWANIE:")
print("=" * 80)
print("\n❓ Pytania:")
print("   1. Czy candles ma volume (v)?")
print("   2. Czy market cap z profile działa?")
print("   3. Które endpointy działają na FREE tier?")
print("\n" + "=" * 80)
