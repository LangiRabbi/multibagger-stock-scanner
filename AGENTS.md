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

### Feature: "Dodaj Piotroski F-Score"

**1. Planning:**
```
TY → @pm-agent: "Dodaj 10-ty wskaźnik Piotroski F-Score"

@pm-agent → @backend-agent:
"Task: Implementuj Piotroski F-Score
- Endpoint: POST /api/scan
- 9 kryteriów finansowych
- Scoring 0-9 → 0-10 pkt
- Tests: 85% coverage
- ETA: 4 godziny"
```

**2. Development:**
```
@backend-agent:
"Plan:
1. Dodaję piotroski.py z 9 kryteriami
2. Integruję w scanner.py
3. Testy test_piotroski.py
4. Commit: feat(backend): Add Piotroski F-Score

⚠️ UWAGA: Zmieniam:
- backend/app/services/piotroski.py (nowy)
- backend/app/services/scanner.py
- tests/test_piotroski.py (nowy)

OK?"

TY: "OK"

@backend-agent: [koduje...]
```

**3. Testing:**
```
@backend-agent → @qa-agent: "Ready for testing: Piotroski F-Score"

@qa-agent:
"Testing:
✅ Unit tests pass (15/15)
✅ Coverage 92%
✅ Integration test pass
❌ Bug: ZeroDivisionError gdy totalAssets = 0

Bug report → @backend-agent"

@backend-agent: [fixuje bug]

@qa-agent:
"Re-test:
✅ All tests pass
✅ Coverage 94%
Approval → @pm-agent"
```

**4. Approval + Deploy:**
```
@pm-agent:
"Feature complete ✓
- 10/10 wskaźników
- Scoring 0-95 działa
→ @devops-agent: Deploy"

@devops-agent:
"Deploy:
1. git push origin main
2. Railway auto-deploy
3. Health check: ✓
4. Sentry monitoring: active"
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
- @backend-agent: Piotroski F-Score (80% done)
- @qa-agent: 8 failed tests (fixing mocki)

BLOCKERS:
- None

TODAY:
1. Finish Piotroski (ETA: 2h)
2. Fix failed tests (ETA: 3h)
3. PR review (@pm-agent)
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