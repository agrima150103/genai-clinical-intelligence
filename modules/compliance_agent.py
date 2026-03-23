def check_compliance(case_data, clinical_data):

    expected_days = case_data.get("expected_response_days", 3)

    violations = []

    # Rule 1: No improvement after expected days
    if clinical_data.get("no_improvement") and clinical_data.get("days_since_medication", 0) >= expected_days:
        violations.append("No improvement beyond expected response time — treatment escalation required.")

    # Rule 2: Worsening symptoms
    if clinical_data.get("worsening"):
        violations.append("Symptoms worsening despite treatment — urgent intervention required.")

    # Rule 3: Low oxygen critical
    if clinical_data.get("low_oxygen"):
        violations.append("Low oxygen levels detected — immediate clinical attention required.")

    # Rule 4: Chest pain ignored
    if clinical_data.get("chest_pain"):
        violations.append("Chest pain detected — cardiac evaluation required.")

    return {
        "compliant": len(violations) == 0,
        "violations": violations
    }