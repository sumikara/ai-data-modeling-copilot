# DWH Architecture Principles

## Rule
Modeling recommendations MUST respect layered DWH architecture and separation of responsibilities.

## When to use
- When mapping source data into target layers.
- When choosing where a rule should live (landing, staging, normalized, dimensional).
- When validating whether transformations are placed correctly.

## Evidence required
- Defined layer contracts.
- Upstream/downstream dependencies.
- Rerun safety and lineage preservation requirements.

## Copilot must NOT do
- Must NOT collapse layers to simplify reasoning.
- Must NOT push enterprise transformations into BI/reporting logic.
- Must NOT skip normalized integration checks before dimensional publication.

## Human approval required
- Any architecture exception (e.g., bypassing a layer).
- Trade-offs between performance and semantic correctness.
