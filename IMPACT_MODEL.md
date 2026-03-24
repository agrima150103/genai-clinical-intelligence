# GenAI Atlas — Business Impact Model

## Problem Size
- India has ~25,000 hospitals (National Health Profile 2022)
- Average hospital: 200 beds, 60–70% occupancy = ~140 active patients/day
- Adverse events from delayed diagnosis / treatment failure affect ~10% of admitted patients globally (WHO)
- Average cost of a preventable adverse event in India: ₹80,000–₹2,00,000 per incident (treatment extension, ICU, litigation)

---

## Impact Calculation (Single Mid-Sized Hospital)

| Metric | Value |
|---|---|
| Active patients/day | 140 |
| Cases with treatment deviation risk (10%) | 14/day |
| Cases GenAI Atlas catches early (estimated 60% detection rate) | ~8/day |
| Average days of unnecessary treatment avoided per catch | 2 days |
| Cost saved per prevented adverse event | ₹1,00,000 |
| **Daily saving** | **₹8,00,000** |
| **Annual saving per hospital** | **₹29 Cr** |

---

## Time Saved (Clinical Staff)

| Task | Manual time | With GenAI Atlas | Saving |
|---|---|---|---|
| Reviewing patient timeline for deviations | 20 min/patient | 2 min (AI flags it) | 18 min |
| Writing compliance notes | 15 min/case | Auto-generated | 15 min |
| Risk escalation decision | 10 min/case | Instant alert | 10 min |
| **Total per flagged case** | **45 min** | **2 min** | **43 min saved** |

With 8 flagged cases/day: **344 minutes = 5.7 hours of clinician time freed per day per hospital.**

---

## Scale Scenario

| Deployment scale | Hospitals | Annual impact |
|---|---|---|
| Pilot | 10 hospitals | ₹290 Cr savings |
| State-level | 500 hospitals | ₹14,500 Cr savings |
| National | 5,000 hospitals | ₹1,45,000 Cr savings |

---

## Revenue Model (SaaS)

- Subscription: ₹50,000/month per hospital
- 500 hospitals = ₹25 Cr ARR
- ROI for hospital: saves ₹29 Cr/year, pays ₹6 L/year → 48x ROI

---

## Assumptions

1. 10% adverse event rate is conservative (WHO global average is 10%, India may be higher due to documentation gaps)
2. 60% early detection rate based on LLM accuracy benchmarks on clinical NLP tasks
3. Cost per adverse event is mid-range of published Indian hospital data
4. Clinician time valued at ₹2,000/hour (specialist), ₹800/hour (resident)

---

## Non-Financial Impact

- Reduced patient mortality from late escalation
- Reduced medical litigation risk for hospitals
- Improved NABH accreditation compliance scores
- Data foundation for future predictive hospital analytics