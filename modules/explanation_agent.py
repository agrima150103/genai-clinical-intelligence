def generate_explanation(clinical_data, compliance_result, risk_result):
    explanations = []

    if clinical_data.get("low_oxygen"):
        explanations.append("Low oxygen saturation indicates clinically significant respiratory compromise.")

    if clinical_data.get("no_improvement"):
        explanations.append("The patient has not improved within the expected treatment window.")

    if clinical_data.get("worsening"):
        explanations.append("Symptoms are worsening despite ongoing treatment.")

    if clinical_data.get("treatment_failure"):
        explanations.append("The current treatment appears ineffective and requires escalation.")

  
    if clinical_data.get("cardiac_risk"):
        explanations.append("The clinical presentation is concerning for a possible cardiac event.")

    if clinical_data.get("missing_ecg"):
        explanations.append("A cardiac evaluation was not performed despite warning signs.")

    if clinical_data.get("tachycardia"):
        explanations.append("Elevated heart rate adds to the patient’s acute risk profile.")

    if clinical_data.get("hypertension"):
        explanations.append("Raised blood pressure strengthens concern for cardiovascular instability.")

   
    if clinical_data.get("overdose_risk"):
        explanations.append("The case indicates suspected medication overdose requiring protocol-based follow-up.")

    if clinical_data.get("mental_health_risk"):
        explanations.append("The patient’s psychiatric comorbidities increase risk and require additional care planning.")

    if clinical_data.get("missing_psychiatric_eval"):
        explanations.append("Psychiatric evaluation was not ordered despite overdose-related risk.")

    if clinical_data.get("unsafe_discharge"):
        explanations.append("Discharge without mental health follow-up creates a serious continuity-of-care gap.")

    
    if clinical_data.get("improving"):
        explanations.append("Clinical symptoms are improving over time.")

    if clinical_data.get("stable_recovery"):
        explanations.append("The patient shows stable recovery with no major deterioration signals.")

    
    if not compliance_result.get("compliant"):
        explanations.append("Clinical guidelines were not followed appropriately.")

    
    if risk_result["risk"] == "High":
        explanations.append("This indicates a high-risk condition requiring urgent intervention.")
    elif risk_result["risk"] == "Medium":
        explanations.append("This indicates a moderate-risk condition requiring timely review.")
    else:
        explanations.append("Treatment progression is within acceptable clinical limits.")

    return explanations