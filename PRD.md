# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Multibagger Stock Scanner

**Version:** 1.1  
**Last Updated:** 2025-10-08  
**Status:** Sprint 2 (65% complete)

---

## EXECUTIVE SUMMARY

Stock scanner z automatycznym scoring 0-95 pkt dla akcji wysokowzrostowych (multibaggers). Wykorzystuje 10 wskaźników fundamentalnych z badań Yartseva (2025).

**Główne cele:**
- Automatyczne skanowanie (10 wskaźników)
- Portfolio CRUD
- Dashboard UI (wykresy, tabele)
- Powiadomienia in-app

---

## PROBLEM STATEMENT

Inwestorzy ręcznie przeglądają setki akcji, tracąc czas i pomijając okazje. Brakuje narzędzia z:
- Automatycznym filtrowaniem (fundamentals + technicals)
- Tracking portfolio w czasie rzeczywistym
- Akcjonalnymi insightami bez przytłaczania

---

## TARGET AUDIENCE

**Primary:**
- Inwestorzy indywidualni (retail) - oszczędności długoterminowe
- Day traderzy - szybkie sygnały wejścia
- Analitycy - automatyzacja screeningu

---

## CORE FEATURES

### 4.1 Stock Scanning Engine (MVP) ✅ 85%
**Priority:** P0

**Status:**
- ✅ Integracja Finnhub (131 metryk FREE)
- ✅ yfinance (volume)
- ✅ 9/10 wskaźników (brakuje: Piotroski)
- ✅ Scoring 0-95 pkt
- ✅ Endpoint POST /api/scan
- ✅ Rate limiting (60/min)
- ✅ Redis cache (15 min)

**Bugs P0:**
1. Brak walidacji `symbols: []`
2. Brak walidacji `min_volume: -1000`
3. 500 errors bez message

**Acceptance Criteria:**
- ✅ Skan 100 akcji < 60s
- ⏳ Accuracy >95% (pending Piotroski)
- ✅ API response < 2s

---

### 4.2 Portfolio Management (MVP) ✅ 90%
**Priority:** P0

**Status:**
- ✅ CRUD endpoints (GET/POST/PUT/DELETE)
- ✅ SQLAlchemy models
- ✅ User isolation (MOCK_USER_ID)
- ⏳ JWT auth (Sprint 3)
- ⏳ Daily price refresh (Celery - Sprint 3)

**Acceptance Criteria:**
- ✅ User add/edit/delete pozycje
- ⏳ Ceny aktualizują się daily (Sprint 3)

---

### 4.3 Dashboard UI (MVP) ✅ 75%
**Priority:** P0

**Status:**
- ✅ Home page
- ✅ Scan page (formularz + results table)
- ✅ Portfolio page (CRUD)
- ✅ Health check page
- ✅ Toast notifications
- ✅ ErrorBoundary
- ✅ WCAG 2.1 AA compliance
- ⏳ Wykresy (Recharts - Sprint 3)

**Acceptance Criteria:**
- ✅ Dashboard < 3s load
- ✅ Responsive (mobile 375px+)
- ✅ Lighthouse score > 85

---

### 4.4 Automated Notifications ⏳ Sprint 3
**Priority:** P1

**Status:**
- ✅ In-app notifications (toast)
- ⏳ n8n webhooks (email/Slack - opcjonalnie)

---

### 4.5 Background Jobs ⏳ Sprint 3
**Priority:** P0

**Status:**
- ⏳ Celery Beat scheduler
- ⏳ Daily scan (9:00 UTC)
- ⏳ Price refresh (8:00 UTC)
- ⏳ Cleanup (>30 dni)

---

### 4.6 User Authentication ⏳ Sprint 3
**Priority:** P1

**Status:**
- ⏳ JWT tokens (access + refresh)
- ⏳ Rejestracja/login
- ⏳ Password reset
- ⏳ OAuth2 (Google - opcjonalnie Sprint 4)

---

## TECH ARCHITECTURE

### 5.1 Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15
- SQLAlchemy 2.0
- Celery + Redis
- Finnhub (131 metryk FREE) + yfinance (volume)

**Frontend:**
- Next.js 15 (React 18)
- TypeScript
- Tailwind CSS 4 + shadcn/ui
- Recharts (wykresy - Sprint 3)

**Infrastructure:**
- Docker + Docker Compose
- Railway.app (hosting)
- GitHub Actions (CI/CD)
- n8n (opcjonalnie - Sprint 3)

### 5.2 Database Schema

**users** (Sprint 3)
- id, email, hashed_password, created_at

**portfolio_items**
- id, user_id (FK), symbol, entry_price, quantity, notes, added_at

**scan_results**
- id, symbol, scan_date, criteria_met (JSON), price, volume, score

---

## RELEASE PLAN

### ✅ v0.1 (MVP) - Week 7 (CURRENT)
**Sprint 2 - 65% complete**

**Done:**
- ✅ Stock scanning (9/10 wskaźników)
- ✅ Portfolio CRUD
- ✅ Dashboard UI (Home, Scan, Portfolio, Health)
- ✅ Redis cache + rate limiter
- ✅ WCAG 2.1 AA
- ✅ Coverage 67%

**To fix (24h):**
- 🔴 3 bugi walidacji
- 🔴 8 failed tests (mocki)

**To finish (tydzień):**
- 🟡 Piotroski F-Score (10-ty wskaźnik)
- 🟡 Frontend testy (Jest setup)

---

### ⏳ v0.2 - Sprint 3 (2-3 tygodnie)
- Celery background jobs (daily scan, price refresh)
- JWT authentication
- Powiadomienia in-app (bell icon)
- n8n webhooks (email/Slack - opcjonalnie)

---

### ⏳ v0.3 - Sprint 4 (tydzień 14)
- Wykresy (Recharts: candlestick, volume)
- Advanced filters (RSI, MA)
- Mobile optimization
- OAuth2 (Google/GitHub)

---

### ⏳ v1.0 - Produkcja
- Railway deployment
- Monitoring (Sentry)
- Performance optimization
- User onboarding

---

## SUCCESS METRICS

### Technical (CURRENT)
- ✅ API uptime: 99.5%
- ✅ P95 response: <2s
- ✅ Test coverage: 67% (target 50%)
- ⏳ Zero critical vulnerabilities (Sentry - Sprint 3)

### Product (Post-MVP)
- MAU: 100+ (Month 3)
- Scan accuracy: >95%
- User retention: >60% (Month 2)
- Avg scans/user/day: 3+

---

## RISKS & MITIGATIONS

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Finnhub rate limits | High | Cache 15 min + retry logic | ✅ Done |
| Finnhub volume = None | High | yfinance fallback | ✅ Done |
| Celery job failures | Medium | Retry logic + Sentry | ⏳ Sprint 3 |
| Scalability (1000+ users) | Medium | Railway Pro → AWS migration | ⏳ Future |
| Data accuracy | High | Validate 2+ sources | ⏳ Sprint 3 |

---

## OPEN QUESTIONS

- [ ] Monetyzacja (free tier + paid)?
- [ ] Domyślne kryteria scanów?
- [ ] Limit pozycji w portfolio (free tier)?
- [ ] Crypto markets (future)?

---

## SPRINT BREAKDOWN

### Sprint 1 ✅ DONE
- Setup (FastAPI, Next.js, Docker)
- PostgreSQL + SQLAlchemy models
- Redis cache
- Basic routing

### Sprint 2 🟡 65% DONE (CURRENT)
**Week 3-5:**
- ✅ Scan engine (9/10 wskaźników)
- ✅ Portfolio CRUD
- ✅ Dashboard UI
- ✅ WCAG 2.1 AA
- 🔴 3 bugi P0 (24h)
- 🟡 8 failed tests (tydzień)
- 🟡 Piotroski F-Score (tydzień)

### Sprint 3 ⏳ PLANNED (2-3 tygodnie)
**Week 6-8:**
- Celery background jobs
- JWT authentication
- n8n webhooks (opcja)
- Wykresy (Recharts)
- Integration tests (Playwright)

### Sprint 4 ⏳ FUTURE
**Week 9+:**
- Advanced filters
- Backtesting (basic)
- Mobile optimization
- OAuth2

---

## CHANGELOG

**2025-10-08 (v1.1):**
- Zaktualizowano status (Sprint 2 - 65%)
- Dodano 3 bugi P0
- Zaktualizowano tech stack (Finnhub + yfinance)
- Dodano sprint breakdown

**2025-10-07 (v1.0):**
- Initial PRD