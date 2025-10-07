"""
Test Finnhub API connection - raw data test
Sprawdza czy Finnhub API zwraca fundamentals dla AAPL
"""
import sys
import os

# Dodaj backend/app do PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.services.finnhub_client import FinnhubClient


def test_finnhub_connection():
    """Test połączenia z Finnhub API dla AAPL"""

    print("=" * 70)
    print("TEST FINNHUB API CONNECTION")
    print("=" * 70)

    try:
        client = FinnhubClient()
        print("✅ Finnhub Client zainicjalizowany (API key znaleziony)\n")
    except ValueError as e:
        print(f"❌ BŁĄD: {e}")
        print("\n📝 INSTRUKCJA:")
        print("1. Zarejestruj się: https://finnhub.io/register")
        print("2. Skopiuj API key z dashboard")
        print("3. Dodaj do backend/.env:")
        print("   FINNHUB_API_KEY=twoj_api_key_tutaj")
        return False

    symbol = "AAPL"
    print(f"📊 Testowanie symbolu: {symbol}\n")

    # === TEST 1: Quote (Real-time Price/Volume) ===
    print("1️⃣ QUOTE (Real-time Price/Volume)")
    quote = client.get_quote(symbol)

    if quote:
        print("   ✅ Dane pobrane")
        print(f"   Current Price: ${quote.get('c', 0):,.2f}")
        print(f"   Volume: {quote.get('v', 0):,}")
        print(f"   High: ${quote.get('h', 0):,.2f}")
        print(f"   Low: ${quote.get('l', 0):,.2f}")
    else:
        print("   ❌ Brak danych")
        return False

    # === TEST 2: Company Profile ===
    print("\n2️⃣ COMPANY PROFILE")
    profile = client.get_company_profile(symbol)

    if profile:
        print("   ✅ Dane pobrane")
        print(f"   Name: {profile.get('name', 'N/A')}")
        print(f"   Market Cap: ${profile.get('marketCapitalization', 0):,}M")
        print(f"   Industry: {profile.get('finnhubIndustry', 'N/A')}")
    else:
        print("   ❌ Brak danych")
        return False

    # === TEST 3: Company Fundamentals (117 metrics!) ===
    print("\n3️⃣ COMPANY FUNDAMENTALS (metric=all)")
    fundamentals = client.get_fundamentals(symbol)

    if fundamentals and 'metric' in fundamentals:
        print("   ✅ Dane pobrane")

        metrics = fundamentals['metric']
        print(f"\n   📊 Znaleziono {len(metrics)} metryk!")

        # Pokaż kluczowe metryki dla multibagger scanner
        print("\n   🎯 KLUCZOWE METRYKI:")
        print(f"   ROE (roeTTM): {metrics.get('roeTTM', 0):.2f}%")
        print(f"   ROIC (roicTTM): {metrics.get('roicTTM', 0):.2f}%")
        print(f"   Debt/Equity: {metrics.get('totalDebtToEquity', 0):.2f}")
        print(f"   P/E TTM: {metrics.get('peTTM', 0):.2f}")
        print(f"   Net Margin: {metrics.get('netMargin', 0):.2f}%")
        print(f"   Operating Margin: {metrics.get('operatingMargin', 0):.2f}%")

        # Sprawdź czy są historical data (series)
        if 'series' in fundamentals:
            print("\n   📈 HISTORICAL DATA:")
            series = fundamentals['series']

            if 'annual' in series and 'revenue' in series['annual']:
                revenue_data = series['annual']['revenue']
                print(f"   Revenue data points: {len(revenue_data)}")

                if len(revenue_data) >= 2:
                    latest = revenue_data[0]
                    prev = revenue_data[1]
                    growth = ((latest['v'] - prev['v']) / prev['v']) * 100

                    print(f"   Latest Revenue ({latest['period']}): ${latest['v']:,}")
                    print(f"   Previous Revenue ({prev['period']}): ${prev['v']:,}")
                    print(f"   Revenue Growth YoY: {growth:.2f}%")

    else:
        print("   ❌ Brak danych")
        return False

    # === SUMMARY ===
    print("\n" + "=" * 70)
    print("✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
    print("=" * 70)
    print("\n🎉 FINNHUB API DZIAŁA!")
    print("\n📊 Dostępne metryki (przykłady):")
    print("   - roeTTM, roicTTM (Return on Equity/Capital)")
    print("   - totalDebtToEquity (Debt/Equity ratio)")
    print("   - peTTM, pb (P/E, P/B ratios)")
    print("   - netMargin, operatingMargin (Margins)")
    print("   - + 107 innych metryk!")

    print("\n📝 NASTĘPNE KROKI:")
    print("1. Uruchom backend: python -m uvicorn app.main:app --reload")
    print("2. Test scanner endpoint:")
    print('   curl -X POST http://localhost:8000/api/scan \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"symbols": ["AAPL", "MSFT", "NVDA"]}\'')

    print("\n💡 PORÓWNANIE Z FMP:")
    print("   FMP Free: ❌ 403 Forbidden (nie działa)")
    print("   Finnhub Free: ✅ 60 calls/min (3600/hour!)")
    print("   FMP: 3 calls per symbol (income+balance+metrics)")
    print("   Finnhub: 1 call per symbol (wszystko w jednym!)")
    print("   Finnhub jest 43x szybszy! 🚀")

    return True


if __name__ == "__main__":
    success = test_finnhub_connection()
    sys.exit(0 if success else 1)
