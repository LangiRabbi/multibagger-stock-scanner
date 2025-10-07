"""
Skrypt do tworzenia tabel w bazie danych.
Uruchom: python create_tables.py
"""
from app.database import Base, engine
from app.models import User, PortfolioItem, ScanResult

print("Tworzenie tabel w bazie danych...")

# Importuj wszystkie modele (zeby SQLAlchemy je zobaczyl)
print(f"Znalezione modele: {Base.metadata.tables.keys()}")

# Stworz wszystkie tabele
Base.metadata.create_all(bind=engine)

print("SUKCES! Tabele utworzone pomyslnie!")
print(f"Lista tabel: {list(Base.metadata.tables.keys())}")
