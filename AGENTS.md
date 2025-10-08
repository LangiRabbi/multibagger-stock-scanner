# 🤖 ZARZĄDZANIE AGENTAMI

5 agentów w `.claude/agents/`

## ROLE

| Agent | Odpowiedzialność | Narzędzia |
|-------|------------------|-----------|
| **@pm-agent** | Planning, breakdown, approval | read_file, list_files |
| **@backend-agent** | Python, FastAPI, SQLAlchemy, Celery | read/write_file, run_terminal, git |
| **@frontend-agent** | React, Next.js, UI, wykresy | read/write_file, run_terminal |
| **@qa-agent** | Pytest, coverage, bug reports | read_file, run_terminal |
| **@devops-agent** | Docker, Railway, CI/CD | read/write_file, run_terminal, git |

## WORKFLOW

### 1. PLANNING (nowy feature)
```
@pm-agent:
1. Rozbij PRD na epic/tasks
2. User stories + acceptance criteria
3. Assign → @backend-agent lub @frontend-agent
```

### 2. DEVELOPMENT
```
@backend-agent / @frontend-agent:
1. Implementuj feature
2. Unit tests (coverage ≥50%)
3. Commit (conventional format)
4. Notify @qa-agent: "Ready for testing"
```

### 3. TESTING
```
@qa-agent:
1. Pytest / Jest
2. Manual testing
3. IF fail → Bug report → @backend-agent
4. IF pass → Approval → @pm-agent
```

### 4. DEPLOYMENT
```
@devops-agent:
1. Merge do main
2. Railway deploy
3. Health check
4. Monitoring (Sentry)
```

## DEFINITION OF DONE (DoD)

- ✅ Code reviewed
- ✅ Tests passing (unit + integration)
- ✅ Coverage ≥ 50%
- ✅ WCAG compliance (frontend)
- ✅ Deployed to staging
- ✅ @pm-agent approval

## PRZYKŁADOWY FLOW

### Feature: "Fix 3 bugi P1 - walidacja"

**1. Planning:**
```
TY → @pm-agent: "Napraw 3 bugi P1 znalezione przez @qa-agent"

@pm-agent → @backend-agent:
"Task: Fix walidacja Pydantic
- BUG 1: symbols: [] → 422 (nie 200)
- BUG 2: min_volume: -1000 → 422 (nie 200)
- BUG 3: 500 errors → proper error handling
- Tests: Sprawdź czy fixed
- ETA: 2 godziny"
```

**2. Development:**
```
@backend-agent:
"Plan:
1. Dodaję field_validator w schemas/scan.py
2. Dodaję ge=0 dla min_volume
3. Dodaję try-except w api/scan.py
4. Uruchamiam pytest

⚠️ UWAGA: Zmieniam:
- backend/app/schemas/scan.py
- backend/app/api/scan.py

OK?"

TY: "OK"

@backend-agent: [koduje...]
```

**3. Testing:**
```
@backend-agent → @qa-agent: "Ready for testing: Bugfixy P1"

@qa-agent:
"Testing:
✅ test_scan_endpoint_validates_empty_symbols PASS
✅ test_scan_endpoint_validates_negative_volume PASS
✅ test_scan_endpoint_handles_scanner_exception PASS
✅ Coverage 77% (target: 50%)

Approval → @pm-agent"
```

**4. Approval + Commit:**
```
@pm-agent:
"Bugfixy complete ✓
- 3/3 bugi P1 fixed
- 77% coverage
→ Commit + Push"

git commit -m "feat(backend): Fix P1 validation bugs + add test suite (77% coverage)"
git push origin main
```

## KOMUNIKACJA (DAILY STANDUP)

**@pm-agent posts:**
- What's in progress
- Blockers
- Today's priorities

**Format:**
```
🎯 SPRINT 2 - DAY 5

IN PROGRESS:
- @qa-agent: 2 failed tests (updating mocki)
- @frontend-dev: Jest setup (testing framework)

BLOCKERS:
- None

TODAY:
1. Fix 2 failed tests (update mocki - ETA: 1h)
2. Jest setup dla frontend (ETA: 2h)
3. Sprint 2 finalizacja
```

## ESCALATION

**Jeśli blokada >24h:**
```
@backend-agent → @pm-agent:
"BLOCKER: Finnhub nie zwraca ROIC dla 30% symboli
Options:
1. Fallback do 0 (skip scoring)
2. Użyć FMP backup (paid)
3. Mark jako incomplete

Rekomendacja: #1
Decyzja?"
```

## PRZEŁĄCZANIE KONTEKSTU

**Gdy wielka zmiana:**
```
@pm-agent → ALL:
"⚠️ BREAKING CHANGE:
Migrujemy z FMP → Finnhub (wszystkie metryki)

@backend-agent: Refactor scanner.py
@qa-agent: Update testy (mocki Finnhub)
@devops-agent: Update .env config

Git branch: feature/finnhub-migration
Target: Sprint 2 end"
```

## AGENT-SPECIFIC NOTES

### @backend-agent
- **Always:** Type hints + docstring PL
- **Before commit:** pytest + coverage check
- **Async:** Użyj async/await dla I/O

### @frontend-agent
- **Always:** WCAG 2.1 AA compliance
- **Before commit:** Lighthouse score ≥ 85
- **TypeScript:** Strict mode

### @qa-agent
- **Coverage:** ≥ 50% (unit), ≥ 30% (integration)
- **Mocki:** Użyj conftest.py fixtures
- **Bug report:** P0/P1/P2 + ETA

### @devops-agent
- **Security:** Secrets w .env (never git)
- **Monitoring:** Sentry dla errors
- **Backup:** Daily DB snapshots

### @pm-agent
- **Breakdown:** Epic → Story → Task
- **Timeline:** Realistic ETA
- **DoD:** Enforce checklist