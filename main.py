"""
Smart Campus Security Gate - Main Program
Run this to start the live webcam recognition window.

Controls:
    q -> quit
"""

import os
import time
import cv2
import face_recognition

import config
from recognition.face_matcher import load_known_faces, match_face
from utils.logger import log_event

# Optional sound support (falls back silently if playsound isn't installed)
try:
    from playsound import playsound
    import threading
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


def play_sound_async(path):
    if SOUND_AVAILABLE and config.ENABLE_SOUND and os.path.exists(path):
        threading.Thread(target=playsound, args=(path,), daemon=True).start()


def main():
    print("Loading known faces...")
    known_data = load_known_faces()
    print(f"Loaded {len(known_data['names'])} known face(s): {known_data['names']}")

    video_capture = cv2.VideoCapture(config.CAMERA_INDEX)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not video_capture.isOpened():
        print("[ERROR] Could not open webcam. Check config.CAMERA_INDEX.")
        return

    # Tracks last-logged time per name to avoid spamming the log every frame
    last_logged = {}

    print("Starting recognition loop. Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to grab frame from webcam.")
            break

        # Resize for faster processing, then scale results back up
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back up face locations
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2

            name, is_match = match_face(face_encoding, known_data)
            status = "GRANTED" if is_match else "DENIED"
            box_color = (0, 200, 0) if is_match else (0, 0, 220)  # BGR: green / red
            label = f"ACCESS GRANTED - {name}" if is_match else "ACCESS DENIED - Unregistered"

            # Draw bounding box + label
            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 8),
                        cv2.FONT_HERSHEY_DUPLEX, 0.55, (255, 255, 255), 1)

            # Log with cooldown so the same person isn't logged every frame
            now = time.time()
            key = name if is_match else f"unknown_{left}_{top}"
            last_time = last_logged.get(key, 0)

            if now - last_time > config.SAME_PERSON_COOLDOWN_SECONDS:
                log_event(name, status)
                last_logged[key] = now
                if is_match:
                    play_sound_async(config.SOUND_GRANTED)
                else:
                    play_sound_async(config.SOUND_DENIED)

        # Header banner
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (40, 40, 40), cv2.FILLED)
        cv2.putText(frame, "SMART CAMPUS SECURITY - LIVE", (10, 27),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        cv2.imshow("Smart Campus Security", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
