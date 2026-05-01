from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

WEIGHTS = {
    "grain": 30,
    "fact_dimension": 20,
    "keys": 15,
    "data_quality": 10,
    "confidence": 10,
    "governance": 15,
}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value).lower()
    return str(value).lower().strip()


def contains_all_terms(text: str, terms: List[str]) -> bool:
    t = normalize_text(text)
    return all(normalize_text(x) in t for x in terms)


def list_contains_term(items: List[Any], term: str) -> bool:
    tt = normalize_text(term)
    return any(tt in normalize_text(i) for i in (items or []))


def detect_forbidden_grain_only(
    recommended_grain: Any, forbidden_terms: List[str], required_terms: List[str]
) -> bool:
    rg = normalize_text(recommended_grain)
    forbidden_hit = any(normalize_text(t) in rg for t in (forbidden_terms or []))
    has_required_terms = contains_all_terms(rg, required_terms or [])
    return forbidden_hit and not has_required_terms


def detect_high_confidence_when_not_allowed(actual: Dict[str, Any], golden: Dict[str, Any]) -> bool:
    confidence = normalize_text(actual.get("confidence_level"))
    allowed = [normalize_text(x) for x in golden.get("expected", {}).get("confidence_allowed", ["low", "medium", "high"])]
    return confidence == "high" and confidence not in allowed


def detect_final_scd_claim(text: str) -> bool:
    t = normalize_text(text)
    caveats = ["do not finalize", "requires human approval", "candidate only", "may be relevant"]
    if any(c in t for c in caveats):
        return False
    return bool(
        re.search(
            r"\b(use\s+scd\s+type\s*[12]|must\s+use\s+type\s*[12]|final\s+scd\s+type\s*[12])\b",
            t,
        )
    )


def detect_sql_or_ddl(text: str) -> bool:
    return bool(
        re.search(
            r"\b(select|insert|update|delete|create\s+table|alter\s+table|drop\s+table)\b",
            normalize_text(text),
        )
    )


def detect_missing_unresolved_questions(actual: Dict[str, Any]) -> bool:
    question_text = " ".join(
        [
            normalize_text(actual.get("unresolved_questions", [])),
            normalize_text(actual.get("modeling_notes", [])),
            normalize_text(actual.get("reasoning_notes", [])),
            normalize_text(actual),
        ]
    )
    return not any(x in question_text for x in ["?", "unknown", "unclear", "need", "pending", "tbd"])


def detect_bridge_requirement(actual: Dict[str, Any]) -> bool:
    return "bridge" not in normalize_text(actual)


def detect_degenerate_dimension_requirement(actual: Dict[str, Any]) -> bool:
    return "degenerate" not in normalize_text(actual)


def detect_factless_fact_requirement(actual: Dict[str, Any]) -> bool:
    text = normalize_text(actual)
    return "factless" not in text and "no measure" not in text


def detect_data_quality_keywords(actual: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    risk_text = normalize_text(actual.get("data_quality_risks", [])) + " " + normalize_text(actual.get("modeling_notes", []))
    missing = []
    for k in expected.get("data_quality_risk_keywords", []):
        if normalize_text(k) not in risk_text:
            missing.append(k)
    return missing


def detect_uncertainty(text: str) -> bool:
    t = normalize_text(text)
    return any(x in t for x in ["uncertain", "caveat", "requires review", "human decision", "not final"])


def compare(actual: Dict[str, Any], golden: Dict[str, Any]) -> Dict[str, Any]:
    scores = WEIGHTS.copy()
    crit = []
    warns = []
    rec = []
    exp = golden.get("expected", {})
    txt = normalize_text(actual)
    rg = normalize_text(actual.get("recommended_grain", actual.get("grain_candidates", [])))

    if actual.get("requires_human_decision") is not True:
        crit.append("requires_human_decision_false")
        scores["governance"] = 0

    if actual.get("confidence_level") not in exp.get("confidence_allowed", ["low", "medium", "high"]):
        crit.append("confidence_not_allowed")
        scores["confidence"] = 0
    if detect_high_confidence_when_not_allowed(actual, golden):
        crit.append("high_confidence_not_allowed")
        scores["confidence"] = 0

    must = exp.get("recommended_grain_must_include", [])
    if must and rg != "uncertain" and not contains_all_terms(rg, must):
        warns.append("grain_missing_required_columns")
        scores["grain"] -= 15

    forbidden_list = exp.get("recommended_grain_must_not_be", ["forbidden"])
    forbidden_term = forbidden_list[0] if forbidden_list else "forbidden"
    if detect_forbidden_grain_only(rg, forbidden_list, must):
        crit.append(f"recommended_grain_is_{forbidden_term}_only")
        scores["grain"] = 0

    dims = actual.get("dimension_candidates", [])
    for d in exp.get("dimension_candidates_must_include", []):
        if not list_contains_term(dims, d):
            warns.append(f"missing_dimension:{d}")
            scores["fact_dimension"] -= 5

    facts = actual.get("fact_candidates", [])
    allowed = exp.get("entity_type_allowed", [])
    if exp.get("fact_candidates_must_include") and not all(
        list_contains_term(facts, f) for f in exp["fact_candidates_must_include"]
    ):
        if not any(a in normalize_text(actual.get("entity_type_guess", "")) for a in map(normalize_text, allowed)):
            warns.append("fact_dimension_mismatch")
            scores["fact_dimension"] -= 10

    measure_must = exp.get("measure_candidates_must_include", [])
    is_factless_case = exp.get("factless_fact_required") or "factless" in txt
    if not (is_factless_case and not measure_must):
        for m in measure_must:
            if not list_contains_term(actual.get("measure_candidates", []), m):
                warns.append(f"missing_measure:{m}")
                scores["keys"] -= 2

    for missing_kw in detect_data_quality_keywords(actual, exp):
        warns.append(f"missing_risk_keyword:{missing_kw}")
        scores["data_quality"] -= 2

    if exp.get("unresolved_questions_required") and detect_missing_unresolved_questions(actual):
        crit.append("missing_unresolved_questions")
        scores["governance"] -= 5
    if exp.get("scd_notes_required") and "scd" not in txt:
        crit.append("missing_scd_notes")
        scores["keys"] -= 5
    if exp.get("bridge_candidate_required") and detect_bridge_requirement(actual):
        crit.append("ignored_many_to_many_bridge")
        scores["fact_dimension"] -= 10
    if exp.get("degenerate_dimension_required") and detect_degenerate_dimension_requirement(actual):
        crit.append("missed_degenerate_dimension")
        scores["fact_dimension"] -= 10
    if exp.get("factless_fact_required") and detect_factless_fact_requirement(actual):
        crit.append("missed_factless_fact_candidate")
        scores["fact_dimension"] -= 10

    if detect_sql_or_ddl(txt):
        crit.append("sql_generated")
        scores["governance"] = 0
    if detect_final_scd_claim(txt):
        crit.append("finalized_scd_type_without_evidence")

    for cf in golden.get("critical_failures", []):
        if normalize_text(cf) in txt:
            crit.append(cf)

    scores = {k: max(0, v) for k, v in scores.items()}
    overall = sum(scores.values())
    passed = overall >= 70 and not any(c in crit for c in ["requires_human_decision_false", "sql_generated"])
    if not detect_uncertainty(txt):
        rec.append("Increase uncertainty signaling and unresolved questions for ambiguous cases.")

    return {
        "case_id": golden.get("case_id", "unknown"),
        "overall_score": overall,
        "passed": passed,
        "decision_area_scores": scores,
        "critical_failures": sorted(set(crit)),
        "warnings": sorted(set(warns)),
        "recommendations": rec,
    }


def compare_files(actual_path: str, golden_path: str) -> Dict[str, Any]:
    return compare(json.loads(Path(actual_path).read_text()), json.loads(Path(golden_path).read_text()))
