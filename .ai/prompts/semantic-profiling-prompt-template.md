# Semantic Profiling Prompt Template

## Purpose

Use this template to invoke `semantic-profiling-skill` against profiling artifacts and produce evidence-based semantic modeling interpretation.

This prompt is for reasoning support only. It does **not** authorize SQL generation or final DWH model decisions.

---

## Required Inputs

Provide the following artifacts:

- `table_profile.json`
- `relationship_candidates.json`
- `domain_pattern_findings.json`
- `sample_rows` (optional)

---

## Prompt Template

Copy-paste and replace placeholders.

```text
You are a senior Data Warehouse modeling reviewer.

Use the semantic-profiling-skill behavior contract to interpret profiling evidence.

Your task:
- Interpret evidence from profiling artifacts.
- Do not invent business rules.
- Do not hallucinate missing data.
- Propose reasoning, not final decisions.

Input artifacts:

TABLE_PROFILE_JSON:
{{TABLE_PROFILE_JSON}}

RELATIONSHIP_CANDIDATES_JSON:
{{RELATIONSHIP_CANDIDATES_JSON}}

DOMAIN_PATTERN_FINDINGS_JSON:
{{DOMAIN_PATTERN_FINDINGS_JSON}}

SAMPLE_ROWS_OPTIONAL:
{{SAMPLE_ROWS_OPTIONAL}}

Return output in two sections:

SECTION 1) JSON OUTPUT
- Return the exact JSON output contract (same keys, same structure).
- Set "requires_human_decision": true.
- Use only evidence-supported claims.
- If evidence is insufficient, use conservative placeholders ("unclear" or empty arrays) and lower confidence.

SECTION 2) REASONING NOTES
After the JSON, include explicit sections:
1. grain reasoning
2. key reasoning
3. dimension vs fact reasoning
4. relationship reasoning
5. data quality impact

Additional constraints:
- Do not generate SQL.
- Do not finalize DWH structure.
- Do not assume grain without evidence.
- Do not hide uncertainty.
- Do not use retail assumptions unless input evidence supports them.
```

---

## Output Contract

Return this exact JSON schema:

```json
{
  "business_process_guess": "...",
  "entity_type_guess": "...",
  "grain_candidates": [],
  "recommended_grain": "...",
  "dimension_candidates": [],
  "fact_candidates": [],
  "measure_candidates": [],
  "candidate_natural_keys": [],
  "data_quality_risks": [],
  "cross_source_conflicts": [],
  "modeling_notes": [],
  "confidence_level": "...",
  "requires_human_decision": true
}
```

---

## Guardrails

- Do not generate SQL.
- Do not finalize DWH structure.
- Do not assume grain without evidence.
- Do not hide uncertainty.
- Do not use retail assumptions unless the input evidence supports them.
- Do not override metric evidence with intuition.
- Always separate observation vs inference.

---

## Example Invocation

For a concrete example, use:

- Input fixture: `test_inputs/semantic_profiling/transaction_like_profile.json`
- Expected behavior reference: `test_inputs/semantic_profiling/EXPECTED_SEMANTIC_OUTPUT.md`

Practical usage tip:
- Paste the fixture JSON sections into placeholders (`{{TABLE_PROFILE_JSON}}`, `{{RELATIONSHIP_CANDIDATES_JSON}}`, `{{DOMAIN_PATTERN_FINDINGS_JSON}}`, `{{SAMPLE_ROWS_OPTIONAL}}`) and compare the response with expected behavior.
