# Hospital Management System with AI/ML (Heart-Disease Risk Prediction)

A Flask-based Hospital Management System with an integrated Machine Learning
module that predicts a patient's heart-disease risk from their vitals.

## Features
- Patient / Doctor / Appointment management (CRUD)
- AI risk prediction automatically computed when a patient is added
  (Random Forest classifier — Low / Moderate / High risk)
- REST API endpoint (`/api/predict-risk`) so the ML model can be reused by
  a chatbot, mobile app, or any other client
- Simple, clean dashboard UI

## Project Structure
```
hms_ai/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models (Patient, Doctor, Appointment)
│   ├── routes.py            # All routes + ML integration
│   ├── ml/
│   │   ├── train_model.py   # Trains and saves the risk model
│   │   └── predictor.py     # Loads model, exposes predict_risk()
│   ├── templates/           # Jinja2 HTML templates
│   └── static/
├── models/                  # Saved trained model (.joblib)
├── data/                    # SQLite database (auto-created)
├── requirements.txt
└── run.py                   # Entry point
```

## Setup

```bash
pip install -r requirements.txt

# 1. Train the ML model (only needed once, or to retrain)
python app/ml/train_model.py

# 2. Run the app
python run.py
```

Then open http://localhost:5000

## About the ML Model
`train_model.py` currently trains on a **synthetic dataset** (~2000 rows)
generated with realistic risk relationships between age, blood pressure,
cholesterol, BMI, smoking, exercise, and family history. This was necessary
because this environment has no internet access to UCI/Kaggle.

**For a real submission, swap in a real dataset**, e.g. the UCI Heart Disease
dataset (or Kaggle's version) — just replace `generate_synthetic_data()` with
a `pd.read_csv(...)` call using the same column names, and the rest of the
pipeline (train/save/predict/Flask integration) needs no changes.

Model performance on the synthetic data: ~69% accuracy (intentionally
realistic — not overfit/perfect, since real medical risk prediction is a
genuinely hard, noisy problem).

## Extending This Project
Ideas to add for a stronger final submission:
- **Appointment no-show prediction** (needs historical appointment data with
  outcomes — can also be synthetic)
- **Symptom-based triage chatbot** (simple intent classifier or LLM API call)
- **Authentication** (admin / doctor / patient login roles)
- **Charts on the dashboard** (e.g. Chart.js for risk distribution over time)
- **Real dataset** swap-in as described above, with proper train/test
  evaluation and a confusion matrix in your report
