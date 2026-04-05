from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db
from models import add_event, get_all_events
from notifier import send_alert

app = Flask(__name__)


@app.route("/")
def index():
    events = get_all_events()
    return render_template("index.html", events=events)


@app.route("/log", methods=["POST"])
def log_event():
    resident_name = request.form.get("resident_name", "Resident A")
    event_type = request.form.get("event_type", "manual_input")
    status = request.form.get("status", "normal")
    notes = request.form.get("notes", "")

    add_event(resident_name, event_type, status, notes)

    if status.lower() in {"warning", "critical", "emergency"}:
        send_alert(f"{resident_name}: {event_type} -> {status}")

    return redirect(url_for("index"))


@app.route("/api/log", methods=["POST"])
def api_log_event():
    data = request.get_json(force=True)

    resident_name = data.get("resident_name", "Resident A")
    event_type = data.get("event_type", "uart_event")
    status = data.get("status", "normal")
    notes = data.get("notes", "")

    add_event(resident_name, event_type, status, notes)

    if status.lower() in {"warning", "critical", "emergency"}:
        send_alert(f"{resident_name}: {event_type} -> {status}")

    return jsonify({"message": "Event logged successfully"}), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
