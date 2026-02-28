import streamlit as st
from ai_features import *

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#0d6efd;
}
.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🩺 AI Doctor Pro</p>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.sidebar.header("Patient Data")

age = st.sidebar.slider("Age", 1, 100, 30)
heart_rate = st.sidebar.slider("Heart Rate", 40, 180, 75)
blood_pressure = st.sidebar.slider("Blood Pressure", 80, 200, 120)
glucose = st.sidebar.slider("Glucose", 60, 200, 100)
bmi = st.sidebar.slider("BMI", 15.0, 40.0, 24.0)
smoking = st.sidebar.selectbox("Smoking", ["No", "Yes"])

# ---------------- ANALYSIS ----------------
if st.sidebar.button("Analyze Health"):

    risk = calculate_risk(
        age,
        heart_rate,
        blood_pressure,
        glucose,
        bmi,
        smoking
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Gauge")
        st.plotly_chart(risk_gauge(risk), use_container_width=True)

    with col2:
        st.subheader("AI Recommendation")
        st.success(ai_recommendation(risk))

    st.subheader("Patient Risk Trend")
    st.pyplot(risk_trend_chart(risk))
