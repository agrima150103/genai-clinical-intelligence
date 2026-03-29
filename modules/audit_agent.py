def generate_audit_log(clinical_data, compliance_result, risk_result):
    logs = []

    logs.append("Step 1: Clinical signals extracted from patient timeline and vitals.")

   
    if clinical_data.get("low_oxygen"):
        logs.append("→ Low oxygen signal detected.")

    if clinical_data.get("no_improvement"):
        logs.append("→ No improvement detected within expected timeframe.")

    if clinical_data.get("worsening"):
        logs.append("→ Worsening symptoms signal detected.")

    if clinical_data.get("treatment_failure"):
        logs.append("→ Treatment failure signal detected.")

    
    if clinical_data.get("cardiac_risk"):
        logs.append("→ Cardiac risk signal detected.")

    if clinical_data.get("missing_ecg"):
        logs.append("→ Missing ECG signal detected.")

    
    if clinical_data.get("overdose_risk"):
        logs.append("→ Suspected overdose signal detected.")

    if clinical_data.get("mental_health_risk"):
        logs.append("→ Mental health risk signal detected.")

    if clinical_data.get("missing_psychiatric_eval"):
        logs.append("→ Missing psychiatric evaluation detected.")

    if clinical_data.get("unsafe_discharge"):
        logs.append("→ Unsafe discharge pathway detected.")

    
    if clinical_data.get("improving"):
        logs.append("→ Improvement trend detected.")

    if clinical_data.get("stable_recovery"):
        logs.append("→ Stable recovery pattern detected.")

    logs.append("Step 2: Compliance rules evaluated.")
    if not compliance_result.get("compliant"):
        logs.append("→ Compliance deviations detected.")
    else:
        logs.append("→ Treatment follows clinical guidelines.")

    logs.append("Step 3: Risk level calculated.")
    logs.append(f"→ Final risk level assigned: {risk_result.get('risk')}.")

    return logs