# Grain Decision Rules

## Rule
Grain MUST be declared explicitly and justified through duplication, uniqueness, and relationship evidence.

## When to use
- Before proposing any fact structure.
- When composite key candidates exist.
- When transaction headers and lines are both present.

## Evidence required
- Candidate grain scoring (high/medium/low).
- Uniqueness ratios for each grain candidate.
- Null-blocking impact on selected grain keys.
- Relationship consistency with dimension joins.

## Copilot must NOT do
- Must NOT leave grain implicit.
- Must NOT choose grain by intuition or table name.
- Must NOT finalize non-unique grain as final without risk disclosure.

## Human approval required
- Final grain declaration.
- Acceptance of uncertain or risk-compromised grain.
