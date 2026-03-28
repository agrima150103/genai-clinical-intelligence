def extract_clinical_signals(case_data):

    timeline = case_data.get("timeline", [])
    vitals = case_data.get("vitals", {})
    age = case_data.get("age", 0)

    signals = {
        "no_improvement": False,
        "worsening": False,
        "medication_started": False,
        "days_since_medication": 0,
        "low_oxygen": False,
        "high_risk_age": False,
        "chest_pain": False
    }

    medication_day = None

    for event in timeline:
        text = event["event"].lower()

        if "prescribed" in text:
            signals["medication_started"] = True
            medication_day = event["day"]

        if "no improvement" in text:
            signals["no_improvement"] = True

        if "worsen" in text or "worsening" in text:
            signals["worsening"] = True

        if "chest pain" in text:
            signals["chest_pain"] = True

    
    if medication_day:
        last_day = timeline[-1]["day"]
        signals["days_since_medication"] = last_day - medication_day

    oxygen = vitals.get("oxygen_saturation", "")

    if isinstance(oxygen, str) and "%" in oxygen:
        try:
            oxygen_value = int(oxygen.replace("%", ""))
            if oxygen_value < 92:
                signals["low_oxygen"] = True
        except:
            pass

    
    if age >= 60:
        signals["high_risk_age"] = True

    return signals