# CareLink Edge

CareLink Edge is a prototype elderly care monitoring and incident management system that combines software and edge-device concepts into a single workflow.

The goal of this project is to help caregivers and care facilities track residents, record incidents, and (in the future) receive real-time alerts from physical devices.

This repository is currently an early-stage MVP / proof of concept.

---

## Features

- Register and manage residents
- Create and track incident reports
- Simple dashboard interface
- SQLite database (no setup required)
- Flask backend (lightweight and easy to run)
- Hardware-ready architecture (FPGA + ESP32 planned)

---

## Project Structure

Carelink-edge/

backend/ → Flask app (main working part)  
esp32_bridge/ → Planned ESP32 Wi-Fi bridge  
fpga/ → Planned FPGA logic  
docs/ → Architecture notes  

---

## What This Project Does

The system follows a simple flow:

1. Add a resident
2. Record an incident or event
3. Store the data
4. Display it in a dashboard
5. Allow monitoring and follow-up

Future goal:

A physical device detects events (button press, fall, health issue) → sends data → backend → dashboard.

---

## Tech Stack

- Python 3
- Flask
- SQLite

Planned:
- ESP32
- FPGA

---

## How to Run (macOS - Beginner Friendly)

### 1. Open Terminal

Press:

Command + Space → type "Terminal" → Enter

---

### 2. Check Python

```bash
python3 --version
```
If you see python version in output continue;

3. Clone the project
```bash
cd ~/Desktop
git clone https://github.com/bucanbenmutlu/Carelink-edge.git
cd Carelink-edge/backend
```

4. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see:
(.venv)

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Run the app
```bash
python3 app.py
```

7. Open in browser

Go to:
http://127.0.0.1:5000

What You Can Do
Add residents
Create incident reports
View records
Test system without hardware

Database
SQLite is used.
Auto-created here:
backend/data/carelink.db
