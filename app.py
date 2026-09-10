"""
Smart Campus Security — Dashboard (Deployable / Portfolio Version)

This is a standalone version of the dashboard, decoupled from the local
webcam recognition module (which needs a physical camera and can't run
on a cloud server). It's meant to be hosted online so anyone can view it
via a link — for your resume, portfolio, or project writeup.

Since there's no real webcam here, it starts with realistic seeded demo
data, and visitors can click "Simulate Entry" to see the dashboard
update live, exactly like it would during your actual event demo.

Run locally:
    python app.py
Deploy:
    See README.md for Render/Railway steps.
"""

import os
import csv
import random
import threading
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "entry_log.csv")
REFRESH_MS = 4000

DEMO_NAMES = ["Shivam", "Priya Verma", "Rohan Sharma", "Ananya Iyer", "Karan Mehta"]
UNKNOWN_LABEL = "Unknown"

_lock = threading.Lock()


def seed_demo_data():
    """Creates a believable entry log with a mix of granted/denied events
    spread over the last hour, so the dashboard never looks empty."""
    if os.path.exists(LOG_FILE):
        return

    rows = [["timestamp", "name", "status"]]
    now = datetime.now()

    for i in range(18):
        minutes_ago = random.randint(1, 58)
        ts = (now - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%d %H:%M:%S")
        is_granted = random.random() < 0.72
        name = random.choice(DEMO_NAMES) if is_granted else UNKNOWN_LABEL
        status = "GRANTED" if is_granted else "DENIED"
        rows.append([ts, name, status])

    # sort by timestamp ascending for a sensible log order
    rows[1:] = sorted(rows[1:], key=lambda r: r[0])

    with open(LOG_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)


def read_all_events():
    if not os.path.exists(LOG_FILE):
        seed_demo_data()
    events = []
    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append(row)
    events.reverse()
    return events


def append_event(name, status):
    with _lock:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, status])


@app.route("/")
def index():
    return render_template("index.html", refresh_ms=REFRESH_MS, demo_mode=True)


@app.route("/api/events")
def api_events():
    events = read_all_events()
    total = len(events)
    granted = sum(1 for e in events if e["status"] == "GRANTED")
    denied = sum(1 for e in events if e["status"] == "DENIED")

    return jsonify({
        "total": total,
        "granted": granted,
        "denied": denied,
        "recent": events[:15],
    })


@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Lets a visitor on the deployed link trigger a fake scan event,
    so they can see the dashboard update live without a real camera."""
    is_granted = random.random() < 0.7
    name = random.choice(DEMO_NAMES) if is_granted else UNKNOWN_LABEL
    status = "GRANTED" if is_granted else "DENIED"
    append_event(name, status)
    return jsonify({"ok": True, "name": name, "status": status})


seed_demo_data()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
