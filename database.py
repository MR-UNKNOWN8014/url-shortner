import sqlite3

DB_PATH = "urls.db"

# INIT - creates the table if it doesn't exist
# Called once when the app starts
def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                short_code  TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                click_count  INTEGER DEFAULT 0
            )
        """)
    conn.commit()
    conn.close()

# Save a new short code
def save_url(short_code: str, original_url: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url)
    )
    conn.commit()
    conn.close()

# Get the record by short code
def get_url(short_code: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT original_url, click_count FROM urls WHERE short_code = ?",
        (short_code,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "original_url": row[0],
        "click_count": row[1]
    }

# Increment click counter
def increment_clicks(short_code: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
        (short_code,)
    )
    conn.commit()
    conn.close()

def get_all_urls() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT short_code, original_url, click_count FROM urls"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"short_code": r[0], "original_url": r[1], "click_count": r[2]}
        for r in rows
    ]