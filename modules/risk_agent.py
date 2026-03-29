def calculate_risk(clinical_data, compliance_result):
    risk_score = 0

    if clinical_data.get("no_improvement"):
        risk_score += 1

    if clinical_data.get("worsening"):
        risk_score += 2

    if clinical_data.get("low_oxygen"):
        risk_score += 3

    if clinical_data.get("high_risk_age"):
        risk_score += 1

    
    if clinical_data.get("cardiac_risk"):
        risk_score += 2

    if clinical_data.get("chest_pain"):
        risk_score += 3

    if clinical_data.get("missing_ecg"):
        risk_score += 3

    if clinical_data.get("tachycardia"):
        risk_score += 1

    if clinical_data.get("hypertension"):
        risk_score += 1

    
    if clinical_data.get("overdose_risk"):
        risk_score += 2

    if clinical_data.get("mental_health_risk"):
        risk_score += 1

    if clinical_data.get("missing_psychiatric_eval"):
        risk_score += 3

    if clinical_data.get("unsafe_discharge"):
        risk_score += 3

    
    if clinical_data.get("specialist_escalation_needed"):
        risk_score += 2

    
    if not compliance_result.get("compliant"):
        risk_score += 2

   
    if clinical_data.get("improving"):
        risk_score -= 1

    if clinical_data.get("stable_recovery"):
        risk_score -= 2

    if risk_score >= 7:
        risk = "High"
        confidence = 95
    elif risk_score >= 3:
        risk = "Medium"
        confidence = 85
    else:
        risk = "Low"
        confidence = 95

    return {
        "risk": risk,
        "confidence": confidence
    }