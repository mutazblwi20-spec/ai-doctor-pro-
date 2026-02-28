import streamlit as st
import pandas as pd
from datetime import datetime
from ai_features import draw_gauge, trend_chart

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Doctor Pro — Final Version")

# ---------------- INPUTS ----------------
st.header("Patient Data")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", 1, 100, 30)
    weight = st.slider("Weight (kg)", 40, 150, 70)

with col2:
    heart_rate = st.slider("Heart Rate", 40, 180, 75)
    blood_pressure = st.slider("Blood Pressure", 80, 200, 120)

with col3:
    glucose = st.slider("Glucose", 70, 200, 100)
    smoking = st.selectbox("Smoking", ["No", "Yes"])

# ---------------- RISK ----------------
def calculate_risk():
    risk = (
        age * 0.2 +
        weight * 0.1 +
        heart_rate * 0.2 +
        blood_pressure * 0.2 +
        glucose * 0.2 +
        (20 if smoking == "Yes" else 0)
    )
    return min(risk / 2, 100)

# ---------------- BUTTON ----------------
if st.button("Analyze Health"):

    risk = calculate_risk()

    st.subheader(f"Risk Score: {risk:.1f}%")

    fig = draw_gauge(risk)
    st.pyplot(fig)

    if risk < 30:
        st.success("Low Risk — maintain healthy lifestyle.")
    elif risk < 60:
        st.warning("Moderate Risk — monitor health regularly.")
    else:
        st.error("High Risk — medical consultation recommended.")

    history = [{"risk": risk}]
    trend = trend_chart(history)
    st.pyplot(trend)
