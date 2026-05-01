# case_03_dimension_or_fact_hybrid (mock)

## Grade
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

## Golden
```json
{
  "case_id": "case_03_dimension_or_fact_hybrid",
  "passed": false,
  "critical_failures": [
    "missing_golden"
  ]
}
```

## Failure categories
- 