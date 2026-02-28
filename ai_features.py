import numpy as np
import matplotlib.pyplot as plt
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image

DB_FILE = "patients.json"

# =============================
# RISK CALCULATION
# =============================
def calculate_risk(age, weight, heart_rate, blood_pressure, glucose, smoking):

    risk = (
        age * 0.2 +
        weight * 0.1 +
        heart_rate * 0.2 +
        blood_pressure * 0.2 +
        glucose * 0.2 +
        (15 if smoking == "Yes" else 0)
    )

    return min(risk / 2, 100)


# =============================
# AI RECOMMENDATIONS
# =============================
def generate_recommendations(risk):

    if risk < 30:
        return [
            "Maintain healthy lifestyle",
            "Exercise regularly",
            "Annual health check"
        ]

    elif risk < 60:
        return [
            "Reduce salt intake",
            "Monitor blood pressure",
            "Improve sleep quality"
        ]

    else:
        return [
            "Consult doctor immediately",
            "Monitor glucose daily",
            "Reduce stress and smoking"
        ]


# =============================
# RISK GAUGE CHART
# =============================
def create_risk_chart(risk):

    fig, ax = plt.subplots()

    ax.pie(
        [risk, 100-risk],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )

    ax.text(
        0, 0,
        f"{risk:.1f}%",
        ha='center',
        va='center',
        fontsize=20,
        fontweight='bold'
    )

    return fig


# =============================
# SAVE PATIENT
# =============================
def save_patient(data):

    try:
        with open(DB_FILE, "r") as f:
            patients = json.load(f)
    except:
        patients = []

    patients.append(data)

    with open(DB_FILE, "w") as f:
        json.dump(patients, f)


# =============================
# LOAD PATIENTS
# =============================
def load_patients():

    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# =============================
# PDF REPORT
# =============================
def generate_pdf_report(risk, recommendations):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, "AI Doctor Pro Medical Report")
    c.drawString(100, 720, f"Risk Score: {risk:.1f}%")

    y = 690
    for rec in recommendations:
        c.drawString(100, y, f"- {rec}")
        y -= 20

    c.save()
    buffer.seek(0)

    return buffer


# =============================
# IMAGE ANALYSIS (Demo AI)
# =============================
def analyze_medical_image(file):

    img = Image.open(file)

    width, height = img.size

    if width * height > 500000:
        return "Possible abnormal tissue detected (AI estimation)"
    else:
        return "No major abnormalities detected"
