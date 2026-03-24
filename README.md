# GenAI Atlas – Clinical Intelligence Dashboard

AI-powered multi-agent clinical decision support system that analyzes patient timelines, detects high-risk conditions, ensures treatment compliance, and generates explainable clinical insights.

---

## Key Features

- Multi-Agent System
  - Clinical Agent → extracts signals
  - Risk Agent → calculates risk level
  - Compliance Agent → checks medical protocol violations
  - Explanation Agent → generates reasoning
  - Audit Agent → tracks decision flow

- Smart Risk Detection
  - Oxygen < 92% → HIGH risk
  - Chest Pain → Cardiac alert
  - No improvement → Escalation needed
  - Symptoms worsening → Critical flag

- Interactive Dashboard
  - Patient timeline visualization
  - Real-time risk alerts
  - Clinical signals display
  - Compliance insights
  - Decision audit trail

---

## Tech Stack

- Python
- Streamlit
- Modular agent-based architecture
- JSON-based simulation

---

## Project Structure
genai-clinical-intelligence/
│
├── app.py # Main Streamlit dashboard
│
├── data/ # Patient case datasets
│ ├── case1.json
│ ├── case2.json
│ └── case3.json
│
├── modules/ # Multi-agent system logic
│ ├── clinical_agent.py # Extracts clinical signals
│ ├── risk_agent.py # Calculates risk level
│ ├── compliance_agent.py # Checks treatment violations
│ ├── explanation_agent.py # Generates explanations
│ ├── audit_agent.py # Tracks decision steps
│ └── reasoning_engine.py # Orchestrates all agents
│
├── architecture/ # System design diagrams (to be added)
│
└── .gitignore # Ignore unnecessary files
