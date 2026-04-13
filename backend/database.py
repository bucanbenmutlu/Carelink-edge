import sqlite3
from pathlib import Path

DB_PATH = Path("data/carelink.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT,
            id_number TEXT,
            nationality TEXT,
            blood_group TEXT,
            allergies TEXT,
            diet TEXT,
            disability TEXT,
            height_cm TEXT,
            weight_kg TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            emergency_contact_relationship TEXT,
            primary_physician_name TEXT,
            primary_physician_phone TEXT,
            primary_physician_address TEXT,
            medical_history TEXT,
            current_medications TEXT,
            vaccinations TEXT,
            infectious_diseases TEXT,
            adl_needs TEXT,
            religious_cultural_preferences TEXT,
            photo_path TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS incident_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_id INTEGER NOT NULL,
            event_datetime TEXT,
            event_type TEXT NOT NULL,
            severity TEXT,
            case_status TEXT,
            description TEXT,
            pulse TEXT,
            blood_pressure TEXT,
            temperature TEXT,
            oxygen_saturation TEXT,
            respiration_rate TEXT,
            medication_name TEXT,
            medication_dosage TEXT,
            medication_time TEXT,
            medication_correctness TEXT,
            witnesses TEXT,
            location TEXT,
            immediate_actions_taken TEXT,
            notifications TEXT,
            follow_up_outcome TEXT,
            staff_involved_signature TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resident_id) REFERENCES residents(id)
        )
    """)

    conn.commit()
    conn.close()
