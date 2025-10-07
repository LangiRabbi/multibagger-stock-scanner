"""
Test FMP API connection - raw data test
Sprawdza czy FMP API zwraca dane dla AAPL
"""
import sys
import os

# Dodaj backend/app do PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.services.fmp_client import FMPClient


def test_fmp_connection():
    """Test połączenia z FMP API dla AAPL"""

    print("=" * 60)
    print("TEST FMP API CONNECTION")
    print("=" * 60)

    try:
        fmp = FMPClient()
        print("✅ FMP Client zainicjalizowany (API key znaleziony)\n")
    except ValueError as e:
        print(f"❌ BŁĄD: {e}")
        print("\n📝 INSTRUKCJA:")
        print("1. Zarejestruj się: https://site.financialmodelingprep.com/developer/docs/pricing")
        print("2. Skopiuj API key")
        print("3. Dodaj do backend/.env:")
        print("   FMP_API_KEY=twoj_api_key_tutaj")
        return False

    symbol = "AAPL"
    print(f"📊 Testowanie symbolu: {symbol}\n")

    # === TEST 1: Income Statement ===
    print("1️⃣ INCOME STATEMENT")
    income = fmp.get_income_statement(symbol)

    if income:
        print("   ✅ Dane pobrane")
        operating_income = income.get('operatingIncome', 0)
        revenue = income.get('revenue', 0)
        print(f"   Operating Income: ${operating_income:,}")
        print(f"   Revenue: ${revenue:,}")
    else:
        print("   ❌ Brak danych")
        return False

    # === TEST 2: Balance Sheet ===
    print("\n2️⃣ BALANCE SHEET")
    balance = fmp.get_balance_sheet(symbol)

    if balance:
        print("   ✅ Dane pobrane")
        total_assets = balance.get('totalAssets', 0)
        current_liabilities = balance.get('totalCurrentLiabilities', 0)
        total_debt = balance.get('totalDebt', 0)
        equity = balance.get('totalStockholdersEquity', 0)

        print(f"   Total Assets: ${total_assets:,}")
        print(f"   Current Liabilities: ${current_liabilities:,}")
        print(f"   Total Debt: ${total_debt:,}")
        print(f"   Stockholders Equity: ${equity:,}")
    else:
        print("   ❌ Brak danych")
        return False

    # === TEST 3: Key Metrics ===
    print("\n3️⃣ KEY METRICS TTM")
    metrics = fmp.get_key_metrics(symbol)

    if metrics:
        print("   ✅ Dane pobrane")
        market_cap = metrics.get('marketCapTTM', 0)
        roe = metrics.get('roeTTM', 0) * 100
        pe_ratio = metrics.get('peRatioTTM', 0)
        revenue_growth = metrics.get('revenueGrowthTTM', 0) * 100

        print(f"   Market Cap: ${market_cap:,}")
        print(f"   ROE: {roe:.2f}%")
        print(f"   P/E Ratio: {pe_ratio:.2f}")
        print(f"   Revenue Growth: {revenue_growth:.2f}%")
    else:
        print("   ❌ Brak danych")
        return False

    # === TEST 4: ROCE Calculation ===
    print("\n4️⃣ ROCE CALCULATION (Return on Capital Employed)")

    if income and balance:
        operating_income = income.get('operatingIncome', 0)
        total_assets = balance.get('totalAssets', 0)
        current_liabilities = balance.get('totalCurrentLiabilities', 0)

        capital_employed = total_assets - current_liabilities
        roce = (operating_income / capital_employed * 100) if capital_employed > 0 else 0

        print(f"   Operating Income: ${operating_income:,}")
        print(f"   Capital Employed: ${capital_employed:,}")
        print(f"   ROCE: {roce:.2f}%")

        if roce > 0:
            print("   ✅ ROCE obliczony poprawnie")
        else:
            print("   ❌ ROCE = 0 (prawdopodobnie błędne dane)")
            return False
    else:
        print("   ❌ Brak danych do obliczenia ROCE")
        return False

    # === SUMMARY ===
    print("\n" + "=" * 60)
    print("✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
    print("=" * 60)
    print("\n📝 NASTĘPNE KROKI:")
    print("1. Uruchom backend: python -m uvicorn app.main:app --reload")
    print("2. Test scanner endpoint:")
    print('   curl -X POST http://localhost:8000/api/scan \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"symbols": ["AAPL", "MSFT", "NVDA"]}\'')

    return True


if __name__ == "__main__":
    success = test_fmp_connection()
    sys.exit(0 if success else 1)
