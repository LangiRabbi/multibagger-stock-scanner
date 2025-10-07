# 🧪 Manual Testing Guide - Sprint 1 MVP

Przewodnik testowania manualnego dla użytkownika (początkujący programista friendly!)

---

## ✅ PRE-REQUISITES (Co musi być gotowe przed testami)

Przed rozpoczęciem testów upewnij się że:

- [ ] Docker Desktop jest uruchomiony (ikona wieloryba w tray)
- [ ] Sklonowałeś repo: `git clone https://github.com/LangiRabbi/multibagger-stock-scanner.git`
- [ ] Jesteś w głównym folderze projektu: `cd multibagger-stock-scanner`

---

## 🐳 TEST #1: Docker Compose - PostgreSQL i Redis

**Cel:** Sprawdzić czy baza danych i Redis działają

### Kroki:

1. Otwórz terminal (PowerShell)
2. Uruchom:
   ```bash
   docker-compose up -d postgres redis
   ```

3. Sprawdź status:
   ```bash
   docker-compose ps
   ```

### ✅ Expected Result (Oczekiwany wynik):

```
NAME                IMAGE                COMMAND        SERVICE    STATUS
multibagger-db      postgres:15-alpine   ...            postgres   Up (healthy)
multibagger-redis   redis:7-alpine       ...            redis      Up (healthy)
```

**Status powinien być:** `Up (healthy)` dla obu kontenerów

### ❌ Co robić jeśli nie działa:

- Jeśli `port 5432 already allocated` → zmień port w docker-compose.yml (już zrobione na 5433)
- Jeśli `Cannot connect to Docker` → uruchom Docker Desktop
- Jeśli `unhealthy` → poczekaj 30 sekund i sprawdź ponownie

---

## 🐍 TEST #2: Backend FastAPI

**Cel:** Sprawdzić czy backend uruchamia się i odpowiada na requesty

### Kroki:

1. Otwórz **nowy terminal** (zostaw Docker w 1. terminalu)
2. Przejdź do folderu backend:
   ```bash
   cd backend
   ```

3. Zainstaluj zależności (jeśli jeszcze nie):
   ```bash
   pip install fastapi uvicorn sqlalchemy python-dotenv pydantic pydantic-settings redis yfinance
   ```

4. Uruchom backend:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Otwórz przeglądarkę i wejdź na:
   - **http://localhost:8000** (strona główna)
   - **http://localhost:8000/health** (health check)
   - **http://localhost:8000/docs** (automatyczna dokumentacja FastAPI - Swagger UI)

### ✅ Expected Result:

**http://localhost:8000** powinno zwrócić:
```json
{
  "message": "Multibagger Stock Scanner API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

**http://localhost:8000/health** powinno zwrócić:
```json
{
  "status": "ok",
  "message": "API is running",
  "database": "connected",
  "redis": "connected"
}
```

**http://localhost:8000/docs** powinno pokazać:
- Interfejs Swagger UI
- Lista endpointów: `/`, `/health`, `/api/info`
- Możliwość testowania API z przeglądarki

### ❌ Co robić jeśli nie działa:

- **Error: `ModuleNotFoundError`** → zainstaluj brakujące pakiety: `pip install [nazwa-pakietu]`
- **Error: `Port 8000 already in use`** → zatrzymaj inny proces na porcie 8000
- **Tabele nie utworzone w PostgreSQL** → uruchom skrypt tworzenia tabel:
  ```bash
  cd backend
  python create_tables.py
  ```
  Powinno wyświetlić: `SUKCES! Tabele utworzone pomyslnie!`

---

## 🗃️ TEST #2.5: Tworzenie Tabel w Bazie Danych

**Cel:** Stworzyć tabele aplikacji w PostgreSQL (users, portfolio_items, scan_results)

### Kroki:

1. Upewnij się że PostgreSQL działa (TEST #1)
2. Przejdź do folderu backend:
   ```bash
   cd backend
   ```

3. Uruchom skrypt tworzenia tabel:
   ```bash
   python create_tables.py
   ```

### ✅ Expected Result:

Skrypt powinien wyświetlić:
```
Tworzenie tabel w bazie danych...
Znalezione modele: dict_keys(['users', 'portfolio_items', 'scan_results'])
[... logi SQLAlchemy ...]
SUKCES! Tabele utworzone pomyslnie!
Lista tabel: ['users', 'portfolio_items', 'scan_results']
```

### Weryfikacja:

Sprawdź czy tabele istnieją:
```bash
docker exec multibagger-db psql -U postgres -d multibagger -c "\dt"
```

Powinno zwrócić:
```
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | portfolio_items | table | postgres
 public | scan_results    | table | postgres
 public | users           | table | postgres
```

### ❌ Co robić jeśli nie działa:

- **Error: Cannot connect to database** → Sprawdź czy PostgreSQL działa (TEST #1)
- **Error: ModuleNotFoundError** → Zainstaluj zależności: `pip install sqlalchemy psycopg2-binary`
- **Tabele już istnieją** → To OK! Skrypt sprawdza czy tabele istnieją przed utworzeniem

**WAŻNE:** Ten krok jest wymagany tylko raz. Po utworzeniu tabel nie musisz tego powtarzać.

---

## ⚛️ TEST #3: Frontend Next.js

**Cel:** Sprawdzić czy frontend uruchamia się i komunikuje z backendem

### Kroki:

1. Otwórz **trzeci terminal** (zostaw backend w 2. terminalu)
2. Przejdź do folderu frontend:
   ```bash
   cd frontend
   ```

3. Zainstaluj zależności (jeśli jeszcze nie):
   ```bash
   npm install
   ```

4. Uruchom frontend:
   ```bash
   npm run dev
   ```

5. Otwórz przeglądarkę i wejdź na:
   - **http://localhost:3000** (strona główna)
   - **http://localhost:3000/health-check** (test połączenia z backendem)

### ✅ Expected Result:

**http://localhost:3000** powinno pokazać:
- Tytuł: "Multibagger Stock Scanner 📈"
- 4 karty z features (Stock Scanner, Portfolio, Dashboard, Alerts)
- Niebieski box z informacjami o Sprint 1 MVP
- Navbar z linkami (Home, Health Check, Scan, Portfolio)

**http://localhost:3000/health-check** powinno pokazać:
- Zielony box z napisem "✅ API is Running"
- Status: `database: connected`, `redis: connected`
- Raw JSON response na dole strony

### ❌ Co robić jeśli nie działa:

- **Error: `Cannot connect to backend`** (czerwony box na /health-check):
  - Sprawdź czy backend działa (TEST #2)
  - Sprawdź czy backend jest na porcie 8000
  - Sprawdź CORS settings w backend/app/main.py

- **Error: `npm ERR! code ENOENT`** → upewnij się że jesteś w folderze `frontend/`
- **Page nie ładuje się** → sprawdź konsolę przeglądarki (F12 → Console)

---

## 🔗 TEST #4: Full Stack Integration

**Cel:** Sprawdzić czy cały stack działa razem

### Kroki:

1. **Upewnij się że wszystko działa:**
   - Docker: `docker-compose ps` (2 kontenery healthy)
   - Backend: http://localhost:8000/health (status ok)
   - Frontend: http://localhost:3000 (strona się ładuje)

2. **Test flow użytkownika:**
   - Wejdź na http://localhost:3000
   - Kliknij "Health Check" w navbarze
   - Sprawdź czy widzisz zielony box z "API is Running"
   - Sprawdź czy JSON response pokazuje `database: connected`

3. **Test dokumentacji API:**
   - Wejdź na http://localhost:8000/docs
   - Rozwiń endpoint `GET /health`
   - Kliknij "Try it out"
   - Kliknij "Execute"
   - Sprawdź Response (powinno być 200 OK)

### ✅ Expected Result:

Wszystkie 3 komponenty działają razem:
- ✅ PostgreSQL + Redis (Docker)
- ✅ Backend FastAPI (Python)
- ✅ Frontend Next.js (React)
- ✅ Komunikacja frontend → backend działa
- ✅ Backend → database działa

---

## 📊 TEST #5: Database Check (Advanced)

**Cel:** Sprawdzić czy tabele zostały utworzone w PostgreSQL

### Kroki:

1. Połącz się z PostgreSQL przez Docker:
   ```bash
   docker exec -it multibagger-db psql -U postgres -d multibagger
   ```

2. Sprawdź listę tabel:
   ```sql
   \dt
   ```

3. Sprawdź strukturę tabeli `users`:
   ```sql
   \d users
   ```

4. Wyjdź z psql:
   ```sql
   \q
   ```

### ✅ Expected Result:

Lista tabel powinna zawierać:
- `users`
- `portfolio_items`
- `scan_results`

Struktura tabeli `users`:
- `id` (integer, primary key)
- `email` (varchar, unique)
- `hashed_password` (varchar)
- `created_at` (timestamp)

### ❌ Co robić jeśli nie działa:

- **Tabele nie istnieją** → Sprawdź logi backendu, upewnij się że `Base.metadata.create_all()` się wykonało
- **Błąd połączenia** → Sprawdź czy PostgreSQL działa (TEST #1)

---

## 🎯 FINAL CHECKLIST (Finalna lista sprawdzeń)

Po zakończeniu wszystkich testów, upewnij się że:

- [ ] Docker Compose: PostgreSQL i Redis działają (healthy)
- [ ] Backend FastAPI: `/health` zwraca `status: ok`
- [ ] Frontend Next.js: Strona główna się ładuje
- [ ] `/health-check` pokazuje zielony box (połączenie działa)
- [ ] Swagger UI (`/docs`) działa i pokazuje endpointy
- [ ] Tabele SQL zostały utworzone (users, portfolio_items, scan_results)
- [ ] Wszystkie 3 terminale działają bez błędów (Docker, Backend, Frontend)

---

## 🐛 COMMON ISSUES (Typowe problemy)

### Problem: "Port already in use"
**Rozwiązanie:**
```bash
# Znajdź proces zajmujący port
netstat -ano | findstr :8000
# Zabij proces (zamień PID)
taskkill /PID [numer-procesu] /F
```

### Problem: "Module not found" w Pythonie
**Rozwiązanie:**
```bash
pip install -r backend/requirements.txt
```

### Problem: "Docker daemon not running"
**Rozwiązanie:**
- Uruchom Docker Desktop
- Poczekaj aż ikona wieloryba przestanie się kręcić

### Problem: Frontend nie łączy się z backendem
**Rozwiązanie:**
- Sprawdź czy backend działa: http://localhost:8000/health
- Sprawdź konsolę przeglądarki (F12)
- Sprawdź CORS w `backend/app/main.py` (powinno być `allow_origins=["http://localhost:3000"]`)

---

## 📸 SCREENSHOTS (Co powinieneś zobaczyć)

### 1. Docker Compose PS
```
STATUS: Up (healthy)
```

### 2. Backend /health
```json
{"status": "ok", "message": "API is running"}
```

### 3. Frontend Home
```
Multibagger Stock Scanner 📈
[4 feature cards]
[MVP info box]
```

### 4. Frontend /health-check
```
✅ API is Running
Database: connected
Redis: connected
```

---

## 🚀 NEXT STEPS (Następne kroki)

Jeśli wszystkie testy przeszły ✅:

**Sprint 1 MVP is COMPLETE!** 🎉

Możesz przejść do:
- **Sprint 2:** Implementacja `/api/scan` endpoint (skanowanie akcji)
- **Sprint 2:** Portfolio CRUD (dodawanie/usuwanie akcji)
- **Sprint 2:** Celery + background jobs

---

## 📞 HELP (Pomoc)

Jeśli coś nie działa:

1. Sprawdź logi:
   - Backend: w terminalu gdzie uruchomiłeś `uvicorn`
   - Frontend: w terminalu gdzie uruchomiłeś `npm run dev`
   - Docker: `docker-compose logs postgres redis`

2. Sprawdź issues na GitHubie:
   https://github.com/LangiRabbi/multibagger-stock-scanner/issues

3. Opisz problem:
   - Co zrobiłeś (kroki)
   - Co się stało (błąd)
   - Co powinno się stać (expected result)
   - Logi/screenshoty

---

**Powodzenia z testami!** 🍀
