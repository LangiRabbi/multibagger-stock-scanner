# Dockerfile dla backendu FastAPI
FROM python:3.11-slim

# Ustaw working directory w kontenerze
WORKDIR /app

# Skopiuj requirements.txt
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod aplikacji
COPY . .

# Expose port 8000
EXPOSE 8000

# Komenda uruchomienia (uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
