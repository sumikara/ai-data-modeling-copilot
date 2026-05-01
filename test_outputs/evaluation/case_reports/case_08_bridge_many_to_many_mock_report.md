# case_08_bridge_many_to_many (mock)

Source mode: **mock**

## Comparator
```json
{
  "case_id": "case_08_bridge_many_to_many",
  "overall_score": 96,
  "passed": true,
  "decision_area_scores": {
    "grain": 30,
    "fact_dimension": 20,
    "keys": 15,
    "data_quality": 6,
    "confidence": 10,
    "governance": 15
  },
  "critical_failures": [],
  "warnings": [
    "missing_risk_keyword:null",
    "missing_risk_keyword:uniqueness"
  ],
  "recommendations": []
}
```

## Failure taxonomy
```json
{
  "case_id": "case_08_bridge_many_to_many",
  "failure_categories": [
    "missing_data_quality_risks"
  ],
  "root_cause_hypotheses": [
    "Needs deeper evidence grounding."
  ],
  "recommended_fix_area": [
    "retrieval"
  ]
}
```

## Grader
```json
{
  "overall_score": 90,
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
      "notes": "grain_candidates count=1"
    },
    {
      "name": "recommended_grain_present_or_uncertain",
      "score": 100,
      "passed": true,
      "notes": "recommended_grain='one row per many-to-many relationship occurrence'"
    },
    {
      "name": "grain_reasoning_evidence",
      "score": 0,
      "passed": false,
      "notes": "No grain reasoning evidence found in modeling_notes."
    },
    {
      "name": "data_quality_risks_non_empty",
      "score": 100,
      "passed": true,
      "notes": "data_quality_risks count=1"
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
