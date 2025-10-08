# 🎯 FINNHUB FREE TIER - SZCZEGÓŁOWA ANALIZA I STATUS

**Data utworzenia raportu:** 2025-10-07
**Ostatni commit:** `161f45b` - Research: Finnhub FREE tier analysis
**Autor:** Lang Rabar

---

## 📋 PODSUMOWANIE OSTATNIEGO COMMITA

### Główne ustalenia z badań:

Commit `161f45b` zawiera kompleksowe testy wszystkich endpointów Finnhub API w celu określenia, co faktycznie działa na **FREE tier**.

**Kluczowe odkrycie:**
- ❌ **Volume NIE jest dostępny** w `/quote` endpoint (zwraca `None`)
- ✅ Wszystkie **fundamentals są dostępne** (131 metryk!)
- ✅ Hybrid approach: **yfinance (volume) + Finnhub (fundamentals)**

---

## ✅ CO DZIAŁA NA FREE TIER

### 1. **Quote Endpoint** (`/quote`)
**Status:** ✅ Działa (HTTP 200)

**Dostępne dane:**
- ✅ `c` - Current Price: $256.48 (AAPL)
- ✅ `h` - High price
- ✅ `l` - Low price
- ✅ `o` - Open price
- ✅ `pc` - Previous Close
- ✅ `t` - Timestamp
- ❌ **`v` - Volume: `None`** - **KRYTYCZNE: Volume NOT available!**

**Implementacja w scanner.py:**
```python
quote = finnhub.get_quote(symbol)
current_price = quote['c']  # ✅ Działa
```

---

### 2. **Company Profile** (`/company-profile2`)
**Status:** ✅ Działa (HTTP 200)

**Dostępne dane:**
- ✅ `marketCapitalization`: 3,809,379 (wartość w MILIONACH!)
- ✅ `shareOutstanding`: 14,840.39
- ✅ `name`: Company name
- ✅ `industry`: Industry sector

**UWAGA:** Market Cap zwracany jest w milionach, wymaga konwersji:

**Implementacja w scanner.py:**
```python
profile = finnhub.get_company_profile(symbol)
market_cap_millions = profile['marketCapitalization']
market_cap = int(market_cap_millions * 1_000_000)  # Konwersja z M na pełną wartość
```

---

### 3. **Basic Financials** (`/company_basic_financials?metric=all`)
**Status:** ✅ Działa (HTTP 200) - **131 metryk dostępnych!**

**Kluczowe metryki dla multibagger scanner:**

| Metryka | Klucz Finnhub | Przykład (AAPL) | Status |
|---------|---------------|-----------------|--------|
| **ROE** | `roeTTM` | 154.92% | ✅ |
| **ROCE** | `series.annual.roic[0].v` | 0.5699 (56.99%) | ✅ |
| **Debt/Equity** | `totalDebt/totalEquityAnnual` | 1.8881 | ✅ |
| **Revenue Growth** | `revenueGrowthTTMYoy` | 5.97% | ✅ |
| **P/E Ratio** | `peTTM` | 38.38 | ✅ |
| **Net Margin** | `netProfitMarginTTM` | 24.3% | ✅ |
| **Operating Margin** | `operatingMarginTTM` | 31.87% | ✅ |

**Implementacja w scanner.py (linie 106-137):**
```python
fundamentals = finnhub.get_fundamentals(symbol)
metrics = fundamentals['metric']

# ROE (Return on Equity) - już w %
roe = metrics.get('roeTTM', 0)

# ROCE (Return on Capital Employed)
# UWAGA: ROCE NIE jest w metrics! Jest w series.annual.roic
roce = 0
if 'series' in fundamentals and 'annual' in fundamentals['series']:
    roic_series = fundamentals['series']['annual'].get('roic', [])
    if roic_series and len(roic_series) > 0:
        # roic to lista dict: [{'period': '2023-09-30', 'v': 0.4532}]
        # wartość to decimal, konwertujemy na %
        roce = roic_series[0].get('v', 0) * 100 if roic_series[0].get('v') else 0

# Debt/Equity - UWAGA: Klucz zawiera "/" w nazwie!
debt_equity = metrics.get('totalDebt/totalEquityAnnual', 999)

# P/E Ratio TTM
forward_pe = metrics.get('peTTM', 999)

# Revenue Growth TTM YoY
revenue_growth = metrics.get('revenueGrowthTTMYoy', 0)
```

---

### 4. **Financials Reported** (`/financials-reported`)
**Status:** ✅ Działa (HTTP 200)

**Dostępne dane:**
- ✅ 15 data entries
- ⚠️ Nie testowane szczegółowo w tym commicie

---

## ❌ CO NIE DZIAŁA (403 Forbidden)

### 1. **Stock Candles** (`/stock/candles`)
**Status:** ❌ HTTP 403 Forbidden (Premium only)

**Powód:** OHLCV data (Open, High, Low, Close, Volume) jest dostępne tylko na płatnych planach.

---

### 2. **Financials** (`/financials`)
**Status:** ❌ HTTP 403 Forbidden (Premium only)

**Powód:** Pełne Income Statement i Balance Sheet wymagają premium.

---

## 🔧 ROZWIĄZANIE: HYBRID APPROACH

### Strategia:
Ponieważ **Finnhub FREE nie ma volume**, ale **yfinance ma volume za darmo**, implementujemy **podejście hybrydowe**:

1. **yfinance** → Volume + Price Changes (7d, 30d)
2. **Finnhub** → Wszystkie fundamentals (ROE, ROCE, Debt/Equity, etc.)

### Implementacja w scanner.py:

**yfinance (tylko dla volume + price changes):**
```python
import yfinance as yf

ticker = yf.Ticker(symbol)

# Volume z 1-dniowej historii
hist = ticker.history(period="1d")
current_volume = int(hist["Volume"].iloc[-1])  # ✅ Działa

# Price changes z 1-miesięcznej historii
hist_month = ticker.history(period="1mo")
price_change_7d = ((current_price - hist_month["Close"].iloc[-7]) / hist_month["Close"].iloc[-7]) * 100
price_change_30d = ((current_price - hist_month["Close"].iloc[0]) / hist_month["Close"].iloc[0]) * 100
```

**Finnhub (dla price + wszystkich fundamentals):**
```python
from app.services.finnhub_client import FinnhubClient

finnhub = FinnhubClient()

# Price z quote
quote = finnhub.get_quote(symbol)
current_price = quote['c']

# Market Cap z profile (konwersja z milionów!)
profile = finnhub.get_company_profile(symbol)
market_cap = int(profile['marketCapitalization'] * 1_000_000)

# Fundamentals z basic_financials
fundamentals = finnhub.get_fundamentals(symbol)
metrics = fundamentals['metric']

roe = metrics['roeTTM']  # ✅
debt_equity = metrics['totalDebt/totalEquityAnnual']  # ✅
revenue_growth = metrics['revenueGrowthTTMYoy']  # ✅
pe = metrics['peTTM']  # ✅

# ROIC (ROCE) z series (NIE metrics!)
roic_series = fundamentals['series']['annual']['roic']
roce = roic_series[0]['v'] * 100  # konwersja z decimal na %
```

---

## 📊 KOMPLETNOŚĆ DANYCH - TABELA

| Metryka | Źródło | Status | Przykład (AAPL) | Uwagi |
|---------|--------|--------|-----------------|-------|
| **Price** | Finnhub `/quote` | ✅ | $256.48 | Realtime |
| **Volume** | yfinance | ✅ | (z history) | Finnhub nie ma! |
| **Market Cap** | Finnhub `/company-profile2` | ✅ | $3.8T | Konwersja z M |
| **ROE** | Finnhub metrics | ✅ | 154.92% | `roeTTM` |
| **ROCE** | Finnhub series | ✅ | 56.99% | `series.annual.roic[0].v` |
| **Debt/Equity** | Finnhub metrics | ✅ | 1.8881 | `totalDebt/totalEquityAnnual` |
| **Revenue Growth** | Finnhub metrics | ✅ | 5.97% | `revenueGrowthTTMYoy` |
| **P/E** | Finnhub metrics | ✅ | 38.38 | `peTTM` |
| **Net Margin** | Finnhub metrics | ✅ | 24.3% | `netProfitMarginTTM` |
| **Operating Margin** | Finnhub metrics | ✅ | 31.87% | `operatingMarginTTM` |
| **Price Change 7d** | yfinance | ✅ | (calculated) | Z history 1mo |
| **Price Change 30d** | yfinance | ✅ | (calculated) | Z history 1mo |

---

## 🔑 PRAWIDŁOWE KLUCZE FINNHUB

### ❌ CZĘSTE BŁĘDY (co NIE działa):

```python
# BŁĄD 1: roicTTM nie istnieje!
roce = metrics.get('roicTTM', 0)  # ❌ NIE MA TAKIEGO KLUCZA

# BŁĄD 2: totalDebtToEquity nie istnieje!
debt_equity = metrics.get('totalDebtToEquity', 999)  # ❌ NIE MA TAKIEGO KLUCZA

# BŁĄD 3: Próba pobrania revenue growth z series (zbyt złożone)
revenue_growth = # obliczenia z series...  # ❌ Niepotrzebnie skomplikowane
```

### ✅ PRAWIDŁOWE KLUCZE:

```python
# ✅ ROCE z series (NIE metrics!)
roic_series = fundamentals['series']['annual'].get('roic', [])
roce = roic_series[0]['v'] * 100 if roic_series else 0  # Konwersja decimal → %

# ✅ Debt/Equity (z "/" w kluczu!)
debt_equity = metrics.get('totalDebt/totalEquityAnnual', 999)

# ✅ Revenue Growth (bezpośrednio z metrics)
revenue_growth = metrics.get('revenueGrowthTTMYoy', 0)

# ✅ ROE (bezpośrednio z metrics, już w %)
roe = metrics.get('roeTTM', 0)

# ✅ P/E Ratio
forward_pe = metrics.get('peTTM', 999)
```

---

## 📁 PLIKI UTWORZONE W COMMICIE

### 1. `backend/FINNHUB_STATUS.md`
**Przeznaczenie:** Kompletna analiza co działa na FREE tier (ten plik)

### 2. `backend/debug_finnhub_metrics.py`
**Przeznaczenie:** Wyświetla WSZYSTKIE 131 dostępnych metryk dla AAPL
**Użycie:**
```bash
cd backend
python debug_finnhub_metrics.py
```

### 3. `backend/test_finnhub_all_endpoints.py`
**Przeznaczenie:** Testuje wszystkie endpointy Finnhub (quote, candles, profile, financials)
**Użycie:**
```bash
cd backend
python test_finnhub_all_endpoints.py
```
**Wynik:** Pokazuje które endpointy zwracają 200 (OK), a które 403 (Forbidden)

### 4. `backend/test_finnhub_quote.py`
**Przeznaczenie:** Potwierdza że `/quote` endpoint **NIE ma volume** (v = None)
**Użycie:**
```bash
cd backend
python test_finnhub_quote.py
```

### 5. `backend/test_scanner_metrics.py`
**Przeznaczenie:** Test czy scanner.py poprawnie pobiera fundamentals z Finnhub
**Użycie:**
```bash
cd backend
python test_scanner_metrics.py
```

---

## 🚀 ZMIANY W SCANNER.PY

### Co zostało poprawione:

**Linie 111-114:** Market Cap konwersja z milionów
```python
# BYŁO:
market_cap = metrics.get('marketCapitalization', 0)

# JEST:
market_cap = metrics.get('marketCapitalization', 0)
market_cap = int(market_cap * 1_000_000) if market_cap else 0  # Konwersja z M
```

**Linie 119-127:** ROCE z series.annual (NIE metrics!)
```python
# BYŁO:
roce = metrics.get('roicTTM', 0)  # ❌ nie istnieje

# JEST:
roce = 0
if 'series' in fundamentals and 'annual' in fundamentals['series']:
    roic_series = fundamentals['series']['annual'].get('roic', [])
    if roic_series and len(roic_series) > 0:
        roce = roic_series[0].get('v', 0) * 100 if roic_series[0].get('v') else 0  # ✅
```

**Linia 131:** Debt/Equity prawidłowy klucz
```python
# BYŁO:
debt_equity = metrics.get('totalDebtToEquity', 999)  # ❌ nie istnieje

# JEST:
debt_equity = metrics.get('totalDebt/totalEquityAnnual', 999)  # ✅ z "/" w kluczu
```

**Linia 137:** Revenue Growth bezpośrednio z metrics
```python
# BYŁO:
# Skomplikowane obliczenia z series...

# JEST:
revenue_growth = metrics.get('revenueGrowthTTMYoy', 0)  # ✅ bezpośrednio z metrics
```

---

## 🔍 WNIOSKI I REKOMENDACJE

### ✅ Co zadziałało:
1. **Finnhub FREE tier ma 131 metryk fundamentalnych** - to więcej niż potrzebujemy!
2. **Hybrid approach działa:** yfinance (volume) + Finnhub (fundamentals)
3. **Wszystkie kluczowe metryki dla multibagger scanner są dostępne GRATIS**

### ⚠️ Ograniczenia FREE tier:
1. **Brak volume w `/quote`** - wymaga yfinance
2. **Brak OHLCV candles** (403) - wymaga yfinance dla price changes
3. **Brak pełnych financials** (403) - ale basic_financials wystarczają

### 📌 Dalsze kroki:

#### Zrobione (commit 161f45b):
- ✅ Testy wszystkich endpointów Finnhub
- ✅ Identyfikacja prawidłowych kluczy metryk
- ✅ Poprawki w scanner.py (linie 109-137)
- ✅ Pliki testowe (debug_finnhub_metrics.py, test_finnhub_all_endpoints.py, etc.)
- ✅ Dokumentacja FINNHUB_STATUS.md

#### TODO (następny commit):
- [ ] **Przetestować scanner.py end-to-end** na AAPL, MSFT, NVDA
- [ ] **Zweryfikować czy wszystkie metryki mają wartości** (nie są 0/None)
- [ ] **Dodać error handling** dla przypadków gdy series.annual.roic nie istnieje
- [ ] **Zoptymalizować liczbę requestów** (rate limit: 60 calls/min na FREE tier)
- [ ] **Dodać unit testy** dla scanner.py z mockami Finnhub responses

---

## 📚 REFERENCJE

### Dokumentacja Finnhub API:
- Quote: https://finnhub.io/docs/api/quote
- Company Profile: https://finnhub.io/docs/api/company-profile2
- Basic Financials: https://finnhub.io/docs/api/company-basic-financials

### Limity FREE tier:
- **60 API calls/minute**
- **30 API calls/second** (burst)
- **No credit card required**

### Konfiguracja (backend/app/config.py):
```python
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "default_key")
```

---

**Status implementacji:** ✅ **GOTOWE DO TESTÓW**
**Problem rozwiązany:** Volume z yfinance, fundamentals z Finnhub
**Następny krok:** End-to-end testy na wielu symbolach (AAPL, MSFT, NVDA, GOOGL, TSLA)

---

*Raport wygenerowany: 2025-10-07*
*Commit: 161f45b20cc9dffdabb4f60e6e93887f8eb98c7c*
*Autor analizy: Claude (PM Agent)*
