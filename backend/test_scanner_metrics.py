"""
Quick test: Czy scanner poprawnie pobiera fundamentals z Finnhub
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.services.scanner import StockScanner

print("=" * 80)
print("TEST SCANNER METRICS - FINNHUB")
print("=" * 80)

# Test na jednym symbolu
symbols = ["AAPL"]

print(f"\n📊 Skanowanie: {symbols}\n")

results = StockScanner.scan_stocks(
    symbols=symbols,
    min_volume=1_000_000,
    min_market_cap=100_000_000,
    max_market_cap=5_000_000_000_000,
    min_roe=10.0,
    min_roce=5.0,
    max_debt_equity=2.0,
    min_revenue_growth=0.0,
    max_forward_pe=100.0
)

if results:
    result = results[0]

    print("✅ WYNIKI:")
    print(f"   Symbol: {result.symbol}")
    print(f"   Price: ${result.price}")
    print(f"   Volume: {result.volume:,}")
    print(f"   Price Change 7d: {result.price_change_7d}%")
    print(f"   Price Change 30d: {result.price_change_30d}%")

    print("\n📊 FUNDAMENTALS:")
    print(f"   Market Cap: ${result.market_cap:,}")
    print(f"   ROE: {result.roe}%")
    print(f"   ROCE: {result.roce}%")
    print(f"   Debt/Equity: {result.debt_equity}")
    print(f"   Revenue Growth: {result.revenue_growth}%")
    print(f"   Forward P/E: {result.forward_pe}")

    print(f"\n🎯 Meets Criteria: {'✅ YES' if result.meets_criteria else '❌ NO'}")

    # Sprawdź czy ROCE != 0 (główny problem wcześniej)
    print("\n" + "=" * 80)
    if result.roce > 0:
        print("✅ SUCCESS! ROCE > 0 - Finnhub fundamentals działają!")
    else:
        print("❌ PROBLEM: ROCE = 0")

    if result.debt_equity > 0 and result.debt_equity < 999:
        print("✅ SUCCESS! Debt/Equity ma wartość!")
    else:
        print("❌ PROBLEM: Debt/Equity nie ma wartości")

    if result.revenue_growth != 0:
        print("✅ SUCCESS! Revenue Growth ma wartość!")
    else:
        print("⚠️  WARNING: Revenue Growth = 0 (może być OK jeśli faktycznie 0)")

    print("=" * 80)

else:
    print("❌ Brak wyników!")

print("\n✅ Test zakończony")
