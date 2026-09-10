"""
Central configuration for the Smart Campus Security system.
Edit these values to tune the system without touching core logic.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Camera settings ---
CAMERA_INDEX = 0          # 0 = default laptop webcam. Try 1 if you have an external cam.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# --- Recognition settings ---
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "data", "known_faces")
ENCODINGS_FILE = os.path.join(BASE_DIR, "data", "encodings.pkl")
MATCH_TOLERANCE = 0.5     # Lower = stricter match. 0.5-0.6 is a good demo range.

# --- Logging ---
ENTRY_LOG_FILE = os.path.join(BASE_DIR, "data", "entry_log.csv")

# --- Cooldown ---
# Prevents the same person from being logged repeatedly every frame.
SAME_PERSON_COOLDOWN_SECONDS = 8

# --- Sounds ---
SOUND_GRANTED = os.path.join(BASE_DIR, "sounds", "access_granted.mp3")
SOUND_DENIED = os.path.join(BASE_DIR, "sounds", "access_denied.mp3")
ENABLE_SOUND = True

# --- Dashboard ---
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000
DASHBOARD_REFRESH_MS = 3000   # auto-refresh interval on the dashboard (ms)
