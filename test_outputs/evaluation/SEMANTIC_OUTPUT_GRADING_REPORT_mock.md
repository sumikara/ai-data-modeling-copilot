# SEMANTIC OUTPUT GRADING REPORT (mock)

## Run ID
- `run_20260430T211825Z_a4d5e3a0`

## Mode
- `mock`

## Input Path
- `test_inputs/semantic_profiling/transaction_like_profile.json`

## Retrieval Query
- `grain decision fact vs dimension SCD rules transaction dataset profiling duplicates keys`

## Retrieved Context Sources
- `knowledge_base/extracted_notes/scd_decision_rules.md`
- `knowledge_base/extracted_notes/grain_decision_rules.md`
- `knowledge_base/extracted_notes/dimensional_modeling_principles.md`

## Retrieved Context (truncated)

```text
### Source: knowledge_base/extracted_notes/scd_decision_rules.md
file_name=scd_decision_rules.md
score=16
why_selected=overlap=8, boost=8, title_bonus=0, boost:scd
---

## 23. Key Integrity Constraints

Integrity checks must ensure:
- no unintended duplicates,
- valid FK-to-dimension resolution,
- stable join behavior across reruns.

---

## 24. Key Conflict Handling

On key conflicts:
- apply trusted-source priority policy,
- apply business conflict rules,
- log discrepancies for audit and remediation.

No silent conflict suppression.

---

## 25. SCD Pitfalls

---

### Source: knowledge_base/extracted_notes/grain_decision_rules.md
file_name=grain_decision_rules.md
score=15
why_selected=overlap=7, boost=8, title_bonus=0, boost:grain
- Acceptance of uncertain or risk-compromised grain.

---

### Source: knowledge_base/extracted_notes/dimensional_modeling_principles.md
file_name=dimensional_modeling_principles.md
score=9
why_selected=overlap=9, boost=0, title_bonus=0
---

## 10. Fact-Dimension Relationship

Fact tables reference dimensions via foreign keys.

```text
fact_sales
- customer_key -> dim_customer
- product_key  -> dim_product
- date_key     -> dim_date
```

Relationship quality must be validated (coverage, unknown/default routing, conformance).

---

## 11. Grain Definition (Critical)

Grain defines exactly what one row means.

Examples:
- one row per transaction
```

## Grading Result

```json
{
  "overall_score": 100,
  "passed": true,
  "checks": [
    {
      "name": "required_json_keys",
      "score": 100,
      "passed": true,
      "notes": "All required keys present."
    },
    {
      "name": "valid_confidence_level",
      "score": 100,
      "passed": true,
      "notes": "confidence_level='medium'"
    },
    {
      "name": "requires_human_decision_true",
      "score": 100,
      "passed": true,
      "notes": "requires_human_decision=True"
    },
    {
      "name": "grain_candidates_non_empty",
      "score": 100,
      "passed": true,
      "notes": "grain_candidates count=2"
    },
    {
      "name": "recommended_grain_present_or_uncertain",
      "score": 100,
      "passed": true,
      "notes": "recommended_grain='one row per transaction_id + product_id + customer_id + transaction_dt'"
    },
    {
      "name": "grain_reasoning_evidence",
      "score": 100,
      "passed": true,
      "notes": "Modeling notes include grain reasoning evidence."
    },
    {
      "name": "data_quality_risks_non_empty",
      "score": 100,
      "passed": true,
      "notes": "data_quality_risks count=2"
    },
    {
      "name": "scd_not_finalized_when_conflict_present",
      "score": 100,
      "passed": true,
      "notes": "No finalized SCD type detected under conflict context."
    },
    {
      "name": "no_obvious_context_contradiction",
      "score": 100,
      "passed": true,
      "notes": "No obvious contradiction detected."
    },
    {
      "name": "no_final_sql_or_ddl",
      "score": 100,
      "passed": true,
      "notes": "No SQL/DDL patterns found."
    }
  ],
  "critical_failures": [],
  "recommendations": []
}
```
