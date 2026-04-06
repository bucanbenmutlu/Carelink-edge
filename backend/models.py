from database import get_connection


def add_resident(full_name, blood_group="", date_of_birth="", diet="", notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO residents (full_name, blood_group, date_of_birth, diet, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (full_name, blood_group, date_of_birth, diet, notes),
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
            residents.full_name AS resident_name,
            residents.blood_group AS resident_blood_group,
            residents.date_of_birth AS resident_dob,
            residents.diet AS resident_diet,
            events.event_type,
            events.status,
            events.notes AS event_notes,
            events.created_at
        FROM events
        JOIN residents ON residents.id = events.resident_id
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


def get_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM residents")
    resident_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) AS count FROM events")
    event_count = cur.fetchone()["count"]

    conn.close()
    return {
        "resident_count": resident_count,
        "event_count": event_count,
    }
