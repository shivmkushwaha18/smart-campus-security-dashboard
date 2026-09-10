"""
Handles writing every recognition event to entry_log.csv,
which the dashboard reads to display live stats.
"""

import os
import csv
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

CSV_HEADERS = ["timestamp", "name", "status"]


def init_log_file():
    """Creates the CSV with headers if it doesn't exist yet."""
    if not os.path.exists(config.ENTRY_LOG_FILE):
        os.makedirs(os.path.dirname(config.ENTRY_LOG_FILE), exist_ok=True)
        with open(config.ENTRY_LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def log_event(name, status):
    """
    status: "GRANTED" or "DENIED"
    """
    init_log_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(config.ENTRY_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, status])


def read_all_events():
    """Returns list of dicts, most recent first. Used by dashboard."""
    init_log_file()
    events = []
    with open(config.ENTRY_LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append(row)
    events.reverse()
    return events
