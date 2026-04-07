from database import get_connection


def add_resident(
    full_name,
    date_of_birth="",
    id_number="",
    nationality="",
    blood_group="",
    allergies="",
    diet="",
    disability="",
    emergency_contact_name="",
    emergency_contact_phone="",
    emergency_contact_relationship="",
    primary_physician_name="",
    primary_physician_phone="",
    primary_physician_address="",
    medical_history="",
    current_medications="",
    vaccinations="",
    infectious_diseases="",
    adl_needs="",
    religious_cultural_preferences="",
    photo_path="",
    notes="",
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO residents (
            full_name, date_of_birth, id_number, nationality, blood_group,
            allergies, diet, disability,
            emergency_contact_name, emergency_contact_phone, emergency_contact_relationship,
            primary_physician_name, primary_physician_phone, primary_physician_address,
            medical_history, current_medications, vaccinations, infectious_diseases,
            adl_needs, religious_cultural_preferences, photo_path, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            full_name, date_of_birth, id_number, nationality, blood_group,
            allergies, diet, disability,
            emergency_contact_name, emergency_contact_phone, emergency_contact_relationship,
            primary_physician_name, primary_physician_phone, primary_physician_address,
            medical_history, current_medications, vaccinations, infectious_diseases,
            adl_needs, religious_cultural_preferences, photo_path, notes
        ),
    )
    conn.commit()
    conn.close()


def get_all_residents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM residents
        ORDER BY full_name ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_resident(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM incident_reports WHERE resident_id = ?", (resident_id,))
    cur.execute("DELETE FROM residents WHERE id = ?", (resident_id,))
    conn.commit()
    conn.close()


def add_incident_report(
    resident_id,
    event_datetime="",
    event_type="",
    severity="",
    case_status="",
    description="",
    pulse="",
    blood_pressure="",
    temperature="",
    oxygen_saturation="",
    respiration_rate="",
    medication_name="",
    medication_dosage="",
    medication_time="",
    medication_correctness="",
    witnesses="",
    location="",
    immediate_actions_taken="",
    notifications="",
    follow_up_outcome="",
    staff_involved_signature="",
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO incident_reports (
            resident_id, event_datetime, event_type, severity, case_status,
            description, pulse, blood_pressure, temperature, oxygen_saturation,
            respiration_rate, medication_name, medication_dosage, medication_time,
            medication_correctness, witnesses, location, immediate_actions_taken,
            notifications, follow_up_outcome, staff_involved_signature
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            resident_id, event_datetime, event_type, severity, case_status,
            description, pulse, blood_pressure, temperature, oxygen_saturation,
            respiration_rate, medication_name, medication_dosage, medication_time,
            medication_correctness, witnesses, location, immediate_actions_taken,
            notifications, follow_up_outcome, staff_involved_signature
        ),
    )
    conn.commit()
    conn.close()


def get_all_incident_reports():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            incident_reports.id,
            residents.full_name AS resident_name,
            residents.id_number AS resident_id_number,
            residents.blood_group AS resident_blood_group,
            incident_reports.event_datetime,
            incident_reports.event_type,
            incident_reports.severity,
            incident_reports.case_status,
            incident_reports.description,
            incident_reports.pulse,
            incident_reports.blood_pressure,
            incident_reports.temperature,
            incident_reports.oxygen_saturation,
            incident_reports.respiration_rate,
            incident_reports.medication_name,
            incident_reports.medication_dosage,
            incident_reports.medication_time,
            incident_reports.medication_correctness,
            incident_reports.witnesses,
            incident_reports.location,
            incident_reports.immediate_actions_taken,
            incident_reports.notifications,
            incident_reports.follow_up_outcome,
            incident_reports.staff_involved_signature,
            incident_reports.created_at
        FROM incident_reports
        JOIN residents ON residents.id = incident_reports.resident_id
        ORDER BY incident_reports.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_incident_report(report_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM incident_reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()


def get_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM residents")
    resident_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) AS count FROM incident_reports")
    report_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM incident_reports
        WHERE severity IN ('Severe', 'Fatal') OR case_status = 'Ongoing'
    """)
    critical_count = cur.fetchone()["count"]

    conn.close()

    return {
        "residents": resident_count,
        "reports": report_count,
        "critical": critical_count,
    }
EOF
