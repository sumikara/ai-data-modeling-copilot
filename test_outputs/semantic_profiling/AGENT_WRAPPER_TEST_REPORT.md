# AGENT_WRAPPER_TEST_REPORT

## 1. Test command used

```bash
python scripts/run_semantic_profiling.py
```

## 2. Input fixture path

- `test_inputs/semantic_profiling/transaction_like_profile.json`

## 3. Output path created

- `test_outputs/semantic_profiling/ACTUAL_SEMANTIC_OUTPUT.md`
- `test_outputs/semantic_profiling/ACTUAL_LLM_RAW_OUTPUT.md`
- `test_outputs/semantic_profiling/ACTUAL_GEMINI_RAW_OUTPUT.md`

## 4. Returned JSON keys (mock mode)

- `business_process_guess`
- `entity_type_guess`
- `grain_candidates`
- `recommended_grain`
- `dimension_candidates`
- `fact_candidates`
- `measure_candidates`
- `candidate_natural_keys`
- `data_quality_risks`
- `cross_source_conflicts`
- `modeling_notes`
- `confidence_level`
- `requires_human_decision`

## 5. Whether all expected keys are present

- **Yes**. All expected keys are present in mock-mode returned JSON.

## 6. Any errors encountered

- `llm` mode error: `Missing OPENAI_API_KEY environment variable`.
- `gemini` mode error: `Missing GEMINI_API_KEY environment variable`.

## 7. Parser issue

Observed issue from audit context:
- Some provider outputs may contain valid JSON but not inside a fenced ```json block, causing:
  - `No fenced ```json block found in LLM output`

## 8. Fix applied

Updated JSON extraction to support robust fallbacks:

1. Parse fenced ` ```json ` blocks first.
2. Parse generic fenced ` ``` ` blocks containing JSON.
3. Fallback to first top-level JSON object by:
   - finding first `{`
   - matching braces until corresponding closing `}`
   - handling string/escape states to avoid brace mismatches inside quoted values.
4. Trim whitespace/invisible prefix chars before parsing.

## 9. Gemini mode parse result

- Full Gemini provider call could not be completed in this environment due to missing `GEMINI_API_KEY`.
- Parser behavior was verified with synthetic representative outputs and succeeded for:
  - fenced ` ```json ` output
  - generic fenced ` ``` ` output
  - unfenced JSON followed by reasoning text
  - JSON containing `}` inside quoted string values

## 10. Current limitation

- Real LLM/Gemini execution requires valid environment credentials and network access.
- Parsing is robust, but end-to-end provider execution still depends on key availability.
