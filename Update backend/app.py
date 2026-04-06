from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from models import add_event, get_all_events, delete_event

app = Flask(__name__)


@app.route("/")
def index():
    events = get_all_events()
    return render_template("index.html", events=events)


@app.route("/log", methods=["POST"])
def log_event():
    resident_name = request.form.get("resident_name")
    event_type = request.form.get("event_type")
    status = request.form.get("status")
    notes = request.form.get("notes")

    add_event(resident_name, event_type, status, notes)
    return redirect(url_for("index"))


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
