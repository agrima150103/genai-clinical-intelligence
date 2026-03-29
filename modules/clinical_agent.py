def extract_clinical_signals(case_data):
    timeline = case_data.get("timeline", [])
    vitals = case_data.get("vitals", {})
    age = case_data.get("age", 0)
    diagnosis = case_data.get("diagnosis", "").lower()
    comorbidities = [c.lower() for c in case_data.get("comorbidities", [])]
    expected_days = case_data.get("expected_response_days", 3)

    signals = {
        "early_symptoms": [],
        "no_improvement": False,
        "worsening": False,
        "medication_started": False,
        "days_since_medication": 0,
        "low_oxygen": False,
        "high_risk_age": False,
        "chest_pain": False,
        "tachycardia": False,
        "hypertension": False,
        "treatment_failure": False,
        "improving": False,
        "stable_recovery": False,
        "cardiac_risk": False,
        "missing_ecg": False,
        "overdose_risk": False,
        "mental_health_risk": False,
        "missing_psychiatric_eval": False,
        "unsafe_discharge": False,
        "specialist_escalation_needed": False,
    }

    medication_day = None

    mental_health_terms = {"depression", "anxiety", "ocd", "bipolar", "psychiatric"}
    if any(term in comorbidities for term in mental_health_terms):
        signals["mental_health_risk"] = True

    if "overdose" in diagnosis:
        signals["overdose_risk"] = True

    if "cardiac" in diagnosis:
        signals["cardiac_risk"] = True

    
    day1_events = [
        event.get("event", "").lower()
        for event in timeline
        if event.get("day") == 1
    ]
    day1_text = " ".join(day1_events)

    early_symptoms = []

    
    if "fever" in day1_text:
        temp = str(vitals.get("temperature", ""))
        if "102" in temp:
            early_symptoms.append("High fever")
        else:
            early_symptoms.append("Fever")

    if "cough" in day1_text:
        early_symptoms.append("Cough")

    if "low oxygen" in day1_text or "low oxygen saturation" in day1_text:
        early_symptoms.append("Low oxygen saturation")

    if "breathing difficulty" in day1_text:
        early_symptoms.append("Mild breathing difficulty")

    if "shortness of breath" in day1_text:
        early_symptoms.append("Shortness of breath")

    if "fatigue" in day1_text:
        early_symptoms.append("Fatigue")

    if "chest pain" in day1_text:
        early_symptoms.append("Chest pain")

    if "unconscious" in day1_text:
        early_symptoms.append("Unconscious presentation")

    if "overdose" in day1_text or "pill overdose" in day1_text:
        early_symptoms.append("Suspected overdose")

    
    if "pneumonia" in diagnosis:
        early_symptoms.extend([
            "High fever",
            "Chest pain",
            "Shortness of breath",
        ])

    if "viral" in diagnosis:
        early_symptoms.extend([
            "Fatigue",
            "Congestion",
            "Sore throat",
            "Dry cough",
            "Fever",
        ])

    if "cardiac" in diagnosis:
        early_symptoms.extend([
            "Abrupt collapse",
            "Palpable pulse",
            "Chest pain",
        ])

    if "overdose" in diagnosis:
        early_symptoms.extend([
            "Behavioral disturbance",
            "Anxiety symptoms",
            "Fatigue",
            "Hyperarousal",
            "Unconscious presentation",
            "Suspected overdose",
        ])

    if "bronchitis" in diagnosis:
        early_symptoms.extend([
            "Chest pain",
            "Fatigue",
            "Persistent cough",
        ])

   
    deduped_symptoms = []
    for symptom in early_symptoms:
        if symptom not in deduped_symptoms:
            deduped_symptoms.append(symptom)

    signals["early_symptoms"] = deduped_symptoms

    
    for event in timeline:
        text = event.get("event", "").lower()

        if "prescribed" in text:
            signals["medication_started"] = True
            medication_day = event.get("day")

        if "no improvement" in text:
            signals["no_improvement"] = True

        if "worsen" in text or "worsening" in text or "shortness of breath" in text:
            signals["worsening"] = True

        if "same medication continued" in text:
            signals["treatment_failure"] = True

        if "improving" in text:
            signals["improving"] = True

        if "full recovery" in text:
            signals["improving"] = True
            signals["stable_recovery"] = True

        if "oxygen stable" in text:
            signals["stable_recovery"] = True

        if "chest pain" in text:
            signals["chest_pain"] = True
            signals["cardiac_risk"] = True

        if "no ecg" in text or "no ecg performed" in text:
            signals["missing_ecg"] = True
            signals["cardiac_risk"] = True

        if "pill overdose" in text or "suspected overdose" in text or "unconscious" in text:
            signals["overdose_risk"] = True

        if "no psychiatric evaluation" in text:
            signals["missing_psychiatric_eval"] = True

        if "discharged without mental health follow-up" in text:
            signals["unsafe_discharge"] = True
            signals["missing_psychiatric_eval"] = True

    if medication_day is not None and timeline:
        last_day = timeline[-1].get("day", medication_day)
        signals["days_since_medication"] = last_day - medication_day

    oxygen = vitals.get("oxygen_saturation", "")
    if isinstance(oxygen, str) and "%" in oxygen:
        try:
            oxygen_value = int(oxygen.replace("%", "").strip())
            if oxygen_value < 92:
                signals["low_oxygen"] = True
        except Exception:
            pass

    heart_rate = vitals.get("heart_rate")
    if isinstance(heart_rate, (int, float)) and heart_rate > 100:
        signals["tachycardia"] = True

    blood_pressure = vitals.get("blood_pressure", "")
    if isinstance(blood_pressure, str) and "/" in blood_pressure:
        try:
            systolic, diastolic = blood_pressure.split("/")
            systolic = int(systolic.strip())
            diastolic = int(diastolic.strip())
            if systolic >= 140 or diastolic >= 90:
                signals["hypertension"] = True
        except Exception:
            pass

    if age >= 60:
        signals["high_risk_age"] = True

    if signals["no_improvement"] and signals["days_since_medication"] >= expected_days:
        signals["treatment_failure"] = True

    if signals["missing_ecg"] or signals["missing_psychiatric_eval"] or signals["treatment_failure"]:
        signals["specialist_escalation_needed"] = True

    if signals["improving"] and not signals["worsening"] and not signals["no_improvement"] and not signals["low_oxygen"]:
        signals["stable_recovery"] = True

    return signals