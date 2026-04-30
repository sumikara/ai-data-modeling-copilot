# AGENT_WRAPPER_TEST_REPORT

## 1. Test command used

```bash
python scripts/run_semantic_profiling_mock.py
```

## 2. Input fixture path

- `test_inputs/semantic_profiling/transaction_like_profile.json`

## 3. Output path created

- `test_outputs/semantic_profiling/ACTUAL_SEMANTIC_OUTPUT.md`

## 4. Returned JSON keys

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

- **Yes**. All expected keys are present in the returned JSON dictionary.

## 6. Any errors encountered

- Initial run error encountered:
  - `ModuleNotFoundError: No module named 'src'` when running `python scripts/run_semantic_profiling_mock.py`.
- Resolution applied:
  - Added repository root insertion into `sys.path` in `scripts/run_semantic_profiling_mock.py`.
- Final run status:
  - Completed successfully with JSON output printed and markdown output file written.

## 7. Current limitation

- The mock LLM does **not** perform real semantic reasoning yet.
- Real LLM/API integration is future work.
