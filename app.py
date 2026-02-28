import streamlit as st
import pandas as pd
from datetime import datetime
from ai_features import *

st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="wide"
)

# -------- DARK MODE ----------
st.markdown("""
<style>
body {background-color:#0e1117;color:white;}
</style>
""", unsafe_allow_html=True)

st.title("🩺 AI Doctor Pro — Smart Medical Dashboard")

page = st.sidebar.selectbox(
    "Navigation",
    ["🏥 Dashboard", "🤖 AI Doctor Chat", "📊 Patient History"]
)

# =================================================
# DASHBOARD
# =================================================
if page == "🏥 Dashboard":

    st.header("Patient Health Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 1, 100, 30)
        weight = st.slider("Weight (kg)", 30, 150, 70)
        height = st.slider("Height (cm)", 120, 210, 170)

    with col2:
        heart_rate = st.slider("Heart Rate", 40, 180, 75)
        blood_pressure = st.slider("Blood Pressure", 80, 200, 120)
        glucose = st.slider("Glucose", 70, 250, 100)

    with col3:
        cholesterol = st.slider("Cholesterol", 100, 300, 180)
        smoking = st.selectbox("Smoking", ["No", "Yes"])
        activity = st.selectbox("Physical Activity", ["High", "Medium", "Low"])

    if st.button("Analyze Health"):

        bmi = calculate_bmi(weight, height)

        risk = calculate_risk(
            age, bmi, heart_rate,
            blood_pressure, glucose,
            cholesterol, smoking, activity
        )

        st.subheader(f"Risk Score: {risk}%")
        st.write(f"BMI: {bmi}")

        fig = create_risk_chart(risk)
        st.pyplot(fig)

        recs = generate_recommendations(risk)

        st.success("AI Recommendations")
        for r in recs:
            st.write("✅", r)

        save_patient({
            "date": str(datetime.now()),
            "risk": risk,
            "bmi": bmi
        })

# =================================================
# CHAT
# =================================================
elif page == "🤖 AI Doctor Chat":

    st.header("AI Doctor Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    msg = st.chat_input("Describe symptoms...")

    if msg:
        st.session_state.messages.append(("You", msg))
        st.session_state.messages.append(
            ("AI Doctor",
             "Please monitor symptoms and consult physician if persistent.")
        )

    for role, m in st.session_state.messages:
        st.write(f"**{role}:** {m}")

# =================================================
# HISTORY
# =================================================
elif page == "📊 Patient History":

    data = load_patients()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.info("No history yet.")
