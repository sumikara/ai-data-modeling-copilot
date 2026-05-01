from __future__ import annotations
from typing import Dict, Any

CATEGORIES=["wrong_grain","overconfident_reasoning","ignored_null_or_duplicate_evidence","wrong_fact_dimension_classification","wrong_snapshot_classification","missed_bridge_table","missed_factless_fact","missed_degenerate_dimension","invented_business_rule","finalized_scd_without_evidence","missing_unresolved_questions","missing_data_quality_risks","weak_knowledge_grounding","sql_or_ddl_generated","schema_contract_failure","human_decision_gate_missing"]

def classify(comparison:Dict[str,Any], actual:Dict[str,Any])->Dict[str,Any]:
    cf=' '.join(comparison.get('critical_failures',[])).lower(); w=' '.join(comparison.get('warnings',[])).lower(); t=str(actual).lower(); out=[]; causes=[]; fix=[]
    if 'grain' in cf or 'recommended_grain' in cf or 'grain_missing' in w: out.append('wrong_grain'); causes.append('Grain evidence underweighted.'); fix+=['prompt','golden_expected']
    if 'confidence_not_allowed' in cf: out.append('overconfident_reasoning'); causes.append('Confidence calibration failure.'); fix+=['prompt','grader']
    if 'null' not in t and 'duplicate' not in t: out.append('ignored_null_or_duplicate_evidence'); fix.append('knowledge_base')
    if 'fact_dimension_mismatch' in w: out.append('wrong_fact_dimension_classification'); fix.append('prompt')
    if 'snapshot' in comparison.get('case_id','') and 'snapshot' not in t: out.append('wrong_snapshot_classification')
    if 'ignored_many_to_many_bridge' in cf: out.append('missed_bridge_table')
    if 'factless' in comparison.get('case_id','') and 'dimension only' in t: out.append('missed_factless_fact')
    if 'missed_degenerate_dimension' in cf: out.append('missed_degenerate_dimension')
    if 'finalized_scd_type_without_evidence' in cf: out.append('finalized_scd_without_evidence')
    if 'missing_unresolved_questions' in cf: out.append('missing_unresolved_questions')
    if 'missing_risk_keyword' in w: out.append('missing_data_quality_risks')
    if 'sql_generated' in cf: out.append('sql_or_ddl_generated')
    if 'missing_required_keys' in cf: out.append('schema_contract_failure')
    if 'requires_human_decision_false' in cf: out.append('human_decision_gate_missing')
    if not out: out.append('weak_knowledge_grounding')
    return {"case_id":comparison.get('case_id','unknown'),"failure_categories":sorted(set(out)),"root_cause_hypotheses":sorted(set(causes)) or ["Needs deeper evidence grounding."],"recommended_fix_area":sorted(set(fix)) or ["retrieval"]}
