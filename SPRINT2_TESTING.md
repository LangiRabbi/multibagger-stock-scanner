# 🧪 Sprint 2 Testing Guide - Stock Scanner + Portfolio

Przewodnik testowania nowych features z Sprint 2.

---

## ✅ PRE-REQUISITES

Zanim zaczniesz, upewnij się że:
- [ ] Sprint 1 działa (Docker, backend, frontend)
- [ ] Backend jest uruchomiony na http://localhost:8000
- [ ] Frontend jest uruchomiony na http://localhost:3000
- [ ] Tabele w bazie danych istnieją

---

## 🔍 TEST #1: Stock Scanner API (Backend)

**Cel:** Sprawdzić czy endpoint `/api/scan` działa i zwraca dane z yfinance

### Kroki:

1. Backend powinien działać: `http://localhost:8000`

2. Otwórz Swagger UI: http://localhost:8000/docs

3. Znajdź endpoint `POST /api/scan`

4. Kliknij "Try it out"

5. Wklej przykładowy request:
   ```json
   {
     "symbols": ["AAPL", "MSFT", "TSLA"],
     "min_volume": 1000000,
     "min_price_change_percent": 2.0
   }
   ```

6. Kliknij "Execute"

### ✅ Expected Result:

Response powinien zawierać:
```json
{
  "total_scanned": 3,
  "matches": X,  // zależy od danych rynkowych
  "results": [
    {
      "symbol": "AAPL",
      "price": 175.50,
      "volume": 50000000,
      "price_change_7d": 3.5,
      "price_change_30d": 8.2,
      "meets_criteria": true
    },
    ...
  ]
}
```

**Status code:** 200 OK

### ❌ Co robić jeśli nie działa:

- **Error: ModuleNotFoundError yfinance** → Zainstaluj: `pip install yfinance`
- **Timeout** → yfinance może być wolny (normalne dla pierwszego wywołania)
- **Symbol not found** → Sprawdź czy symbol istnieje (np. użyj AAPL, MSFT)

---

## 📊 TEST #2: Stock Scanner UI (Frontend)

**Cel:** Sprawdzić czy formularz skanowania działa

### Kroki:

1. Otwórz frontend: http://localhost:3000

2. Kliknij "Scan" w navbarze

3. Powinieneś zobaczyć formularz z polami:
   - Stock Symbols
   - Min Volume
   - Min Price Change %

4. Wpisz:
   - Symbols: `AAPL, MSFT, TSLA, GOOGL`
   - Min Volume: `1000000`
   - Min Price Change: `1.0`

5. Kliknij "Scan Stocks"

6. Poczekaj 5-10 sekund (yfinance pobiera dane)

### ✅ Expected Result:

Powinieneś zobaczyć:
- Tabela z wynikami
- Każda akcja ma: Symbol, Price, Volume, Change 7d, Change 30d, Status
- Akcje spełniające kryteria mają zielone tło i "✓ Match"
- Nagłówek: "Scan Results: X / 4 akcji spełnia kryteria"

### ❌ Co robić jeśli nie działa:

- **Error: Failed to fetch** → Sprawdź czy backend działa (http://localhost:8000/health)
- **Error: CORS** → Sprawdź backend/app/main.py (allow_origins powinno zawierać http://localhost:3000)
- **Tabela pusta** → Sprawdź konsolę przeglądarki (F12 → Console)

---

## 💼 TEST #3: Portfolio API (Backend)

**Cel:** Sprawdzić wszystkie CRUD operacje

### A. GET /api/portfolio (lista)

1. Swagger UI: http://localhost:8000/docs
2. Endpoint: `GET /api/portfolio`
3. Execute

**Expected:** Lista pozycji (może być pusta `[]`)

### B. POST /api/portfolio (dodaj)

1. Endpoint: `POST /api/portfolio`
2. Request:
   ```json
   {
     "symbol": "AAPL",
     "entry_price": 150.00,
     "quantity": 10,
     "notes": "Long term hold"
   }
   ```
3. Execute

**Expected:**
- Status: 201 Created
- Response zawiera ID, user_id, symbol, entry_price, quantity, notes, added_at

### C. GET /api/portfolio (sprawdź czy dodane)

1. Endpoint: `GET /api/portfolio`
2. Execute

**Expected:** Lista zawiera AAPL

### D. PUT /api/portfolio/{id} (edytuj)

1. Skopiuj ID z poprzedniego response
2. Endpoint: `PUT /api/portfolio/{id}`
3. Path parameter: `id` = [twoje ID]
4. Request:
   ```json
   {
     "notes": "Updated notes!"
   }
   ```
5. Execute

**Expected:** Notatka zmieniona

### E. DELETE /api/portfolio/{id} (usuń)

1. Endpoint: `DELETE /api/portfolio/{id}`
2. Path parameter: `id` = [twoje ID]
3. Execute

**Expected:** Status 204 No Content

### F. GET /api/portfolio (sprawdź czy usunięte)

**Expected:** Lista nie zawiera AAPL

---

## 📁 TEST #4: Portfolio UI (Frontend)

**Cel:** Sprawdzić interfejs zarządzania portfolio

### A. Wyświetlanie listy

1. Otwórz: http://localhost:3000/portfolio
2. Powinieneś zobaczyć:
   - Tytuł "My Portfolio"
   - Button "+ Add Stock"
   - Tabela (może być pusta)

### B. Dodawanie pozycji

1. Kliknij "+ Add Stock"
2. Formularz się rozwinie
3. Wpisz:
   - Symbol: `MSFT`
   - Entry Price: `350.00`
   - Quantity: `5`
   - Notes: `Tech stock`
4. Kliknij "Add to Portfolio"

**Expected:**
- Formularz się zamyka
- Tabela odświeża się
- MSFT pojawia się w tabeli

### C. Usuwanie pozycji

1. Znajdź MSFT w tabeli
2. Kliknij "Delete"
3. Potwierdź w dialogu

**Expected:**
- MSFT znika z tabeli
- Licznik "Your Stocks (X)" się zmniejsza

### D. Pusta lista

1. Usuń wszystkie pozycje
2. Powinieneś zobaczyć:
   - "Brak akcji w portfolio. Dodaj pierwsza!"

---

## 🔗 TEST #5: Full Integration Flow

**Cel:** Test pełnego przepływu: Scan → Add to Portfolio

### Scenariusz:

1. **Scan:**
   - Przejdź do http://localhost:3000/scan
   - Skanuj: `AAPL, MSFT, TSLA`
   - Zobacz wyniki

2. **Zapamiętaj:**
   - Która akcja spełnia kryteria (zielone tło)
   - Jaką ma cenę

3. **Add to Portfolio:**
   - Przejdź do http://localhost:3000/portfolio
   - Kliknij "+ Add Stock"
   - Dodaj akcję ze skanu (symbol + cena)

4. **Verify:**
   - Akcja powinna być w portfolio
   - Cena powinna się zgadzać

---

## 📊 TEST #6: Database Verification

**Cel:** Sprawdzić czy dane są persystowane w PostgreSQL

### Kroki:

1. Dodaj 2-3 akcje przez UI (http://localhost:3000/portfolio)

2. Sprawdź bazę danych:
   ```bash
   docker exec multibagger-db psql -U postgres -d multibagger -c "SELECT * FROM portfolio_items;"
   ```

3. Powinieneś zobaczyć:
   - Dodane akcje
   - Kolumny: id, user_id, symbol, entry_price, quantity, notes, added_at

4. Sprawdź user_id:
   ```bash
   docker exec multibagger-db psql -U postgres -d multibagger -c "SELECT DISTINCT user_id FROM portfolio_items;"
   ```

**Expected:** user_id = 1 (MOCK_USER_ID)

---

## 🎯 FINAL CHECKLIST - Sprint 2

Po zakończeniu wszystkich testów:

- [ ] Scanner API działa (Swagger)
- [ ] Scanner UI działa (formularz + wyniki)
- [ ] Portfolio API: GET/POST/PUT/DELETE (wszystkie działają)
- [ ] Portfolio UI: Lista + Dodawanie + Usuwanie
- [ ] Dane persystowane w PostgreSQL
- [ ] Full integration flow: Scan → Add → Verify
- [ ] Navbar zawiera linki: Home, Health Check, Scan, Portfolio

---

## 🐛 COMMON ISSUES

### 1. yfinance timeout / slow

**Problem:** Skan trwa >30 sekund

**Rozwiązanie:**
- To normalne przy pierwszym wywołaniu
- yfinance pobiera dane z Yahoo Finance
- Przy kolejnych wywołaniach będzie szybciej (cache)
- Zmniejsz liczbę symboli (zamiast 10 daj 3-4)

### 2. CORS error w przeglądarce

**Problem:** Console pokazuje "CORS policy blocked"

**Rozwiązanie:**
- Sprawdź backend/app/main.py
- `allow_origins` powinno zawierać `http://localhost:3000`
- Zrestartuj backend

### 3. Portfolio items nie zapisują się

**Problem:** Po dodaniu, lista jest pusta

**Rozwiązanie:**
- Sprawdź console przeglądarki (F12)
- Sprawdź logi backendu
- Sprawdź czy PostgreSQL działa: `docker-compose ps`
- Sprawdź tabele: `docker exec multibagger-db psql -U postgres -d multibagger -c "\dt"`

### 4. Module not found: yfinance

**Problem:** Backend error: ModuleNotFoundError: No module named 'yfinance'

**Rozwiązanie:**
```bash
cd backend
pip install yfinance
```

---

## 📸 SCREENSHOTS - Co powinieneś zobaczyć

### 1. Swagger UI - /api/scan
- Endpoint visible
- Request schema (symbols, min_volume, min_price_change_percent)
- Response schema (total_scanned, matches, results)

### 2. Scan Page (Frontend)
- Formularz z 3 polami
- Button "Scan Stocks"
- Tabela z wynikami (po skanie)
- Zielone tło dla akcji spełniających kryteria

### 3. Portfolio Page (Frontend)
- Button "+ Add Stock"
- Tabela z kolumnami: Symbol, Entry Price, Quantity, Notes, Added, Actions
- Button "Delete" przy każdej pozycji

### 4. Database (psql)
```
 id | user_id | symbol | entry_price | quantity | notes | added_at
----+---------+--------+-------------+----------+-------+----------
  1 |       1 | AAPL   |      150.00 |    10.00 | ...   | 2025-...
  2 |       1 | MSFT   |      350.00 |     5.00 | ...   | 2025-...
```

---

## 🚀 NEXT: Sprint 3

Jeśli wszystkie testy przeszły ✅, gotowe do Sprint 3:
- Celery background jobs (daily scans)
- n8n webhooks (email notifications)
- User authentication (JWT)

---

**Powodzenia z testami Sprint 2!** 🍀
