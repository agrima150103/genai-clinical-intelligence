def check_compliance(case_data, clinical_data):
    violations = []

    if clinical_data.get("treatment_failure"):
        violations.append("No improvement beyond expected response time — treatment escalation required.")

    if clinical_data.get("worsening"):
        violations.append("Symptoms worsening despite treatment — urgent intervention required.")

    if clinical_data.get("low_oxygen"):
        violations.append("Low oxygen levels detected — immediate clinical attention required.")

    if clinical_data.get("missing_ecg"):
        violations.append("Chest pain / suspected cardiac event without ECG — urgent cardiac evaluation required.")

    if clinical_data.get("missing_psychiatric_eval"):
        violations.append("Suspected overdose without psychiatric evaluation — mental health assessment required.")

    if clinical_data.get("unsafe_discharge"):
        violations.append("Discharge without mental health follow-up — unsafe discharge pathway detected.")

    if clinical_data.get("specialist_escalation_needed") and not clinical_data.get("stable_recovery"):
        violations.append("Specialist escalation indicated based on detected risk signals.")

    return {
        "compliant": len(violations) == 0,
        "violations": violations
    }