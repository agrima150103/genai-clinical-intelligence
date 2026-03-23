def analyze_case(case_data):
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
            explanations.append(
                "No improvement observed beyond expected response time."
            )
            recommendations.append(
                "Escalate treatment and reassess diagnosis immediately."
            )

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

    # Confidence score logic
    confidence_score = 85 if risk_level == "High" else 60 if risk_level == "Medium" else 95

    return {
        "deviation": deviation_detected,
        "risk": risk_level,
        "explanations": explanations,
        "recommendations": recommendations,
        "confidence": confidence_score
    }