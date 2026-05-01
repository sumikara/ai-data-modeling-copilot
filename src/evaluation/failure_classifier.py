from __future__ import annotations
from typing import Dict,Any,List

CATS=["wrong_grain","overconfident_reasoning","ignored_null_or_duplicate_evidence","wrong_fact_dimension_classification","invented_business_rule","finalized_scd_without_evidence","missing_unresolved_questions","missing_data_quality_risks","weak_knowledge_grounding","sql_or_ddl_generated","schema_contract_failure"]

def classify(comparison:Dict[str,Any], actual:Dict[str,Any])->List[str]:
    out=[]; cf=" ".join(comparison.get("critical_failures",[])).lower(); warns=" ".join(comparison.get("warnings",[])).lower(); text=str(actual).lower()
    if "forbidden_grain" in cf or "recommended_grain_missing" in warns: out.append("wrong_grain")
    if "confidence_not_allowed" in cf: out.append("overconfident_reasoning")
    if "missing_expected_data_quality_risks" in warns: out.append("missing_data_quality_risks")
    if "missing_unresolved_questions" in cf: out.append("missing_unresolved_questions")
    if "finalized_scd_without_evidence" in cf: out.append("finalized_scd_without_evidence")
    if "sql_or_ddl_generated" in cf: out.append("sql_or_ddl_generated")
    if "missing_required_keys" in cf: out.append("schema_contract_failure")
    if "null" not in text and "duplicate" not in text: out.append("ignored_null_or_duplicate_evidence")
    return sorted(set(out))
