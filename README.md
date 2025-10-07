# Multibagger Stock Scanner 📈

Aplikacja webowa do automatycznego skanowania rynków akcji w poszukiwaniu okazji inwestycyjnych (multibaggers). Wykorzystuje wieloagentową architekturę (multi-agent) do rozwoju produktu.

---

## 🎯 Features (Sprint 1 MVP)

✅ **Backend:**
- FastAPI z SQLAlchemy ORM
- PostgreSQL database (users, portfolio_items, scan_results)
- Redis cache
- Health check endpoint
- Docker Compose setup

✅ **Frontend:**
- Next.js 15 (App Router)
- TypeScript + Tailwind CSS
- Responsive navbar
- Health check page (test połączenia z backendem)

🚧 **Coming Soon (Sprint 2):**
- Stock scanning engine (yfinance integration)
- Portfolio CRUD API
- Celery background jobs
- n8n automation workflows

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- PostgreSQL 15
- SQLAlchemy
- Redis
- yfinance (stock data)

**Frontend:**
- Next.js 15
- React 18
- TypeScript
- Tailwind CSS

**Infrastructure:**
- Docker + Docker Compose
- n8n (workflows)
- GitHub Actions (CI/CD)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

### 1. Clone Repository

```bash
git clone https://github.com/LangiRabbi/multibagger-stock-scanner.git
cd multibagger-stock-scanner
```

### 2. Start Docker Compose (PostgreSQL + Redis)

```bash
docker-compose up -d postgres redis
```

Sprawdź status:
```bash
docker-compose ps
```

Oba kontenery powinny mieć status `Up (healthy)`.

### 3. Create Database Tables

**WAŻNE:** Ten krok jest wymagany tylko raz (przy pierwszym uruchomieniu):

```bash
cd backend

# Install dependencies (jeśli jeszcze nie)
pip install fastapi uvicorn sqlalchemy python-dotenv pydantic pydantic-settings redis yfinance

# Create tables
python create_tables.py
```

Powinno wyświetlić: `SUKCES! Tabele utworzone pomyslnie!`

Weryfikacja:
```bash
docker exec multibagger-db psql -U postgres -d multibagger -c "\dt"
```

Powinny być 3 tabele: `users`, `portfolio_items`, `scan_results`.

### 4. Run Backend (FastAPI)

W tym samym terminalu (lub nowym):

```bash
cd backend

# Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend będzie dostępny na:
- API: http://localhost:8000
- Health check: http://localhost:8000/health
- Docs (Swagger UI): http://localhost:8000/docs

### 5. Run Frontend (Next.js)

Otwórz kolejny terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend będzie dostępny na:
- Home: http://localhost:3000
- Health Check: http://localhost:3000/health-check

---

## 🧪 Testing

Zanim zaczniesz korzystać z aplikacji, przetestuj czy wszystko działa:

**Przeczytaj:** [TESTING.md](./TESTING.md) - pełny przewodnik testowania manualnego (krok po kroku).

### Quick Health Check

1. Backend: http://localhost:8000/health → powinno zwrócić `{"status": "ok"}`
2. Frontend: http://localhost:3000/health-check → powinno pokazać zielony box
3. Docker: `docker-compose ps` → oba kontenery `Up (healthy)`

---

## 📁 Project Structure

```
multibagger-stock-scanner/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── config.py       # Settings
│   │   ├── database.py     # SQLAlchemy setup
│   │   └── models/         # Database models
│   │       ├── user.py
│   │       ├── portfolio.py
│   │       └── scan.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                # Next.js application
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   └── health-check/   # Health check page
│   ├── components/
│   │   └── Navbar.tsx
│   └── package.json
│
├── docker-compose.yml       # Docker services (PostgreSQL, Redis)
├── PRD.md                   # Product Requirements Document
├── TESTING.md               # Manual testing guide
└── README.md                # This file
```

---

## 🔑 Environment Variables

### Backend (.env)

Skopiuj `.env.example` do `.env`:
```bash
cd backend
cp .env.example .env
```

Edytuj wartości w `.env`:
```bash
# Database
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=multibagger
DB_HOST=localhost
DB_PORT=5433

# Redis
REDIS_URL=redis://localhost:6379

# API
PORT=8000
MIN_VOLUME=1000000
```

---

## 📊 Database

### Modele (Tabele)

**users** - użytkownicy aplikacji
- id (PK)
- email (unique)
- hashed_password
- created_at

**portfolio_items** - pozycje w portfolio użytkownika
- id (PK)
- user_id (FK → users.id)
- symbol (np. AAPL)
- entry_price
- quantity
- notes
- added_at

**scan_results** - wyniki skanów akcji
- id (PK)
- symbol
- scan_date
- criteria_met (JSON)
- price
- volume

### Sprawdzenie tabel

```bash
docker exec -it multibagger-db psql -U postgres -d multibagger
\dt    # lista tabel
\d users    # struktura tabeli users
\q    # wyjście
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f postgres
docker-compose logs -f redis

# Restart services
docker-compose restart

# Check status
docker-compose ps
```

---

## 🤝 Multi-Agent Development

Projekt wykorzystuje wieloagentową architekturę rozwoju:

- **@pm-agent** (Product Manager) - planowanie, delegacja tasków
- **@backend-agent** (Backend Developer) - FastAPI, SQLAlchemy, Celery
- **@frontend-agent** (Frontend Developer) - Next.js, React, UI/UX
- **@qa-agent** (QA Engineer) - testy, bug reports
- **@devops-agent** (DevOps Engineer) - Docker, deployment, CI/CD

Więcej informacji: [PRD.md](./PRD.md)

---

## 📝 API Endpoints

### Current (Sprint 1)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/api/info` | Configuration info |

### Coming Soon (Sprint 2)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scan` | Scan stocks by criteria |
| GET | `/api/portfolio` | Get user's portfolio |
| POST | `/api/portfolio` | Add stock to portfolio |
| PUT | `/api/portfolio/{id}` | Update portfolio item |
| DELETE | `/api/portfolio/{id}` | Remove from portfolio |

---

## 🐛 Troubleshooting

### Port already in use

```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID [process-id] /F

# Or change port in .env:
PORT=8001
```

### Docker issues

```bash
# Restart Docker Desktop
# Clean volumes
docker-compose down -v
docker-compose up -d --force-recreate
```

### Module not found (Python)

```bash
cd backend
pip install -r requirements.txt
```

### Cannot connect to backend (Frontend)

1. Check if backend is running: http://localhost:8000/health
2. Check CORS settings in `backend/app/main.py`
3. Check browser console (F12) for errors

---

## 📚 Documentation

- [PRD.md](./PRD.md) - Product Requirements Document
- [TESTING.md](./TESTING.md) - Manual Testing Guide
- [CLAUDE.md](./CLAUDE.md) - Agent development guidelines
- Backend API Docs: http://localhost:8000/docs (Swagger UI)

---

## 🎯 Roadmap

### ✅ Sprint 1 (Week 1-2) - MVP Foundation
- Docker Compose setup
- FastAPI + SQLAlchemy models
- Next.js + basic UI
- Health check endpoint

### 🚧 Sprint 2 (Week 3-5) - Core Features
- Stock scanning engine (yfinance)
- Portfolio CRUD API
- Celery background jobs
- Dashboard UI with charts

### 📅 Sprint 3 (Week 6) - Integration
- n8n webhooks (notifications)
- User authentication (JWT)
- E2E tests

### 📅 Sprint 4 (Week 7) - Deployment
- Railway/Render deployment
- CI/CD pipeline (GitHub Actions)
- Performance testing

---

## 📄 License

MIT

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

- GitHub: [LangiRabbi/multibagger-stock-scanner](https://github.com/LangiRabbi/multibagger-stock-scanner)
- Issues: [GitHub Issues](https://github.com/LangiRabbi/multibagger-stock-scanner/issues)

---

**Built with ❤️ using Multi-Agent Architecture**
