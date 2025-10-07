# 🧪 Sprint 2 Testing Guide - Stock Scanner + Portfolio CRUD

Przewodnik testowania dla Sprint 2 (dla początkujących!)

---

## ⚠️ WAŻNE: Przed Testami

### Problem znaleziony podczas testów:
**Portfolio API wymaga użytkownika w bazie danych!**

Jeśli próbujesz dodać akcję do portfolio i dostajesz błąd:
```
ForeignKeyViolation: Key (user_id)=(1) is not present in table "users"
```

**Rozwiązanie:** Uruchom skrypt tworzący mock użytkownika:

```bash
cd backend
python seed_mock_user.py
```

Powinno wyświetlić:
```
✅ SUKCES! Mock użytkownik utworzony:
   ID: 1, Email: test@example.com, Created: 2025-10-07...
```

---

## ✅ PRE-REQUISITES

- [ ] Docker Desktop uruchomiony
- [ ] PostgreSQL i Redis działają (`docker-compose ps` → healthy)
- [ ] Tabele utworzone (`python backend/create_tables.py`)
- [ ] **Mock użytkownik utworzony (`python backend/seed_mock_user.py`)** ← NOWE!
- [ ] Backend działa (`http://localhost:8000/health`)
- [ ] Frontend działa (`http://localhost:3000`)

---

## 🧪 TEST #1: Stock Scanner API

**Endpoint:** `POST /api/scan`

### Test w przeglądarce (Swagger UI):

1. Otwórz: http://localhost:8000/docs
2. Rozwiń `POST /api/scan`
3. Kliknij "Try it out"
4. Wpisz symbole akcji (oddzielone przecinkami):
   ```json
   {
     "symbols": "AAPL,MSFT,TSLA,GOOGL",
     "min_volume": 1000000,
     "min_price_change_7d": null
   }
   ```
5. Kliknij "Execute"

### ✅ Expected Result:

```json
{
  "total_scanned": 4,
  "matches": 2,
  "results": [
    {
      "symbol": "AAPL",
      "price": 150.00,
      "volume": 50000000,
      "price_change_7d": 5.2,
      "price_change_30d": 10.5,
      "meets_criteria": true
    },
    ...
  ]
}
```

### Test z curl:

```bash
curl -X POST "http://localhost:8000/api/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "AAPL,MSFT,TSLA",
    "min_volume": 1000000
  }'
```

---

## 🧪 TEST #2: Portfolio CRUD API

**Endpoints:**
- `GET /api/portfolio` - Pobierz wszystkie pozycje
- `POST /api/portfolio` - Dodaj akcję
- `PUT /api/portfolio/{id}` - Edytuj pozycję
- `DELETE /api/portfolio/{id}` - Usuń pozycję

### Test 2.1: Pobierz Portfolio (GET)

```bash
curl http://localhost:8000/api/portfolio
```

**Expected:** `[]` (pusta tablica jeśli nie dodałeś jeszcze akcji)

### Test 2.2: Dodaj Akcję (POST)

```bash
curl -X POST "http://localhost:8000/api/portfolio" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "entry_price": 150.00,
    "quantity": 10,
    "notes": "Long term hold"
  }'
```

**Expected:**
```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "AAPL",
  "entry_price": 150.0,
  "quantity": 10.0,
  "notes": "Long term hold",
  "added_at": "2025-10-07T12:00:00Z"
}
```

### Test 2.3: Edytuj Pozycję (PUT)

```bash
curl -X PUT "http://localhost:8000/api/portfolio/1" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated notes - watching for breakout"
  }'
```

### Test 2.4: Usuń Pozycję (DELETE)

```bash
curl -X DELETE "http://localhost:8000/api/portfolio/1"
```

**Expected:** Status 204 No Content

---

## 🧪 TEST #3: Frontend - Stock Scanner Page

### Kroki:

1. Otwórz: http://localhost:3000/scan
2. Wpisz symbole: `AAPL, MSFT, TSLA, GOOGL`
3. Ustaw min volume: `1000000`
4. Kliknij "Scan Stocks"

### ✅ Expected Result:

- Loading indicator pojawia się
- Po 3-5 sekundach wyniki się ładują
- Tabela pokazuje:
  - Symbol
  - Price
  - Volume
  - Change 7d
  - Change 30d
  - Status (✓ Match lub ✗ No Match)
- Nagłówek pokazuje: "Scan Results: X / Y akcji spełnia kryteria"

---

## 🧪 TEST #4: Frontend - Portfolio Page

### Kroki:

1. Otwórz: http://localhost:3000/portfolio
2. Kliknij "+ Add Stock"
3. Wypełnij formularz:
   - Symbol: AAPL
   - Entry Price: 150.00
   - Quantity: 10
   - Notes: Test position
4. Kliknij "Add to Portfolio"

### ✅ Expected Result:

- Formularz znika
- Akcja pojawia się w tabeli portfolio
- Licznik "Your Stocks (X)" się aktualizuje
- Możesz kliknąć "Delete" aby usunąć pozycję

---

## ❌ Common Issues (Typowe Problemy)

### Problem 1: "Failed to fetch" w Portfolio

**Przyczyna:** Backend nie działa lub CORS problem

**Rozwiązanie:**
1. Sprawdź czy backend działa: http://localhost:8000/health
2. Sprawdź console przeglądarki (F12 → Console)
3. Sprawdź CORS w `backend/app/main.py` (powinno być `http://localhost:3000`)

### Problem 2: "ForeignKeyViolation: user_id not found"

**Przyczyna:** Brak mock użytkownika w bazie

**Rozwiązanie:**
```bash
cd backend
python seed_mock_user.py
```

### Problem 3: Stock Scanner nie zwraca danych

**Przyczyna:** yfinance API może być powolne lub timeout

**Rozwiązanie:**
- Poczekaj 5-10 sekund
- Spróbuj z mniejszą liczbą symboli (np. tylko AAPL,MSFT)
- Sprawdź logi backendu czy są błędy

### Problem 4: "Internal Server Error" podczas dodawania do portfolio

**Przyczyna:** Prawdopodobnie brak mock użytkownika

**Rozwiązanie:**
1. Sprawdź logi backendu (`uvicorn` terminal)
2. Uruchom `python seed_mock_user.py`
3. Spróbuj ponownie

---

## 🎯 FINAL CHECKLIST

Po zakończeniu testów sprawdź:

- [ ] Stock Scanner działa (zwraca wyniki dla AAPL, MSFT, etc.)
- [ ] Portfolio GET zwraca listę akcji
- [ ] Portfolio POST dodaje nowe pozycje
- [ ] Portfolio DELETE usuwa pozycje
- [ ] Frontend /scan pokazuje wyniki skanowania
- [ ] Frontend /portfolio pokazuje listę akcji
- [ ] Możesz dodać i usunąć akcje przez UI
- [ ] Nie ma błędów w konsoli przeglądarki (F12)
- [ ] Mock użytkownik istnieje w bazie (user_id=1)

---

## 🚀 NEXT STEPS

Jeśli wszystkie testy przeszły ✅:

**Sprint 2 is COMPLETE!** 🎉

Możesz przejść do:
- **Sprint 3:** User Authentication (JWT)
- **Sprint 3:** n8n Webhooks (notyfikacje)
- **Sprint 3:** Dashboard z wykresami

---

## 📸 SCREENSHOTS (Co powinieneś zobaczyć)

### 1. Stock Scanner Results
```
Scan Results: 2 / 4 akcji spełnia kryteria

Symbol | Price  | Volume    | Change 7d | Change 30d | Status
-------|--------|-----------|-----------|------------|--------
AAPL   | 150.00 | 50000000  | +5.2%     | +10.5%     | ✓ Match
MSFT   | 320.00 | 30000000  | +3.1%     | +8.2%      | ✓ Match
TSLA   | 250.00 | 80000000  | -2.1%     | +15.0%     | ✗ No Match
```

### 2. Portfolio Page
```
My Portfolio

Your Stocks (3)

Symbol | Entry Price | Quantity | Notes           | Added      | Actions
-------|-------------|----------|-----------------|------------|--------
AAPL   | $150.00     | 10       | Long term hold  | 10/07/2025 | Delete
TSLA   | $250.00     | 5        | Growth stock    | 10/07/2025 | Delete
GOOGL  | $140.00     | 8        | Tech giant      | 10/07/2025 | Delete
```

---

**Powodzenia z testami Sprint 2!** 🍀
