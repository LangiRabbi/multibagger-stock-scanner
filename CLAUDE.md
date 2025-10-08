# 🎯 STOCK SCANNER - ESSENTIALS

**Version:** 2.1 | **Updated:** 2025-10-08 | **Status:** Sprint 2 (65%)

## 📚 DOKUMENTACJA

@INDICATORS.md - Scoring 0-95 pkt (9 wskaźników)  
@AGENTS.md - Workflow 5 agentów  
@STANDARDS.md - Git + WCAG + code style  
@PRD.md - Product requirements

## 🎯 PROJEKT

Stock scanner z automatycznym scoring 0-95 pkt dla akcji multibagger.

**Funkcje:**
- Scanner API (9 wskaźników fundamentalnych)
- Portfolio CRUD
- Dashboard UI
- Powiadomienia in-app

## 📊 STATUS (Sprint 2)

### ✅ DZIAŁA (90%)
- POST /api/scan (9 wskaźników - KOMPLET)
- Portfolio CRUD
- Frontend UI (Home, Scan, Portfolio, Health)
- Redis cache + rate limiter (60 calls/min)
- WCAG 2.1 AA
- Coverage: 77% ✓

### 🔴 P0 (NAPRAWIONE ✅)
1. ✅ `symbols: []` → 422 (FIXED)
2. ✅ `min_volume: -1000` → 422 (FIXED)
3. ✅ 500 errors → proper error handling (FIXED)

### 🟡 P1 (tydzień)
- 2 failed tests (mocki - wymaga update)
- Frontend testy (Jest setup)

### 🔵 Sprint 3
- Celery jobs
- JWT auth
- n8n (opcja)

## 📦 STACK (FREE)

**Backend:** FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis  
**Frontend:** Next.js 15, React 18, TypeScript, Tailwind 4  
**Data:** Finnhub (131 metryk) + yfinance (volume)

**Limity:** 60 calls/min, Redis cache 15 min

## 🔧 WORKFLOW

1. **TY:** pytanie/zadanie
2. **AGENT:** plan → pytam o pozwolenie
3. **KODUJĘ:** komentarze PL + type hints
4. **TESTUJĘ:** pytest/npm test
5. **COMMIT:** conventional format

## ⚠️ PYTAJ PRZED

- Usuwanie plików
- `pip install` / `npm install`
- Zmiany `.env`, `config.py`
- Git force push
- DB migrations

## 🤖 AGENTY

| Agent | Kiedy |
|-------|-------|
| @pm-agent | Planning, breakdown |
| @backend-agent | Python/FastAPI |
| @frontend-agent | React/Next.js |
| @qa-agent | Testy, bugi |
| @devops-agent | Docker, deploy |

Szczegóły: @AGENTS.md

## 📝 GIT

Format: `<type>(scope): subject`

```bash
git commit -m "fix(backend): Add validation for empty symbols"
git commit -m "feat(frontend): Add portfolio delete modal"
```

Types: feat, fix, test, docs, refactor  
Scopes: backend, frontend, db, docker

Więcej: @STANDARDS.md

## 📊 WSKAŹNIKI (9 total)

**Fundamentalne (z Finnhub API):**
1. Market Cap (10-500M range)
2. ROE (Return on Equity %)
3. ROCE (Return on Capital Employed %)
4. Debt/Equity (max 30%)
5. Revenue Growth (YoY %)
6. Forward P/E (max 15)

**Cenowe (z yfinance):**
7. Volume (min 1M)
8. Price Change 7d (%)
9. Price Change 30d (%)

Pełne: @INDICATORS.md

## 🔥 PRIORYTET

### ✅ DONE (dziś)
- ✅ Walidacja Pydantic (symbols, min_volume)
- ✅ Error handling w /api/scan
- ✅ 77% test coverage

### Tydzień
- 2 failed tests (update mocki)
- Jest setup (frontend)

## 📚 PLIKI

- STATUS_PROJEKTU.md (1286) - status
- FINNHUB_STATUS.md (390) - FREE tier
- QA_REPORT_SPRINT2.md (476) - bugi
- PRD.md - requirements

## 🎓 BEST PRACTICES

**Python:**
```python
async def get_metrics(symbol: str) -> Dict[str, float]:
    """Pobiera metryki z Finnhub.
    
    Args:
        symbol: Ticker np. "AAPL"
    Returns:
        Dict z metrykami
    """
```

**React:**
```tsx
// ✅ WCAG
<button className="bg-blue-600 text-white">OK</button>

// ❌ ZŁY kontrast
<button className="text-gray-400">Bad</button>
```

## 🚨 PITFALLS

1. ✅ Finnhub volume = None → yfinance
2. ✅ FMP 403 → Finnhub
3. 🟡 Brak mocków → 8 fails
4. ❌ text-gray-400 → WCAG violation