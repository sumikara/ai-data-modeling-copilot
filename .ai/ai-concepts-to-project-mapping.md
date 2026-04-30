# AI Concepts → Project Mapping

## 1. AI Fluency Concepts

### Intent
**Concept (brief):** Intent is the explicit objective the system is trying to achieve.

**Repo mapping:**
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`
- `legacy_dwh_reference/04_profiling/ORIGINAL_DOMAIN_PROFILING.md`

**How implemented / planned:**
- Intent is currently documented as: build an evidence-first profiling foundation for DWH modeling decisions (grain, keying, relationships, validation), not a generic “run AI on CSV” demo.
- The design doc already encodes intent through stage separation and governance rules.

---

### Context
**Concept (brief):** Context is the operational and domain information needed to make correct decisions.

**Repo mapping:**
- `legacy_dwh_reference/` (entire folder as historical context corpus)
- `legacy_dwh_reference/MIGRATION_MATRIX.md`
- `legacy_dwh_reference/04_profiling/ORIGINAL_DOMAIN_PROFILING.md`

**How implemented / planned:**
- Context currently lives in markdown and legacy references.
- Future agents should retrieve from this corpus before suggesting modeling or SQL decisions.

---

### Iteration
**Concept (brief):** Iteration is refining outputs through repeated runs with feedback.

**Repo mapping:**
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md` (versioned design evolution)
- Git history (commit-by-commit refinement)

**How implemented / planned:**
- Iteration already occurs manually via document revisions.
- Later, iteration should be formalized as run → findings → human feedback → rerun with updated constraints.

---

### Evaluation
**Concept (brief):** Evaluation checks whether outputs are accurate, useful, and policy-compliant.

**Repo mapping:**
- Planned `09_validation_tests/` under `legacy_dwh_reference/`
- Profiling outputs described in `PROFILING_ENGINE_DESIGN.md` (e.g., `grain_evidence_report.md`, `profiling_to_modeling_trace.md`)

**How implemented / planned:**
- Full automated evaluation is not yet implemented.
- Evaluation is currently design-defined and should become executable checks in validation modules.

---

### Discernment
**Concept (brief):** Discernment is deciding when evidence is sufficient vs ambiguous.

**Repo mapping:**
- Human approval gate section in `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`

**How implemented / planned:**
- Discernment is encoded via “AI suggests, human approves” for grain, SCD, natural keys, and fact/dimension classification.

---

### Diligence
**Concept (brief):** Diligence is consistent adherence to process, traceability, and quality gates.

**Repo mapping:**
- Multi-stage pipeline + artifact requirements in `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`
- Repository hygiene files: `README.md`, `requirements.txt`, `.gitignore`

**How implemented / planned:**
- Diligence is currently process-documented.
- It becomes real when each pipeline stage emits required artifacts and fails closed on missing evidence.

---

## 2. Tools, Skills, Agents

### Definitions
- **Tool:** A callable capability that performs a bounded operation (e.g., profile table, run SQL, validate keys).
- **Skill:** A reusable workflow recipe that sequences tools with constraints and expected outputs.
- **Agent:** A goal-driven orchestrator that selects and runs skills/tools across steps, using memory/state and checkpoints.

### Project mapping

#### Already tools (or tool-like modules)
- `src/profiling/csv_reader.py` (data input utility)
- `src/profiling/column_profiler.py` (column metric generator)
- `src/profiling/key_detector.py` (key heuristics)
- `src/profiling/relationship_detector.py` (relationship heuristics)
- `src/profiling/profile_runner.py` (workflow entrypoint)

#### Will become tools
- Raw landing reconciliation executor (SQL-driven)
- Clean staging transformation audit executor
- Grain evidence generator
- Modeling trace generator
- Validation test runner (PK/FK/dup/grain checks)

Likely future paths:
- `src/profiling/` (extended SQL-capable profilers)
- `src/validation/` (new)
- `src/modeling/` (new)

#### Should be skills
- “Run full profiling pipeline” skill (intake → landing audit → staging audit → post-staging profiling)
- “Generate grain evidence pack” skill
- “Prepare modeling decision brief” skill

Skill source material:
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`
- `legacy_dwh_reference/04_profiling/ORIGINAL_DOMAIN_PROFILING.md`

#### Will be agents
- Data Intake Agent
- Standardization Audit Agent
- Technical Profiling Agent
- Domain Pattern Agent
- Modeling Agent

These are already conceptually defined in:
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`

---

## 3. Claude Code in Action (Agentic Workflow)

This project naturally fits a multi-step agentic workflow because DWH modeling decisions require staged evidence.

### Multi-step workflows
1. Ingest/read source descriptors and landing metadata.
2. Validate landing completeness and lineage.
3. Audit clean staging standardization.
4. Run technical profiling.
5. Run domain-aware pattern interpretation.
6. Produce modeling recommendations + traceability.
7. Require human approval before structural SQL outputs.

### Orchestration
- `src/profiling/profile_runner.py` is an early orchestrator for one segment (CSV profiling).
- The future orchestrator must cover SQL-based staging and profiling stages too.

### Structured execution
- Expected artifact chain is already documented in `PROFILING_ENGINE_DESIGN.md`.
- Structured outputs are required to avoid opaque LLM-only reasoning.

### Stateful reasoning
- State should include: batch lineage, staging audit deltas, candidate grain alternatives, and unresolved conflicts.
- This is currently design-level and not yet persisted as a formal state store.

### Pipeline mapping
- Profiling pipeline and staging→profiling→modeling flow are explicitly defined in `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`.

---

## 4. MCP (Model Context Protocol)

### What MCP is
MCP is a standard way for models/agents to access structured external context and tools (databases, files, services) through a consistent protocol.

### Current status in this repo
- Current repository state: **no MCP server/module is implemented yet**.

### Where MCP should fit next
- **Database access:** read profiling source tables, staging tables, and run controlled SQL checks.
- **File access:** expose profiling artifacts, legacy docs, and generated reports as retrievable resources.
- **Profiling execution:** trigger stage-specific profiling runs as MCP tools.
- **SQL execution:** controlled, audited SQL execution interface for validation/profiling queries.

Likely integration zones:
- new `mcp/` or `src/mcp/` module
- adapters around `src/profiling/` and future `src/validation/`

---

## 5. Hooks

### What hooks are
Hooks are pre/post execution controls that enforce policy, quality gates, and operational safety around workflow steps.

### Hook opportunities in this project

- **Before SQL generation**
  - Check that `grain_evidence_report.md` and `profiling_to_modeling_trace.md` exist and are current.
  - Block SQL generation if evidence is missing.

- **After profiling**
  - Validate required artifact completeness (`table_profile.json`, `relationship_candidates.json`, etc.).
  - Fail workflow if required outputs are absent or malformed.

- **Before modeling decisions**
  - Ensure unresolved conflict count is below threshold.
  - Require confidence + caveat sections for recommendations.

- **Before execution (DDL/DML)**
  - Require explicit human approval record.
  - Verify “what not to do” rules are not violated.

---

## 6. Evaluation & Grading Systems

### What evaluation/grading means
Evaluation grades whether agent outputs meet correctness, evidence, governance, and usefulness requirements.

### Mapping to this project
- **Validation layer:** maps to `legacy_dwh_reference/09_validation_tests/` intent and future executable validation modules.
- **Data quality checks:** null/blank, parse success, completeness, conflict rates from profiling artifacts.
- **Grain validation:** compare candidate grain signatures against duplication/event patterns.
- **Duplicate checks:** entity and event duplication metrics from post-staging profiles.
- **FK/PK validation:** candidate keys + relationship overlap checks + referential consistency tests.
- **Modeling correctness checks:** trace each recommendation to concrete evidence in profiling artifacts.

Expected grading outputs (future):
- pass/fail scorecards per stage
- confidence + risk tags
- “blocked until human review” flags for critical unresolved decisions

---

## 7. Prompt Engineering

### Core concepts
- **Structured prompts:** fixed sections, required evidence fields, and deterministic response schema.
- **Role prompting:** explicit agent role per task (e.g., profiler vs modeler).
- **Constraints:** hard rules (no DDL before evidence, no ungrounded assumptions).
- **Output formats:** JSON/markdown contracts for downstream automation.

### Mapping to this project
- **Future profiling agent prompts** should require stage, inputs, metric formulas, and artifact schema.
- **Modeling agent prompts** should require candidate alternatives + evidence citations + confidence + caveats.
- **SQL generation prompts** should require approved grain/key decisions before output.

Prompt guardrails should reference:
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`
- `legacy_dwh_reference/04_profiling/ORIGINAL_DOMAIN_PROFILING.md`

---

## 8. RAG (Retrieval Augmented Generation)

### What RAG is
RAG retrieves relevant repository/domain knowledge at runtime and injects it into model reasoning so outputs are grounded in real project context.

### Mapping to this repo

Primary knowledge base:
- `legacy_dwh_reference/` as domain and migration context
- `legacy_dwh_reference/04_profiling/ORIGINAL_DOMAIN_PROFILING.md`
- `legacy_dwh_reference/04_profiling/PROFILING_ENGINE_DESIGN.md`
- `legacy_dwh_reference/MIGRATION_MATRIX.md`
- `legacy_dwh_reference/10_known_errors_and_fixes/` (future troubleshooting memory)

### What AI should retrieve
- DWH rules and governance constraints
- Naming conventions and layer semantics
- SCD logic references (future content in `08_scd_logic/`)
- Profiling patterns and historical reasoning templates

### Practical retrieval design (future)
- Chunk docs by section headers.
- Attach metadata: layer, stage, decision type, confidence, last update.
- Retrieve top-k by task type (profiling, modeling, SQL generation, validation).
- Require citation of retrieved snippets in agent outputs.

---

## 9. What This Project Actually Is (Final Clarification)

### This project is **NOT**
- Not a generic “upload CSV and get perfect star schema” toy.
- Not a prompt-only SQL generator.
- Not a system where LLM intuition can replace profiling evidence.
- Not production-ready autonomous data modeling yet.

### This project **IS**
- An evidence-first AI Data Modeling Copilot foundation.
- A staged profiling + reasoning architecture rooted in DWH practice.
- A governance-aware system where AI proposes and humans approve critical decisions.
- A repo that is currently in design-and-foundation phase, with partial tooling and major agent/orchestration pieces still to be built.

---

## 10. Gaps Between Skilljar Knowledge and Current Repo

### Already implemented
- Foundational profiling modules under `src/profiling/`.
- Historical context and profiling design documentation under `legacy_dwh_reference/`.
- Explicit human-governance principles in profiling design.

### Partially implemented
- Orchestration exists only for early CSV-based profiling flow (`profile_runner.py`), not full SQL-stage flow.
- Validation and grading are defined conceptually but not yet executable.
- Agent role decomposition is documented but not implemented as runtime agents.

### Missing
- End-to-end multi-stage execution (raw intake → landing → staging audit → post-staging profiling).
- MCP integration for database/file/tool interoperability.
- Hook framework for pre/post policy checks.
- Formal evaluation harness and scorecards.
- RAG pipeline (indexing, retrieval, citations).
- Prompt templates and strict schemas per agent role.
- Human approval workflow implementation (records, status gates, audit trail).
- Modeling and SQL-generation modules that enforce evidence prerequisites.
