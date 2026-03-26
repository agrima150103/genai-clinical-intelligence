import streamlit as st
import json

from modules.clinical_agent import extract_clinical_signals
from modules.compliance_agent import check_compliance
from modules.risk_agent import calculate_risk
from modules.explanation_agent import generate_explanation
from modules.audit_agent import generate_audit_log
from modules.reasoning_engine import analyze_case

st.set_page_config(page_title="GenAI Atlas", layout="wide")

# ── STYLING ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }

.signal {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 20px;
    margin: 5px;
    color: white;
    font-weight: 500;
}
.red   { background: #ff4b4b; }
.green { background: #00c853; }

.risk-high {
    background: linear-gradient(90deg, #ff0000, #ff4b4b);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: white;
}
.risk-medium {
    background: linear-gradient(90deg, #ff8c00, #ffa500);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: white;
}
.risk-low {
    background: linear-gradient(90deg, #00c853, #00e676);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: white;
}

.llm-badge {
    background: #7c3aed;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
}
.fallback-badge {
    background: #6b7280;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
}

.causal-box {
    background: rgba(124, 58, 237, 0.08);
    border-left: 4px solid #7c3aed;
    padding: 14px;
    border-radius: 8px;
}
.whatif-box {
    background: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #ef4444;
    padding: 14px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.title("🧠 GenAI Atlas — Clinical Intelligence Dashboard")
st.caption("AI-powered Multi-Agent Clinical Decision System | Powered by Groq (Llama3)")

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About GenAI Atlas")
    st.markdown("""
GenAI Atlas detects silent clinical failures before they escalate.

Agents:
- Clinical Agent — signal extraction  
- Compliance Agent — guideline checks  
- Risk Agent — severity scoring  
- Reasoning Engine — LLM causal analysis  
- Explanation Agent — plain-language summary  
- Audit Agent — decision trail  
""")

    st.markdown("---")

    # ✅ FIXED SETTINGS BLOCK (THIS WAS YOUR ERROR)
    st.header("⚙️ Settings")

    mode = st.radio(
        "Decision Mode",
        ["Hybrid", "LLM Only", "Rule-Based Only"]
    )

# ── FILE UPLOAD ──────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Patient Case JSON", type="json")

if uploaded_file:
    case_data = json.load(uploaded_file)

    # ── PATIENT INFO ────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patient ID", case_data.get("patient_id", "N/A"))
    col2.metric("Age", case_data.get("age", "N/A"))
    col3.metric("Expected recovery (days)", case_data.get("expected_response_days", "N/A"))
    col4.metric("Timeline events", len(case_data.get("timeline", [])))

    st.markdown(f"**Diagnosis:** {case_data.get('diagnosis', 'N/A')}")

    if case_data.get("comorbidities"):
        st.markdown(f"**Comorbidities:** {', '.join(case_data['comorbidities'])}")

    # ── TIMELINE ────────────────────────────────────────────────────────────
    st.subheader("🗂 Clinical Timeline")
    for event in case_data["timeline"]:
        st.write(f"Day {event['day']} → {event['event']}")

    # ── RUN ANALYSIS ────────────────────────────────────────────────────────
    if st.button("🚀 Run GenAI Analysis"):
        with st.spinner("Running analysis..."):

            clinical_data = extract_clinical_signals(case_data)
            compliance_result = check_compliance(case_data, clinical_data)
            risk_result = calculate_risk(clinical_data, compliance_result)
            explanation = generate_explanation(clinical_data, compliance_result, risk_result)
            audit_logs = generate_audit_log(clinical_data, compliance_result, risk_result)

            llm_result = analyze_case(case_data)

        # ── MODE SWITCH LOGIC ───────────────────────────────────────────────
        if mode == "LLM Only":
            final_risk = llm_result.get("risk", "Low")
            source = "llm"

        elif mode == "Rule-Based Only":
            final_risk = risk_result["risk"]
            source = "fallback"

        else:  # Hybrid
            final_risk = risk_result["risk"]
            source = llm_result.get("source", "fallback")

        # ── DEBUG PANEL ─────────────────────────────────────────────────────
        with st.expander("🔍 Debug Panel"):
            st.write("Rule Risk:", risk_result["risk"])
            st.write("LLM Risk:", llm_result.get("risk"))
            st.write("Mode:", mode)

        # ── SOURCE BADGE ────────────────────────────────────────────────────
        if source == "llm":
            st.markdown('<span class="llm-badge">LLM Powered</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="fallback-badge">Rule-Based</span>', unsafe_allow_html=True)

        # ── RISK BANNER ─────────────────────────────────────────────────────
        if final_risk == "High":
            st.markdown('<div class="risk-high">HIGH RISK</div>', unsafe_allow_html=True)
        elif final_risk == "Medium":
            st.markdown('<div class="risk-medium">MEDIUM RISK</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-low">LOW RISK</div>', unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        # ── LEFT ────────────────────────────────────────────────────────────
        with col1:
            st.subheader("Clinical Signals")

            def pill(text, condition):
                cls = "red" if condition else "green"
                return f'<span class="signal {cls}">{text}</span>'

            st.markdown(
                pill("Low oxygen", clinical_data["low_oxygen"]) +
                pill("High-risk age", clinical_data["high_risk_age"]) +
                pill("Chest pain", clinical_data["chest_pain"]) +
                pill("Worsening", clinical_data["worsening"]) +
                pill("No improvement", clinical_data["no_improvement"]),
                unsafe_allow_html=True,
            )

            st.subheader("Compliance")
            if compliance_result["compliant"]:
                st.success("Compliant")
            else:
                st.error("Violations detected")
                for v in compliance_result["violations"]:
                    st.write("•", v)

        # ── RIGHT ───────────────────────────────────────────────────────────
        with col2:
            st.subheader("Recommendations")

            recs = llm_result.get("recommendations") or explanation
            for r in recs:
                st.write("•", r)

            confidence = llm_result.get("confidence", 70)
            st.metric("Confidence", f"{confidence}%")

        # ── LLM EXTRA OUTPUT ────────────────────────────────────────────────
        if source == "llm":
            if llm_result.get("causal_reasoning"):
                st.subheader("Causal Reasoning")
                st.markdown(f'<div class="causal-box">{llm_result["causal_reasoning"]}</div>', unsafe_allow_html=True)

            if llm_result.get("what_if"):
                st.subheader("What If Scenario")
                st.markdown(f'<div class="whatif-box">{llm_result["what_if"]}</div>', unsafe_allow_html=True)

        # ── EXPLANATION ─────────────────────────────────────────────────────
        st.subheader("Explanation")
        for e in (llm_result.get("explanations") or explanation):
            st.write("•", e)

        # ── AUDIT ───────────────────────────────────────────────────────────
        st.subheader("Audit Trail")
        for log in audit_logs:
            st.write("•", log)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.caption("GenAI Atlas | Multi-Agent Clinical Intelligence System")