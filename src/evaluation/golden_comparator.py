from __future__ import annotations
import json,re
from pathlib import Path
from typing import Any, Dict, List
WEIGHTS={"grain":30,"fact_dimension":20,"keys":15,"data_quality":10,"confidence":10,"governance":15}

def normalize_text(v:Any)->str:
    if v is None:return ""
    return (json.dumps(v) if isinstance(v,(dict,list)) else str(v)).lower()

def contains_all_terms(text:str,terms:List[str])->bool:
    t=normalize_text(text); return all(normalize_text(x) in t for x in terms)

def list_contains_term(items,term): return any(normalize_text(term) in normalize_text(i) for i in (items or []))
def detect_sql_or_ddl(text:str)->bool: return bool(re.search(r"\b(select|insert|update|delete|create\s+table|alter\s+table|drop\s+table)\b",normalize_text(text)))

def detect_final_scd_claim(text:str)->bool:
    t=normalize_text(text)
    soft=["do not finalize","requires human approval","candidate only","may be relevant"]
    hard=["use scd type 2","use type 2","final scd type 2","must use type 1","definitively type 2","final scd type 1"]
    return any(h in t for h in hard) and not any(s in t for s in soft)

def detect_forbidden_grain_only(rec, forbidden, required):
    r=normalize_text(rec)
    return any(normalize_text(f) in r for f in forbidden) and (required and not all(normalize_text(x) in r for x in required))

def detect_high_confidence_when_not_allowed(actual,golden):
    allowed=golden.get('expected',{}).get('confidence_allowed',[])
    conf=normalize_text(actual.get('confidence_level',''))
    return conf=='high' and 'high' not in [normalize_text(x) for x in allowed]

def detect_missing_unresolved_questions(actual):
    text=' '.join([normalize_text(actual.get('unresolved_questions',[])),normalize_text(actual.get('modeling_notes',[])),normalize_text(actual.get('reasoning_notes',[])),normalize_text(actual)])
    return not any(x in text for x in ['unresolved','question','clarify','confirm'])

def detect_bridge_requirement(actual):
    t=normalize_text(actual)
    return any(x in t for x in ['bridge','associative','many-to-many','many to many'])

def detect_degenerate_dimension_requirement(actual):
    t=normalize_text(actual)
    return ('degenerate' in t) or ('invoice_number' in t) or ('order_number' in t)

def detect_factless_fact_requirement(actual):
    t=normalize_text(actual)
    return any(x in t for x in ['factless','event occurrence','attendance'])

def detect_data_quality_keywords(actual, expected):
    t=' '.join([normalize_text(actual.get('data_quality_risks',[])),normalize_text(actual.get('modeling_notes',[])),normalize_text(actual.get('unresolved_questions',[]))])
    return [k for k in expected.get('data_quality_risk_keywords',[]) if normalize_text(k) not in t]

def compare(actual:Dict[str,Any],golden:Dict[str,Any])->Dict[str,Any]:
    scores=WEIGHTS.copy(); crit=[]; warn=[]; rec=[]; exp=golden.get('expected',{})
    rg=actual.get('recommended_grain',actual.get('grain_candidates',[]))
    if actual.get('requires_human_decision') is not True: crit.append('requires_human_decision_false'); scores['governance']=0
    if detect_high_confidence_when_not_allowed(actual,golden): crit.append('confidence_high_despite_ambiguity'); scores['confidence']=0
    if actual.get('confidence_level') not in exp.get('confidence_allowed',['low','medium','high']): crit.append('confidence_not_allowed'); scores['confidence']=0
    if exp.get('recommended_grain_must_include') and not contains_all_terms(rg, exp.get('recommended_grain_must_include')) and normalize_text(rg)!='uncertain': warn.append('grain_missing_required_columns'); scores['grain']-=10
    if detect_forbidden_grain_only(rg, exp.get('recommended_grain_must_not_be',[]), exp.get('recommended_grain_must_include',[])):
        forbidden = exp.get('recommended_grain_must_not_be',['forbidden'])[0]
        crit.append(f"recommended_grain_is_{forbidden}_only"); scores['grain']=0
    for d in exp.get('dimension_candidates_must_include',[]):
        if not list_contains_term(actual.get('dimension_candidates',[]),d): warn.append(f'missing_dimension:{d}'); scores['fact_dimension']-=4
    if exp.get('fact_candidates_must_include') and not all(list_contains_term(actual.get('fact_candidates',[]),x) for x in exp['fact_candidates_must_include']): warn.append('missing_expected_fact_candidate'); scores['fact_dimension']-=6
    if exp.get('measure_candidates_must_include'):
        for m in exp['measure_candidates_must_include']:
            if not list_contains_term(actual.get('measure_candidates',[]),m): warn.append(f'missing_measure:{m}'); scores['keys']-=2
    if exp.get('factless_fact_allowed') and not detect_factless_fact_requirement(actual): warn.append('missing_factless_fact_signal')
    if exp.get('unresolved_questions_required') and detect_missing_unresolved_questions(actual): crit.append('missing_unresolved_questions'); scores['governance']-=5
    if exp.get('scd_notes_required') and ('scd' not in normalize_text(actual)): crit.append('missing_scd_notes')
    if exp.get('bridge_candidate_required') and not detect_bridge_requirement(actual): crit.append('ignored_many_to_many_bridge'); scores['fact_dimension']-=8
    if exp.get('degenerate_dimension_required') and not detect_degenerate_dimension_requirement(actual): crit.append('missing_degenerate_dimension'); scores['fact_dimension']-=8
    missing_risks=detect_data_quality_keywords(actual, exp)
    for k in missing_risks: warn.append(f'missing_risk_keyword:{k}'); scores['data_quality']-=2
    text=normalize_text(actual)
    if detect_sql_or_ddl(text): crit.append('sql_generated'); scores['governance']=0
    if detect_final_scd_claim(text): crit.append('finalized_scd_type_without_evidence')
    scores={k:max(0,v) for k,v in scores.items()}; overall=sum(scores.values()); passed=(overall>=70 and 'requires_human_decision_false' not in crit and 'sql_generated' not in crit)
    if not passed: rec.append('Use stronger uncertainty wording and explicit human decision questions.')
    return {"case_id":golden.get('case_id','unknown'),"overall_score":overall,"passed":passed,"decision_area_scores":scores,"critical_failures":sorted(set(crit)),"warnings":sorted(set(warn)),"recommendations":rec}

def compare_files(actual_path:str,golden_path:str)->Dict[str,Any]:
    return compare(json.loads(Path(actual_path).read_text()),json.loads(Path(golden_path).read_text()))
