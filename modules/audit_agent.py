def generate_audit_log(clinical_data, compliance_result, risk_result):

    logs = []

    # Step 1: Clinical
    logs.append("Step 1: Clinical signals extracted from patient timeline.")

    if clinical_data.get("no_improvement"):
        logs.append("→ No improvement detected within expected timeframe.")

    if clinical_data.get("worsening"):
        logs.append("→ Symptoms worsening detected.")

    # Step 2: Compliance
    logs.append("Step 2: Compliance rules evaluated.")

    if not compliance_result.get("compliant"):
        logs.append("→ Treatment deviates from clinical guidelines.")
    else:
        logs.append("→ Treatment follows clinical guidelines.")

    # Step 3: Risk
    logs.append("Step 3: Risk level calculated.")
    logs.append(f"→ Final risk level assigned: {risk_result.get('risk')}.")

    return logs