from database import get_connection


def add_event(resident_name, event_type, status, notes=""):
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
    cur.execute(
        """
        SELECT id, resident_name, event_type, status, notes, created_at
        FROM events
        ORDER BY created_at DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_event(event_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
