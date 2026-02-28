import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from ai_features import (
    calculate_risk,
    generate_recommendations,
    create_risk_chart,
    save_patient,
    load_patients,
    generate_pdf_report,
    analyze_medical_image
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🩺",
    layout="wide"
)

# ---------------- DARK MODE ----------------
st.markdown("""
<style>
body {
    background-color:#0e1117;
    color:white;
}
.block-container {
    padding-top:2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🩺 AI Doctor Pro — Medical AI Dashboard")

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "Navigation",
    ["🏥 Dashboard", "🤖 AI Doctor Chat", "🧠 Image Analysis", "📊 Patient History"]
)

# =====================================================
# 🏥 DASHBOARD
# =====================================================
if page == "🏥 Dashboard":

    st.header("Patient Health Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 1, 100, 30)
        weight = st.slider("Weight (kg)", 30, 150, 70)

    with col2:
        heart_rate = st.slider("Heart Rate", 40, 180, 75)
        blood_pressure = st.slider("Blood Pressure", 80, 200, 120)

    with col3:
        glucose = st.slider("Glucose", 70, 200, 100)
        smoking = st.selectbox("Smoking", ["No", "Yes"])

    if st.button("Analyze Health"):

        risk = calculate_risk(
            age, weight, heart_rate,
            blood_pressure, glucose, smoking
        )

        st.subheader(f"Risk Score: {risk:.1f}%")

        fig = create_risk_chart(risk)
        st.pyplot(fig)

        recommendations = generate_recommendations(risk)

        st.success("AI Recommendations")
        for r in recommendations:
            st.write("✅", r)

        save_patient({
            "date": str(datetime.now()),
            "risk": risk
        })

        pdf = generate_pdf_report(risk, recommendations)

        st.download_button(
            "📄 Download Medical Report",
            pdf,
            file_name="medical_report.pdf"
        )

# =====================================================
# 🤖 AI CHAT
# =====================================================
elif page == "🤖 AI Doctor Chat":

    st.header("AI Doctor Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Describe your symptoms...")

    if user_input:
        st.session_state.messages.append(("You", user_input))
        response = "Based on your symptoms, I recommend medical evaluation and healthy monitoring."
        st.session_state.messages.append(("AI Doctor", response))

    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")

# =====================================================
# 🧠 IMAGE ANALYSIS
# =====================================================
elif page == "🧠 Image Analysis":

    st.header("Medical Image Analysis")

    file = st.file_uploader("Upload Medical Image")

    if file:
        result = analyze_medical_image(file)
        st.image(file)
        st.success(result)

# =====================================================
# 📊 HISTORY
# =====================================================
elif page == "📊 Patient History":

    st.header("Patient History")

    data = load_patients()

    if len(data) > 0:
        df = pd.DataFrame(data)
        st.dataframe(df)

        fig = create_risk_chart(df["risk"].iloc[-1])
        st.pyplot(fig)
    else:
        st.info("No patient history yet.")
