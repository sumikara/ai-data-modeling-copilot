"""Evaluation/grading layer for semantic profiling outputs."""

from __future__ import annotations

import re
from typing import Any, Dict, List

REQUIRED_KEYS = {
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
}

VALID_CONFIDENCE = {"low", "medium", "high"}


def _contains_sql_or_ddl(text: str) -> bool:
    patterns = [r"\bselect\b", r"\binsert\b", r"\bupdate\b", r"\bdelete\b", r"\bcreate\s+table\b", r"\balter\s+table\b"]
    lowered = text.lower()
    return any(re.search(p, lowered) for p in patterns)


def grade_semantic_output(output: dict, retrieved_context: str = "") -> dict:
    """
    Return grading result for semantic profiling output.
    """
    checks: List[Dict[str, Any]] = []
    critical_failures: List[str] = []
    recommendations: List[str] = []

    def add_check(name: str, passed: bool, notes: str, score_pass: int = 100, score_fail: int = 0) -> None:
        checks.append({"name": name, "score": score_pass if passed else score_fail, "passed": passed, "notes": notes})

    # 1. Required JSON keys exist
    missing = sorted(REQUIRED_KEYS - set(output.keys()))
    passed = len(missing) == 0
    add_check("required_json_keys", passed, "All required keys present." if passed else f"Missing keys: {missing}")
    if not passed:
        critical_failures.append("Missing required JSON keys.")

    # 2. confidence_level valid
    conf = output.get("confidence_level")
    passed = conf in VALID_CONFIDENCE
    add_check("valid_confidence_level", passed, f"confidence_level={conf!r}")

    # 3. requires_human_decision true
    rhd = output.get("requires_human_decision") is True
    add_check("requires_human_decision_true", rhd, f"requires_human_decision={output.get('requires_human_decision')!r}")
    if not rhd:
        critical_failures.append("requires_human_decision must be true.")

    # 4. grain_candidates not empty
    grains = output.get("grain_candidates") if isinstance(output.get("grain_candidates"), list) else []
    passed = len(grains) > 0
    add_check("grain_candidates_non_empty", passed, f"grain_candidates count={len(grains)}")
    if not passed:
        recommendations.append("Provide at least one evidence-based grain candidate.")

    # 5. recommended_grain present or uncertain
    rg = output.get("recommended_grain")
    passed = isinstance(rg, str) and rg.strip() != ""
    add_check("recommended_grain_present_or_uncertain", passed, f"recommended_grain={rg!r}")

    # 6. grain reasoning evidence in modeling_notes
    notes = output.get("modeling_notes") if isinstance(output.get("modeling_notes"), list) else []
    notes_text = "\n".join(str(n) for n in notes)
    has_grain_evidence = any(token in notes_text.lower() for token in ["grain_notes", "grain reasoning", "grain"])
    add_check("grain_reasoning_evidence", has_grain_evidence, "Modeling notes include grain reasoning evidence." if has_grain_evidence else "No grain reasoning evidence found in modeling_notes.")

    # 7. data_quality_risks not empty
    risks = output.get("data_quality_risks") if isinstance(output.get("data_quality_risks"), list) else []
    passed = len(risks) > 0
    add_check("data_quality_risks_non_empty", passed, f"data_quality_risks count={len(risks)}")
    if not passed:
        recommendations.append("Include concrete data quality risks that influence modeling decisions.")

    # 8. if SCD/conflict appears, output must not finalize SCD type
    all_text = (notes_text + "\n" + str(output.get("cross_source_conflicts", ""))).lower()
    scd_or_conflict_present = any(t in all_text for t in ["scd", "conflict", "cross_source"])
    finalized_scd = any(t in all_text for t in ["final scd type", "use type 1", "use type 2", "finalize scd"]) and "do not finalize" not in all_text
    passed = not (scd_or_conflict_present and finalized_scd)
    add_check("scd_not_finalized_when_conflict_present", passed, "No finalized SCD type detected under conflict context." if passed else "SCD type appears finalized despite conflict/SCD signals.")
    if not passed:
        critical_failures.append("SCD type was finalized despite conflict/SCD signals.")

    # 9. context contradiction check
    contradiction = False
    contradiction_notes = "No obvious contradiction detected."
    if retrieved_context:
        ctx = retrieved_context.lower()
        out = (str(output.get("recommended_grain", "")) + "\n" + notes_text).lower()
        if "requires_human_decision" in ctx and output.get("requires_human_decision") is not True:
            contradiction = True
            contradiction_notes = "Output contradicts context emphasis on human decision requirement."
    add_check("no_obvious_context_contradiction", not contradiction, contradiction_notes)

    # 9b. knowledge grounding evidence when retrieved context is provided (warning-only)
    if retrieved_context:
        source_labels = re.findall(r"^### Source: (.+)$", retrieved_context, flags=re.MULTILINE)
        notes_lower = notes_text.lower()
        has_section = "knowledge grounding" in notes_lower or "knowledge_grounding" in notes_lower
        source_hits = 0
        for src in source_labels:
            stem = src.split("/")[-1].replace(".md", "").replace("_", " ").lower()
            key_terms = [t for t in stem.split() if len(t) > 3]
            if any(t in notes_lower for t in key_terms):
                source_hits += 1
        grounded = has_section or source_hits > 0
        add_check(
            "knowledge_grounding_evidence",
            grounded,
            "Knowledge grounding detected in modeling notes." if grounded else "No explicit knowledge grounding references found.",
            score_pass=100,
            score_fail=60,
        )
        if not grounded:
            recommendations.append(
                "Add SECTION 3 knowledge grounding or reference retrieved KB rules in modeling_notes."
            )

    # 10. output must not contain final SQL or DDL
    sql_found = _contains_sql_or_ddl(str(output))
    add_check("no_final_sql_or_ddl", not sql_found, "No SQL/DDL patterns found." if not sql_found else "Found SQL/DDL-like text in output.")
    if sql_found:
        critical_failures.append("Output contains SQL/DDL, violating guardrails.")

    overall_score = int(sum(c["score"] for c in checks) / max(len(checks), 1))
    passed = overall_score >= 70 and len(critical_failures) == 0

    if overall_score < 85:
        recommendations.append("Strengthen evidence traceability in modeling_notes for higher grading confidence.")

    return {
        "overall_score": overall_score,
        "passed": passed,
        "checks": checks,
        "critical_failures": critical_failures,
        "recommendations": recommendations,
    }
