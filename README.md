# Smart Campus Security — Live Dashboard (Deployed)

🔗 **Live Demo:** https://smart-campus-security-dashboard.onrender.com/

A live dashboard for a webcam-based face recognition access control system.
This deployed version shows realistic seeded demo data and includes a
**"Simulate Entry"** button — click it to watch the stats, chart, and
entry feed update in real time.

> Note: this online version does not connect to a real webcam (cloud
> servers don't have physical cameras). The full working system — with
> live face recognition via webcam — runs locally on a laptop for the
> actual event demo. This deployment is a portfolio-friendly preview of
> just the dashboard.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Chart.js
- **Hosting:** Render (free tier)

## Features

- Live-updating stats: total scans, granted, denied
- Granted vs Denied doughnut chart
- Real-time entry feed with timestamps
- "Simulate Entry" button for interactive demo without a camera

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

## Deploy Your Own Copy

1. Fork or clone this repo
2. Sign up at [render.com](https://render.com)
3. New Web Service → connect this repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Deploy

## Related Project

This dashboard is part of a larger Smart Campus Security system built for
an Engineering Day project — full webcam-based face recognition, live
access control, and this dashboard, running together on a local laptop
for the physical event demo.
