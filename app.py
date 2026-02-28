import streamlit as st
import pandas as pd
from datetime import datetime
from ai_features import (
    calculate_risk,
    generate_recommendations,
    draw_gauge,
    save_patient,
    load_patients,
    trend_chart
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Doctor Pro — Smart Medical Dashboard")

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "Navigation",
    ["🏥 Dashboard", "🤖 AI Doctor Chat", "📊 Patient History"]
)

# =====================================================
# 🏥 DASHBOARD
# =====================================================
if page == "🏥 Dashboard":

    st.header("Patient Health Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Patient Name")
        age = st.slider("Age", 1, 100, 30)
        weight = st.slider("Weight (kg)", 30, 150, 70)

    with col2:
        height = st.slider("Height (cm)", 120, 220, 170)
        heart_rate = st.slider("Heart Rate", 40, 180, 75)
        blood_pressure = st.slider("Blood Pressure", 80, 200, 120)

    with col3:
        glucose = st.slider("Glucose", 70, 250, 100)
        cholesterol = st.slider("Cholesterol", 100, 300, 180)
        smoking = st.selectbox("Smoking", ["No", "Yes"])

    if st.button("Analyze Health"):

        bmi = weight / ((height/100) ** 2)

        risk = calculate_risk(
            age, bmi, heart_rate,
            blood_pressure, glucose,
            cholesterol, smoking
        )

        st.subheader(f"Risk Score: {risk:.1f}%")

        fig = draw_gauge(risk)
        st.pyplot(fig)

        st.success("AI Recommendations")
        recs = generate_recommendations(risk)

        for r in recs:
            st.write("✅", r)

        save_patient({
            "name": name,
            "date": str(datetime.now()),
            "risk": risk
        })

# =====================================================
# 🤖 AI CHAT
# =====================================================
elif page == "🤖 AI Doctor Chat":

    st.header("AI Doctor Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Describe symptoms...")

    if user_input:
        st.session_state.messages.append(("You", user_input))

        response = """
Based on your symptoms:
• Stay hydrated
• Monitor vitals
• Seek medical consultation if symptoms persist
"""
        st.session_state.messages.append(("AI Doctor", response))

    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")

# =====================================================
# 📊 HISTORY
# =====================================================
elif page == "📊 Patient History":

    st.header("Patient History")

    data = load_patients()

    if len(data) > 0:
        df = pd.DataFrame(data)
        st.dataframe(df)

        fig = trend_chart(data)
        st.pyplot(fig)
    else:
        st.info("No patient history yet.")
