# Multibagger Stock Scanner (FastAPI)

A minimal FastAPI scaffold for a stock scanner service.

## Prerequisites
- Python 3.11+
- Windows PowerShell (this guide uses PowerShell commands)

## Setup
1. Clone or open the project folder.
2. Create and activate a virtual environment:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create a `.env` file (optional) by copying the example:
   ```powershell
   Copy-Item .env.example .env
   ```

## Running the app
Using Uvicorn (recommended during development):
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or directly via Python (also loads `reload`):
```powershell
python .\main.py
```

## Endpoints
- `GET /health` – basic health check
- `POST /scan` – placeholder scan endpoint
  - Body example:
    ```json
    { "symbol": "AAPL" }
    ```

## Configuration
Use `.env` variables to override defaults:
- `PORT` – server port (default: 8000)
- `MIN_VOLUME` – minimum volume threshold for scan (default: 1000000)
- `ALPHA_VANTAGE_API_KEY`, `FINNHUB_API_KEY` – optional keys if you later integrate data providers

## Notes
- This is a starter scaffold. Replace the placeholder logic in `scan_stock` with real screening rules and data fetching.
