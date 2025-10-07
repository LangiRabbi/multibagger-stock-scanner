# Product Requirements Document (PRD)
## Multibagger Stock Scanner

**Version:** 1.0
**Last Updated:** 2025-10-07
**Status:** Draft

---

## 1. Executive Summary

Multibagger Stock Scanner to aplikacja webowa pozwalająca inwestorom automatycznie skanować rynki akcji w poszukiwaniu okazji inwestycyjnych spełniających określone kryteria techniczne i fundamentalne. System wykorzystuje wieloagentową architekturę do zarządzania cyklem życia produktu od planowania przez development, testing aż po deployment.

**Główne cele:**
- Automatyczne skanowanie akcji na podstawie konfigurowalnych kryteriów
- Zarządzanie portfolio kandydatów
- Wizualizacja danych i trendów
- Automatyczne powiadomienia o nowych okazjach

---

## 2. Problem Statement

Inwestorzy muszą ręcznie przeglądać setki akcji, tracąc czas i często pomijając wartościowe okazje. Brakuje narzędzia, które:
- Automatycznie filtruje akcje według kryterium fundamentalnych i technicznych
- Śledzi portfolio kandydatów w czasie rzeczywistym
- Dostarcza akcjonalne insighty bez przytłaczania informacjami

---

## 3. Target Audience

**Primary Users:**
- Inwestorzy indywidualni (retail) z podstawową wiedzą o rynkach
- Day traderzy szukający sygnałów wejścia
- Analitycy chcący automatyzować screening

**User Personas:**
- **Jan (Retail Investor):** 35 lat, inwestuje oszczędności, szuka okazji długoterminowych
- **Anna (Day Trader):** 28 lat, aktywnie traduje, potrzebuje szybkich alertów
- **Marek (Analyst):** 42 lata, analizuje dziesiątki spółek dziennie, potrzebuje automatyzacji

---

## 4. Core Features & Requirements

### 4.1 Stock Scanning Engine (MVP)
**Priority:** P0 (Must Have)

**User Story:**
_"Jako inwestor chcę automatycznie skanować akcje według zdefiniowanych kryteriów, aby znaleźć potencjalne okazje inwestycyjne."_

**Functional Requirements:**
- [ ] Integracja z yfinance do pobierania danych (OHLCV, volume, market cap)
- [ ] Konfigurowalne kryteria skanowania:
  - Volume > threshold (np. 1M)
  - Price change % (dzień, tydzień, miesiąc)
  - RSI (Relative Strength Index)
  - Moving averages (SMA 50/200)
  - Market cap range
- [ ] Endpoint `POST /api/scan` przyjmujący JSON z kryteriami
- [ ] Zwraca listę symboli spełniających kryteria + podstawowe metryki
- [ ] Rate limiting (max 10 req/min)

**Technical Requirements:**
- FastAPI backend
- SQLAlchemy do persystencji wyników
- Celery + Redis do asynchronicznych skanów
- Cache (Redis) na 15 min dla danych rynkowych

**Acceptance Criteria:**
- Skan 100 akcji trwa < 60s
- Accuracy 95%+ (porównanie z ręcznym screeningiem)
- API response time < 2s

---

### 4.2 Portfolio Management
**Priority:** P0 (Must Have)

**User Story:**
_"Jako użytkownik chcę zapisywać ciekawe akcje do portfolio kandydatów, aby śledzić ich rozwój w czasie."_

**Functional Requirements:**
- [ ] CRUD dla portfolio:
  - `POST /api/portfolio` – dodaj pozycję (symbol, notes, entry price)
  - `GET /api/portfolio` – lista pozycji
  - `PUT /api/portfolio/{id}` – edytuj notatkę
  - `DELETE /api/portfolio/{id}` – usuń pozycję
- [ ] Automatyczne odświeżanie cen (daily via Celery beat)
- [ ] Tracking P&L (profit/loss) dla każdej pozycji

**Technical Requirements:**
- PostgreSQL do przechowywania portfolio
- Authentication (JWT tokens)
- User-specific data isolation

**Acceptance Criteria:**
- User może dodać/usunąć/edytować pozycje
- Ceny aktualizują się codziennie o 8:00 UTC
- P&L kalkulacja z accuracy 100%

---

### 4.3 Dashboard UI
**Priority:** P0 (Must Have)

**User Story:**
_"Jako użytkownik chcę mieć dashboard z listą kandydatów i wykresami, aby szybko ocenić sytuację rynkową."_

**Functional Requirements:**
- [ ] Widok główny:
  - Tabela kandydatów (symbol, price, change %, volume)
  - Sortowanie/filtrowanie
  - Pagination (50 per page)
- [ ] Wykresy:
  - Candlestick chart dla wybranej akcji (7-90 dni)
  - Volume bars
  - Moving averages overlay
- [ ] Formularz dodawania do portfolio
- [ ] Responsive design (mobile-friendly)

**Technical Requirements:**
- Next.js 14 (App Router)
- Recharts lub Chart.js dla wykresów
- Tailwind CSS + shadcn/ui components
- React Query do cache'owania

**Acceptance Criteria:**
- Dashboard ładuje się < 3s
- Wykresy responsywne (działa na mobile 375px+)
- Lighthouse score > 85

---

### 4.4 Automated Notifications (n8n)
**Priority:** P1 (Should Have)

**User Story:**
_"Jako użytkownik chcę otrzymywać powiadomienia email/Slack, gdy skan znajdzie nowe okazje."_

**Functional Requirements:**
- [ ] Webhook w FastAPI (`POST /api/webhooks/scan-complete`)
- [ ] n8n workflow:
  - Trigger: Webhook od FastAPI
  - Filter: Tylko nowe kandydaty (nie w portfolio)
  - Send email via SendGrid/SMTP
  - Slack message (optional)
- [ ] Configurable w UI (włącz/wyłącz notyfikacje)

**Technical Requirements:**
- n8n self-hosted (Docker) lub cloud
- Environment vars dla SMTP/Slack credentials
- Rate limiting (max 1 email/godzinę)

**Acceptance Criteria:**
- Email dostarczany < 5 min od znalezienia
- 0 false positives (tylko nowe kandydaty)

---

### 4.5 Background Jobs
**Priority:** P0 (Must Have)

**User Story:**
_"Jako system chcę automatycznie skanować rynek codziennie i aktualizować dane."_

**Functional Requirements:**
- [ ] Celery Beat scheduler:
  - Daily scan o 9:00 UTC (po otwarciu US markets)
  - Portfolio price refresh o 8:00 UTC
  - Cleanup starych scanów (>30 dni) o 2:00 UTC
- [ ] Monitoring (Flower dashboard)

**Technical Requirements:**
- Celery + Redis broker
- PostgreSQL jako result backend
- Docker Compose dla local dev
- Sentry do error tracking

**Acceptance Criteria:**
- Jobs działają zgodnie z schedule (99.9% uptime)
- Retry logic (3 próby przy failure)
- Alerting przy krytycznych błędach

---

### 4.6 User Authentication
**Priority:** P1 (Should Have)

**User Story:**
_"Jako użytkownik chcę mieć prywatne portfolio zabezpieczone hasłem."_

**Functional Requirements:**
- [ ] Rejestracja/login (email + password)
- [ ] JWT tokens (access + refresh)
- [ ] Password reset via email
- [ ] OAuth2 (Google/GitHub) – opcjonalnie P2

**Technical Requirements:**
- FastAPI Users library
- bcrypt do hashowania haseł
- Redis do session management

**Acceptance Criteria:**
- OWASP compliance (password strength, rate limiting)
- Token expiry: 1h (access), 7d (refresh)

---

### 4.7 Advanced Filtering (Post-MVP)
**Priority:** P2 (Nice to Have)

**Functional Requirements:**
- [ ] Custom indicator formulas (user-defined)
- [ ] Backtesting engine (simulate strategy)
- [ ] Sector/industry filters
- [ ] Fundamental ratios (P/E, P/B, debt/equity)

---

## 5. Technical Architecture

### 5.1 Stack Overview

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15
- SQLAlchemy ORM
- Celery + Redis
- yfinance for market data

**Frontend:**
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS + shadcn/ui
- Recharts

**Infrastructure:**
- Docker + Docker Compose
- Railway.app or Render (hosting)
- n8n (workflows)
- GitHub Actions (CI/CD)

### 5.2 UI/UX & Accessibility Guidelines

**⚠️ OBOWIĄZKOWE: Wszystkie strony MUSZĄ spełniać WCAG 2.1 Level AA**

#### 5.2.1 Color Contrast Requirements

**Minimum Ratios (WCAG 2.1 AA):**
- Normal text (< 18px): **4.5:1**
- Large text (≥ 18px or ≥ 14px bold): **3:1**
- UI Components (borders, icons): **3:1**

#### 5.2.2 Approved Color Palette (Tailwind Classes)

**✅ WCAG-Compliant Colors:**

| Element | Tailwind Class | Hex Color | Contrast Ratio (white bg) | Usage |
|---------|---------------|-----------|---------------------------|-------|
| **Primary Headings** | `text-gray-900` | `#111827` | **21:1** ✓ | h1, h2, main titles |
| **Body Text** | `text-gray-800` | `#1F2937` | **12:1** ✓ | Paragraphs, descriptions |
| **Secondary Text** | `text-gray-700` | `#374151` | **7:1** ✓ | Labels, captions |
| **Disabled/Muted** | `text-gray-600` | `#4B5563` | **4.6:1** ✓ | Disabled states |
| **Placeholders** | `text-gray-500` | `#6B7280` | **4.5:1** ✓ | Input placeholders |
| **Primary Links** | `text-blue-700` | `#1D4ED8` | **7.7:1** ✓ | Clickable links |
| **Link Hover** | `text-blue-900` | `#1E3A8A` | **12.6:1** ✓ | Link hover state |
| **Success** | `text-green-700` | `#15803D` | **4.7:1** ✓ | Success messages |
| **Error** | `text-red-700` | `#B91C1C` | **5.9:1** ✓ | Error messages |
| **Warning** | `text-yellow-700` | `#A16207` | **4.7:1** ✓ | Warnings |

**❌ FORBIDDEN Colors (Poor Contrast):**
- `text-gray-400`, `text-gray-300`, `text-gray-200` - **NEVER USE for text**
- `text-blue-400`, `text-green-400` - **NEVER USE on white background**

#### 5.2.3 Typography Standards

**Font Sizes & Weights:**
```css
/* Headings - always text-gray-900 */
h1: text-4xl font-bold text-gray-900    /* 36px */
h2: text-3xl font-bold text-gray-900    /* 30px */
h3: text-2xl font-bold text-gray-900    /* 24px */
h4: text-xl font-bold text-gray-900     /* 20px */

/* Body Text - text-gray-800 */
p: text-base text-gray-800              /* 16px */
small: text-sm text-gray-700            /* 14px */

/* Labels - text-gray-900 font-bold */
label: text-sm font-bold text-gray-900  /* 14px bold */

/* Links - text-blue-700 hover:text-blue-900 */
a: text-blue-700 hover:text-blue-900 underline
```

#### 5.2.4 Form Elements Standards

**Input Fields:**
```tsx
<input
  className="border-2 border-gray-400 bg-white text-gray-900
             placeholder-gray-500 focus:border-blue-500 focus:outline-none
             px-3 py-2 rounded"
  placeholder="Enter value"
/>
```

**Buttons:**
```tsx
/* Primary */
<button className="bg-blue-600 text-white font-semibold hover:bg-blue-700
                   px-4 py-2 rounded">
  Submit
</button>

/* Danger */
<button className="bg-red-600 text-white font-semibold hover:bg-red-700
                   px-4 py-2 rounded">
  Delete
</button>

/* Secondary */
<button className="border-2 border-gray-400 text-gray-900 font-semibold
                   hover:bg-gray-100 px-4 py-2 rounded">
  Cancel
</button>
```

#### 5.2.5 WCAG Checklist (Every Page)

**Before Deployment:**
- [ ] All text has contrast ≥ 4.5:1 (normal) or ≥ 3:1 (large)
- [ ] All interactive elements (buttons, links) have ≥ 3:1 contrast
- [ ] Focus indicators visible (blue border)
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Alt text for all images/icons
- [ ] Forms have labels with `for` attribute
- [ ] Error messages are descriptive and high-contrast
- [ ] No color-only information (use icons/text too)

**Testing Tools:**
- Chrome DevTools: Lighthouse (Accessibility score ≥ 90)
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- axe DevTools: https://www.deque.com/axe/devtools/

#### 5.2.6 Dark Mode (Future)

**⚠️ Sprint 4+** - Gdy dodajemy dark mode, kontrasty muszą być odwrócone:
- Background: `bg-gray-900`
- Text: `text-gray-100` (ratio ≥ 15:1)
- Secondary: `text-gray-300` (ratio ≥ 9:1)

---

### 5.3 System Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  Next.js (UI)   │─────▶│  FastAPI     │
└─────────────────┘      └──────┬───────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌────────┐
              │PostgreSQL│ │ Redis  │ │ Celery │
              └──────────┘ └────────┘ └────────┘
                                         │
                                         ▼
                                    ┌─────────┐
                                    │  n8n    │
                                    └─────────┘
```

### 5.4 Database Schema (Core Tables)

**users**
- id (PK)
- email (unique)
- hashed_password
- created_at

**portfolio_items**
- id (PK)
- user_id (FK)
- symbol
- entry_price
- quantity
- notes
- added_at

**scan_results**
- id (PK)
- symbol
- scan_date
- criteria_met (JSON)
- price
- volume

---

## 6. Multi-Agent Development Workflow

### 6.1 Agents & Responsibilities

| Agent | Role | Tools | Responsibilities |
|-------|------|-------|------------------|
| **@pm-agent** | Product Manager | read_file, list_files | Feature breakdown, backlog, acceptance |
| **@backend-agent** | Backend Developer | read_file, write_file, run_terminal, git | FastAPI, SQLAlchemy, Celery, integrations |
| **@frontend-agent** | Frontend Developer | read_file, write_file, run_terminal | Next.js, UI components, charts |
| **@qa-agent** | QA Engineer | read_file, run_terminal, list_files | Pytest, integration tests, bug reports |
| **@devops-agent** | DevOps Engineer | read_file, write_file, run_terminal, git | Docker, n8n, deployment, CI/CD |

### 6.2 Development Phases

**Phase 1: Foundation (Week 1-2)**
- @pm-agent: Rozbij PRD na epic/tasks
- @backend-agent: Setup FastAPI, PostgreSQL, modele danych
- @frontend-agent: Next.js scaffold, routing, basic layout
- @devops-agent: Docker Compose, environment config

**Phase 2: Core Features (Week 3-5)**
- @backend-agent: Scan engine, portfolio CRUD, Celery jobs
- @frontend-agent: Dashboard, wykresy, formularze
- @qa-agent: Unit tests (coverage >80%)

**Phase 3: Integration (Week 6)**
- @backend-agent: n8n webhook integration
- @frontend-agent: Auth UI (login/register)
- @qa-agent: Integration tests, E2E (Playwright)

**Phase 4: Deployment (Week 7)**
- @devops-agent: Railway setup, CI/CD pipelines
- @qa-agent: Performance testing, security audit
- @pm-agent: User acceptance testing

### 6.3 Communication Protocol

**Daily Standup (async):**
- @pm-agent posts:
  - What's in progress
  - Blockers
  - Today's priorities

**Task Assignment:**
```
@pm-agent → @backend-agent: "Implement /api/scan endpoint"
@backend-agent → @qa-agent: "Ready for testing: /api/scan"
@qa-agent → @pm-agent: "Bug found: timeout on 500+ symbols"
@pm-agent → @backend-agent: "Fix timeout bug (P0)"
```

**Definition of Done:**
- Code reviewed
- Tests passing (unit + integration)
- Deployed to staging
- @pm-agent approval

---

## 7. Success Metrics

**Product Metrics:**
- MAU (Monthly Active Users): 100+ by Month 3
- Scan accuracy: >95%
- User retention: >60% (Month 2)
- Avg scans per user/day: 3+

**Technical Metrics:**
- API uptime: 99.5%
- P95 response time: <2s
- Test coverage: >80%
- Zero critical security vulnerabilities

---

## 8. Release Plan

**v0.1 (MVP) – Target: Week 7**
- Stock scanning engine
- Portfolio management
- Basic dashboard
- Manual scans only

**v0.2 – Target: Week 10**
- Automated daily scans
- Email notifications (n8n)
- User authentication

**v0.3 – Target: Week 14**
- Advanced filters (RSI, MA)
- Backtesting (basic)
- Mobile optimization

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| yfinance rate limits | High | Implement caching, fallback to Finnhub |
| Celery job failures | Medium | Retry logic, Sentry monitoring |
| Scalability (1000+ users) | Medium | Start with Railway Pro, plan migration to AWS |
| Data accuracy | High | Validate against 2+ sources, manual audits |

---

## 10. Open Questions

- [ ] Czy monetyzować (free tier + paid)?
- [ ] Jakie kryteria domyślne dla scanów?
- [ ] Maksymalna liczba pozycji w portfolio (limit na free tier)?
- [ ] Czy dodać crypto markets w przyszłości?

---

## 11. Appendix

**References:**
- yfinance docs: https://github.com/ranaroussi/yfinance
- FastAPI best practices: https://fastapi.tiangolo.com/
- n8n docs: https://docs.n8n.io/

**Glossary:**
- **Multibagger:** Akcja, która zwraca 2x+ inwestycji
- **RSI:** Relative Strength Index (momentum indicator)
- **OHLCV:** Open, High, Low, Close, Volume

---

## Changelog

- **2025-10-07:** Initial draft (v1.0)
