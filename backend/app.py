import os
from functools import wraps

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    session,
    url_for,
)
from database import init_db
from demo import demo_engine
from models import (
    add_resident,
    get_all_residents,
    delete_resident,
    add_incident_report,
    get_all_incident_reports,
    delete_incident_report,
    get_counts,
    resolve_incident_report,
)

app = Flask(__name__)
app.secret_key = os.environ.get("CARELINK_SECRET_KEY", "carelink-static-demo-secret")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

USERS = {
    "bucan": "bucan2010",
    "demo": "demo2026",
}


def resolve_next_path(next_path):
    default_path = url_for("index")
    if not next_path:
        return default_path

    if next_path.startswith(("http://", "https://")):
        return default_path

    script_root = request.script_root or ""
    if script_root and next_path.startswith(script_root):
        return next_path
    if next_path.startswith("/"):
        return f"{script_root}{next_path}" if script_root else next_path
    return default_path


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def serialize_rows(rows):
    return [dict(row) for row in rows]


def build_dashboard_payload(advance_demo=False):
    demo = demo_engine.maybe_advance() if advance_demo else demo_engine.snapshot()
    residents = serialize_rows(get_all_residents())
    reports = serialize_rows(get_all_incident_reports())
    stats = get_counts()
    return {
        "residents": residents,
        "reports": reports,
        "stats": stats,
        "demo": demo,
    }


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))

    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if USERS.get(username) == password:
            session["username"] = username
            next_path = resolve_next_path(request.form.get("next"))
            return redirect(next_path)
        error = "Incorrect username or password."

    return render_template("login.html", error=error, next=request.args.get("next", ""))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    payload = build_dashboard_payload()
    return render_template(
        "index.html",
        residents=payload["residents"],
        reports=payload["reports"],
        stats=payload["stats"],
        demo=payload["demo"],
        current_user=session.get("username", ""),
    )


@app.route("/add_resident", methods=["POST"])
@login_required
def create_resident():
    full_name = request.form.get("full_name", "").strip()
    if full_name:
        add_resident(
            full_name=full_name,
            date_of_birth=request.form.get("date_of_birth", "").strip(),
            id_number=request.form.get("id_number", "").strip(),
            nationality=request.form.get("nationality", "").strip(),
            blood_group=request.form.get("blood_group", "").strip(),
            allergies=request.form.get("allergies", "").strip(),
            diet=request.form.get("diet", "").strip(),
            disability=request.form.get("disability", "").strip(),
            emergency_contact_name=request.form.get("emergency_contact_name", "").strip(),
            emergency_contact_phone=request.form.get("emergency_contact_phone", "").strip(),
            emergency_contact_relationship=request.form.get("emergency_contact_relationship", "").strip(),
            primary_physician_name=request.form.get("primary_physician_name", "").strip(),
            primary_physician_phone=request.form.get("primary_physician_phone", "").strip(),
            primary_physician_address=request.form.get("primary_physician_address", "").strip(),
            medical_history=request.form.get("medical_history", "").strip(),
            current_medications=request.form.get("current_medications", "").strip(),
            vaccinations=request.form.get("vaccinations", "").strip(),
            infectious_diseases=request.form.get("infectious_diseases", "").strip(),
            adl_needs=request.form.get("adl_needs", "").strip(),
            religious_cultural_preferences=request.form.get("religious_cultural_preferences", "").strip(),
            photo_path=request.form.get("photo_path", "").strip(),
            notes=request.form.get("notes", "").strip(),
            height_cm=request.form.get("height_cm", "").strip(),
            weight_kg=request.form.get("weight_kg", "").strip(),
        )
    return redirect(url_for("index"))


@app.route("/add_report", methods=["POST"])
@login_required
def create_report():
    resident_id = request.form.get("resident_id", "").strip()
    event_type = request.form.get("event_type", "").strip()
    if resident_id and event_type:
        add_incident_report(
            resident_id=resident_id,
            event_datetime=request.form.get("event_datetime", "").strip(),
            event_type=event_type,
            severity=request.form.get("severity", "").strip(),
            case_status=request.form.get("case_status", "").strip(),
            description=request.form.get("description", "").strip(),
            pulse=request.form.get("pulse", "").strip(),
            blood_pressure=request.form.get("blood_pressure", "").strip(),
            temperature=request.form.get("temperature", "").strip(),
            oxygen_saturation=request.form.get("oxygen_saturation", "").strip(),
            respiration_rate=request.form.get("respiration_rate", "").strip(),
            medication_name=request.form.get("medication_name", "").strip(),
            medication_dosage=request.form.get("medication_dosage", "").strip(),
            medication_time=request.form.get("medication_time", "").strip(),
            medication_correctness=request.form.get("medication_correctness", "").strip(),
            witnesses=request.form.get("witnesses", "").strip(),
            location=request.form.get("location", "").strip(),
            immediate_actions_taken=request.form.get("immediate_actions_taken", "").strip(),
            notifications=request.form.get("notifications", "").strip(),
            follow_up_outcome=request.form.get("follow_up_outcome", "").strip(),
            staff_involved_signature=request.form.get("staff_involved_signature", "").strip(),
        )
    return redirect(url_for("index"))


@app.route("/delete_resident/<int:resident_id>", methods=["POST"])
@login_required
def remove_resident(resident_id):
    delete_resident(resident_id)
    return redirect(url_for("index"))

@app.route("/delete_report/<int:report_id>", methods=["POST"])
@login_required
def remove_report(report_id):
    delete_incident_report(report_id)
    return redirect(url_for("index"))


@app.route("/reports/<int:report_id>/resolve", methods=["POST"])
@login_required
def resolve_report(report_id):
    outcome = ""
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        outcome = payload.get("follow_up_outcome", "").strip()
    else:
        outcome = request.form.get("follow_up_outcome", "").strip()

    if not outcome:
        outcome = "Resident stabilized after caregiver follow-up and documented handoff."

    resolve_incident_report(report_id, outcome)

    if request.is_json:
        return jsonify(build_dashboard_payload())
    return redirect(url_for("index"))


@app.route("/demo/toggle", methods=["POST"])
@login_required
def toggle_demo():
    enabled = demo_engine.toggle()
    payload = build_dashboard_payload()
    payload["demo"]["enabled"] = enabled
    return jsonify(payload)


@app.route("/api/dashboard")
@login_required
def dashboard_data():
    payload = build_dashboard_payload(advance_demo=True)
    return jsonify(payload)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
