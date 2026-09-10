import os
import pickle
import numpy as np
from PIL import Image
import face_recognition

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def load_image_as_rgb(path):
    with Image.open(path) as img:
        rgb_img = img.convert("RGB")
        arr = np.array(rgb_img, dtype=np.uint8)
        arr = np.ascontiguousarray(arr)
        return arr


def build_encodings():
    known_encodings = []
    known_names = []

    if not os.path.exists(config.KNOWN_FACES_DIR):
        os.makedirs(config.KNOWN_FACES_DIR)

    image_files = [
        f for f in os.listdir(config.KNOWN_FACES_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print("[WARN] No images found in data/known_faces/.")

    for filename in image_files:
        path = os.path.join(config.KNOWN_FACES_DIR, filename)
        name = os.path.splitext(filename)[0].replace("_", " ")

        try:
            image = load_image_as_rgb(path)
        except Exception as e:
            print(f"[SKIP] Could not read {filename} ({e}), skipping.")
            continue

        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            print(f"[SKIP] No face detected in {filename}, skipping.")
            continue

        known_encodings.append(encodings[0])
        known_names.append(name)
        print(f"[OK] Encoded {name}")

    data = {"encodings": known_encodings, "names": known_names}
    with open(config.ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print(f"\nSaved {len(known_names)} face encodings to {config.ENCODINGS_FILE}")
    return data


if __name__ == "__main__":
    build_encodings()