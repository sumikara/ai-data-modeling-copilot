"""Validation rules for semantic profiling JSON output."""

from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_KEYS = [
    "business_process_guess",
    "entity_type_guess",
    "grain_candidates",
    "recommended_grain",
    "dimension_candidates",
    "fact_candidates",
    "measure_candidates",
    "candidate_natural_keys",
    "data_quality_risks",
    "cross_source_conflicts",
    "modeling_notes",
    "confidence_level",
    "requires_human_decision",
]


LIST_KEYS = [
    "grain_candidates",
    "dimension_candidates",
    "fact_candidates",
    "measure_candidates",
    "candidate_natural_keys",
    "data_quality_risks",
    "modeling_notes",
]


VALID_CONFIDENCE_LEVELS = {"low", "medium", "high"}


def validate_semantic_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate semantic profiling output payload against required rules."""
    errors: List[str] = []
    warnings: List[str] = []

    for key in REQUIRED_KEYS:
        if key not in payload:
            errors.append(f"Missing required key: {key}")

    if errors:
        return {"is_valid": False, "errors": errors, "warnings": warnings}

    confidence_level = payload.get("confidence_level")
    if confidence_level not in VALID_CONFIDENCE_LEVELS:
        errors.append(
            "confidence_level must be one of: low, medium, high "
            f"(got: {confidence_level!r})"
        )

    if payload.get("requires_human_decision") is not True:
        errors.append("requires_human_decision must be true")

    for key in LIST_KEYS:
        if not isinstance(payload.get(key), list):
            errors.append(f"{key} must be a list")

    recommended_grain = payload.get("recommended_grain")
    if not isinstance(recommended_grain, str) or not recommended_grain.strip():
        errors.append("recommended_grain must not be empty")

    if isinstance(recommended_grain, str) and recommended_grain.strip() and recommended_grain != "uncertain":
        notes = payload.get("modeling_notes", [])
        if isinstance(notes, list):
            has_grain_note = any("grain" in str(note).lower() for note in notes)
            if not has_grain_note:
                errors.append(
                    "modeling_notes must contain at least one note mentioning grain "
                    "when recommended_grain != 'uncertain'"
                )

    if isinstance(payload.get("grain_candidates"), list) and len(payload["grain_candidates"]) == 0:
        warnings.append("grain_candidates is empty")

    if isinstance(payload.get("measure_candidates"), list) and len(payload["measure_candidates"]) == 0:
        warnings.append("measure_candidates is empty")

    return {"is_valid": len(errors) == 0, "errors": errors, "warnings": warnings}
