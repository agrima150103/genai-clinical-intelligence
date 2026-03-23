def generate_explanation(clinical_data, compliance_result, risk_result):

    explanations = []

    # Clinical reasoning
    if clinical_data["no_improvement"]:
        explanations.append("Patient showed no improvement within expected treatment duration.")

    if clinical_data["worsening"]:
        explanations.append("Patient symptoms are worsening despite ongoing treatment.")

    # Compliance reasoning
    if not compliance_result["compliant"]:
        explanations.append("Clinical guidelines were not followed appropriately.")

    # Risk reasoning
    if risk_result["risk"] == "High":
        explanations.append("This indicates a high-risk condition requiring urgent intervention.")
    elif risk_result["risk"] == "Medium":
        explanations.append("This indicates a moderate-risk condition requiring timely review.")
    else:
        explanations.append("Treatment progression is within acceptable clinical limits.")

    return explanations