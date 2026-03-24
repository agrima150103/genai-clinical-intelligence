import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_case(case_data):
    """
    GenAI-powered reasoning engine.
    Sends patient case to an LLM and gets structured clinical analysis back.
    Falls back to rule-based logic if LLM call fails.
    """

    # ── Build the prompt ──────────────────────────────────────────────────────
    prompt = f"""You are an expert clinical decision support AI.
Analyze the following patient case and return a structured JSON response.

PATIENT CASE:
{json.dumps(case_data, indent=2)}

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{{
  "deviation": true or false,
  "risk": "High" or "Medium" or "Low",
  "explanations": ["explanation 1", "explanation 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "confidence": integer between 0 and 100,
  "causal_reasoning": "One paragraph explaining the clinical reasoning chain",
  "what_if": "What would happen if no intervention is taken in the next 24 hours"
}}

Guidelines:
- "deviation" = true if treatment is not following clinical best practice
- "risk" = High if immediate danger to patient, Medium if urgent review needed, Low if stable
- "explanations" = list the specific clinical signals that led to your assessment
- "recommendations" = actionable clinical steps the care team should take now
- "confidence" = your confidence level in this assessment (0-100)
- "causal_reasoning" = a clear chain of clinical logic connecting the signals to your risk conclusion
- "what_if" = a brief scenario if the current situation continues unchanged
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical decision support AI. "
                        "You analyze patient cases and return structured JSON assessments. "
                        "Always respond with valid JSON only, no extra text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=800,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)

        # Ensure all required fields exist
        result.setdefault("deviation", False)
        result.setdefault("risk", "Low")
        result.setdefault("explanations", [])
        result.setdefault("recommendations", [])
        result.setdefault("confidence", 70)
        result.setdefault("causal_reasoning", "")
        result.setdefault("what_if", "")
        result["source"] = "llm"

        return result

    except Exception as e:
        # ── Fallback: rule-based logic if LLM fails ───────────────────────────
        print(f"[WARNING] LLM call failed: {e}. Using rule-based fallback.")
        return _rule_based_fallback(case_data)


def _rule_based_fallback(case_data):
    """
    Original rule-based logic used as fallback when LLM is unavailable.
    """
    timeline = case_data.get("timeline", [])
    expected_days = case_data.get("expected_response_days", 3)

    deviation_detected = False
    risk_level = "Low"
    explanations = []
    recommendations = []

    medication_started = False
    days_since_medication = 0

    for event in timeline:
        event_text = event["event"].lower()

        if "prescribed" in event_text:
            medication_started = True
            days_since_medication = 0

        if medication_started:
            days_since_medication += 1

        if "no improvement" in event_text and days_since_medication > expected_days:
            deviation_detected = True
            risk_level = "High"
            explanations.append("No improvement observed beyond expected response time.")
            recommendations.append("Escalate treatment and reassess diagnosis immediately.")

        if "worsen" in event_text:
            deviation_detected = True
            risk_level = "High"
            explanations.append("Symptoms worsening despite treatment.")
            recommendations.append("Urgent clinical intervention required.")

        if "same medication continued" in event_text:
            deviation_detected = True
            if risk_level != "High":
                risk_level = "Medium"
            explanations.append("Treatment not escalated despite lack of response.")
            recommendations.append("Review treatment protocol.")

    if not deviation_detected:
        explanations.append("Treatment progression within acceptable clinical limits.")
        recommendations.append("Continue monitoring.")

    confidence_score = 85 if risk_level == "High" else 60 if risk_level == "Medium" else 95

    return {
        "deviation": deviation_detected,
        "risk": risk_level,
        "explanations": explanations,
        "recommendations": recommendations,
        "confidence": confidence_score,
        "causal_reasoning": "Rule-based analysis (LLM unavailable).",
        "what_if": "",
        "source": "fallback",
    }