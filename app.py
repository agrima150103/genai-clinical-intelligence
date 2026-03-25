import streamlit as st
import json

from modules.clinical_agent import extract_clinical_signals
from modules.compliance_agent import check_compliance
from modules.risk_agent import calculate_risk
from modules.explanation_agent import generate_explanation
from modules.audit_agent import generate_audit_log
from modules.reasoning_engine import analyze_case

st.set_page_config(page_title="GenAI Atlas", layout="wide")

st.markdown("""
<style>
.block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
hr { display: none !important; }
p:empty { display: none; }

.card {
    background: rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 14px;
}

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
    display: inline-block;
    background: #7c3aed;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 8px;
}
.fallback-badge {
    display: inline-block;
    background: #6b7280;
    color: white;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 8px;
}
.causal-box {
    background: rgba(124, 58, 237, 0.08);
    border-left: 4px solid #7c3aed;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-style: italic;
}
.whatif-box {
    background: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #ef4444;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.title("🧠 GenAI Atlas — Clinical Intelligence Dashboard")
st.caption("AI-powered Multi-Agent Clinical Decision System | Powered by GPT-4o-mini")

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About GenAI Atlas")
    st.markdown("""
**GenAI Atlas** detects silent clinical failures before they escalate.

**Agents:**
- 🔬 Clinical Agent — signal extraction
- ⚖️ Compliance Agent — guideline checks
- ⚠️ Risk Agent — severity scoring
- 🧠 Reasoning Engine — LLM causal analysis
- 📋 Explanation Agent — plain-language summary
- 📊 Audit Agent — decision trail

**GenAI Layer:**
- GPT-4o-mini for causal reasoning
- Structured JSON output
- What-if scenario generation
- Fallback to rule-based logic if LLM unavailable
    """)

# ── FILE UPLOAD ──────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Patient Case JSON", type="json")

if uploaded_file:
    case_data = json.load(uploaded_file)

    # Patient info
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patient ID", case_data.get("patient_id", "N/A"))
    col2.metric("Age", case_data.get("age", "N/A"))
    col3.metric("Expected recovery (days)", case_data.get("expected_response_days", "N/A"))
    col4.metric("Timeline events", len(case_data.get("timeline", [])))

    # Diagnosis + comorbidities
    st.markdown(f"**Diagnosis:** {case_data.get('diagnosis', 'N/A')}")
    comorbidities = case_data.get("comorbidities", [])
    if comorbidities:
        st.markdown(f"**Comorbidities:** {', '.join(comorbidities)}")

    # Timeline
    st.subheader("🗂 Clinical Timeline")
    for event in case_data["timeline"]:
        st.write(f"📅 Day {event['day']} → {event['event']}")

    # ── RUN ANALYSIS ──────────────────────────────────────────────────────────
    if st.button("🚀 Run GenAI Analysis"):
        with st.spinner("Running multi-agent GenAI analysis..."):

            # Rule-based agents
            clinical_data   = extract_clinical_signals(case_data)
            compliance_result = check_compliance(case_data, clinical_data)
            risk_result     = calculate_risk(clinical_data, compliance_result)
            explanation     = generate_explanation(clinical_data, compliance_result, risk_result)
            audit_logs      = generate_audit_log(clinical_data, compliance_result, risk_result)

            # GenAI reasoning engine
            llm_result = analyze_case(case_data)

        risk = llm_result.get("risk", risk_result.get("risk", "Low"))
        source = llm_result.get("source", "fallback")

        # Source badge
        badge_html = (
            f'<span class="llm-badge">{llm_result.get("provider", "LLM")}</span>'
            if source == "llm"
            else '<span class="fallback-badge">Rule-based fallback</span>'
        )
        st.markdown(f"**Analysis source:** {badge_html}", unsafe_allow_html=True)

        # ── RISK BANNER ───────────────────────────────────────────────────────
        if risk == "High":
            st.markdown('<div class="risk-high">🚨 HIGH RISK — IMMEDIATE CLINICAL ATTENTION REQUIRED</div>', unsafe_allow_html=True)
        elif risk == "Medium":
            st.markdown('<div class="risk-medium">⚠️ MEDIUM RISK — URGENT REVIEW NEEDED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-low">✅ LOW RISK — STABLE CONDITION</div>', unsafe_allow_html=True)

        st.markdown("---")
        col_left, col_right = st.columns(2)

        with col_left:
            # ── CLINICAL SIGNALS ──────────────────────────────────────────────
            st.subheader("🔬 Clinical Signals")
            def pill(text, condition, icon):
                cls = "red" if condition else "green"
                return f'<span class="signal {cls}">{icon} {text}</span>'

            st.markdown(
                pill("Low oxygen",    clinical_data["low_oxygen"],     "🫁") +
                pill("High-risk age", clinical_data["high_risk_age"],  "👴") +
                pill("Chest pain",    clinical_data["chest_pain"],     "❤️") +
                pill("Worsening",     clinical_data["worsening"],      "📉") +
                pill("No improvement",clinical_data["no_improvement"], "⏱️"),
                unsafe_allow_html=True,
            )

            # ── COMPLIANCE ────────────────────────────────────────────────────
            st.subheader("⚖️ Compliance Check")
            if compliance_result["compliant"]:
                st.success("Treatment follows medical guidelines.")
            else:
                st.error("Compliance violations detected")
                for v in compliance_result["violations"]:
                    st.write(f"• {v}")

        with col_right:
            # ── LLM RECOMMENDATIONS ───────────────────────────────────────────
            st.subheader("💊 AI Recommendations")
            recs = llm_result.get("recommendations") or explanation
            for rec in recs:
                st.write(f"• {rec}")

            # Confidence
            confidence = llm_result.get("confidence", risk_result.get("confidence", 70))
            st.metric("Confidence score", f"{confidence}%")

        # ── CAUSAL REASONING (GenAI) ──────────────────────────────────────────
        causal = llm_result.get("causal_reasoning", "")
        if causal and source == "llm":
            st.subheader("🧠 GenAI Causal Reasoning")
            st.markdown(f'<div class="causal-box">{causal}</div>', unsafe_allow_html=True)

        # ── WHAT-IF SCENARIO (GenAI) ──────────────────────────────────────────
        what_if = llm_result.get("what_if", "")
        if what_if and source == "llm":
            st.subheader("🔮 What If No Action Is Taken?")
            st.markdown(f'<div class="whatif-box">{what_if}</div>', unsafe_allow_html=True)

        # ── EXPLANATION ───────────────────────────────────────────────────────
        st.subheader("📋 Clinical Explanation")
        llm_explanations = llm_result.get("explanations") or explanation
        for exp in llm_explanations:
            st.write(f"• {exp}")

        # ── AUDIT TRAIL ───────────────────────────────────────────────────────
        st.subheader("📊 Decision Audit Trail")
        for log in audit_logs:
            st.write(f"• {log}")
        if source == "llm":
            st.write("• Step 4: LLM reasoning engine called — Groq (Llama3)")
            st.write("• Step 5: Causal reasoning and what-if scenario generated")

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.caption("⚡ GenAI Atlas | ET Gen AI Hackathon | Multi-Agent Clinical Intelligence System")