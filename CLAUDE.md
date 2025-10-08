# 🎯 STOCK SCANNER - ESSENTIALS

**Version:** 2.1 | **Updated:** 2025-10-08 | **Status:** Sprint 2 (65%)

## 📚 DOKUMENTACJA

@INDICATORS.md - Scoring 0-95 pkt (10 wskaźników)  
@AGENTS.md - Workflow 5 agentów  
@STANDARDS.md - Git + WCAG + code style  
@PRD.md - Product requirements

## 🎯 PROJEKT

Stock scanner z automatycznym scoring 0-95 pkt dla akcji multibagger.

**Funkcje:**
- Scanner API (10 wskaźników fundamentalnych)
- Portfolio CRUD
- Dashboard UI
- Powiadomienia in-app

## 📊 STATUS (Sprint 2)

### ✅ DZIAŁA (85%)
- POST /api/scan (9/10 wskaźników)
- Portfolio CRUD
- Frontend UI (Home, Scan, Portfolio, Health)
- Redis cache + rate limiter (60 calls/min)
- WCAG 2.1 AA
- Coverage: 67% ✓

### 🔴 P0 (24h)
1. `symbols: []` → 200 (powinno 422)
2. `min_volume: -1000` → 200 (powinno 422)
3. 500 errors bez message

**Fix:** `schemas/scan.py` + `api/scan.py`

### 🟡 P1 (tydzień)
- 8 failed tests (mocki)
- Piotroski F-Score
- Frontend testy (Jest)

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

## 📊 SCORING (0-95)

- FCF Yield: 20 pkt
- ROE: 15 pkt
- Revenue Growth: 15 pkt
- Market Cap: 10 pkt
- ROCE: 10 pkt
- P/E: 10 pkt
- Piotroski: 10 pkt
- Debt/Equity: 10 pkt
- Net Margin: 5 pkt

**Wynik:**
- 76-95: STRONG BUY
- 57-75: BUY
- 38-56: HOLD
- 0-37: AVOID

Pełne: @INDICATORS.md

## 🔥 PRIORYTET

### Dziś (2-3h)
```python
# schemas/scan.py
symbols: List[str] = Field(min_length=1)
min_volume: Optional[int] = Field(ge=0)

# api/scan.py
try:
    results = StockScanner.scan_stocks(...)
except Exception as e:
    raise HTTPException(500, "Scan failed")
```

### Tydzień
- 8 failed tests (mocki)
- Piotroski F-Score
- Jest setup

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