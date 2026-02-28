import json
import os
import matplotlib.pyplot as plt

DATA_FILE = "patients.json"

# =============================
# Risk Calculation
# =============================
def calculate_risk(age, bmi, heart_rate,
                   blood_pressure, glucose,
                   cholesterol, smoking):

    risk = (
        age * 0.15 +
        bmi * 0.2 +
        heart_rate * 0.1 +
        blood_pressure * 0.15 +
        glucose * 0.2 +
        cholesterol * 0.1 +
        (15 if smoking == "Yes" else 0)
    )

    return min(risk / 3, 100)


# =============================
# Recommendations
# =============================
def generate_recommendations(risk):

    if risk < 30:
        return [
            "Maintain healthy lifestyle",
            "Exercise regularly",
            "Annual medical check"
        ]

    elif risk < 60:
        return [
            "Improve diet",
            "Monitor blood pressure",
            "Reduce stress"
        ]

    else:
        return [
            "Consult doctor soon",
            "Monitor glucose daily",
            "Lifestyle change required"
        ]


# =============================
# Gauge Chart
# =============================
def draw_gauge(risk):

    fig, ax = plt.subplots()

    ax.pie(
        [risk, 100-risk],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )

    ax.text(
        0, 0,
        f"{risk:.0f}%",
        ha='center',
        va='center',
        fontsize=22,
        fontweight='bold'
    )

    return fig


# =============================
# Save Patient
# =============================
def save_patient(data):

    history = load_patients()
    history.append(data)

    with open(DATA_FILE, "w") as f:
        json.dump(history, f)


# =============================
# Load Patients
# =============================
def load_patients():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


# =============================
# Trend Chart
# =============================
def trend_chart(history):

    risks = [h["risk"] for h in history]

    fig, ax = plt.subplots()
    ax.plot(risks, marker="o")
    ax.set_title("Patient Risk Trend")
    ax.set_ylabel("Risk %")
    ax.set_xlabel("Visits")

    return fig
