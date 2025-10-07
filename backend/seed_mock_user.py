"""
Skrypt do utworzenia mock użytkownika (user_id=1)
Potrzebny dla Portfolio API w Sprint 2 (przed dodaniem autentykacji)
"""
import sys
from sqlalchemy import text
from app.database import engine

def create_mock_user():
    """Tworzy mock użytkownika o ID=1"""
    print("Tworzenie mock użytkownika...")

    with engine.connect() as conn:
        # Sprawdź czy użytkownik już istnieje
        result = conn.execute(text("SELECT COUNT(*) FROM users WHERE id = 1"))
        count = result.scalar()

        if count > 0:
            print("✅ Mock użytkownik już istnieje (user_id=1)")
            # Wyświetl dane użytkownika
            result = conn.execute(text("SELECT id, email, created_at FROM users WHERE id = 1"))
            user = result.fetchone()
            print(f"   ID: {user[0]}, Email: {user[1]}, Created: {user[2]}")
            return

        # Utwórz mock użytkownika
        conn.execute(
            text("""
                INSERT INTO users (email, hashed_password, created_at)
                VALUES ('test@example.com', 'hashed_password_mock', NOW())
            """)
        )
        conn.commit()

        print("✅ SUKCES! Mock użytkownik utworzony:")

        # Wyświetl utworzonego użytkownika
        result = conn.execute(text("SELECT id, email, created_at FROM users"))
        user = result.fetchone()
        print(f"   ID: {user[0]}, Email: {user[1]}, Created: {user[2]}")
        print("")
        print("Teraz możesz dodawać akcje do portfolio przez API /api/portfolio")

if __name__ == "__main__":
    try:
        create_mock_user()
    except Exception as e:
        print(f"❌ BŁĄD: {e}")
        sys.exit(1)
