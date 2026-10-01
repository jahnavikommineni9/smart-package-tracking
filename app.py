import random
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("packages.db")

SEED_PACKAGES = [
    ("PKG-24001", "Ananya Rao", "Vijayawada", "In Transit", 5.2, 48, 0.3),
    ("PKG-24002", "Rahul Kumar", "Hyderabad", "Picked Up", 22.4, 55, 0.2),
    ("PKG-24003", "Meera Reddy", "Chennai", "In Transit", 8.1, 62, 1.8),
    ("PKG-24004", "Arjun Das", "Bengaluru", "Delivered", 24.0, 45, 0.1),
    ("PKG-24005", "Kavya Nair", "Visakhapatnam", "Exception", 31.5, 71, 2.4),
]

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_id TEXT UNIQUE NOT NULL,
                recipient TEXT NOT NULL,
                destination TEXT NOT NULL,
                status TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                shock REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        if conn.execute("SELECT COUNT(*) FROM packages").fetchone()[0] == 0:
            now = datetime.now().isoformat(timespec="seconds")
            conn.executemany("""
                INSERT INTO packages
                (tracking_id, recipient, destination, status, temperature, humidity, shock, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [(*p, now) for p in SEED_PACKAGES])

def all_packages():
    with connect_db() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM packages ORDER BY tracking_id")]

def alerts(package):
    result = []
    if package["temperature"] < 2 or package["temperature"] > 8:
        result.append("Temperature out of range")
    if package["humidity"] > 70:
        result.append("High humidity")
    if package["shock"] > 1.5:
        result.append("Shock detected")
    return result

@app.get("/")
def dashboard():
    return render_template("index.html")

@app.get("/api/packages")
def api_packages():
    packages = all_packages()
    query = request.args.get("q", "").strip().lower()
    if query:
        packages = [p for p in packages if query in p["tracking_id"].lower()
                    or query in p["recipient"].lower() or query in p["destination"].lower()]
    for package in packages:
        package["alerts"] = alerts(package)
    return jsonify(packages)

@app.get("/api/summary")
def api_summary():
    packages = all_packages()
    return jsonify({
        "total": len(packages),
        "in_transit": sum(p["status"] == "In Transit" for p in packages),
        "delivered": sum(p["status"] == "Delivered" for p in packages),
        "alerts": sum(bool(alerts(p)) for p in packages)
    })

@app.post("/api/simulate")
def simulate():
    """Simulate telemetry from package sensors; use validated device data in production."""
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM packages WHERE status != 'Delivered'").fetchall()
        for p in rows:
            temperature = max(-5, min(45, p["temperature"] + random.uniform(-1.2, 1.2)))
            humidity = max(20, min(100, p["humidity"] + random.uniform(-4, 4)))
            shock = max(0, p["shock"] + random.uniform(-0.3, 0.5)) if random.random() < 0.25 else max(0, p["shock"] - 0.1)
            conn.execute("""
                UPDATE packages SET temperature=?, humidity=?, shock=?, updated_at=? WHERE id=?
            """, (round(temperature, 1), round(humidity, 1), round(shock, 2),
                  datetime.now().isoformat(timespec="seconds"), p["id"]))
    packages = all_packages()
    return jsonify({"message": "Package sensor data updated", "packages": packages})

@app.patch("/api/packages/<tracking_id>/status")
def update_status(tracking_id):
    payload = request.get_json(silent=True) or {}
    allowed = {"Picked Up", "In Transit", "Delivered", "Exception"}
    status = payload.get("status")
    if status not in allowed:
        return jsonify({"error": "Invalid status"}), 400
    with connect_db() as conn:
        cur = conn.execute("UPDATE packages SET status=?, updated_at=? WHERE tracking_id=?",
                           (status, datetime.now().isoformat(timespec="seconds"), tracking_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Package not found"}), 404
    return jsonify({"message": "Status updated", "tracking_id": tracking_id, "status": status})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
