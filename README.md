# CareLink Edge

CareLink Edge is a prototype elderly care monitoring and incident management system designed to combine software and edge-device concepts into a single workflow.

The project is intended to support caregivers and care facilities by providing a simple dashboard for resident registration, incident reporting, and structured event tracking. In its broader vision, the system can also integrate with embedded hardware such as FPGA and ESP32-based devices to capture real-world alerts and forward them to the backend.

At its current stage, the repository is best understood as an early proof of concept and MVP-style prototype.

---

## Features

- Register and manage resident records
- Create and track incident reports
- View residents and incidents from a simple dashboard
- Store data locally using SQLite
- Prototype-ready structure for future FPGA and ESP32 integration
- Simple Flask backend for easy local development and testing

---

## Project Structure
What This Project Does

CareLink Edge is built around a simple workflow:

Register a resident in the system
Record an incident or health-related event
Store the data in the backend
Display the information on a caregiver-facing dashboard
Support monitoring and follow-up actions

The long-term goal is to allow a physical device to detect alerts and send them into the platform automatically.

For example:

a panic button press
a fall detection event
an abnormal vital sign reading
a medication-related incident

These events could eventually be captured by an embedded device and transmitted to the software platform over Wi-Fi.

Hardware Vision

This repository also includes the early structure for future embedded integration.

FPGA layer

The FPGA side is intended to handle low-level physical logic such as:

reading hardware inputs
debounce logic for button presses
alert state machine handling
UART transmission
LED and buzzer control
ESP32 bridge

The ESP32 side is intended to act as a Wi-Fi bridge:

receive UART data from the FPGA
connect to a wireless network
send alert or sensor data to the backend
Backend

The backend receives and stores the information, then displays it in the dashboard.

Overall flow
[Button / Sensor / Device]
          ↓
        FPGA
          ↓ UART
       ESP32
          ↓ Wi-Fi
   Flask Backend
          ↓
     Dashboard

At the moment, you do not need the hardware parts to test the backend.
The backend can be run and tested as a standalone software prototype.

Tech Stack
Python 3
Flask
SQLite
Planned: ESP32
Planned: FPGA logic
Running the Project on macOS

This guide is written for beginners.

1. Open Terminal

On your Mac:

press Command + Space
type Terminal
press Enter
2. Check if Python 3 is installed

In Terminal, run:

python3 --version

You should see a version like:

Python 3.10.x

If Python is not installed, install it first from the official Python website or with Homebrew.

3. Check if Git is installed

Run:

git --version

If a Git version is shown, you are ready.

4. Clone the repository

Go to the folder where you want to download the project.
For example, to download it to your Desktop:

cd ~/Desktop

Now clone the repository:

git clone https://github.com/bucanbenmutlu/Carelink-edge.git

Enter the project folder:

cd Carelink-edge

Then move into the backend folder:

cd backend
5. Create a virtual environment

A virtual environment keeps the project dependencies separate from the rest of your system.

Run:

python3 -m venv .venv

This creates a local virtual environment inside the backend folder.

Now activate it:

source .venv/bin/activate

After this, your Terminal line should start with something like:

(.venv)
6. Install dependencies

Run:

pip install -r requirements.txt

This installs Flask and the required Python packages.

7. Start the application

Run:

python3 app.py

If everything is set up correctly, the Flask app will start and show a local URL.

Usually it will be:

http://127.0.0.1:5000
8. Open the app in your browser

Open Chrome or Safari and go to:

http://127.0.0.1:5000

You should see the CareLink Edge dashboard.

What You Can Do in the Dashboard

Once the backend is running, you can:

add residents
create incident reports
review stored incident history
test the system without any physical hardware

This makes it possible to try the project as a software-only demo before connecting real devices.

Database

The project uses SQLite for local storage.

The database file is created automatically inside:

backend/data/carelink.db

You do not need PostgreSQL or MySQL for this prototype.

Troubleshooting
Virtual environment is not active

If you do not see (.venv) in Terminal, activate it again:

source .venv/bin/activate
Flask is not found

Make sure you installed the requirements:

pip install -r requirements.txt
App does not open in browser

Make sure the Flask app is running in Terminal and then open:

http://127.0.0.1:5000
Port is already in use

If port 5000 is already being used by another program, stop the other program or change the Flask port in the code.

Current Status

CareLink Edge is currently a prototype, not a production-ready healthcare platform.

It demonstrates:

the resident and incident workflow
the backend storage model
the structure for future embedded integration

The backend is the most practical part to run today, while the FPGA and ESP32 folders represent the longer-term hardware direction of the project.

Intended Use Cases

This system is designed with elderly care environments in mind, including:

assisted living centers
nursing homes
home caregiver systems
monitoring-focused smart care environments

Possible future scenarios include:

panic/emergency button alerts
fall detection
pulse or health threshold alerts
medication incidents
patient wandering detection
caregiver event logging
