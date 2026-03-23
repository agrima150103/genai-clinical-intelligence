import streamlit as st
import json

from modules.clinical_agent import extract_clinical_signals
from modules.compliance_agent import check_compliance
from modules.risk_agent import calculate_risk
from modules.explanation_agent import generate_explanation
from modules.audit_agent import generate_audit_log

st.set_page_config(page_title="GenAI Atlas", layout="wide")

# ================= SAFE CSS =================
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Remove extra top/bottom space */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}

/* Remove unwanted lines (hr elements) */
hr {
    display: none !important;
}

/* Remove empty paragraphs */
p:empty {
    display: none;
}

/* Card styling */
.card {
    background: rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 14px;
    backdrop-filter: blur(8px);
}

/* Signal pills */
.signal {
    display:inline-block;
    padding:8px 14px;
    border-radius:20px;
    margin:5px;
    color:white;
    font-weight:500;
}

.red { background:#ff4b4b; }
.green { background:#00c853; }

/* Risk banners */
.risk-high {
    background: linear-gradient(90deg, #ff0000, #ff4b4b);
    padding: 16px;
    border-radius: 12px;
    text-align:center;
    font-weight:bold;
    color:white;
}

.risk-low {
    background: linear-gradient(90deg, #00c853, #00e676);
    padding: 16px;
    border-radius: 12px;
    text-align:center;
    font-weight:bold;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🧠 GenAI Atlas - Clinical Intelligence Dashboard")
st.caption("AI-powered Multi-Agent Clinical Decision System")

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("📂 Upload Patient Case JSON", type="json")

if uploaded_file:

    case_data = json.load(uploaded_file)

    # ================= PATIENT INFO =================
    col1, col2, col3 = st.columns(3)
    col1.metric("Patient ID", case_data.get("patient_id"))
    col2.metric("Expected Days", case_data.get("expected_response_days"))
    col3.metric("Events", len(case_data.get("timeline", [])))

    # ================= TIMELINE =================
    st.subheader("🗂 Clinical Timeline")
    for event in case_data["timeline"]:
        st.write(f"📅 Day {event['day']} → {event['event']}")

    # ================= BUTTON =================
    if st.button("🚀 Run AI Analysis"):

        clinical_data = extract_clinical_signals(case_data)
        compliance_result = check_compliance(case_data, clinical_data)
        risk_result = calculate_risk(clinical_data, compliance_result)
        explanation = generate_explanation(clinical_data, compliance_result, risk_result)
        audit_logs = generate_audit_log(clinical_data, compliance_result, risk_result)

        risk = risk_result["risk"]

        # ================= RISK =================
        if risk == "High":
            st.markdown('<div class="risk-high">🚨 HIGH RISK PATIENT — IMMEDIATE ATTENTION REQUIRED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-low">✅ LOW RISK — STABLE CONDITION</div>', unsafe_allow_html=True)

        # ================= SIGNALS =================
        st.subheader("🧠 Clinical Signals")

        def pill(text, condition, icon):
            if condition:
                return f'<span class="signal red">{icon} {text}</span>'
            else:
                return f'<span class="signal green">{icon} {text}</span>'

        st.markdown(
            pill("Low Oxygen", clinical_data["low_oxygen"], "🫁") +
            pill("High Risk Age", clinical_data["high_risk_age"], "👴") +
            pill("Chest Pain", clinical_data["chest_pain"], "❤️"),
            unsafe_allow_html=True
        )

        # ================= COMPLIANCE =================
        st.subheader("⚖️ Compliance Check")

        if compliance_result["compliant"]:
            st.success("Treatment follows medical guidelines.")
        else:
            st.error("Compliance Violations Detected")
            for v in compliance_result["violations"]:
                st.write(f"• {v}")

        # ================= EXPLANATION =================
        st.subheader("📋 Clinical Explanation")
        for exp in explanation:
            st.write(f"• {exp}")

        # ================= AUDIT =================
        st.subheader("📊 Decision Audit Trail")
        for log in audit_logs:
            st.write(f"• {log}")

# ================= FOOTER =================
st.caption("⚡ Built for GenAI Hackathon | Multi-Agent Clinical Intelligence System")