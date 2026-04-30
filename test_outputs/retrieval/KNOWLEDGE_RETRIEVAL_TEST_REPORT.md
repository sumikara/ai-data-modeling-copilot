# KNOWLEDGE RETRIEVAL TEST REPORT

## Test Date
- 2026-04-30

## Test Command
```bash
python scripts/test_knowledge_retrieval.py
```

## Query 1
**Query:** `grain decision fact dimension transaction dataset`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/dimensional_modeling_principles.md`
2. `knowledge_base/extracted_notes/grain_decision_rules.md`
3. `knowledge_base/extracted_notes/partitioning_parallelism_performance_optimization.md`

**Why relevant:**
- Dimensional modeling principles directly cover fact vs dimension decisions and grain declaration.
- Grain decision rules file is explicitly aligned with grain selection.
- Partitioning note is partially relevant due to fact-table design/performance overlap.

**Acceptable?**
- **Yes (good).** Top 2 are highly relevant.

**Weak/missing points:**
- Third result could be replaced by a more directly semantic-modeling-specific rule file if available.

---

## Query 2
**Query:** `SCD type 2 natural key surrogate key customer attributes`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/dimensional_modeling_principles.md`
2. `knowledge_base/extracted_notes/scd_decision_rules.md`
3. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md`

**Why relevant:**
- SCD decision rules are directly relevant to Type 2 handling.
- Dimensional modeling principles include key modeling and dimension behavior guidance.
- ETL foundations provide supporting context for surrogate/business key handling flows.

**Acceptable?**
- **Yes (good).** Relevant SCD and modeling files are present in top 3.

**Weak/missing points:**
- `scd_decision_rules.md` ideally should rank first for this query.

---

## Query 3
**Query:** `source triplet lineage source_system source_table source_id`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md`
2. `knowledge_base/extracted_notes/deduplication_and_conformance_rules.md`
3. `knowledge_base/local_rules/layer_responsibilities.md`

**Why relevant:**
- ETL foundations and dedup/conformance include source-system handling concepts.
- Layer responsibilities can include lineage flow ownership.

**Acceptable?**
- **Partially acceptable.** Results are related, but not optimal.

**Weak/missing points:**
- `knowledge_base/extracted_notes/source_triplet_and_lineage_rules.md` should appear in top results and did not.
- Indicates weakness in plain keyword overlap and chunk targeting.

---

## Query 4
**Query:** `default row unknown member null foreign key`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/dimensional_modeling_principles.md`
2. `knowledge_base/extracted_notes/scd_decision_rules.md`
3. `knowledge_base/extracted_notes/deduplication_and_conformance_rules.md`

**Why relevant:**
- Dimensional modeling and SCD notes can mention unknown/default key handling context.
- Dedup/conformance includes key integrity and quality concerns.

**Acceptable?**
- **Partially acceptable.** Related, but not specific enough.

**Weak/missing points:**
- `knowledge_base/extracted_notes/default_row_strategy.md` should likely rank in top 3 and did not.

---

## Query 5
**Query:** `partitioning fact table monthly refresh performance`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/partitioning_parallelism_performance_optimization.md`
2. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md`
3. `knowledge_base/extracted_notes/dimensional_modeling_principles.md`

**Why relevant:**
- Partitioning/performance note is exactly aligned with query intent.
- ETL foundations and dimensional modeling provide supporting context for fact-table and refresh strategy.

**Acceptable?**
- **Yes (strong).** Primary result is highly relevant.

**Weak/missing points:**
- Could also benefit from `dwh_refresh_materialized_views_final_system_design.md` in top 3 for explicit refresh focus.

---

## Overall Retrieval Assessment

- Local keyword retrieval is functioning and returns generally relevant context for broad modeling/performance prompts.
- Strong cases: Query 1, Query 2, Query 5.
- Weak cases: Query 3 (lineage/source triplet specificity), Query 4 (default row strategy specificity).

## Obvious Missing/Weak Retrieval Cases

1. Exact-domain files with narrow terms can be outranked by longer high-frequency docs.
2. No phrase weighting or exact-title boosting (e.g., `source_triplet`, `default_row`).
3. Chunk extraction chooses first matching window; may miss the most semantically relevant section in a file.

## Acceptability Verdict

- **Acceptable for current simple local RAG smoke stage**, with clear precision limitations expected from pure keyword overlap.
- Suitable as a baseline before adding weighted scoring or vector retrieval.
