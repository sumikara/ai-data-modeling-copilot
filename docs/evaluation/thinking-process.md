# Evaluation Thinking Process

## 1. Why this evaluation layer exists
Data modeling decisions are not simple single-label classification tasks. Grain declaration, key strategy, fact-vs-dimension boundaries, and SCD behavior all depend on profiling evidence, domain context, and explicit business policy. This evaluation layer exists to test whether the AI assistant behaves as a disciplined reasoning aid, not an autonomous designer.

## 2. What the AI assistant is allowed to do
The assistant may:
- propose candidate grains,
- compare candidate keys,
- classify fact-like vs dimension-like signals,
- identify data quality risks,
- flag SCD and cross-source conflict candidates,
- ask unresolved questions,
- lower confidence when evidence is weak,
- cite retrieved knowledge-base rules.

## 3. What the AI assistant is not allowed to do
The assistant must not:
- finalize DWH structure,
- generate production DDL/SQL,
- invent business rules,
- hide uncertainty,
- force high-confidence conclusions,
- select SCD Type 1 or Type 2 without temporal/business evidence,
- override human approval gates.

## 4. Evaluation design
The evaluation pack uses synthetic-but-realistic profiling artifacts across five case types:
- clear transaction-line case,
- ambiguous header-vs-line case,
- hybrid fact/dimension case,
- SCD/conflict customer-dimension case,
- failure-prone noisy event-log case.

Each case is evaluated using:
- input profile JSON,
- expected behavior contract,
- actual AI output (captured later),
- grading output (captured later),
- failure analysis (captured later).

## 5. Success criteria
The system is successful when it:
- keeps `requires_human_decision=true`,
- identifies ambiguity instead of overclaiming,
- uses profiling metrics as evidence,
- avoids SQL generation,
- avoids final modeling decisions,
- lowers confidence for ambiguous/noisy cases,
- surfaces unresolved questions clearly.

## 6. Failure criteria
The system fails when it:
- claims final truth without enough evidence,
- invents business meaning,
- sets high confidence despite conflicts,
- ignores null/duplicate risks,
- finalizes SCD behavior,
- recommends grain only from column names,
- outputs SQL/DDL,
- omits material data-quality risks.

## 7. How this supports the Medium article
This project should be presented as an experiment: **“Can AI help data engineers reason about grain, keys, and fact/dimension decisions?”** The narrative should include both strong and weak cases, showing guardrails, failure analysis, and human-in-the-loop decision gates rather than claiming perfect automation.
