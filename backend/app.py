from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from models import *

app = Flask(__name__)


@app.route("/")
def index():
    residents = get_all_residents()
    events = get_all_events()
    stats = get_stats()
    return render_template("index.html", residents=residents, events=events, stats=stats)


@app.route("/add_resident", methods=["POST"])
def add_resident_route():
    add_resident(
        request.form.get("full_name"),
        request.form.get("blood_group"),
        request.form.get("date_of_birth"),
        request.form.get("diet"),
        request.form.get("notes"),
    )
    return redirect(url_for("index"))


@app.route("/log_event", methods=["POST"])
def log_event_route():
    add_event(
        request.form.get("resident_id"),
        request.form.get("event_type"),
        request.form.get("status"),
        request.form.get("notes"),
    )
    return redirect(url_for("index"))


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
