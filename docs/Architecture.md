# CareLink Edge Architecture

## System Overview
CareLink Edge is designed as a three-layer system:

1. FPGA Layer
- button input handling
- alert state machine
- local LED/buzzer logic
- UART transmission

2. ESP32 Layer
- receives UART packets
- sends data to backend over WiFi

3. Backend Layer
- stores events
- displays logs
- supports future notifications

## First MVP
The first MVP does not require real hardware.
It simulates the system with a Python backend and prepares the FPGA/ESP32 structure.
