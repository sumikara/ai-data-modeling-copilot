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

Reasoning procedure (must follow before final JSON):
1) Candidate grain enumeration
   - List all plausible grain candidates explicitly.
2) Candidate grain scoring
   - Score each candidate grain using:
     - uniqueness evidence
     - duplication patterns
     - relationship consistency
3) Grain selection
   - Select the highest-supported grain as recommended_grain.
   - If no candidate is strongly supported, set recommended_grain to "uncertain" and lower confidence_level.

Natural key procedure (must follow):
- For candidate_natural_keys, prefer columns/column combinations with:
  - high uniqueness ratio
  - low null ratio
  - business-like meaning
- Do not rely on naming alone.
- Explicitly explain:
  - why each candidate is considered
  - why it may fail as a stable key

Fact vs dimension classification procedure (must follow):
- Fact-like signals:
  - presence of aggregatable measures
  - repeated event-like rows
  - composite grain
  - transaction/event/date behavior
- Dimension-like signals:
  - descriptive attributes
  - stable entity descriptors
  - identifier + attributes structure
  - relationship to facts rather than event rows
- If evidence is mixed:
  - mark classification as "hybrid/unclear"
  - explain what additional evidence is needed

Evidence traceability requirement:
For every major decision or recommendation, reference specific evidence from input artifacts.
Use evidence phrases such as:
- "based on uniqueness ratio of ..."
- "based on duplication pattern in ..."
- "based on relationship candidate ..."
- "based on null ratio of ..."

Major decisions requiring explicit evidence traceability:
- business_process_guess
- entity_type_guess
- recommended_grain
- dimension_candidates
- fact_candidates
- candidate_natural_keys
- data_quality_risks

Return output in two sections:

SECTION 1) JSON OUTPUT
- Return the exact JSON output contract (same keys, same structure).
- Set "requires_human_decision": true.
- Set confidence_level using only: "low", "medium", "high".
- Confidence rules:
  - low = conflicting signals or missing evidence
  - medium = partial support but ambiguity exists
  - high = strong evidence across multiple independent signals
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

Before finalizing, run this internal checklist:
- Did I validate grain using duplication patterns?
- Did I justify natural keys using uniqueness and null ratios?
- Did I distinguish fact vs dimension using structure, not naming?
- Did I avoid assumptions not supported by data?
- Did I explicitly highlight uncertainty?
- Did I set confidence_level using only low/medium/high?
- Did I keep requires_human_decision as true?
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
  "confidence_level": "low | medium | high",
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

---

## Internal Reasoning Checklist

Before finalizing the response, verify:

- Did I validate grain using duplication patterns?
- Did I justify natural keys using uniqueness and null ratios?
- Did I distinguish fact vs dimension using structure, not naming?
- Did I avoid assumptions not supported by data?
- Did I explicitly highlight uncertainty?
- Did I set confidence_level using the allowed values only?
- Did I keep requires_human_decision as true?
