# GenAI Atlas — Clinical Intelligence Platform

> AI-powered multi-agent system for early clinical failure detection with **LLM reasoning + rule-based guardrails**.
> Built for the ET Gen AI Hackathon — Domain-Specialized AI Agents with Compliance Enforcement.

---

## The Problem

In Indian hospitals, silent treatment failures often go undetected:

* No improvement but treatment continues
* Critical vitals (oxygen, BP) are ignored
* Escalation decisions are delayed

**These delays lead to ICU admissions, higher mortality, and financial loss.**

---

## Our Solution

**GenAI Atlas** detects clinical deviations early using a **multi-agent + GenAI hybrid system**.

---

## System Architecture

```
Patient Data → Clinical Agent → Compliance Agent → Risk Agent
                                                        ↓
                              Audit Agent ← Explanation Agent ← Reasoning Engine (LLM)
                                                        ↓
                                          Streamlit Dashboard
```

---

## Agents

| Agent                  | Role                                                                    |
| ---------------------- | ----------------------------------------------------------------------- |
| `clinical_agent.py`    | Extracts clinical signals (low oxygen, worsening, chest pain, age risk) |
| `compliance_agent.py`  | Checks guideline adherence and flags violations                         |
| `risk_agent.py`        | Calculates severity (High / Medium / Low)                               |
| `reasoning_engine.py`  | **Groq (Llama3)** — advanced clinical reasoning                         |
| `explanation_agent.py` | Converts outputs into doctor-friendly explanations                      |
| `audit_agent.py`       | Generates full decision audit trail                                     |

---

## GenAI Layer (Groq - Llama3)

The system uses **Groq (Llama3)** for:

* Context-aware clinical reasoning
* Structured JSON outputs
* Causal explanation generation
* What-if scenario simulation

---

## Hybrid Intelligence (Key Innovation)

GenAI Atlas uses a **3-layer intelligence system**:

1. **LLM Mode (Groq)** → deep reasoning
2. **Rule-Based Mode** → deterministic safety checks
3. **Hybrid Mode** → combines both outputs

➡️ Ensures **accuracy, reliability, and compliance**

---

## Key Features

* 🚨 Early detection of clinical failures
* 🧠 LLM-powered reasoning (Groq)
* ⚖️ Compliance enforcement (medical rules)
* 📊 Full audit trail for every decision
* 🔮 What-if scenario simulation
* 🔁 Automatic fallback if LLM unavailable
* 🧑‍⚕️ Actionable recommendations for doctors

---

## Setup Instructions

### 1. Clone repository

```bash
git clone https://github.com/agrima150103/genai-clinical-intelligence.git
cd genai-clinical-intelligence
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit groq python-dotenv
```

### 4. Add API Key

Create `.env` file:

```
GROQ_API_KEY=your_key_here
```

---

### 5. Run the app

```bash
streamlit run app.py
```

---

## Demo Cases

* `case1.json` → Pneumonia (High Risk)
* `case2.json` → Viral (Low Risk)
* `case3.json` → Cardiac Failure (Critical)
* `case4.json` → Overdose (Compliance failure)
* `case5.json` → Bronchitis (Recovery)

---

## Tech Stack

* Python
* Streamlit
* Groq (Llama3)
* Modular AI agents

---

## Business Impact

* ₹29 Cr annual savings per hospital
* 5.7 clinician hours saved daily
* 48x ROI for hospitals

---

## Why It Matters

GenAI Atlas transforms hospitals from **reactive care → proactive intelligence systems**.

---

## Hackathon

ET Gen AI Hackathon — Domain-Specialized AI Agents with Guardrails
