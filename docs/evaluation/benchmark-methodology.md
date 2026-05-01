# Benchmark Methodology

Purpose: evaluate AI-assisted semantic modeling benchmark quality as decision support, not autonomous truth.

Scoring rubric: grain 30, fact_dimension 20, keys 15, data_quality 10, confidence 10, governance 15.

Critical failures include wrong forbidden grain, missing human gate, SQL/DDL output, overconfidence under ambiguity/conflict, and forced modeling claims without evidence.

Confidence calibration: low/medium allowed for ambiguous cases unless evidence is strong.

Human decision gate: `requires_human_decision=true` is mandatory.

Model comparison plan: run mock, llm, and gemini modes using identical fixtures and golden constraints.
