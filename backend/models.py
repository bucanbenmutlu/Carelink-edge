from database import get_connection


def add_resident(full_name, blood_group="", dob="", diet="", notes=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO residents (full_name, blood_group, date_of_birth, diet, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, blood_group, dob, diet, notes))

    conn.commit()
    conn.close()


def get_all_residents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM residents ORDER BY full_name ASC")

    rows = cur.fetchall()
    conn.close()
    return rows


def add_event(resident_id, event_type, status, notes=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO events (resident_id, event_type, status, notes)
        VALUES (?, ?, ?, ?)
    """, (resident_id, event_type, status, notes))

    conn.commit()
    conn.close()


def get_all_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            events.id,
            residents.full_name AS resident_name,
            residents.blood_group,
            residents.date_of_birth,
            residents.diet,
            events.event_type,
            events.status,
            events.notes AS event_notes,
            events.created_at
        FROM events
        LEFT JOIN residents ON residents.id = events.resident_id
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


def get_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM residents")
    residents = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM events")
    events = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM events
        WHERE status='critical' OR status='emergency'
    """)
    critical = cur.fetchone()[0]

    conn.close()

    return {
        "residents": residents,
        "events": events,
        "critical": critical
    }
