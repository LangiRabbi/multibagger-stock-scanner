# 📝 STANDARDS - GIT, WCAG, CODE STYLE

## GIT COMMITS (CONVENTIONAL)

### Format
```
<type>(<scope>): <subject>

<body> (opcjonalnie)
```

### Types
- `feat` - Nowa funkcjonalność
- `fix` - Naprawa buga
- `test` - Testy
- `docs` - Dokumentacja
- `refactor` - Refactoring (bez zmian funkcjonalnych)
- `perf` - Optymalizacja
- `chore` - Build, dependencies

### Scopes
- `backend` - Backend API
- `frontend` - Frontend UI
- `db` - Database
- `docker` - Infrastructure
- `deps` - Dependencies

### Przykłady
```bash
✅ DOBRE
git commit -m "feat(backend): Add field_validator for symbols validation"
git commit -m "fix(frontend): Fix portfolio delete button contrast (WCAG)"
git commit -m "test(backend): Add pytest for /api/scan validation"

❌ ZŁE
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "changes"
```

### Pre-commit checklist
- [ ] Testy przechodzą (`pytest` / `npm test`)
- [ ] Coverage ≥ 50%
- [ ] Type hints (Python)
- [ ] WCAG compliance (frontend)
- [ ] Komentarze PO POLSKU

---

## WCAG 2.1 AA (OBOWIĄZKOWE)

### Minimum Ratios
- Normal text (<18px): **4.5:1**
- Large text (≥18px): **3:1**
- UI components: **3:1**

### Approved Tailwind Colors

| Element | Class | Hex | Ratio | Usage |
|---------|-------|-----|-------|-------|
| **Headings** | `text-gray-900` | #111827 | 21:1 | h1-h4 |
| **Body** | `text-gray-800` | #1F2937 | 12:1 | Paragraphs |
| **Secondary** | `text-gray-700` | #374151 | 7:1 | Labels |
| **Links** | `text-blue-700` | #1D4ED8 | 7.7:1 | Links |
| **Link Hover** | `text-blue-900` | #1E3A8A | 12.6:1 | Hover |
| **Success** | `text-green-700` | #15803D | 4.7:1 | Success |
| **Error** | `text-red-700` | #B91C1C | 5.9:1 | Errors |

### ❌ FORBIDDEN (Poor Contrast)
- `text-gray-400` - 2.8:1 (FAIL)
- `text-gray-300` - 1.9:1 (FAIL)
- `text-blue-400` - 3.2:1 (FAIL na small text)

### Typography
```css
/* Headings */
h1: text-4xl font-bold text-gray-900
h2: text-3xl font-bold text-gray-900
h3: text-2xl font-bold text-gray-900

/* Body */
p: text-base text-gray-800
small: text-sm text-gray-700

/* Labels */
label: text-sm font-bold text-gray-900

/* Links */
a: text-blue-700 hover:text-blue-900 underline
```

### Form Elements
```tsx
// Input
<input
  className="border-2 border-gray-400 bg-white text-gray-900
             placeholder-gray-500 focus:border-blue-500"
  placeholder="Enter value"
/>

// Button Primary
<button className="bg-blue-600 text-white font-semibold
                   hover:bg-blue-700 px-4 py-2 rounded">
  Submit
</button>

// Button Danger
<button className="bg-red-600 text-white font-semibold
                   hover:bg-red-700 px-4 py-2 rounded">
  Delete
</button>
```

### WCAG Checklist
- [ ] Kontrast ≥ 4.5:1 (normal) lub ≥ 3:1 (large)
- [ ] Focus indicators widoczne (blue border)
- [ ] Keyboard navigation (Tab, Enter, Space)
- [ ] Alt text dla obrazów/ikon
- [ ] Labels z `for` attribute
- [ ] Error messages high-contrast
- [ ] Lighthouse Accessibility ≥ 90

### Testing Tools
- Chrome DevTools → Lighthouse
- WebAIM Contrast Checker
- axe DevTools

---

## PYTHON CODE STYLE

### Type Hints (OBOWIĄZKOWE)
```python
# ✅ ZAWSZE
from typing import List, Dict, Optional

async def get_metrics(symbol: str) -> Dict[str, float]:
    """Pobiera metryki z Finnhub API.
    
    Args:
        symbol: Ticker akcji (np. "AAPL")
    
    Returns:
        Dict z metrykami (ROE, ROCE, FCF Yield, etc.)
        
    Raises:
        HTTPException: Jeśli symbol nie istnieje
    """
    pass

# ❌ NIGDY
def get_metrics(symbol):  # Brak typów!
    pass
```

### Docstrings (PO POLSKU)
```python
# ✅ ZAWSZE
def calculate_score(roe: float, roce: float) -> int:
    """Oblicza scoring dla wskaźników rentowności.
    
    Scoring:
    - ROE >20%: 15 pkt
    - ROCE >15%: 10 pkt
    
    Args:
        roe: Return on Equity (%)
        roce: Return on Capital Employed (%)
    
    Returns:
        Punkty 0-25
    """
    pass

# ❌ ZŁE (po angielsku)
def calculate_score(roe: float, roce: float) -> int:
    """Calculates scoring for profitability metrics."""
    pass
```

### Async/Await
```python
# ✅ Dla I/O operations
async def fetch_stock_data(symbol: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/{symbol}")
        return response.json()

# ❌ Synchroniczny I/O (WOLNE!)
def fetch_stock_data(symbol: str) -> dict:
    response = requests.get(f"/api/{symbol}")  # Blocking!
    return response.json()
```

### Error Handling
```python
# ✅ HTTPException z detail
from fastapi import HTTPException

try:
    data = StockScanner.scan_stocks(symbols)
except ValueError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(422, detail=f"Invalid input: {e}")
except Exception as e:
    logger.error(f"Scan failed: {e}")
    raise HTTPException(500, detail="Unable to process scan")

# ❌ Generyczny except bez message
try:
    data = StockScanner.scan_stocks(symbols)
except:
    raise HTTPException(500)  # Brak info dla usera!
```

---

## REACT/NEXT.JS CODE STYLE

### TypeScript (STRICT)
```tsx
// ✅ Interfaces
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  label, 
  onClick, 
  disabled = false 
}) => {
  return (
    <button 
      className="bg-blue-600 text-white px-4 py-2 rounded"
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

// ❌ Brak typów
export const Button = (props) => {  // Any!
  return <button onClick={props.onClick}>{props.label}</button>;
};
```

### WCAG Compliance
```tsx
// ✅ Proper contrast + aria
<button 
  className="bg-blue-600 text-white font-semibold 
             hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
  aria-label="Submit form"
>
  Submit
</button>

// ❌ Słaby kontrast + brak aria
<button className="text-gray-400">
  Submit
</button>
```

### Error Boundaries
```tsx
// ✅ Każda strona z ErrorBoundary
export default function ScanPage() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <ScanForm />
    </ErrorBoundary>
  );
}
```

### React Query (Cache)
```tsx
// ✅ Cache dla API calls
const { data, isLoading } = useQuery({
  queryKey: ['portfolio'],
  queryFn: fetchPortfolio,
  staleTime: 5 * 60 * 1000,  // 5 min
});

// ❌ Fetch w useEffect (NO CACHE!)
useEffect(() => {
  fetch('/api/portfolio').then(r => r.json()).then(setData);
}, []);
```

---

## TESTING STANDARDS

### Backend (Pytest)
```python
# ✅ Mocki zamiast API calls
@pytest.fixture
def mock_finnhub(mocker):
    mock = mocker.patch("app.services.scanner.FinnhubClient")
    mock.return_value.get_metrics.return_value = {
        "roeTTM": 25.5,
        "peTTM": 12.3
    }
    return mock

def test_scan_stocks(mock_finnhub):
    result = StockScanner.scan_stocks(["AAPL"])
    assert result[0]["score"] > 50

# ❌ Prawdziwe API calls
def test_scan_stocks():
    result = StockScanner.scan_stocks(["AAPL"])  # Slow + flaky!
```

### Frontend (Jest)
```tsx
// ✅ Render + user interaction
import { render, screen, fireEvent } from '@testing-library/react';

test('portfolio delete button works', () => {
  render(<Portfolio />);
  const deleteBtn = screen.getByRole('button', { name: /delete/i });
  fireEvent.click(deleteBtn);
  expect(screen.getByText(/confirm delete/i)).toBeInTheDocument();
});
```

### Coverage Targets
- **Unit tests:** ≥ 50%
- **Integration tests:** ≥ 30%
- **E2E tests:** Critical paths only

---

## SECURITY

### Secrets Management
```python
# ✅ .env file
FINNHUB_API_KEY=abc123
DATABASE_URL=postgresql://...

# ❌ NIGDY w kodzie!
FINNHUB_API_KEY = "abc123"  # SECURITY RISK!
```

### SQL Injection Prevention
```python
# ✅ SQLAlchemy ORM
db.query(Portfolio).filter(Portfolio.id == portfolio_id)

# ❌ Raw SQL
db.execute(f"SELECT * FROM portfolio WHERE id = {portfolio_id}")
```

### CORS
```python
# ✅ Specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.stockscanner.com"],
    allow_credentials=True,
)

# ❌ Wildcard (UNSAFE!)
allow_origins=["*"]
```