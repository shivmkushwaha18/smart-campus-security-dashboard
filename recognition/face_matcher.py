"""
Loads saved encodings and provides a function to match a live face
encoding against known students.
"""

import os
import pickle
import face_recognition

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def load_known_faces():
    if not os.path.exists(config.ENCODINGS_FILE):
        print("[WARN] No encodings file found. Run register_faces.py first.")
        return {"encodings": [], "names": []}

    with open(config.ENCODINGS_FILE, "rb") as f:
        return pickle.load(f)


def match_face(face_encoding, known_data):
    """
    Compares a single face encoding against all known encodings.
    Returns (name, is_match) - name is "Unknown" if no match found.
    """
    if len(known_data["encodings"]) == 0:
        return "Unknown", False

    matches = face_recognition.compare_faces(
        known_data["encodings"], face_encoding, tolerance=config.MATCH_TOLERANCE
    )
    face_distances = face_recognition.face_distance(
        known_data["encodings"], face_encoding
    )

    if len(face_distances) == 0:
        return "Unknown", False

    best_match_index = face_distances.argmin()

    if matches[best_match_index]:
        return known_data["names"][best_match_index], True

    return "Unknown", False
