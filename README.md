 # CareLink Edge

CareLink Edge is a real-time elderly health monitoring and caregiver alert system designed as a hardware-software co-design project.

The long-term goal is to combine FPGA-based digital logic, embedded communication, and a Python backend for resident status monitoring, local alerts, and caregiver notifications.

## Current MVP
This first version focuses on:
- resident status input
- medication tracking
- emergency alert triggering
- backend logging
- simple dashboard

## Planned Hardware Architecture
- FPGA: alert logic, FSM, debouncing, UART
- ESP32: UART-to-WiFi bridge
- Python backend: logging, dashboard, notifications

## Project Status
MVP software structure in progress.
FPGA simulation and backend integration are the first milestones.
