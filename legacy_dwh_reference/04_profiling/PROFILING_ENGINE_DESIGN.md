# Profiling Engine Design (Module 1)

## 1. Correct Profiling Context

The historical DWH profiling flow was **not** “raw CSV directly to modeling decisions.”

Profiling can happen at multiple stages, but the **main modeling-oriented profiling** happened after **basic clean staging**, where values became comparable and lineage remained available.

### Stage 1: Raw Intake

**Input examples**
- CSV / flat files
- Cloud object files
- PostgreSQL foreign/external table access

**Purpose**
- Readability/access check
- Schema alignment check
- File-level smoke tests (e.g., row count expectations)

### Stage 2: Raw Landing

**Input**
- Persisted raw landing tables

**Purpose**
- Preserve source rows with minimal transformation
- Maintain traceable ingestion history

**Typical lineage fields**
- `batch_id`
- `load_type`
- `source_file_name`
- `load_dts`
- `source_row_num`

### Stage 3: Clean Staging

**Input**
- Raw landing tables

**Purpose**
- Apply basic standardization before modeling profiling
- Keep transformations minimal, explicit, and auditable

**Typical standardization actions**
- `TRIM`
- `LOWER`
- `REPLACE` spaces with underscores
- `COALESCE` / `NULLIF` defaults
- Regex-based date parsing
- Regex-based numeric casting
- Preserve source lineage fields

### Stage 4: Post-Staging Profiling

**Input**
- Clean staging tables

**Purpose (main DWH modeling profiling layer)**
- Grain discovery
- Candidate key checks
- Duplicate analysis
- Cross-source conflict checks
- Entity identity checks
- Relationship inference
- Data quality rule design

---

## 2. Why Not Profile Only Raw CSV?

Raw-level profiling is useful for **file readiness and ingestion safety**, but it is insufficient alone for robust DWH modeling decisions.

### Why post-staging profiling is stronger for modeling

- Blank/null-like values are normalized.
- Casing/spacing noise is reduced.
- Date/numeric fields become more comparable.
- Source lineage is available for traceability.
- Candidate keys and duplicates can be tested more reliably.

### Important limitation

Too much cleansing before profiling can hide source quality problems.

**Therefore:** both raw-level and post-staging profiling are required, but for different goals:
- Raw-level profiling = intake and ingestion confidence
- Post-staging profiling = modeling-grade evidence

---

## 3. Profiling Layer Separation

| Profiling Stage | Input | Main Questions | Example Checks | Output Artifact | Used For |
|---|---|---|---|---|---|
| Raw intake profiling | Files / external tables | Can we read and structurally trust incoming files? | Header/schema validation, file row counts, mandatory column existence | `raw_intake_profile.json` | Intake readiness, ingestion smoke checks |
| Raw landing reconciliation | Raw landing tables + intake metadata | Did landing preserve expected source content? | Source vs landed row-count reconciliation, lineage completeness checks | `raw_landing_reconciliation.json` | Load validation, lineage confidence |
| Clean staging transformation audit | Raw + clean staging tables | Were basic standardizations applied correctly and transparently? | Null/blank normalization deltas, parse success deltas, audit of transformed fields | `clean_staging_audit.json` | Transformation trust, pre-modeling quality confidence |
| Post-staging technical profiling | Clean staging tables | What technical signals exist for keys, duplicates, and relationships? | Uniqueness/null ratios, candidate PK tests, overlap-based relationship candidates | `table_profile.json`, `relationship_candidates.json` | Technical evidence for modeling decisions |
| Domain-aware modeling profiling | Post-staging profiles + pattern logic | What modeling implications emerge from domain-aware patterns? | Reconciliation/conflict/grain/hierarchy patterns with evidence links | `domain_pattern_findings.json`, `grain_evidence_report.md`, `profiling_to_modeling_trace.md` | Grain, fact/dimension, natural key, SCD decision support |

---

## 4. Generic vs Domain-Aware Profiling

- **Generic profiling** works across datasets and provides deterministic technical metrics.
- **Domain-aware profiling** applies reusable reasoning patterns and must not hardcode retail entities.
- The historical retail profiling pack is a **worked example** of domain-aware reasoning performed mainly **after clean staging**.

This design keeps the engine reusable while preserving historical DWH decision quality.

---

## 5. Reusable Patterns from Historical Flow

| Pattern name | When to run | Required input stage | What question it answers | DWH modeling decision it supports | Possible JSON output fields |
|---|---|---|---|---|---|
| File/external table smoke test | Intake start | Raw intake | Is source readable and structurally aligned? | Whether ingestion can proceed safely | `file_name`, `read_success`, `observed_columns`, `expected_columns_missing`, `row_count_estimate` |
| Raw landing row-count reconciliation | After raw load | Raw landing | Did landing preserve source row volume? | Trust in upstream ingestion and reconciliation tolerance | `source_row_count`, `landed_row_count`, `delta_count`, `delta_ratio`, `status` |
| Lineage-aware raw load validation | After raw load | Raw landing | Is lineage complete enough for traceability? | Ability to audit and backtrack modeling anomalies | `lineage_fields_present`, `null_lineage_counts`, `batch_coverage`, `source_file_coverage` |
| Clean staging transformation audit | After clean staging refresh | Clean staging + raw landing | Did standardization improve comparability without losing traceability? | Confidence to use staged data for modeling profiling | `pre_post_null_delta`, `pre_post_parse_success_delta`, `transformed_columns`, `lineage_preserved` |
| Critical identifier completeness after standardization | Early post-staging profiling | Clean staging | Are key identifiers complete enough after normalization? | Candidate key viability and join reliability | `identifier_column`, `null_ratio`, `blank_ratio`, `effective_completeness_score` |
| Cast-readiness and parse-success checks | Post-staging profiling | Clean staging | Are dates/numerics reliably castable for downstream logic? | Readiness for facts, measures, and temporal modeling | `column_name`, `numeric_parse_success_ratio`, `date_parse_success_ratio`, `parse_error_examples` |
| Candidate transaction/event grain testing | Core modeling profiling | Clean staging | What event/transaction grain is supported by duplication patterns? | Fact grain definition | `grain_candidate_columns`, `duplicate_signature_count`, `uniqueness_ratio`, `grain_confidence` |
| Cross-source entity overlap/conflict testing | Core modeling profiling | Clean staging (multi-source) | Do entities overlap with conflicting attributes across sources? | Conformance, mastering, and SCD risk planning | `entity_key`, `overlap_ratio`, `conflict_columns`, `conflict_rate`, `source_pair` |
| Descriptor-based identity testing | Core modeling profiling | Clean staging | Do descriptive signatures indicate hidden duplicates/identity drift? | Natural key and entity resolution strategy | `descriptor_signature`, `signature_collision_count`, `conflicting_ids`, `identity_confidence` |
| Hierarchy stability testing | Core modeling profiling | Clean staging | Are hierarchical relationships stable and coherent? | Dimension hierarchy design and conformed key strategy | `child_key`, `parent_key`, `violating_rows`, `instability_ratio`, `hierarchy_status` |
| Cardinality and frequency snapshots | Core modeling profiling | Clean staging | What relationship/cardinality behavior appears in data? | Fact/dimension boundary and bridge-table need | `column_pair`, `cardinality_type`, `frequency_top_values`, `relationship_confidence` |

---

## 6. AI Copilot Use

Future AI agents should consume outputs stage-by-stage, not as a single undifferentiated profile dump.

### Data Intake Agent
- Uses raw intake artifacts to validate readability, schema shape, and intake smoke tests.
- Blocks downstream steps when intake safety checks fail.

### Standardization Audit Agent
- Uses raw landing + clean staging audit artifacts.
- Verifies minimal, transparent standardization and lineage preservation.

### Technical Profiling Agent
- Uses post-staging technical profiles.
- Produces deterministic key/duplicate/relationship evidence.

### Domain Pattern Agent
- Applies reusable patterns to technical evidence.
- Produces modeling-oriented findings with confidence and caveats.

### Modeling Agent
- Consumes traceability artifacts (`grain_evidence_report.md`, `profiling_to_modeling_trace.md`).
- Produces **proposed** modeling options, not auto-final decisions.

---

## 7. Human Approval Gate

AI can recommend but must not finalize the following without profiling evidence and explicit human approval:

- Grain
- Fact/dimension classification
- Natural keys
- SCD strategy
- DDL structure

### Governance rule

No final model decision is accepted unless:
1. Evidence exists in profiling artifacts.
2. Decision rationale is traceable.
3. Human reviewer signs off.

---

## 8. What Not To Do

- Do not run only generic pandas profiling and call it DWH profiling.
- Do not profile only raw CSV and infer final grain too early.
- Do not hardcode retail entities into the generic engine.
- Do not hide source quality problems by over-cleaning before profiling.
- Do not generate final DWH SQL before post-staging profiling and grain evidence.

---

## Design Outcome

This module design aligns with the corrected historical flow:

CSV / external access → raw landing → clean staging → profiling → modeling decisions.

It preserves both:
- Deterministic technical profiling
- Domain-aware, evidence-based reasoning for DWH architecture
