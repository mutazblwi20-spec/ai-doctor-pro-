import numpy as np
import matplotlib.pyplot as plt
import json
import os

DATA_FILE = "patients.json"

# =============================
# BMI
# =============================
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m**2), 2)

# =============================
# Risk Calculator (AI Logic)
# =============================
def calculate_risk(age, bmi, heart_rate,
                   blood_pressure, glucose,
                   cholesterol, smoking, activity):

    score = 0

    score += age * 0.2
    score += bmi * 1.5
    score += heart_rate * 0.1
    score += blood_pressure * 0.15
    score += glucose * 0.2
    score += cholesterol * 0.15

    if smoking == "Yes":
        score += 15

    if activity == "Low":
        score += 10

    risk = min(score / 5, 100)
    return round(risk, 2)

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
            "Reduce sugar intake",
            "Monitor blood pressure"
        ]

    else:
        return [
            "Consult a doctor soon",
            "Perform full medical tests",
            "Lifestyle change required"
        ]

# =============================
# Gauge Chart
# =============================
def create_risk_chart(risk):

    fig, ax = plt.subplots()

    ax.pie(
        [risk, 100-risk],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )

    ax.text(0, 0, f"{risk}%", ha="center", va="center",
            fontsize=22, fontweight="bold")

    return fig

# =============================
# Save History
# =============================
def save_patient(data):

    history = load_patients()
    history.append(data)

    with open(DATA_FILE, "w") as f:
        json.dump(history, f)

# =============================
# Load History
# =============================
def load_patients():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)
