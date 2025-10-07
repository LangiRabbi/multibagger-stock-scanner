# 🎯 FINNHUB FREE TIER - STATUS

Data: 2025-10-07

## ✅ CO DZIAŁA NA FREE TIER:

### 1. **Quote** (`/quote`)
- ✅ Current Price (`c`): $256.48
- ✅ High/Low (`h`, `l`)
- ✅ Open (`o`)
- ✅ Previous Close (`pc`)
- ❌ **Volume (`v`)**: `None` - NIE DZIAŁA!

### 2. **Company Profile** (`/company-profile2`)
- ✅ Market Cap: 3,809,379M (miliony!)
- ✅ Share Outstanding: 14,840.39
- ✅ Name, Industry

### 3. **Basic Financials** (`/company_basic_financials?metric=all`)
- ✅ **131 metryk** w response
- ✅ ROE (roeTTM): 154.92%
- ✅ ROIC z series.annual: 56.99%
- ✅ Debt/Equity (totalDebt/totalEquityAnnual): 1.8881
- ✅ Revenue Growth (revenueGrowthTTMYoy): 5.97%
- ✅ P/E (peTTM): 38.38
- ✅ Net Margin (netProfitMarginTTM): 24.3%
- ✅ Operating Margin (operatingMarginTTM): 31.87%

### 4. **Financials Reported** (`/financials-reported`)
- ✅ Działa (15 entries)
- ⚠️ Nie testowane dokładnie

---

## ❌ CO NIE DZIAŁA (403 Forbidden):

1. **Candles** (`/stock/candles`) - OHLCV data
2. **Financials** (`/financials`) - Income Statement/Balance Sheet

---

## 🔧 ROZWIĄZANIE: HYBRID APPROACH

### **yfinance** (tylko dla volume + price changes):
```python
hist = ticker.history(period="1d")
current_volume = int(hist["Volume"].iloc[-1])  # ✅ działa

hist_month = ticker.history(period="1mo")
# price_change_7d, price_change_30d  # ✅ działa
```

### **Finnhub** (dla wszystkich fundamentals):
```python
# Price
quote = finnhub.get_quote(symbol)
current_price = quote['c']  # ✅

# Market Cap
profile = finnhub.get_company_profile(symbol)
market_cap = profile['marketCapitalization'] * 1_000_000  # konwersja z M

# Fundamentals
fundamentals = finnhub.get_fundamentals(symbol)
metrics = fundamentals['metric']

roe = metrics['roeTTM']  # ✅
debt_equity = metrics['totalDebt/totalEquityAnnual']  # ✅
revenue_growth = metrics['revenueGrowthTTMYoy']  # ✅
pe = metrics['peTTM']  # ✅

# ROIC (ROCE) z series
roic_series = fundamentals['series']['annual']['roic']
roce = roic_series[0]['v'] * 100  # konwersja z decimal na %
```

---

## 📊 KOMPLETNOŚĆ DANYCH:

| Metryka | Źródło | Status | Wartość (AAPL) |
|---------|--------|--------|----------------|
| **Price** | Finnhub quote | ✅ | $256.48 |
| **Volume** | yfinance | ✅ | (z hist) |
| **Market Cap** | Finnhub profile | ✅ | $3.8T |
| **ROE** | Finnhub metrics | ✅ | 154.92% |
| **ROCE** | Finnhub series | ✅ | 56.99% |
| **Debt/Equity** | Finnhub metrics | ✅ | 1.8881 |
| **Revenue Growth** | Finnhub metrics | ✅ | 5.97% |
| **P/E** | Finnhub metrics | ✅ | 38.38 |
| **Price Change 7d** | yfinance | ✅ | (hist calc) |
| **Price Change 30d** | yfinance | ✅ | (hist calc) |

---

## 🚀 NASTĘPNE KROKI:

1. ✅ Poprawić `scanner.py`:
   - Volume z yfinance (`period="1d"`)
   - Price z Finnhub quote
   - Market Cap z Finnhub profile (konwersja * 1M)
   - Fundamentals z Finnhub metrics (prawidłowe klucze)
   - ROCE z Finnhub series.annual.roic

2. ✅ Przetestować na AAPL, MSFT, NVDA

3. ✅ Commit zmian

---

## 🔑 PRAWIDŁOWE KLUCZE FINNHUB:

```python
# BYŁO (źle):
roce = metrics.get('roicTTM', 0)  # ❌ nie istnieje
debt_equity = metrics.get('totalDebtToEquity', 999)  # ❌ nie istnieje

# JEST (dobrze):
# ROCE z series
roic_series = fundamentals['series']['annual'].get('roic', [])
roce = roic_series[0]['v'] * 100 if roic_series else 0  # ✅

# Debt/Equity (z "/" w kluczu!)
debt_equity = metrics.get('totalDebt/totalEquityAnnual', 999)  # ✅

# Revenue Growth
revenue_growth = metrics.get('revenueGrowthTTMYoy', 0)  # ✅
```

---

**Status:** GOTOWE DO IMPLEMENTACJI
**Problem:** Finnhub FREE nie ma volume → używamy yfinance tylko dla volume
**Rozwiązanie:** Hybrid: yfinance (volume) + Finnhub (fundamentals)
