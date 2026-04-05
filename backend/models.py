from database import get_connection


def add_event(resident_name: str, event_type: str, status: str, notes: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (resident_name, event_type, status, notes)
        VALUES (?, ?, ?, ?)
        """,
        (resident_name, event_type, status, notes),
    )
    conn.commit()
    conn.close()


def get_all_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, resident_name, event_type, status, notes, created_at
        FROM events
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
