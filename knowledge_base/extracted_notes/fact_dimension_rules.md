# Fact vs Dimension Rules

## Rule
Entity classification MUST be based on behavioral evidence, not lexical labels.

## When to use
- During semantic interpretation of profiled tables.
- When recommending target dimensional structures.
- When deciding whether an entity is event-like, descriptive, or hybrid.

## Evidence required
- Repetition patterns and event signatures.
- Presence and type of aggregatable measures.
- Relationship directionality and cardinality.
- Attribute stability indicators.

## Copilot must NOT do
- Must NOT classify solely from suffixes/prefixes.
- Must NOT force binary classification when evidence is mixed.
- Must NOT ignore hybrid outcomes requiring decomposition.

## Human approval required
- Hybrid decomposition decisions.
- Reclassification that affects historical reports/KPIs.
