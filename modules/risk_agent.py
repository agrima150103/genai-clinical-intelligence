def calculate_risk(clinical_data, compliance_result):

    risk_score = 0

    # Base rules
    if clinical_data.get("no_improvement"):
        risk_score += 1

    if clinical_data.get("worsening"):
        risk_score += 2

    # New intelligent rules
    if clinical_data.get("low_oxygen"):
        risk_score += 3

    if clinical_data.get("chest_pain"):
        risk_score += 3

    if clinical_data.get("high_risk_age"):
        risk_score += 1

    # Compliance violations boost risk
    if not compliance_result.get("compliant"):
        risk_score += 2

    # Final classification
    if risk_score >= 6:
        risk = "High"
        confidence = 95
    elif risk_score >= 3:
        risk = "Medium"
        confidence = 80
    else:
        risk = "Low"
        confidence = 95

    return {
        "risk": risk,
        "confidence": confidence
    }