# AI Data Modeling Copilot Repository Audit (2026-04-30)

## 1. Repo Structure

### Top-level implementation areas
- `.ai/` — prompt/skill contracts + concept mapping docs.
- `knowledge_base/` — extracted notes, local rules, approved-source metadata, worked examples.
- `src/` — Python runtime implementation (agent wrapper, deterministic profiling, validator).
- `scripts/` — manual runners for mock/LLM/Gemini and validation.
- `test_inputs/` and `test_outputs/` — single fixture and generated markdown/raw artifacts.
- `legacy_dwh_reference/` — conceptual/reference design docs (not runtime-integrated).

### Focused directory snapshot
- `.ai/prompts/semantic-profiling-prompt-template.md`
- `.ai/skills/semantic-profiling-skill.md`
- `src/agents/semantic_profiling_agent.py`
- `src/profiling/{csv_reader.py,column_profiler.py,key_detector.py,relationship_detector.py,profile_runner.py}`
- `src/validation/semantic_output_validator.py`
- `scripts/{run_semantic_profiling.py,run_semantic_profiling_mock.py,validate_semantic_output.py}`
- `knowledge_base/{approved_sources,extracted_notes,local_rules,worked_examples}`

Assessment: structure is coherent for a prototype; runtime paths are narrow (one implemented agent + support utilities).

---

## 2. Knowledge Base Audit

### Are files split by topic?
Yes. Topics are split into many focused files (SCD, partitioning, PL/pgSQL, query optimization, ETL, etc.) plus local rule files and a worked example.

### AI-usable vs notes
- Many files are now structured with “AI Copilot rules”, constraints, and approval gates.
- However, there is no machine retrieval/indexing pipeline that makes these files executable context.

### Do files contain rules/constraints/decision logic?
Mostly yes in `extracted_notes/` and `local_rules/` (explicit rule bullets and guardrails).

### RAG readiness
Partially RAG-ready (content format is usable), but operationally **not RAG-enabled** (no chunking/indexing/retriever integration in runtime agent path).

### File-by-file usability classification

#### `knowledge_base/extracted_notes/`
- **Usable by AI**
  - `ai_fluency_operating_principles.md`
  - `data_warehouse_etl_foundations.md`
  - `deduplication_and_conformance_rules.md`
  - `dimensional_modeling_principles.md`
  - `etl_orchestration_and_quality_rules.md`
  - `query_execution_join_optimizer_rules.md`
  - `scd_decision_rules.md`
  - `partitioning_parallelism_performance_optimization.md`
  - `plpgsql_functions_procedures_server_side_logic.md`
  - `dwh_refresh_materialized_views_final_system_design.md`
- **Partially usable**
  - `methodology_summary.md` (high-level summary; less directly executable)
  - `dwh_architecture_principles.md` (short, principle-only)
  - `default_row_strategy.md` (narrow scope)
  - `fact_dimension_rules.md` (short rule card)
  - `grain_decision_rules.md` (short rule card)
  - `source_triplet_and_lineage_rules.md` (short rule card)
- **Not usable**
  - none strictly unusable as content; unusability is mainly due to missing retrieval wiring.

#### `knowledge_base/local_rules/`
- **Usable by AI**
  - `data_quality_rules.md`, `deduplication_rules.md`, `dwh_architecture_rules.md`, `layer_responsibilities.md`, `lineage_rules.md`, `performance_rules.md`, `scd_rules.md`
- These are concise and policy-like, but currently documentation-only at runtime.

#### Other KB areas
- `approved_sources/` and `worked_examples/` are **partially usable** reference artifacts; no code consumes them.

---

## 3. Agent Layer Audit

### What agents exist?
Only one runtime agent module: `src/agents/semantic_profiling_agent.py`.

### What it actually does
- Loads profiling artifacts from a combined JSON or directory structure.
- Injects artifacts into a prompt template.
- Executes one of three modes:
  - `mock`: deterministic hardcoded response
  - `llm`: OpenAI chat completion
  - `gemini`: Gemini generate_content with fallback/retry
- Parses JSON out of LLM text output and writes markdown/raw output files.

### Does it use prompt templates?
Yes (`.ai/prompts/semantic-profiling-prompt-template.md`).

### Does it use knowledge base?
No direct use of `knowledge_base/` in code path.

### Does it use profiling artifacts?
Yes, explicitly (`table_profile`, `relationship_candidates`, `domain_pattern_findings`, optional `sample_rows`).

### Prompt+LLM wrapper or real reasoning pipeline?
Primarily prompt orchestration + provider call + JSON parsing. Reasoning itself is delegated to LLM output contract; there is no symbolic planner, policy engine, or multi-step agent graph.

---

## 4. Prompt System Audit

### Reusability
Moderately reusable: strong placeholders and explicit contract sections.

### Structure quality
High for a single prompt: includes required inputs, prohibited actions, reasoning checklist, output schema, and confidence rules.

### Determinism
Partial only:
- deterministic for `mock` mode,
- non-deterministic for live LLM providers despite temperature 0 (still model variability).

### Constraint enforcement
Prompt enforces behavior textually; hard enforcement in runtime is limited to output-key validation and simple checks (not deep policy compliance).

---

## 5. Skill System Audit

### Are skills well defined?
Yes, `semantic-profiling-skill.md` is detailed and specific.

### Are they actually used?
Only indirectly as documentation context. Runtime code does not parse or execute skill files as formal machine policies.

### Enforceable or documentation?
Mostly documentation. Enforceability is weak without a runtime rule engine.

---

## 6. Test System Audit

### Inputs/outputs
- One primary input fixture (`transaction_like_profile.json`).
- Output files are mostly generated artifacts and manual reports.

### Meaningfulness
- Validator checks output shape, required keys, list typing, and minimal grain-note linkage.
- It does **not** validate semantic correctness, evidence quality, hallucination risk, or business-model validity.

Conclusion: tests validate contract structure, not model correctness.

---

## 7. LLM Integration Audit

### Mock vs real usage
- `mock` mode is robust and deterministic.
- OpenAI/Gemini modes rely on environment keys and basic client calls.

### Correct usage quality
- OpenAI call is straightforward and acceptable for prototype use.
- Gemini fallback and retry logic exists with two model names and retry-on-unavailable heuristics.

### JSON parsing robustness
Reasonably robust for common formats:
- fenced `json` block,
- generic fenced block,
- first top-level JSON object scan.

### Error handling maturity
Prototype-grade:
- catches provider failures and returns structured error payloads,
- writes fallback raw output file when possible,
- lacks telemetry, typed exception taxonomy, circuit breakers, and retry observability.

---

## 8. Retrieval / RAG Audit (Critical)

No retrieval system exists in runtime:
- no vector DB,
- no embedding pipeline,
- no keyword retrieval,
- no document selection/ranking,
- no context injection from `knowledge_base/` at inference time.

Result: LLM runs blind to repository knowledge base unless a human manually pastes context.

---

## 9. MCP / Tooling Audit

No repository-internal MCP server/tool abstraction found.
- No MCP server config or runtime tool routing layer in `src/`.
- No external knowledge connector layer.

Scripts provide manual execution only.

---

## 10. System Maturity Evaluation

Overall classification: **Semi-working prototype**.

- **Production-ready component(s):** deterministic CSV profiling utilities are close to productionizable building blocks.
- **Prototype component(s):** semantic profiling agent, prompt/skill enforcement, and validation harness.
- **Conceptual/documentation-heavy areas:** large portions of knowledge base and legacy reference.

Not a production-ready end-to-end AI Data Modeling Copilot.

---

## 11. Top 10 Critical Gaps

1. No retrieval/RAG integration from `knowledge_base/` into agent runtime.
2. No multi-agent orchestration (single wrapper only, no planner/evaluator workflow).
3. No policy engine to enforce skill/rule constraints programmatically.
4. No semantic correctness tests (only structural JSON validation).
5. Very limited fixtures; no broad dataset/model scenario coverage.
6. No persistent run metadata/trace store for auditability and regression analysis.
7. No robust production observability (metrics, traces, failure taxonomy, SLOs).
8. No deployment/runtime packaging for service operation (API layer, job runner, config profiles).
9. No governance execution layer (approval workflow, lineage capture, role-based action gates).
10. No automated benchmarking against expected modeling decisions (golden set evaluation).

---

## 12. Brutally Honest Final Verdict

This system is **real as a prototype scaffolding**, not fake—but much of its “copilot intelligence” is currently conceptual/documentary.

What is real now:
- deterministic profiling code,
- a callable semantic wrapper with provider integrations,
- prompt/skill contracts,
- a large curated knowledge corpus.

What is missing for a true copilot:
- retrieval-grounded reasoning,
- enforceable decision policies,
- multi-step agentic workflow,
- semantic evaluation harness,
- production operations/governance stack.

**Actual current state:** a well-organized, evidence-oriented prototype with useful components, but not yet a production AI Data Modeling Copilot system.
