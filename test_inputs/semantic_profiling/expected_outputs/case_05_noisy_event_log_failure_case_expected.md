# Expected Semantic Behavior: case_05_noisy_event_log_failure_case

## Purpose
Ensure conservative behavior on noisy event logs with weak identity evidence.

## Expected JSON behavior
```json
{
  "business_process_guess": "web interaction event capture (low reliability)",
  "entity_type_guess": "event-like log (uncertain)",
  "grain_candidates": [
    "event_id",
    "session_id + event_timestamp + event_type",
    "user_id + event_timestamp + page_url"
  ],
  "recommended_grain": "uncertain",
  "dimension_candidates": ["user", "session", "date"],
  "fact_candidates": ["web_event_candidate"],
  "measure_candidates": [],
  "candidate_natural_keys": [],
  "data_quality_risks": ["event_id not unique enough", "high user_id null ratio", "weak composite keys", "properties_json parse issues"],
  "cross_source_conflicts": [],
  "modeling_notes": ["do not finalize fact design", "requires identity and dedup policy"],
  "confidence_level": "low",
  "requires_human_decision": true
}
```

## Expected reasoning
- Grain reasoning lists options but caveats each.
- Key reasoning emphasizes null-blocking and weak uniqueness.
- Fact vs dimension reasoning remains provisional.
- Unresolved questions ask for event-ID generation, dedup rules, timestamp quality, and user/session identity policy.

## What would count as a failure
- High-confidence `event_id` finalization.
- Final fact-table design claims as settled truth.
- SQL/DDL output.
- `requires_human_decision=false`.
