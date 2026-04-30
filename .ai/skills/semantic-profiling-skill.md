# semantic-profiling-skill

## Purpose

Interpret structured profiling outputs and convert them into semantic understanding signals for data warehouse modeling.

This skill is an **evidence interpreter**, not a model finalizer.

### Must NOT do
- Must NOT generate SQL.
- Must NOT finalize modeling decisions.
- Must NOT claim certainty where profiling evidence is weak.

### Must do
- Propose modeling reasoning grounded in profiling artifacts.
- Surface ambiguity and require human review when needed.

---

## Input

Expected inputs:

- `table_profile.json`
- `relationship_candidates.json`
- `domain_pattern_findings.json`
- `sample_rows` (optional)

### Minimum input contract

- `table_profile.json` must include table/column metrics (null ratio, uniqueness ratio, duplicates, top values, parse readiness).
- `relationship_candidates.json` must include overlap/cardinality hypotheses.
- `domain_pattern_findings.json` must include pattern-level findings (e.g., conflicts, hierarchy instability, descriptor identity concerns).
- `sample_rows` can be used only as supporting context, never as primary evidence over metrics.

---

## Output

Return this exact structured shape:

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

### Output field guidance

`confidence_level` must be one of: `low`, `medium`, `high`.

`confidence_level` cannot be `high` if any of the following are true:
- selected grain has null-blocking risk
- key uniqueness is below perfect or near-perfect threshold
- major relationship coverage is below strong confidence
- unresolved SCD or cross-source conflict issues exist


- `business_process_guess`: short hypothesis (e.g., “sales transaction capture”).
- `entity_type_guess`: table tendency (e.g., event/fact-like, master/dimension-like, bridge-like, unclear).
- `grain_candidates`: list of candidate grains with evidence references.
- `recommended_grain`: best-supported candidate, still provisional.
- `dimension_candidates`: attribute groups likely to behave as dimensions.
- `fact_candidates`: event-like entities/measures likely suitable for fact modeling.
- `measure_candidates`: additive/semi-additive metric candidates (if evidence exists).
- `candidate_natural_keys`: possible business keys with completeness/uniqueness caveats.
- `data_quality_risks`: modeling-impacting risks (nulls, conflicts, parse failures, duplicates).
- `cross_source_conflicts`: conflicting entity attributes/identifiers across sources.
- `modeling_notes`: assumptions, caveats, unresolved questions.
- `confidence_level`: one of `low`, `medium`, `high`.
- `requires_human_decision`: must remain `true`.

---

## Required reasoning behavior

The skill must:

1. Use profiling metrics as primary evidence.
2. List all grain candidates explicitly and score each candidate qualitatively as `high`, `medium`, or `low`.
3. Grain scoring must consider:
   - uniqueness ratio
   - duplicate pattern
   - null blocking
   - relationship consistency
   - whether grain preserves important dimensional context
4. Select the highest-supported grain based on the scoring evidence, not narrative preference.
5. If no grain is clearly supported, set `recommended_grain` to `"uncertain"` and set `confidence_level` to `low` or `medium`.
6. For every candidate natural key, explicitly evaluate:
   - uniqueness evidence
   - null sensitivity
   - stability over time
   - business meaning
   - whether key appears synthetic or business-derived
   - why key may fail
7. Candidate natural keys must never be accepted based on naming alone.
8. If a fallback key removes a major dimension (`customer`, `product`, `store`, `date`, or `source system`), label it as `risky fallback`, explain dimensional context loss, and require explicit human/business policy before use.
9. Detect SCD-relevant signals when cross-source conflicts or changing descriptors exist; flag impacted attributes as SCD candidates and discuss whether Type 1 or Type 2 may be relevant, without finalizing SCD type.
10. For each relationship candidate include:
   - source column
   - target table/entity (if available)
   - overlap ratio
   - inferred cardinality (`many-to-one`, `one-to-many`, `one-to-one`, `many-to-many`, or `unclear`)
   - confidence (`low`, `medium`, `high`)
   - modeling implication
11. Distinguish fact-like vs dimension-like behavior based on structure and evidence, not naming conventions.
12. Highlight ambiguity instead of forced guessing.
13. State uncertainty explicitly when evidence is insufficient or conflicting.

---

## Constraints

- DO NOT hallucinate missing data.
- DO NOT finalize DWH structure.
- DO NOT invent business rules absent from evidence.
- ALWAYS provide reasoning behind each major output.

If an output cannot be supported:
- return a conservative placeholder (e.g., `"unclear"` or empty list),
- add a clear note in `modeling_notes`,
- lower `confidence_level`.

---

## Mandatory reasoning sections

Every run must include these reasoning sections in `modeling_notes` (or a sibling explanation block if your runtime wrapper supports it). Use the following structured headings for machine readability: `grain_notes`, `key_notes`, `dimension_notes`, `relationship_notes`, `quality_notes`, `scd_notes`, `unresolved_questions`.

1. **grain reasoning**
   - Why each grain candidate is plausible/improbable.
   - Which duplication/uniqueness signals support the recommendation.

2. **key reasoning**
   - Candidate natural key logic.
   - Completeness and uniqueness caveats.

3. **dimension vs fact reasoning**
   - Why entity behavior appears event-like vs descriptive/master-like.
   - Whether mixed behavior exists and requires decomposition.

4. **relationship reasoning**
   - Relationship hypotheses from overlap/cardinality evidence.
   - Confidence and unresolved conflicts.

5. **data quality impact**
   - How nulls, parse failures, and conflicts affect modeling reliability.
   - What must be remediated before final decisions.

---

## Style requirements

- Structured and deterministic response shape.
- Evidence-first claims only.
- No vague statements (“seems fine”, “looks good”) without metrics.
- Explicit assumptions and uncertainty markers.
- Clear separation between **observation**, **inference**, and **recommendation**.

---

## Suggested execution flow

1. Parse and validate input artifacts.
2. Summarize key technical signals (duplicates, uniqueness, cardinality, relationship overlap).
3. Build grain candidates and rank by evidence strength.
4. Identify entity behavior (fact-like/dimension-like/mixed).
5. Extract natural key candidates with caveats.
6. Compile data quality and cross-source risks.
7. Produce structured output with confidence and human-decision flag set to `true`.

---

## Example behavior (transaction-like dataset)

### Example input signals (simplified)
- `order_id` uniqueness: 0.42
- (`order_id`, `line_nbr`) uniqueness: 1.00
- `customer_id` null ratio: 0.01
- `order_date` date parse success: 0.99
- Relationship candidate: `customer_id` -> `customer.customer_id` overlap 0.97
- Duplicate signatures observed at order header level, not at line level

### Example interpretation (short)
- Grain candidates:
  - `order_id` (weak, duplicates too high)
  - (`order_id`, `line_nbr`) (strong, uniqueness supports line-grain)
- Recommended grain: `one row per order line`
- Fact-like signal: transactional measures present (e.g., amount/qty-like behavior)
- Dimension candidates: customer/product/date descriptors
- Risk: 1% missing `customer_id` may break full conformance
- Confidence: `medium`
- `requires_human_decision`: `true`

### Example output skeleton
```json
{
  "business_process_guess": "order capture",
  "entity_type_guess": "fact-like transactional",
  "grain_candidates": [
    "one row per order_id",
    "one row per order_id + line_nbr"
  ],
  "recommended_grain": "one row per order_id + line_nbr",
  "dimension_candidates": ["customer", "product", "date"],
  "fact_candidates": ["order_line_sales"],
  "measure_candidates": ["line_amount", "line_quantity"],
  "candidate_natural_keys": ["order_id + line_nbr"],
  "data_quality_risks": ["customer_id has 1% nulls"],
  "cross_source_conflicts": [],
  "modeling_notes": [
    "grain reasoning: line-level uniqueness is complete while header-level uniqueness is not.",
    "key reasoning: composite key is complete and unique in observed profile.",
    "dimension vs fact reasoning: repeated event pattern plus additive-like measures suggest fact behavior.",
    "relationship reasoning: high customer_id overlap supports customer dimension linkage.",
    "data quality impact: customer_id nulls require policy decision before strict FK enforcement."
  ],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

---

## Integration note

This skill is designed for later agentic workflows (e.g., Domain Pattern Agent / Modeling Agent handoff).
It should be invoked only after post-staging profiling artifacts are available.

---

## Test Fixture

Use the following human-readable fixture files to validate expected reasoning behavior:

- `test_inputs/semantic_profiling/transaction_like_profile.json`
- `test_inputs/semantic_profiling/EXPECTED_SEMANTIC_OUTPUT.md`

This fixture is a behavior contract for future Modeling Agent integration, not an automated test harness yet.



---

## Manual Run Audit Learnings

Based on the first manual run, this skill must enforce stronger reasoning discipline:

- formal grain scoring
- stronger natural key reasoning
- risky fallback labeling
- SCD awareness
- relationship cardinality + confidence interpretation
- structured reasoning notes for machine readability
