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
1. `knowledge_base/extracted_notes/grain_decision_rules.md` (score=13)
2. `knowledge_base/extracted_notes/dimensional_modeling_principles.md` (score=5)
3. `knowledge_base/extracted_notes/partitioning_parallelism_performance_optimization.md` (score=5)

**Why relevant:**
- File-level boost for `grain` correctly prioritizes grain-specific rules.
- Dimensional modeling principles remain strongly relevant for fact/dimension context.

**Acceptable?**
- **Yes (improved).** Ranking is now better aligned with query intent.

---

## Query 2
**Query:** `SCD type 2 natural key surrogate key customer attributes`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/scd_decision_rules.md` (score=16)
2. `knowledge_base/extracted_notes/dimensional_modeling_principles.md` (score=8)
3. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md` (score=6)

**Why relevant:**
- SCD file now ranks first due to `scd` boost and overlap.
- Supporting files provide key/dimension context.

**Acceptable?**
- **Yes (improved).** Desired SCD-first behavior achieved.

---

## Query 3 (Re-evaluated)
**Query:** `source triplet lineage source_system source_table source_id`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/source_triplet_and_lineage_rules.md` (score=11)
2. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md` (score=6)
3. `knowledge_base/extracted_notes/deduplication_and_conformance_rules.md` (score=6)

**Why relevant:**
- `lineage` boost now correctly elevates `source_triplet_and_lineage_rules.md` to rank #1.
- Remaining files are still contextually related to source/system traceability.

**Acceptable?**
- **Yes (fixed).** Previously weak case is now strong and targeted.

---

## Query 4 (Re-evaluated)
**Query:** `default row unknown member null foreign key`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/default_row_strategy.md` (score=20)
2. `knowledge_base/extracted_notes/dimensional_modeling_principles.md` (score=7)
3. `knowledge_base/extracted_notes/scd_decision_rules.md` (score=7)

**Why relevant:**
- Combined boosts for `default row` and `unknown member` strongly prioritize `default_row_strategy.md`.
- Supporting files include related FK/conformance semantics.

**Acceptable?**
- **Yes (fixed).** Previously weak case now retrieves the correct specialized rule file first.

---

## Query 5
**Query:** `partitioning fact table monthly refresh performance`

**Top retrieved files:**
1. `knowledge_base/extracted_notes/partitioning_parallelism_performance_optimization.md` (score=6)
2. `knowledge_base/extracted_notes/data_warehouse_etl_foundations.md` (score=3)
3. `knowledge_base/extracted_notes/dimensional_modeling_principles.md` (score=3)

**Why relevant:**
- Partitioning/performance file remains correctly ranked first by overlap.

**Acceptable?**
- **Yes (strong).** Maintains expected behavior.

---

## Hybrid Scoring Validation

Scoring now reflects:
- `keyword_overlap_score`
- `file_boost_score`
- `title_match_bonus`

Output now includes retrieval diagnostics:
- `file_name`
- `score`
- `why_selected`

This made ranking behavior transparent and easier to debug.

## Overall Verdict

- Retrieval quality is improved for targeted weak cases.
- Specifically, both previously weak queries are fixed:
  - source triplet/lineage query now returns lineage rules first,
  - default row query now returns default-row strategy first.
- System remains simple and local (no embeddings/vector DB), as required.
