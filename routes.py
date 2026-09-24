from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Patient, Doctor, Appointment
from app.ml.predictor import predict_risk

main = Blueprint("main", __name__)


# ---------- Dashboard ----------
@main.route("/")
def dashboard():
    patient_count = Patient.query.count()
    doctor_count = Doctor.query.count()
    appt_count = Appointment.query.count()
    high_risk_count = Patient.query.filter_by(risk_label="High").count()
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    return render_template(
        "dashboard.html",
        patient_count=patient_count,
        doctor_count=doctor_count,
        appt_count=appt_count,
        high_risk_count=high_risk_count,
        recent_patients=recent_patients,
    )


# ---------- Patients ----------
@main.route("/patients")
def patient_list():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template("patients.html", patients=patients)


@main.route("/patients/add", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        form = request.form
        patient = Patient(
            name=form["name"],
            age=int(form["age"]),
            gender=form.get("gender"),
            contact=form.get("contact"),
            resting_bp=float(form.get("resting_bp") or 120),
            cholesterol=float(form.get("cholesterol") or 200),
            bmi=float(form.get("bmi") or 25),
            max_heart_rate=float(form.get("max_heart_rate") or (220 - int(form["age"]))),
            smoker=bool(form.get("smoker")),
            exercise_hours_week=float(form.get("exercise_hours_week") or 2),
            family_history=bool(form.get("family_history")),
        )

        vitals = {
            "age": patient.age,
            "resting_bp": patient.resting_bp,
            "cholesterol": patient.cholesterol,
            "bmi": patient.bmi,
            "max_heart_rate": patient.max_heart_rate,
            "smoker": int(patient.smoker),
            "exercise_hours_week": patient.exercise_hours_week,
            "family_history": int(patient.family_history),
        }
        prob, label = predict_risk(vitals)
        patient.risk_score = prob
        patient.risk_label = label

        db.session.add(patient)
        db.session.commit()
        flash(f"Patient added. Predicted heart-disease risk: {label} ({prob*100:.1f}%)", "success")
        return redirect(url_for("main.patient_list"))

    return render_template("add_patient.html")


@main.route("/patients/<int:patient_id>")
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("patient_detail.html", patient=patient)


# ---------- Doctors ----------
@main.route("/doctors")
def doctor_list():
    doctors = Doctor.query.all()
    return render_template("doctors.html", doctors=doctors)


@main.route("/doctors/add", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        doctor = Doctor(
            name=request.form["name"],
            specialization=request.form["specialization"],
            available=bool(request.form.get("available")),
        )
        db.session.add(doctor)
        db.session.commit()
        flash("Doctor added successfully.", "success")
        return redirect(url_for("main.doctor_list"))
    return render_template("add_doctor.html")


# ---------- Appointments ----------
@main.route("/appointments")
def appointment_list():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template("appointments.html", appointments=appointments)


@main.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    if request.method == "POST":
        appt = Appointment(
            patient_id=int(request.form["patient_id"]),
            doctor_id=int(request.form["doctor_id"]),
            date=request.form["date"],
            time=request.form["time"],
            reason=request.form.get("reason"),
        )
        db.session.add(appt)
        db.session.commit()
        flash("Appointment booked.", "success")
        return redirect(url_for("main.appointment_list"))
    return render_template("add_appointment.html", patients=patients, doctors=doctors)


# ---------- ML API (standalone endpoint, e.g. for a chatbot/triage widget) ----------
@main.route("/api/predict-risk", methods=["POST"])
def api_predict_risk():
    data = request.get_json(force=True)
    required = ["age", "resting_bp", "cholesterol", "bmi", "max_heart_rate",
                "smoker", "exercise_hours_week", "family_history"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    prob, label = predict_risk(data)
    return jsonify({"risk_probability": prob, "risk_label": label})
