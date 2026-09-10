"""
Run this script whenever you add/update photos in data/known_faces/.

Usage:
    python recognition/register_faces.py

This regenerates data/encodings.pkl so main.py recognizes the new faces.
"""

from face_encoder import build_encodings

if __name__ == "__main__":
    print("Registering faces from data/known_faces/ ...\n")
    build_encodings()
    print("\nDone. You can now run main.py")
