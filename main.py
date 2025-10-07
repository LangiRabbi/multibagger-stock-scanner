from fastapi import FastAPI
from pydantic import BaseModel
import os


class ScanRequest(BaseModel):
    symbol: str


app = FastAPI(title="Multibagger Stock Scanner", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan")
def scan_stock(payload: ScanRequest):
    # Placeholder scanning logic; replace with real indicators later
    min_volume = int(os.getenv("MIN_VOLUME", "1000000"))
    return {
        "symbol": payload.symbol,
        "meetsCriteria": True,
        "criteria": {"minVolume": min_volume},
    }


# If running via `python main.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)


