# Smart Campus Security — Dashboard (Deployable Version)

This is a standalone version of the live dashboard, meant to be hosted online
so you can share a real link in your resume, portfolio, or project writeup.

**Important:** this deployed version does NOT connect to a real webcam —
cloud servers don't have physical cameras. It starts with realistic seeded
demo data, and includes a "Simulate Entry" button so anyone visiting the
link can watch the dashboard update live, just like it does during your
actual event demo with `main.py` running locally.

Your real, camera-connected system (`main.py` + local dashboard) still runs
entirely on your own laptop for the actual event — this is a separate,
internet-facing copy for showing off afterward.

## Deploy to Render (free, ~5 minutes)

1. **Create a GitHub repo** and push this `dashboard-deploy` folder to it
   (rename the repo/folder to whatever you like, e.g. `campus-security-dashboard`).

2. **Sign up at [render.com](https://render.com)** (free, no card required for
   the free tier).

3. Click **New +** → **Web Service** → connect your GitHub repo.

4. Configure it:
   - **Root Directory:** leave blank if this folder is the repo root, otherwise
     set it to `dashboard-deploy`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

5. Click **Create Web Service**. Render will build and deploy automatically.
   After a minute or two, you'll get a live URL like:
   ```
   https://campus-security-dashboard.onrender.com
   ```

6. Open it — you'll see the dashboard with seeded demo entries. Click
   **Simulate Entry** to add a new scan and watch the stats/chart/feed
   update live.

**Free tier note:** Render's free web services "sleep" after 15 minutes of
no traffic and take ~30-50 seconds to wake up on the next visit. That's
fine for a portfolio link — just mention it if you're showing it live to
someone ("give it a few seconds to wake up").

## Alternative: Railway

Same idea, slightly different UI:
1. Sign up at [railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo
3. Railway auto-detects Python + the `Procfile` and deploys automatically
4. Generate a public domain from the service's Settings tab

## Running it locally first (recommended before deploying)

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` — confirm the demo data and Simulate button
both work before pushing to GitHub/Render.

## Files

```
dashboard-deploy/
├── app.py                 Standalone Flask app (seeded demo data + /api/simulate)
├── requirements.txt       flask, gunicorn
├── Procfile                Tells Render/Railway how to start the app
├── templates/index.html    Dashboard page (with demo banner + Simulate button)
└── static/style.css, script.js
```
