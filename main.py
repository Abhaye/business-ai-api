from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Create DB + table
conn = sqlite3.connect("updates.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT
)
""")
conn.commit()

@app.post("/update")
def receive_update(data: dict):
    message = str(data.get("message"))
    cursor.execute("INSERT INTO updates (message) VALUES (?)", (message,))
    conn.commit()
    return {"status": "received"}

@app.get("/updates")
def get_updates():
    cursor.execute("SELECT * FROM updates")
    rows = cursor.fetchall()
    return [{"id": r[0], "message": r[1]} for r in rows]
