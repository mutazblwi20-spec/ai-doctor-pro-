 import streamlit as st
import pandas as pd
import os
from ai_features import *

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="centered"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#0d6efd;
}
.result-box{
    padding:25px;
    border-radius:15px;
    background:white;
    box-shadow:0px 5px 25px rgba(0,0,0,0.15);
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<p class="main-title">🩺 AI Doctor Pro</p>', unsafe_allow_html=True)
st.write("Smart Medical AI Assistant")

# ---------------- INPUTS ----------------
age = st.slider("Age", 1, 100, 30)
heart_rate = st.slider("Heart Rate", 40, 180, 75)
blood_pressure = st.slider("Blood Pressure", 80, 200, 120)
cholesterol = st.slider("Cholesterol", 100, 300, 180)
glucose = st.slider("Glucose", 70, 200, 100)
smoking = st.selectbox("Smoking", ["No", "Yes"])

# ---------------- ANALYSIS ----------------
if st.button("Analyze Health"):

    risk_score = (
        age * 0.15 +
        heart_rate * 0.15 +
        blood_pressure * 0.2 +
        cholesterol * 0.2 +
        glucose * 0.2 +
        (20 if smoking == "Yes" else 0)
    ) / 5

    if risk_score > 80:
        result = "⚠️ High Risk"
    elif risk_score > 50:
        result = "🟡 Medium Risk"
    else:
        result = "✅ Low Risk"

    st.markdown(
        f'<div class="result-box"><h2>{result}</h2></div>',
        unsafe_allow_html=True
    )

    # -------- SAVE PATIENT --------
    save_patient_data({
        "age": age,
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "cholesterol": cholesterol,
        "glucose": glucose,
        "risk": risk_score
    })

# ---------------- DASHBOARD ----------------
st.subheader("📊 Patient Risk Trend")

history = load_patient_history()

if len(history) > 0:
    risks = history["risk"].tolist()
    fig = plot_risk_trend(risks)
    st.pyplot(fig)
else:
    st.info("No patient history yet.")