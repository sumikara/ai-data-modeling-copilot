# Failure Analysis Template

## Case ID
## Input fixture
## Expected behavior document
## Actual output file
## Grading report file
## Summary of result
- Passed:
- Overall score:
- Critical failures:

## Expected vs actual comparison
| Decision area | Expected | Actual | Match? | Notes |
|---|---|---|---|---|
| Business process | | | | |
| Entity type | | | | |
| Recommended grain | | | | |
| Natural keys | | | | |
| Fact/dimension classification | | | | |
| Data quality risks | | | | |
| SCD handling | | | | |
| Confidence level | | | | |
| Human decision gate | true | | | |

## Failure categories
Check all that apply:
- [ ] Overconfident grain decision
- [ ] Ignored duplicate/null evidence
- [ ] Invented business rules
- [ ] Confused fact vs dimension
- [ ] Finalized SCD type without enough evidence
- [ ] Failed to surface unresolved questions
- [ ] Generated SQL/DDL
- [ ] Did not ground reasoning in profile evidence
- [ ] Did not reference retrieved knowledge-base rules
- [ ] Missing required JSON keys

## Root cause hypothesis
Explain whether the failure seems caused by:
- weak prompt instruction
- insufficient profile evidence
- missing knowledge-base rule
- grader too weak
- ambiguous synthetic fixture
- model hallucination
- parsing/extraction issue

## Proposed fix
State whether to fix:
- prompt template
- knowledge base
- grader rule
- input profiling schema
- expected behavior document

## Follow-up test
Describe how to re-run and what improved behavior should look like.
