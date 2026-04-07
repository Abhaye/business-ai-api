from fastapi import FastAPI
from datetime import datetime
import json
import os

app = FastAPI()

# File to store updates
DATA_FILE = "updates.json"

# Load existing updates if the file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            updates = json.load(f)
        except json.JSONDecodeError:
            updates = []
else:
    updates = []

# Save updates to file
def save_updates():
    with open(DATA_FILE, "w") as f:
        json.dump(updates, f, indent=2)

@app.post("/update")
def receive_update(update: dict):
    update["received_at"] = datetime.utcnow().isoformat()
    updates.append(update)
    save_updates()
    return {"status": "received", "total_updates": len(updates)}

@app.get("/updates")
def get_updates():
    return updates