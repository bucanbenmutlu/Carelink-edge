# CareLink Edge

CareLink Edge is a Flask-based elderly care operations demo that combines resident records, incident management, and simulated edge-device telemetry in a single dashboard.

The current version is designed as a presentation-ready product demo for elderly homes, municipal care centers, and assisted living facilities. It works without physical hardware and demonstrates how alerts can be detected, triaged, followed up, and resolved visibly.

## Current Demo Scope

- Protected login screen with static demo users
- Resident management
- Manual incident entry
- Realtime demo telemetry from 3 mock edge devices
- Slower, more realistic device sync rhythm
- Active alert queue and resolved interventions
- Manual `Mark as Resolved` flow from the incident preview
- SQLite-backed resident and incident storage

## Demo Login

The app uses static demo accounts.

- `bucan / bucan2010`
- `demo / demo2026`

These are intentionally hardcoded for demo use only. They are not meant for production.

## Project Structure

```text
Carelink-edge/
├── backend/         Flask application, templates, demo engine, SQLite usage
├── esp32_bridge/    Planned ESP32 bridge work
├── fpga/            Planned FPGA-side work
├── docs/            Architecture and roadmap notes
└── README.md
```

## Tech Stack

- Python 3
- Flask
- SQLite
- HTML / CSS / vanilla JavaScript

Planned hardware path:

`Device -> FPGA -> ESP32 -> Backend -> Dashboard`

## Local Installation

### 1. Open the project

```bash
cd "/Users/benmutlu/Desktop/Python & Projects/Bucan/web/Carelink-edge/backend"
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
python3 app.py
```

### 5. Open it in your browser

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## What To Test

After login:

- Open the dashboard
- Start `Demo Mode`
- Watch device telemetry update every few seconds
- See incident reports appear as exceptions
- Use `Incident Report Form`
- In `Realtime Exception Preview`, close an open case with `Mark as Resolved`
- Check that resolved cases move into green resolved sections

## Data Storage

SQLite is created automatically in:

```text
backend/data/carelink.db
```

## Notes About The Demo

- This project is a demo / MVP, not a production medical platform
- Authentication is intentionally static
- No hardware is required to run the current version
- The device layer is simulated through the demo engine in `backend/demo.py`

## Quick Update Checklist

If you pull a newer version later:

```bash
cd "/Users/benmutlu/Desktop/Python & Projects/Bucan/web/Carelink-edge/backend"
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Send This To Another GitHub Repository

If you want to push this code to someone else's GitHub repository, first create an empty repo there, then run:

```bash
cd "/Users/benmutlu/Desktop/Python & Projects/Bucan/web/Carelink-edge"
git remote -v
```

If you want to replace the current remote with the new GitHub repo:

```bash
git remote set-url origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

If you want to keep the current remote and add a second one:

```bash
git remote add other https://github.com/USERNAME/REPO.git
git push -u other main
```

If the main branch name is different, check it with:

```bash
git branch
```

Then push that branch instead:

```bash
git push -u other BRANCH_NAME
```

## Optional: First Commit Before Pushing

If you still have local changes:

```bash
git status
git add .
git commit -m "Update CareLink Edge demo"
git push -u origin main
```
