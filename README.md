# GenAI Atlas — Clinical Intelligence Platform

> AI-powered multi-agent system for early clinical failure detection and decision intelligence.
> Built for the ET Gen AI Hackathon 2024 — Problem Statement 5: Domain-Specialized AI Agents with Compliance Guardrails.

---

## The Problem

In Indian hospitals, silent treatment failures go undetected for days:
- A patient on the wrong antibiotic shows no improvement — but the same medication continues
- Oxygen saturation drops to dangerous levels with no escalation
- Cardiac events are missed because no ECG is ordered

**GenAI Atlas catches these failures before they become crises.**

---

## How It Works

A pipeline of specialized agents analyzes each patient case:

```
Patient Data → Clinical Agent → Compliance Agent → Risk Agent
                                                        ↓
                              Audit Agent ← Explanation Agent ← Reasoning Engine (LLM)
                                                        ↓
                                          Streamlit Dashboard
```

| Agent | Role |
|---|---|
| `clinical_agent.py` | Extracts signals: low oxygen, worsening, chest pain, high-risk age |
| `compliance_agent.py` | Checks against clinical guidelines, flags violations |
| `risk_agent.py` | Scores severity: High / Medium / Low with confidence % |
| `reasoning_engine.py` | **GPT-4o-mini** — causal reasoning + what-if scenario generation |
| `explanation_agent.py` | Translates findings into plain clinical language |
| `audit_agent.py` | Logs every decision step for traceability |

---

## GenAI Integration

The `reasoning_engine.py` calls **GPT-4o-mini** with the full patient case JSON and receives:
- Structured risk assessment
- Causal reasoning chain (why this risk level was assigned)
- What-if scenario (what happens if no action is taken)
- Confidence score

Falls back to rule-based logic automatically if the LLM is unavailable.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/agrima150103/genai-clinical-intelligence.git
cd genai-clinical-intelligence
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install streamlit openai
```

### 4. Set your OpenAI API key
```bash
# Mac/Linux
export OPENAI_API_KEY=your_key_here

# Windows
set OPENAI_API_KEY=your_key_here
```
Or create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

### 6. Upload a test case
Upload any of the files in the `data/` folder:
- `case1.json` — High-risk pneumonia patient (no improvement, low oxygen)
- `case2.json` — Low-risk viral infection (stable, recovering)
- `case3.json` — Cardiac emergency (missed ECG, escalation failure)

---

## Sample Output

For `case1.json` (high-risk pneumonia):

```
RISK LEVEL: HIGH
Confidence: 92%

Causal Reasoning: Patient P001 (age 58, diabetic, hypertensive) presented with
suspected pneumonia. Antibiotic A was prescribed on Day 2. By Day 4, oxygen
saturation had dropped to 89% — below the critical 92% threshold — and no
improvement was observed. Despite worsening vitals, the same medication continued
on Day 6. This pattern indicates treatment failure with high probability of
secondary infection or antibiotic resistance.

What If No Action: If untreated in the next 24 hours, the patient risks respiratory
failure, ICU admission, and significantly elevated mortality risk given the
comorbidity profile.
```

---

## Project Structure

```
genai-clinical-intelligence/
│
├── app.py                  # Streamlit dashboard (main entry point)
├── modules/
│   ├── clinical_agent.py   # Signal extraction
│   ├── compliance_agent.py # Guideline violation checks
│   ├── risk_agent.py       # Risk scoring
│   ├── reasoning_engine.py # GPT-4o-mini LLM integration
│   ├── explanation_agent.py# Plain-language summaries
│   └── audit_agent.py      # Decision trail logging
├── data/
│   ├── case1.json          # High-risk case (pneumonia)
│   ├── case2.json          # Low-risk case (viral)
│   └── case3.json          # Cardiac emergency
├── architecture/           # System architecture diagram (PDF)
├── IMPACT_MODEL.md         # Business impact calculation
└── .gitignore
```

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** — interactive dashboard
- **OpenAI GPT-4o-mini** — GenAI reasoning layer
- **Modular multi-agent architecture** — each agent is independently testable

---

## Business Impact

- **5.7 clinician hours saved per day** per hospital (344 minutes across flagged cases)
- **₹29 Cr annual savings** per mid-sized hospital from prevented adverse events
- **48x ROI** on SaaS subscription cost
- Scales to national deployment: ₹1,45,000 Cr potential savings across 5,000 hospitals

See [IMPACT_MODEL.md](./IMPACT_MODEL.md) for full calculation with assumptions.

---

## Hackathon

**ET Gen AI Hackathon** | Problem Statement 5: Domain-Specialized AI Agents with Compliance Guardrails
