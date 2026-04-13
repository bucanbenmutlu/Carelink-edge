from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from models import (
    add_resident,
    get_all_residents,
    delete_resident,
    add_incident_report,
    get_all_incident_reports,
    delete_incident_report,
    get_counts,
)

app = Flask(__name__)


@app.route("/")
def index():
    residents = get_all_residents()
    reports = get_all_incident_reports()
    stats = get_counts()
    return render_template(
        "index.html",
        residents=residents,
        reports=reports,
        stats=stats,
    )


@app.route("/add_resident", methods=["POST"])
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
        )
    return redirect(url_for("index"))


@app.route("/add_report", methods=["POST"])
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
def remove_resident(resident_id):
    delete_resident(resident_id)
    return redirect(url_for("index"))


@app.route("/delete_report/<int:report_id>", methods=["POST"])
def remove_report(report_id):
    delete_incident_report(report_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
