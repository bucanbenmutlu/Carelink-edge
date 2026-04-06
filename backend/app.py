from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from models import (
    add_resident,
    get_all_residents,
    add_event,
    get_all_events,
    delete_event,
    delete_resident,
    get_counts,
)

app = Flask(__name__)


@app.route("/")
def index():
    residents = get_all_residents()
    events = get_all_events()
    counts = get_counts()
    return render_template(
        "index.html",
        residents=residents,
        events=events,
        counts=counts,
    )


@app.route("/add_resident", methods=["POST"])
def create_resident():
    full_name = request.form.get("full_name", "").strip()
    blood_group = request.form.get("blood_group", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()
    diet = request.form.get("diet", "").strip()
    allergies = request.form.get("allergies", "").strip()
    disability = request.form.get("disability", "").strip()
    notes = request.form.get("notes", "").strip()

    if full_name:
        add_resident(
            full_name=full_name,
            blood_group=blood_group,
            date_of_birth=date_of_birth,
            diet=diet,
            allergies=allergies,
            disability=disability,
            notes=notes,
        )

    return redirect(url_for("index"))


@app.route("/log_event", methods=["POST"])
def log_event():
    resident_id = request.form.get("resident_id", "").strip()
    event_type = request.form.get("event_type", "").strip()
    status = request.form.get("status", "").strip()
    notes = request.form.get("notes", "").strip()

    if resident_id and event_type and status:
        add_event(
            resident_id=resident_id,
            event_type=event_type,
            status=status,
            notes=notes,
        )

    return redirect(url_for("index"))


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    return redirect(url_for("index"))


@app.route("/delete_resident/<int:resident_id>", methods=["POST"])
def delete_resident_route(resident_id):
    delete_resident(resident_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
