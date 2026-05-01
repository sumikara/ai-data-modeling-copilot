# case_07_factless_fact_attendance (mock)

## Comparator
```json
{
  "case_id": "case_07_factless_fact_attendance",
  "overall_score": 100,
  "passed": true,
  "decision_area_scores": {
    "grain": 30,
    "fact_dimension": 20,
    "keys": 15,
    "data_quality": 10,
    "confidence": 10,
    "governance": 15
  },
  "critical_failures": [],
  "warnings": [],
  "recommendations": []
}
```

## Failure taxonomy
```json
{
  "case_id": "case_07_factless_fact_attendance",
  "failure_categories": [
    "weak_knowledge_grounding"
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
  "overall_score": 70,
  "passed": false,
  "checks": [
    {
      "name": "required_json_keys",
      "score": 0,
      "passed": false,
      "notes": "Missing keys: ['business_process_guess', 'cross_source_conflicts']"
    },
    {
      "name": "valid_confidence_level",
      "score": 100,
      "passed": true,
      "notes": "confidence_level='low'"
    },
    {
      "name": "requires_human_decision_true",
      "score": 100,
      "passed": true,
      "notes": "requires_human_decision=True"
    },
    {
      "name": "grain_candidates_non_empty",
      "score": 0,
      "passed": false,
      "notes": "grain_candidates count=0"
    },
    {
      "name": "recommended_grain_present_or_uncertain",
      "score": 100,
      "passed": true,
      "notes": "recommended_grain='uncertain'"
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
  "critical_failures": [
    "Missing required JSON keys."
  ],
  "recommendations": [
    "Provide at least one evidence-based grain candidate.",
    "Strengthen evidence traceability in modeling_notes for higher grading confidence."
  ]
}
```
