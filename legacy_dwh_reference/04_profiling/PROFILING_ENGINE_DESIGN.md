# Profiling Engine Design (Module 1)

## 1. Goal of the Profiling Engine

The first profiling module of the AI Data Modeling Copilot must be designed as a **two-layer engine**:

1. **Generic profiling layer** (dataset-agnostic)
2. **Domain-aware profiling pattern layer** (reasoning-pattern aware, not entity hardcoded)

This separation preserves reusability while still capturing the practical modeling intelligence seen in the original domain profiling work.

- The **generic layer** produces deterministic baseline statistics and structural signals for any tabular source.
- The **domain-aware layer** interprets those signals through reusable data warehousing patterns to support modeling decisions.

The objective is to produce **evidence artifacts** that are machine-readable, reviewable by humans, and traceable to downstream DWH design decisions.

---

## 2. Generic Profiling Layer

The generic profiling layer defines universal checks that should work for any dataset, regardless of business domain.

### 2.1 Table-level checks

- Row count
- Column count

### 2.2 Column-level checks

- Data type inference
- Null ratio and blank ratio
- Distinct count
- Uniqueness ratio
- Duplicate value count
- Top values / frequency distribution snapshot
- Min/max (where type-compatible)
- Numeric parse readiness
- Date parse readiness

### 2.3 Key-oriented checks

- Candidate primary key detection
- Possible natural key detection
- Low-cardinality categorical detection

### 2.4 Cross-table checks

- Cross-table column-name matching
- Value overlap-based relationship candidates

### 2.5 Generic layer principles

- Deterministic outputs (same input => same output)
- No domain hardcoding
- Reproducible calculations
- Clear metrics definitions
- Machine-readable outputs for downstream interpretation

---

## 3. Domain-Aware Profiling Pattern Layer

The domain-aware pattern layer converts legacy domain logic into reusable reasoning templates.

**Important:** The goal is to extract transferable patterns from the retail profiling approach **without hardcoding retail entities, table names, or assumptions**.

### Pattern catalog

| Pattern name | What question it answers | Original retail example | Generalized version | Possible output artifact | DWH modeling decision it supports |
|---|---|---|---|---|---|
| Source-to-source reconciliation pattern | Do two source representations of the same business data agree? | EXT vs SRC reconciliation checks | Compare paired upstream representations (landing vs curated source, API vs file extract, etc.) using row-level and key-level alignment metrics | `domain_pattern_findings.json` + reconciliation section in `profile_summary.md` | Source trust ranking, preferred source selection, merge strategy |
| Critical identifier completeness pattern | Are business-critical IDs complete enough to support joins and keys? | Blank checks on critical identifiers | Evaluate null/blank ratios for join-critical identifiers and required business keys | `domain_pattern_findings.json` | Join feasibility, candidate key viability, DQ rule priorities |
| Repeated transaction / event grain pattern | Does the data contain repeated events that reveal true fact grain? | Duplicate transaction and line-grain checks | Detect repeated event signatures and multiplicity by candidate grain columns | `grain_evidence_report.md` + `domain_pattern_findings.json` | Fact table grain definition, degenerate dimension decisions |
| Descriptor-based entity identity pattern | Can descriptive attributes reveal duplicate or fragmented entity identity? | Product descriptor duplication and descriptor hash comparison | Compare normalized descriptor signatures/hashes to detect same-entity variants across records | `domain_pattern_findings.json` | Natural key design, entity resolution rules, survivorship logic |
| Cross-source entity conflict pattern | Do entities conflict across source systems? | Customer overlap and conflicts across sources | Detect overlapping identifiers with conflicting attributes/status across systems | `domain_pattern_findings.json` + conflict appendix in `profile_summary.md` | Mastering strategy, conformance rules, SCD risk awareness |
| Geography/location hierarchy stability pattern | Is location hierarchy consistent enough for dimensional modeling? | Geography consistency and business key checks | Validate hierarchical consistency (e.g., child-parent compatibility, code-name coherence) | `domain_pattern_findings.json` | Dimension hierarchy design, conformed geography key strategy |
| Cardinality snapshot pattern | What cardinality behavior suggests relationship type and table role? | Cardinality snapshots from source profiling | Capture cardinality signatures for key column pairs over snapshots | `relationship_candidates.json` + `profile_summary.md` | 1:1 vs 1:N reasoning, bridge need detection, dimension/fact boundary |
| Source-specific attribute presence pattern | Which attributes exist only in specific sources and what does that imply? | Source-specific field presence observations | Track attribute sparsity/presence by source and segment | `domain_pattern_findings.json` | Mapping coverage, optionality decisions, satellite/extension table design |
| Cleansing-standardization need detection pattern | Where does formatting inconsistency block keying, joins, or metrics? | Date-format and numeric-like text quality checks | Detect parse instability, format drift, unit inconsistency, and text normalization need | `domain_pattern_findings.json` + DQ section in `profile_summary.md` | Pre-staging normalization rules, parsing contracts, validation checks |

### Domain-aware layer principles

- Pattern-based, not domain-hardcoded
- Evidence-first interpretation
- Explicit confidence and caveats per finding
- Every suggested decision must link to profiling evidence

---

## 4. AI Copilot Use

Future AI Copilot components should consume profiling outputs as structured evidence for decision support, not as blind automation triggers.

Primary use areas:

- **Grain discovery**: infer candidate grains from repeat-pattern and uniqueness evidence.
- **Fact/dimension reasoning**: classify entity role using cardinality, change behavior, and event repetition signals.
- **Candidate key selection**: rank technical vs natural key options with completeness and uniqueness support.
- **Source-to-target mapping**: align source attributes to target model using reconciliation and attribute-presence signals.
- **SCD decision support**: identify change volatility and conflict patterns that indicate SCD strategy candidates.
- **Data quality rule generation**: transform recurring quality findings into formal DQ checks.
- **Validation test design**: derive regression-ready tests tied to expected grain, keys, and relationships.

---

## 5. Required Output Artifacts

The profiling engine must emit the following artifacts:

1. `table_profile.json`  
   Per-table generic profiling metrics.

2. `relationship_candidates.json`  
   Cross-table relationship hypotheses with overlap and confidence signals.

3. `domain_pattern_findings.json`  
   Pattern-layer findings, each mapped to evidence and suggested modeling implications.

4. `profile_summary.md`  
   Human-readable consolidated summary of profiling outcomes.

5. `grain_evidence_report.md`  
   Explicit grain reasoning report with supporting metrics and unresolved ambiguities.

6. `profiling_to_modeling_trace.md`  
   Traceability matrix from profiling evidence to proposed modeling decisions.

---

## 6. Human Approval Gate

Profiling can produce **recommendations**, but it must not auto-finalize critical modeling decisions.

The following decisions require explicit human approval:

- Grain
- SCD type
- Natural key
- Fact/dimension classification

### Gate policy

- Engine output = **suggested decision + evidence + confidence + caveats**
- Human reviewer = **final decision authority**
- Any unapproved suggestion must remain a draft recommendation

---

## 7. What Not To Do

To protect model quality and governance, the profiling module must explicitly avoid the following:

- Do not hardcode retail assumptions into the generic profiler.
- Do not treat old retail SQL as universal logic.
- Do not let LLM components invent modeling decisions without profiling evidence.
- Do not generate SQL DWH structures before profiling and grain evidence exist.

---

## Design Outcome

This design ensures the first module is:

- Deterministic
- Evidence-driven
- Domain-adaptable
- Human-governed
- Ready to evolve into AI-assisted (but not AI-hallucinated) data modeling workflows
