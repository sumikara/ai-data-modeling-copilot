# SEMANTIC OUTPUT GRADING REPORT (gemini)

## Mode
- `gemini`

## Retrieval Query
- `grain decision fact vs dimension SCD rules transaction dataset profiling duplicates keys`

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
  "overall_score": 0,
  "passed": false,
  "checks": [],
  "critical_failures": [
    "semantic_profiling_execution_failed: Missing GEMINI_API_KEY environment variable"
  ],
  "recommendations": [
    "Resolve provider/API issues (credentials, quota, availability) and rerun grading.",
    "Use --mode mock for deterministic local grading when provider is unavailable."
  ],
  "execution_error": {
    "error": "Missing GEMINI_API_KEY environment variable",
    "raw_output_path": "test_outputs/semantic_profiling/ACTUAL_GEMINI_RAW_OUTPUT.md",
    "requires_human_decision": true
  }
}
```
