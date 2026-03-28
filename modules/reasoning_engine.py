import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=".env")
except ImportError:
    pass

client = None
llm_provider = None

try:
    from groq import Groq
    groq_key = os.getenv("GROQ_API_KEY")

    print("DEBUG → GROQ KEY:", groq_key)   

    if groq_key:
        client = Groq(api_key=groq_key)
        llm_provider = "groq"
    else:
        print("❌ GROQ API KEY NOT FOUND")

except ImportError:
    print("❌ GROQ PACKAGE NOT INSTALLED")

if client is None:
    try:
        from openai import OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            client = OpenAI(api_key=openai_key)
            llm_provider = "openai"
    except ImportError:
        pass


def analyze_case(case_data):
    if client is None:
        print("[WARNING] No API key found. Using rule-based fallback.")
        return _rule_based_fallback(case_data)

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
}}"""

    try:
        if llm_provider == "groq":
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a clinical decision support AI. Always respond with valid JSON only, no extra text."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=800,
            )
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a clinical decision support AI. Always respond with valid JSON only, no extra text."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=800,
            )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        result.setdefault("deviation", False)
        result.setdefault("risk", "Low")
        result.setdefault("explanations", [])
        result.setdefault("recommendations", [])
        result.setdefault("confidence", 70)
        result.setdefault("causal_reasoning", "")
        result.setdefault("what_if", "")
        result["source"] = "llm"
        result["provider"] = "Groq (Llama3)" if llm_provider == "groq" else "GPT-4o-mini"
        return result

    except Exception as e:
        print(f"[WARNING] LLM call failed: {e}. Using rule-based fallback.")
        return _rule_based_fallback(case_data)


def _rule_based_fallback(case_data):
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
        "provider": "Rule-based fallback",
    }