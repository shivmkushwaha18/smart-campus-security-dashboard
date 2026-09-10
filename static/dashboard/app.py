"""
Flask dashboard for Smart Campus Security.

Run separately from main.py:
    python dashboard/app.py

Then open http://localhost:5000 in a browser.
It reads the same entry_log.csv that main.py writes to,
so run both at the same time during your demo.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.logger import read_all_events

from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", refresh_ms=config.DASHBOARD_REFRESH_MS)


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
        "recent": events[:15]   # most recent 15 events for the live feed
    })


if __name__ == "__main__":
    app.run(host=config.DASHBOARD_HOST, port=config.DASHBOARD_PORT, debug=True)
