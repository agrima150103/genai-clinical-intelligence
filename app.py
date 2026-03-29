import streamlit as st
import streamlit.components.v1 as components
import json

from modules.clinical_agent import extract_clinical_signals
from modules.compliance_agent import check_compliance
from modules.risk_agent import calculate_risk
from modules.explanation_agent import generate_explanation
from modules.audit_agent import generate_audit_log
from modules.reasoning_engine import analyze_case

st.set_page_config(page_title="GenAI Atlas", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "mode" not in st.session_state:
    st.session_state.mode = "Hybrid"

if "applied_mode" not in st.session_state:
    st.session_state.applied_mode = "Hybrid"

if "case_data" not in st.session_state:
    st.session_state.case_data = None

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None


def toggle_about():
    st.session_state.page = "home" if st.session_state.page == "about" else "about"


def on_uploader_change():
    uploaded_file = st.session_state.get("case_uploader")
    if uploaded_file is None:
        return

    new_case = json.loads(uploaded_file.getvalue().decode("utf-8"))
    new_name = uploaded_file.name

    if st.session_state.uploaded_name != new_name or st.session_state.case_data != new_case:
        st.session_state.case_data = new_case
        st.session_state.uploaded_name = new_name
        st.session_state.analysis = None


def run_analysis():
    case_data = st.session_state.case_data
    if not case_data:
        return

    with st.spinner("Running multi-agent clinical analysis..."):
        clinical_data = extract_clinical_signals(case_data)
        compliance_result = check_compliance(case_data, clinical_data)
        risk_result = calculate_risk(clinical_data, compliance_result)
        explanation = generate_explanation(clinical_data, compliance_result, risk_result)
        audit_logs = generate_audit_log(clinical_data, compliance_result, risk_result)
        llm_result = analyze_case(case_data)

    st.session_state.analysis = {
        "clinical_data": clinical_data,
        "compliance_result": compliance_result,
        "risk_result": risk_result,
        "explanation": explanation,
        "audit_logs": audit_logs,
        "llm_result": llm_result,
    }
    st.session_state.applied_mode = st.session_state.mode


def get_mode_view_data():
    analysis = st.session_state.analysis
    if not analysis:
        return None

    risk_result = analysis["risk_result"]
    explanation = analysis["explanation"]
    llm_result = analysis["llm_result"]

    mode = st.session_state.applied_mode

    if mode == "LLM Only":
        final_risk = llm_result.get("risk", "Low")
        recommendations = llm_result.get("recommendations", [])
        explanations = llm_result.get("explanations", [])
        source = "llm"
        mode_label = "🤖 LLM Mode: Pure AI reasoning"

    elif mode == "Rule-Based Only":
        final_risk = risk_result["risk"]
        recommendations = explanation
        explanations = explanation
        source = "rule"
        mode_label = "📏 Rule-Based Mode: Deterministic clinical logic"

    else:
        final_risk = risk_result["risk"]
        recommendations = (
            ["[RULE] " + r for r in explanation]
            + ["[AI] " + r for r in llm_result.get("recommendations", [])]
        )
        explanations = explanation + llm_result.get("explanations", [])
        source = "hybrid"
        mode_label = "⚡ Hybrid Mode: Rule-based detection + AI reasoning"

    return {
        "final_risk": final_risk,
        "recommendations": recommendations,
        "explanations": explanations,
        "source": source,
        "mode_label": mode_label,
        "applied_mode": mode,
    }


st.markdown(
    """
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

html, body, [class*="css"] {
    background-color: #091413;
    color: white;
    scroll-behavior: smooth;
}

.stApp {
    background: #091413;
    color: white;
}

.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1500px;
}

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(176, 228, 204, 0.18);
    background: #0d1a1a;
    color: white;
    transition: 0.18s ease;
}
.stButton > button:hover {
    border-color: #408A71;
    color: white;
}

.top-controls {
    margin-bottom: 0.65rem;
}

div[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}

div[data-testid="stExpander"] details {
    border: none !important;
    background: transparent !important;
}

div[data-testid="stExpander"] summary {
    list-style: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.5rem !important;
    min-height: 64px !important;
    padding: 0.7rem 1.25rem !important;
    border-radius: 999px !important;
    background: #285A48 !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 8px 22px rgba(0,0,0,0.28) !important;
    transition: 0.18s ease !important;
    width: fit-content !important;
}

div[data-testid="stExpander"] summary:hover {
    background: #408A71 !important;
}

div[data-testid="stExpander"] summary::-webkit-details-marker {
    display: inline-block !important;
    color: white !important;
}

div[data-testid="stExpander"] details[open] summary {
    margin-bottom: 0.7rem !important;
}

div[data-testid="stExpander"] details > div {
    background: #0d1a1a !important;
    border: 1px solid rgba(176, 228, 204, 0.14) !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.25) !important;
    padding: 0.8rem 0.9rem !important;
    width: 250px !important;
    max-width: 250px !important;
}

div[data-testid="stExpander"] * {
    color: white !important;
}

div[data-testid="stExpander"] div[role="radiogroup"] {
    gap: 0.4rem !important;
}

.hero-wrap {
    margin-top: 1rem;
    margin-bottom: 2rem;
}
.hero-center {
    max-width: 1350px;
    margin: 0 auto;
    text-align: center;
}
.hero-title {
    font-size: 4.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.05;
    color: #F4F5F6;
    margin-bottom: 0.75rem;
    text-align: center;
}
.hero-subtitle {
    color: #B0E4CC;
    font-size: 1.45rem;
    margin-bottom: 0.8rem;
    text-align: center;
}
.hero-caption {
    color: rgba(255,255,255,0.55);
    margin-top: 1rem;
    text-align: left;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 0.75rem 0.75rem 0 0.75rem;
}

.section-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(176, 228, 204, 0.08);
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
}

.about-card {
    background: rgba(64, 138, 113, 0.10);
    border-left: 4px solid #408A71;
    padding: 18px 20px;
    border-radius: 0 16px 16px 0;
    min-height: 300px;
}
.about-card-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #F4F5F6;
    margin-bottom: 1rem;
}
.about-card-list {
    color: white;
    font-size: 1.05rem;
    line-height: 2.0;
}

.signal {
    display: inline-block;
    padding: 10px 16px;
    border-radius: 999px;
    margin: 6px 6px 6px 0;
    font-weight: 600;
    font-size: 14px;
    color: white;
    background: #2b7058;
}

.risk-high {
    background: linear-gradient(90deg, #9f1f1f, #d13232);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    font-weight: 700;
    color: white;
    margin: 0.75rem 0 1rem 0;
}
.risk-medium {
    background: linear-gradient(90deg, #9a6110, #d68a17);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    font-weight: 700;
    color: white;
    margin: 0.75rem 0 1rem 0;
}
.risk-low {
    background: linear-gradient(90deg, #285A48, #408A71);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    font-weight: 700;
    color: white;
    margin: 0.75rem 0 1rem 0;
}

.mode-pill {
    background: rgba(64, 138, 113, 0.16);
    border: 1px solid rgba(64, 138, 113, 0.35);
    color: #B0E4CC;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 1rem;
}

.pending-mode {
    background: rgba(176, 228, 204, 0.10);
    border: 1px solid rgba(176, 228, 204, 0.18);
    color: #B0E4CC;
    padding: 10px 14px;
    border-radius: 12px;
    margin-top: 0.75rem;
    margin-bottom: 0.75rem;
}

.causal-box {
    background: rgba(64, 138, 113, 0.10);
    border-left: 4px solid #408A71;
    padding: 14px 16px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 1rem;
}
.whatif-box {
    background: rgba(176, 228, 204, 0.08);
    border-left: 4px solid #B0E4CC;
    padding: 14px 16px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 1rem;
}

@media (max-width: 950px) {
    .hero-title { font-size: 2.7rem; }
    .hero-subtitle { font-size: 1.1rem; }
    .hero-wrap { margin-top: 1rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="top-controls">', unsafe_allow_html=True)

left_col, spacer_col, right_col = st.columns([2.6, 9, 1.2])

with left_col:
    with st.expander("⚙️ Settings", expanded=False):
        st.markdown("**Decision Mode**")
        st.radio(
            " ",
            ["Hybrid", "LLM Only", "Rule-Based Only"],
            key="mode",
            label_visibility="collapsed",
        )

with right_col:
    st.button("About", key="about_top_button", on_click=toggle_about)

st.markdown("</div>", unsafe_allow_html=True)

components.html(
    """
    <script>
    const doc = window.parent.document;

    if (!doc.body.dataset.expanderOutsideCloseBound) {
        doc.body.dataset.expanderOutsideCloseBound = "true";

        doc.addEventListener("click", function(event) {
            const openExpanders = doc.querySelectorAll('div[data-testid="stExpander"] details[open]');
            openExpanders.forEach(function(expander) {
                if (!expander.contains(event.target)) {
                    expander.removeAttribute("open");
                }
            });
        }, true);
    }
    </script>
    """,
    height=0,
)

if st.session_state.page == "about":
    st.markdown('<div class="hero-wrap"><div class="hero-center">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">About GenAI Atlas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">GenAI Atlas detects silent clinical failures before they escalate.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div></div>", unsafe_allow_html=True)

    col_agents, col_genai = st.columns(2, gap="large")

    with col_agents:
        st.markdown(
            """
<div class="about-card">
    <div class="about-card-title">Agents</div>
    <div class="about-card-list">
        • Clinical Agent — signal extraction<br>
        • Compliance Agent — guideline checks<br>
        • Risk Agent — severity scoring<br>
        • Reasoning Engine — LLM causal analysis<br>
        • Explanation Agent — plain-language summary<br>
        • Audit Agent — decision trail
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_genai:
        st.markdown(
            """
<div class="about-card">
    <div class="about-card-title">GenAI Layer</div>
    <div class="about-card-list">
        • LLM reasoning<br>
        • Structured outputs<br>
        • What-if scenarios<br>
        • Fallback support
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.stop()

st.markdown('<div class="hero-wrap"><div class="hero-center">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">GenAI Atlas — Clinical Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-powered Multi-Agent Clinical Decision System</div>', unsafe_allow_html=True)

st.file_uploader(
    "Upload Patient Case",
    type="json",
    key="case_uploader",
    on_change=on_uploader_change,
)

st.markdown("</div></div>", unsafe_allow_html=True)

case_data = st.session_state.case_data

if case_data:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patient ID", case_data.get("patient_id", "N/A"))
    col2.metric("Age", case_data.get("age", "N/A"))
    col3.metric("Expected recovery (days)", case_data.get("expected_response_days", "N/A"))
    col4.metric("Timeline events", len(case_data.get("timeline", [])))

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Clinical Timeline")
    for event in case_data["timeline"]:
        st.write(f"Day {event['day']} → {event['event']}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.analysis and st.session_state.mode != st.session_state.applied_mode:
        st.markdown(
            f"<div class='pending-mode'>Selected mode is <b>{st.session_state.mode}</b>. Click <b>Run GenAI Analysis</b> to refresh results from the last applied mode: <b>{st.session_state.applied_mode}</b>.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Run Analysis", key="run_analysis_button", on_click=run_analysis)

view = get_mode_view_data()

if view and st.session_state.analysis:
    analysis = st.session_state.analysis
    clinical_data = analysis["clinical_data"]
    compliance_result = analysis["compliance_result"]
    risk_result = analysis["risk_result"]
    audit_logs = analysis["audit_logs"]
    llm_result = analysis["llm_result"]

    final_risk = view["final_risk"]
    recommendations = view["recommendations"]
    explanations = view["explanations"]
    source = view["source"]
    mode_label = view["mode_label"]

    st.markdown(f"<div class='mode-pill'>{mode_label}</div>", unsafe_allow_html=True)

    if final_risk == "High":
        st.markdown('<div class="risk-high">🚨 HIGH RISK</div>', unsafe_allow_html=True)
    elif final_risk == "Medium":
        st.markdown('<div class="risk-medium">⚠️ MEDIUM RISK</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-low">✅ LOW RISK</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)

        st.subheader("Early Symptoms")
        early_symptoms = clinical_data.get("early_symptoms", [])
        if early_symptoms:
            st.markdown(
                "".join([f'<span class="signal">{symptom}</span>' for symptom in early_symptoms]),
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<span class="signal">No early symptoms captured</span>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("Clinical Signals")

        signal_labels = {
            "low_oxygen": "Low oxygen",
            "high_risk_age": "High-risk age",
            "chest_pain": "Chest pain",
            "worsening": "Worsening",
            "no_improvement": "No improvement",
            "tachycardia": "Tachycardia",
            "hypertension": "Hypertension",
            "treatment_failure": "Treatment failure",
            "improving": "Improving",
            "stable_recovery": "Stable recovery",
            "cardiac_risk": "Cardiac risk",
            "missing_ecg": "Missing ECG",
            "overdose_risk": "Overdose risk",
            "mental_health_risk": "Mental health risk",
            "missing_psychiatric_eval": "Missing psych eval",
            "unsafe_discharge": "Unsafe discharge",
            "specialist_escalation_needed": "Specialist escalation",
        }

        active_signals = [label for key, label in signal_labels.items() if clinical_data.get(key)]

        if active_signals:
            st.markdown(
                "".join([f'<span class="signal">{label}</span>' for label in active_signals]),
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<span class="signal">No major signals detected</span>', unsafe_allow_html=True)

        st.subheader("Compliance")
        if compliance_result["compliant"]:
            st.success("Compliant")
        else:
            st.error("Violations detected")
            for v in compliance_result["violations"]:
                st.write(f"• {v}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Recommendations")

        if view["applied_mode"] == "Hybrid":
            st.markdown("**🧩 Combined Intelligence (Rules + AI)**")

        for r in recommendations:
            st.write(f"• {r}")

        confidence = llm_result.get("confidence", risk_result.get("confidence", 70))
        st.metric("Confidence", f"{confidence}%")
        st.markdown("</div>", unsafe_allow_html=True)

    if source in ["llm", "hybrid"]:
        if llm_result.get("causal_reasoning"):
            st.subheader("Causal Reasoning")
            st.markdown(f'<div class="causal-box">{llm_result["causal_reasoning"]}</div>', unsafe_allow_html=True)

        if llm_result.get("what_if"):
            st.subheader("What If Scenario")
            st.markdown(f'<div class="whatif-box">{llm_result["what_if"]}</div>', unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Explanation")
    for e in explanations:
        st.write(f"• {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Audit Trail")
    for log in audit_logs:
        st.write(f"• {log}")
    st.markdown("</div>", unsafe_allow_html=True)