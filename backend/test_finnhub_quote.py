"""
Test: Co zwraca Finnhub quote (price/volume) dla AAPL
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.services.finnhub_client import FinnhubClient

client = FinnhubClient()

print("=" * 80)
print("FINNHUB QUOTE TEST")
print("=" * 80)

symbol = "AAPL"

# Quote (real-time price/volume)
print(f"\n📊 Quote dla {symbol}:\n")
quote = client.get_quote(symbol)

if quote:
    print(f"Raw response: {quote}\n")

    print("Parsed values:")
    print(f"  c (current price): {quote.get('c')}")
    print(f"  h (high): {quote.get('h')}")
    print(f"  l (low): {quote.get('l')}")
    print(f"  o (open): {quote.get('o')}")
    print(f"  pc (previous close): {quote.get('pc')}")
    print(f"  t (timestamp): {quote.get('t')}")
    print(f"  v (volume): {quote.get('v')}")

    # Sprawdź czy volume działa
    volume = quote.get('v', 0)
    print(f"\n✅ Volume: {volume:,}")

    if volume > 0:
        print("✅ SUCCESS - Volume ma wartość!")
    else:
        print("⚠️  WARNING - Volume = 0 (może być after hours)")

else:
    print("❌ Brak danych quote")

print("\n" + "=" * 80)

# Test na kilku symbolach
print("\nTEST - Volume dla różnych symboli:")
print("=" * 80)

for sym in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
    q = client.get_quote(sym)
    if q:
        vol = q.get('v', 0)
        price = q.get('c', 0)
        print(f"{sym:6s} - Price: ${price:8.2f}  Volume: {vol:>15,}")
    else:
        print(f"{sym:6s} - ❌ Brak danych")

print("=" * 80)
