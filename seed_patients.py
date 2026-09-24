"""
Adds a handful of demo patients with varied profiles so you can see the
AI risk model produce a realistic spread of Low / Moderate / High results.

Run once, after the database and model already exist:
    python seed_patients.py
"""
from app import create_app, db
from app.models import Patient, Doctor
from app.ml.predictor import predict_risk

DEMO_PATIENTS = [
    # name, age, gender, contact, resting_bp, cholesterol, bmi, max_hr, smoker, exercise, family_history
    ("Anjali Mehta", 24, "Female", "9000000001", 110, 170, 21, 195, False, 6, False),
    ("Suresh Nair", 45, "Male", "9000000002", 130, 210, 27, 165, False, 3, True),
    ("Ramesh Kumar", 58, "Male", "9000000003", 150, 260, 31, 140, True, 0.5, True),
    ("Priya Sharma", 35, "Female", "9000000004", 118, 190, 23, 178, False, 5, False),
    ("Arjun Reddy", 62, "Male", "9000000005", 160, 280, 33, 125, True, 0, True),
    ("Kavya Iyer", 29, "Female", "9000000006", 115, 180, 22, 188, False, 4, False),
    ("Vikram Joshi", 50, "Male", "9000000007", 140, 230, 29, 150, True, 1, False),
]


def seed():
    app = create_app()
    with app.app_context():
        if Doctor.query.count() == 0:
            db.session.add(Doctor(name="Dr. Asha Rao", specialization="Cardiology", available=True))
            db.session.add(Doctor(name="Dr. Vikram Singh", specialization="General Medicine", available=True))
            db.session.add(Doctor(name="Dr. Meera Pillai", specialization="Endocrinology", available=True))
            db.session.commit()
            print("3 demo doctors added.\n")

        added = 0
        for (name, age, gender, contact, bp, chol, bmi, hr, smoker,
             exercise, fam_hist) in DEMO_PATIENTS:

            if Patient.query.filter_by(name=name).first():
                continue  # skip if already added

            vitals = {
                "age": age, "resting_bp": bp, "cholesterol": chol, "bmi": bmi,
                "max_heart_rate": hr, "smoker": int(smoker),
                "exercise_hours_week": exercise, "family_history": int(fam_hist),
            }
            prob, label = predict_risk(vitals)

            patient = Patient(
                name=name, age=age, gender=gender, contact=contact,
                resting_bp=bp, cholesterol=chol, bmi=bmi, max_heart_rate=hr,
                smoker=smoker, exercise_hours_week=exercise, family_history=fam_hist,
                risk_score=prob, risk_label=label,
            )
            db.session.add(patient)
            added += 1
            print(f"{name:15s} age={age:2d}  ->  {label:8s} ({prob*100:.1f}%)")

        db.session.commit()
        print(f"\n{added} demo patients added.")


if __name__ == "__main__":
    seed()
