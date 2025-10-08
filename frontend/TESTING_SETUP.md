# Frontend Testing Setup (Next.js 15)

**Status:** 🟡 Przygotowane - wymaga konfiguracji

Frontend tests NIE zostały uruchomione w ramach tego QA sprint, ponieważ Next.js 15 wymaga specjalnej konfiguracji Jest. Poniżej instrukcja setupu.

---

## 📦 Instalacja Zależności

```bash
cd frontend
npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

---

## ⚙️ Konfiguracja

### 1. Stwórz `jest.config.js`

```javascript
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  testMatch: [
    '**/__tests__/**/*.test.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],
}

module.exports = createJestConfig(customJestConfig)
```

---

### 2. Stwórz `jest.setup.js`

```javascript
import '@testing-library/jest-dom'
```

---

### 3. Dodaj do `package.json`

```json
"scripts": {
  "test": "jest",
  "test:watch": "jest --watch",
  "test:coverage": "jest --coverage"
}
```

---

## 📁 Struktura Testów (Przygotowane)

```
frontend/
├── __tests__/
│   ├── components/
│   │   ├── Navbar.test.tsx       (DO STWORZENIA)
│   │   └── ErrorBoundary.test.tsx (DO STWORZENIA)
│   └── app/
│       ├── scan.test.tsx          (DO STWORZENIA)
│       └── portfolio.test.tsx     (DO STWORZENIA)
```

---

## 🧪 Przykładowy Test

**`__tests__/components/Navbar.test.tsx`:**

```typescript
import { render, screen } from '@testing-library/react'
import { Navbar } from '@/components/Navbar'

describe('Navbar Component', () => {
  it('renderuje logo', () => {
    render(<Navbar />)
    const logo = screen.getByText(/Multibagger/i)
    expect(logo).toBeInTheDocument()
  })

  it('renderuje wszystkie linki nawigacyjne', () => {
    render(<Navbar />)
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Scan')).toBeInTheDocument()
    expect(screen.getByText('Portfolio')).toBeInTheDocument()
  })
})
```

---

## 🚀 Uruchomienie Testów

```bash
npm test
```

---

## 📊 Expected Coverage

**Target:** Min 50% coverage dla komponentów

**Priority:**
1. Navbar.tsx
2. ErrorBoundary component (scan/page.tsx)
3. Scan page form
4. Portfolio table

---

## ⚠️ Known Issues (Next.js 15)

1. **Server Components:** Next.js 15 używa Server Components by default - wymaga `'use client'` directive w testowanych komponentach
2. **App Router:** Testy z Next.js App Router wymagają specjalnej konfiguracji mocków
3. **Turbopack:** Może konfliktować z Jest - użyj `--turbopack=false` podczas testów

---

**Przygotowane przez:** QA Agent
**Data:** 2025-10-08
