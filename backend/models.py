from database import get_connection


def add_resident(full_name, date_of_birth="", emergency_contact="", allergies="",
                 blood_group="", height_cm="", diet="", notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO residents
        (full_name, date_of_birth, emergency_contact, allergies, blood_group, height_cm, diet, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (full_name, date_of_birth, emergency_contact, allergies, blood_group, height_cm, diet, notes),
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


def get_resident_by_id(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM residents
        WHERE id = ?
    """, (resident_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_event(resident_id, event_type, status, notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (resident_id, event_type, status, notes)
        VALUES (?, ?, ?, ?)
        """,
        (resident_id, event_type, status, notes),
    )
    conn.commit()
    conn.close()


def get_all_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            events.id,
            events.resident_id,
            residents.full_name AS resident_name,
            events.event_type,
            events.status,
            events.notes,
            events.created_at
        FROM events
        JOIN residents ON events.resident_id = residents.id
        ORDER BY events.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_event(event_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM residents")
    resident_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) AS count FROM events")
    event_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM events
        WHERE LOWER(status) = 'critical' OR LOWER(status) = 'emergency'
    """)
    critical_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM events
        WHERE LOWER(status) = 'warning'
    """)
    warning_count = cur.fetchone()["count"]

    conn.close()

    return {
        "resident_count": resident_count,
        "event_count": event_count,
        "critical_count": critical_count,
        "warning_count": warning_count,
    }
