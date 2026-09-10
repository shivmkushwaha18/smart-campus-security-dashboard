# Smart Campus Security — Webcam Face Recognition + Live Dashboard

A webcam-based access control demo: known students get "ACCESS GRANTED",
unregistered visitors get "ACCESS DENIED", and everything is logged live
to a browser dashboard with stats and a real-time entry feed.

## 1. Setup (do this first, before event day)

```bash
# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

**Note on `face_recognition`:** it depends on `dlib`, which can be tricky to
install on Windows. If `pip install face_recognition` fails:
- Windows: install via `pip install cmake` first, then
  `pip install dlib` (may need Visual Studio Build Tools), then
  `pip install face_recognition`. Alternatively, use `conda install -c conda-forge dlib`.
- Mac/Linux: usually installs cleanly with pip directly.

Do this step at least a day before your event — dlib installation issues
are the #1 time-sink for this kind of project.

## 2. Register faces

1. Add clear, front-facing photos of your team/volunteers to:
   `data/known_faces/`
   Name each file after the person, e.g. `Rohan_Sharma.jpg`
2. Run:
   ```bash
   python recognition/register_faces.py
   ```
   This creates `data/encodings.pkl`. Re-run this any time you add new photos.

## 3. Run the demo (two windows, side by side)

**Window 1 — webcam recognition:**
```bash
python main.py
```
Press `q` to quit.

**Window 2 — live dashboard (open in browser):**
```bash
python dashboard/app.py
```
Then open **http://localhost:5000** in your browser.

Run both at the same time. `main.py` writes to `data/entry_log.csv`,
and the dashboard reads from the same file every few seconds, so both
update live as people walk up to the camera.

## 4. Booth demo tips

- Register 2-3 teammates beforehand so you can show "ACCESS GRANTED" reliably.
- Let random visitors try too — they'll get "ACCESS DENIED", which is
  actually a good demo moment (shows the system correctly rejects unknown faces).
- Keep lighting even on faces — backlit/dim booths hurt recognition accuracy.
- If you want zero risk of accuracy issues on stage, pre-register a few
  "surprise" visitor volunteers 10 minutes before your slot.

## 5. Optional extensions (mention as future scope if short on time)

- Physical gate arm via a servo + Arduino/Raspberry Pi Pico, triggered
  over serial when `main.py` grants access.
- SMS/email alert to admin on repeated "DENIED" attempts (Twilio API).
- Emotion detection layer for a "mood check" feature at entry.
- Switch `entry_log.csv` to SQLite for larger-scale/production use.

## File structure

```
smart-campus-security/
├── main.py                    # Webcam recognition loop
├── config.py                  # All settings
├── recognition/
│   ├── face_encoder.py        # Builds encodings from known_faces/
│   ├── face_matcher.py        # Matches live face to known encodings
│   └── register_faces.py      # Run this to (re)build encodings
├── data/
│   ├── known_faces/           # Put student/team photos here
│   ├── encodings.pkl          # Auto-generated
│   └── entry_log.csv          # Auto-generated scan log
├── dashboard/
│   ├── app.py                 # Flask server
│   ├── templates/index.html
│   └── static/style.css, script.js
├── sounds/                    # access_granted.mp3 / access_denied.mp3 (optional)
├── utils/logger.py            # Writes/reads entry_log.csv
└── requirements.txt
```
