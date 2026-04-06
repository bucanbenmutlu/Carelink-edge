from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db
from models import (
    add_resident,
    get_all_residents,
    get_resident_by_id,
    add_event,
    get_all_events,
    delete_event,
    get_dashboard_stats,
)
from notifier import send_alert

app = Flask(__name__)


@app.route("/")
def index():
    residents = get_all_residents()
    events = get_all_events()
    stats = get_dashboard_stats()
    return render_template(
        "index.html",
        residents=residents,
        events=events,
        stats=stats
    )


@app.route("/add_resident", methods=["POST"])
def create_resident():
    full_name = request.form.get("full_name", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()
    emergency_contact = request.form.get("emergency_contact", "").strip()
    allergies = request.form.get("allergies", "").strip()
    blood_group = request.form.get("blood_group", "").strip()
    height_cm = request.form.get("height_cm", "").strip()
    diet = request.form.get("diet", "").strip()
    notes = request.form.get("notes", "").strip()

    if full_name:
        add_resident(
            full_name=full_name,
            date_of_birth=date_of_birth,
            emergency_contact=emergency_contact,
            allergies=allergies,
            blood_group=blood_group,
            height_cm=height_cm,
            diet=diet,
            notes=notes,
        )

    return redirect(url_for("index"))


@app.route("/log", methods=["POST"])
def log_event():
    resident_id = request.form.get("resident_id")
    event_type = request.form.get("event_type", "manual_input")
    status = request.form.get("status", "normal")
    notes = request.form.get("notes", "")

    if not resident_id:
        return redirect(url_for("index"))

    add_event(resident_id, event_type, status, notes)

    resident = get_resident_by_id(resident_id)
    resident_name = resident["full_name"] if resident else "Unknown Resident"

    if status.lower() in {"warning", "critical", "emergency"}:
        send_alert(f"{resident_name}: {event_type} -> {status}")

    return redirect(url_for("index"))


@app.route("/api/log", methods=["POST"])
def api_log_event():
    data = request.get_json(force=True)

    resident_id = data.get("resident_id")
    event_type = data.get("event_type", "uart_event")
    status = data.get("status", "normal")
    notes = data.get("notes", "")

    if not resident_id:
        return jsonify({"error": "resident_id is required"}), 400

    add_event(resident_id, event_type, status, notes)

    resident = get_resident_by_id(resident_id)
    resident_name = resident["full_name"] if resident else "Unknown Resident"

    if status.lower() in {"warning", "critical", "emergency"}:
        send_alert(f"{resident_name}: {event_type} -> {status}")

    return jsonify({"message": "Event logged successfully"}), 201


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
