from datetime import datetime
from threading import Lock

from models import (
    add_incident_report,
    add_resident,
    clear_demo_incident_reports,
    get_all_residents,
)


DEVICES = [
    {
        "id": "bed-sensor-01",
        "name": "Bed Pressure Pad",
        "label": "Room 204 Bed A",
        "type": "Bed Sensor",
        "assigned_to": "Aylin Demir",
        "bridge": "ESP32 Bridge A",
        "firmware": "v1.8.4",
        "power": "AC Powered",
        "signal": "-48 dBm",
        "latency": "42 ms",
        "status": "Monitoring",
        "last_reading": "Occupancy stable, night mode active",
        "telemetry": {
            "primary": "Pressure load 57.8 kg",
            "secondary": "Micro-movement 2/min",
            "tertiary": "Exit risk low",
        },
    },
    {
        "id": "wearable-band-02",
        "name": "Wearable Health Band",
        "label": "Resident Wrist Unit",
        "type": "Wearable",
        "assigned_to": "Kemal Yildiz",
        "bridge": "ESP32 Bridge B",
        "firmware": "v2.3.1",
        "power": "Battery 84%",
        "signal": "-62 dBm",
        "latency": "78 ms",
        "status": "Monitoring",
        "last_reading": "Pulse 74 bpm, SpO2 97%",
        "telemetry": {
            "primary": "Pulse 74 bpm",
            "secondary": "SpO2 97%",
            "tertiary": "Skin temp 36.6 C",
        },
    },
    {
        "id": "room-button-03",
        "name": "Smart Room Call Button",
        "label": "North Wing Corridor",
        "type": "Call Button",
        "assigned_to": "Fatma Kaya",
        "bridge": "ESP32 Bridge C",
        "firmware": "v1.2.7",
        "power": "Battery 92%",
        "signal": "-54 dBm",
        "latency": "35 ms",
        "status": "Monitoring",
        "last_reading": "No active assistance request",
        "telemetry": {
            "primary": "Last press 7h ago",
            "secondary": "Ack line healthy",
            "tertiary": "Tamper status normal",
        },
    },
]

SCENARIOS = [
    {
        "name": "Bed Exit Assisted",
        "device_id": "bed-sensor-01",
        "event_type": "Wandering",
        "severity": "Minor",
        "case_status": "Resolved",
        "description": "Bed pressure dropped during overnight monitoring and the assigned caregiver verified a safe bed exit.",
        "location": "Room 204",
        "pulse": "82 bpm",
        "blood_pressure": "128/80",
        "temperature": "36.7 C",
        "oxygen_saturation": "98%",
        "respiration_rate": "18/min",
        "follow_up_outcome": "Resident assisted back to bed and sleep routine resumed without escalation.",
        "device_status": "Monitoring",
        "device_reading": "Exit event confirmed, bedside support delivered",
        "alert_level": "info",
    },
    {
        "name": "Pulse Spike Reviewed",
        "device_id": "wearable-band-02",
        "event_type": "Vital Change",
        "severity": "Moderate",
        "case_status": "Resolved",
        "description": "Wearable stream showed a short pulse rise during activity and the duty nurse completed a seated recheck.",
        "location": "Common Area",
        "pulse": "104 bpm",
        "blood_pressure": "136/84",
        "temperature": "37.1 C",
        "oxygen_saturation": "96%",
        "respiration_rate": "20/min",
        "follow_up_outcome": "Vitals settled after rest and hydration; monitoring returned to baseline.",
        "device_status": "Monitoring",
        "device_reading": "Transient tachycardia resolved on follow-up",
        "alert_level": "info",
    },
    {
        "name": "Emergency Button Response",
        "device_id": "room-button-03",
        "event_type": "Emergency",
        "severity": "Moderate",
        "case_status": "Resolved",
        "description": "Room call button was pressed for assistance and the assigned responder acknowledged the request promptly.",
        "location": "Room 110",
        "pulse": "90 bpm",
        "blood_pressure": "134/82",
        "temperature": "36.8 C",
        "oxygen_saturation": "97%",
        "respiration_rate": "18/min",
        "follow_up_outcome": "Resident request completed at bedside and call was closed by caregiver.",
        "device_status": "Monitoring",
        "device_reading": "Call accepted and completed in 51 sec",
        "alert_level": "warning",
    },
    {
        "name": "Low Oxygen Follow-up",
        "device_id": "wearable-band-02",
        "event_type": "Vital Change",
        "severity": "Severe",
        "case_status": "Ongoing",
        "description": "Wearable telemetry showed a sustained oxygen dip and respiratory follow-up was started.",
        "location": "Recreation Area",
        "pulse": "92 bpm",
        "blood_pressure": "136/86",
        "temperature": "36.9 C",
        "oxygen_saturation": "89%",
        "respiration_rate": "22/min",
        "follow_up_outcome": "Resident moved to observation bay and physician callback requested.",
        "device_status": "Critical",
        "device_reading": "Sustained SpO2 low threshold breach",
        "alert_level": "critical",
    },
    {
        "name": "Medication Reminder Closed",
        "device_id": "room-button-03",
        "event_type": "Medication Error",
        "severity": "Minor",
        "case_status": "Resolved",
        "description": "Medication acknowledgement window passed briefly before caregiver confirmation was logged at the station.",
        "location": "Medication Station",
        "pulse": "78 bpm",
        "blood_pressure": "126/80",
        "temperature": "36.5 C",
        "oxygen_saturation": "98%",
        "respiration_rate": "17/min",
        "medication_name": "Metformin",
        "medication_dosage": "500 mg",
        "medication_time": "08:00",
        "medication_correctness": "Confirmed",
        "follow_up_outcome": "Medication delivered and electronic chart updated with manual verification.",
        "device_status": "Monitoring",
        "device_reading": "Reminder acknowledged and closed",
        "alert_level": "info",
    },
]

DEMO_RESIDENTS = [
    {
        "full_name": "Aylin Demir",
        "date_of_birth": "1945-07-18",
        "id_number": "CL-1001",
        "nationality": "Turkish",
        "blood_group": "A+",
        "allergies": "Penicillin",
        "diet": "Low salt",
        "disability": "Mobility assistance",
        "height_cm": "160",
        "weight_kg": "62",
        "emergency_contact_name": "Mert Demir",
        "emergency_contact_phone": "+90 555 120 1111",
        "emergency_contact_relationship": "Son",
        "notes": "Uses walker and prefers morning check-ins.",
    },
    {
        "full_name": "Kemal Yildiz",
        "date_of_birth": "1939-11-04",
        "id_number": "CL-1002",
        "nationality": "Turkish",
        "blood_group": "O-",
        "allergies": "None known",
        "diet": "Diabetic",
        "disability": "Hearing impairment",
        "height_cm": "173",
        "weight_kg": "76",
        "emergency_contact_name": "Selin Yildiz",
        "emergency_contact_phone": "+90 555 220 2222",
        "emergency_contact_relationship": "Daughter",
        "notes": "Requires medication reminders after breakfast.",
    },
    {
        "full_name": "Fatma Kaya",
        "date_of_birth": "1942-03-29",
        "id_number": "CL-1003",
        "nationality": "Turkish",
        "blood_group": "B+",
        "allergies": "Latex",
        "diet": "Soft diet",
        "disability": "Mild cognitive decline",
        "height_cm": "158",
        "weight_kg": "58",
        "emergency_contact_name": "Emre Kaya",
        "emergency_contact_phone": "+90 555 330 3333",
        "emergency_contact_relationship": "Grandson",
        "notes": "Evening wandering risk is higher after 20:00.",
    },
]


class DemoEngine:
    def __init__(self):
        self._lock = Lock()
        self.enabled = False
        self.tick = 0
        self.poll_interval_ms = 6500
        self.feed = []
        self.active_alerts = []
        self.last_tick_at = ""
        self.devices = [dict(device) for device in DEVICES]

    def ensure_demo_residents(self):
        residents = get_all_residents()
        if residents:
            return residents

        for resident in DEMO_RESIDENTS:
            add_resident(**resident)
        return get_all_residents()

    def toggle(self):
        with self._lock:
            self.enabled = not self.enabled
            if self.enabled:
                clear_demo_incident_reports()
                self.ensure_demo_residents()
                self.tick = 0
                self.feed = []
                self.active_alerts = []
                self.last_tick_at = ""
                self.devices = [dict(device) for device in DEVICES]
            else:
                self.active_alerts = []
                for device in self.devices:
                    device["status"] = "Idle"
            return self.enabled

    def snapshot(self):
        with self._lock:
            return self._snapshot_unlocked()

    def _snapshot_unlocked(self):
        return {
            "enabled": self.enabled,
            "tick": self.tick,
            "poll_interval_ms": self.poll_interval_ms,
            "last_tick_at": self.last_tick_at,
            "devices": [dict(device) for device in self.devices],
            "feed": list(self.feed[:8]),
            "active_alerts": list(self.active_alerts[:4]),
        }

    def _normal_device_telemetry(self, device, now):
        phase = self.tick + len(device["id"])
        if device["id"] == "bed-sensor-01":
            return {
                "status": "Monitoring",
                "last_reading": "Occupancy stable, night mode active",
                "telemetry": {
                    "primary": f"Pressure load {57 + (phase % 4)}.{phase % 10} kg",
                    "secondary": f"Micro-movement {(phase % 3) + 1}/min",
                    "tertiary": "Exit risk low",
                },
                "signal": "-48 dBm",
                "latency": f"{38 + (phase % 7)} ms",
                "last_seen": now,
            }
        if device["id"] == "wearable-band-02":
            return {
                "status": "Monitoring",
                "last_reading": "Wearable stream healthy",
                "telemetry": {
                    "primary": f"Pulse {72 + (phase % 6)} bpm",
                    "secondary": f"SpO2 {96 + (phase % 2)}%",
                    "tertiary": f"Skin temp 36.{5 + (phase % 3)} C",
                },
                "signal": "-62 dBm",
                "latency": f"{72 + (phase % 10)} ms",
                "power": f"Battery {82 - (self.tick % 5)}%",
                "last_seen": now,
            }
        return {
            "status": "Monitoring",
            "last_reading": "No active assistance request",
            "telemetry": {
                "primary": f"Last press {(phase % 9) + 1}h ago",
                "secondary": "Ack line healthy",
                "tertiary": "Tamper status normal",
            },
            "signal": "-54 dBm",
            "latency": f"{30 + (phase % 8)} ms",
            "power": f"Battery {90 - (self.tick % 4)}%",
            "last_seen": now,
        }

    def maybe_advance(self):
        with self._lock:
            if not self.enabled:
                return self._snapshot_unlocked()

            residents = self.ensure_demo_residents()
            if not residents:
                return self._snapshot_unlocked()

            resident = residents[self.tick % len(residents)]
            scenario = SCENARIOS[self.tick % len(SCENARIOS)]
            now = datetime.now()
            time_label = now.strftime("%Y-%m-%d %H:%M:%S")
            resident_name = resident["full_name"]

            add_incident_report(
                resident_id=resident["id"],
                event_datetime=time_label,
                event_type=scenario["event_type"],
                severity=scenario["severity"],
                case_status=scenario["case_status"],
                description=f'{scenario["description"]} Resident: {resident_name}.',
                pulse=scenario.get("pulse", ""),
                blood_pressure=scenario.get("blood_pressure", ""),
                temperature=scenario.get("temperature", ""),
                oxygen_saturation=scenario.get("oxygen_saturation", ""),
                respiration_rate=scenario.get("respiration_rate", ""),
                medication_name=scenario.get("medication_name", ""),
                medication_dosage=scenario.get("medication_dosage", ""),
                medication_time=scenario.get("medication_time", ""),
                medication_correctness=scenario.get("medication_correctness", ""),
                witnesses="Auto-generated CareLink demo event",
                location=scenario.get("location", ""),
                immediate_actions_taken="Auto-escalated by demo device rule.",
                notifications="Caregiver dashboard highlighted automatically.",
                follow_up_outcome=scenario.get("follow_up_outcome", ""),
                staff_involved_signature="Demo Engine",
            )

            for device in self.devices:
                device.update(self._normal_device_telemetry(device, time_label))
                if device["id"] == scenario["device_id"]:
                    device["status"] = scenario["device_status"]
                    device["last_reading"] = scenario["device_reading"]
                    device["last_seen"] = time_label
                    if device["id"] == "bed-sensor-01":
                        device["telemetry"] = {
                            "primary": "Pressure drop event closed",
                            "secondary": "Bedside response 24 sec",
                            "tertiary": "Resident safe",
                        }
                    elif device["id"] == "wearable-band-02":
                        device["telemetry"] = {
                            "primary": f"Pulse {scenario.get('pulse', '—')}",
                            "secondary": f"SpO2 {scenario.get('oxygen_saturation', '—')}",
                            "tertiary": f"BP {scenario.get('blood_pressure', '—')}",
                        }
                    else:
                        device["telemetry"] = {
                            "primary": scenario["device_reading"],
                            "secondary": "Responder acknowledged",
                            "tertiary": "Ticket synced to dashboard",
                        }
                elif device["status"] in {"Critical", "Alert"}:
                    device["status"] = "Monitoring"

            feed_item = {
                "time": time_label,
                "scenario": scenario["name"],
                "resident_name": resident_name,
                "device_name": next(
                    device["name"] for device in self.devices if device["id"] == scenario["device_id"]
                ),
                "severity": scenario["severity"],
                "case_status": scenario["case_status"],
                "location": scenario.get("location", "Facility"),
                "reading": scenario["device_reading"],
                "outcome": scenario.get("follow_up_outcome", ""),
            }
            self.feed.insert(0, feed_item)
            self.feed = self.feed[:8]

            if scenario["alert_level"] in {"warning", "critical"}:
                self.active_alerts.insert(
                    0,
                    {
                        "time": time_label,
                        "resident_name": resident_name,
                        "scenario": scenario["name"],
                        "severity": scenario["severity"],
                        "device_name": feed_item["device_name"],
                        "reading": scenario["device_reading"],
                        "level": scenario["alert_level"],
                    },
                )
                self.active_alerts = self.active_alerts[:4]
            else:
                self.active_alerts = self.active_alerts[:2]

            self.tick += 1
            self.last_tick_at = time_label
            return self._snapshot_unlocked()


demo_engine = DemoEngine()
