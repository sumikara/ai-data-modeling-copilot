from __future__ import annotations
import json,re
from pathlib import Path
from typing import Any,Dict
REQ_KEYS={"business_process_guess","entity_type_guess","grain_candidates","recommended_grain","dimension_candidates","fact_candidates","measure_candidates","candidate_natural_keys","data_quality_risks","cross_source_conflicts","modeling_notes","confidence_level","requires_human_decision"}

def _has_sql(text:str)->bool:
    return bool(re.search(r"\b(select|insert|update|delete|create\s+table|alter\s+table)\b",text,re.I))

def compare(actual:Dict[str,Any], golden:Dict[str,Any])->Dict[str,Any]:
    crit=[];warn=[];rec=[];scores={k:100 for k in ["grain","fact_dimension","keys","data_quality","confidence","governance"]}
    missing=REQ_KEYS-set(actual)
    if missing: crit.append(f"missing_required_keys:{sorted(missing)}"); scores["governance"]=0
    exp=golden.get("expected",{})
    if actual.get("requires_human_decision") is not True: crit.append("requires_human_decision_false"); scores["governance"]=0
    if actual.get("confidence_level") not in exp.get("confidence_allowed",["low","medium","high"]): crit.append("confidence_not_allowed"); scores["confidence"]=0
    rg=str(actual.get("recommended_grain",""))
    for bad in exp.get("recommended_grain_must_not_be",[]):
        if bad and bad.lower()==rg.lower(): crit.append("forbidden_grain_selected"); scores["grain"]=0
    for must in exp.get("recommended_grain_must_include",[]):
        if must and must.lower() not in rg.lower() and rg.lower()!="uncertain": warn.append(f"recommended_grain_missing:{must}"); scores["grain"]=max(scores["grain"],50)
    for area,key in [("fact_dimension","fact_candidates"),("fact_dimension","dimension_candidates"),("data_quality","data_quality_risks")]:
        vals=" ".join(map(str,actual.get(key,[]))).lower()
        must=exp.get(f"{key}_must_include",[])
        if must and not any(m.lower() in vals for m in must): warn.append(f"missing_expected_{key}"); scores[area]=min(scores[area],60)
    if exp.get("unresolved_questions_required",False):
        notes=" ".join(map(str,actual.get("modeling_notes",[]))).lower()
        if "unresolved" not in notes: crit.append("missing_unresolved_questions"); scores["governance"]=min(scores["governance"],40)
    atxt=json.dumps(actual).lower()
    if _has_sql(atxt): crit.append("sql_or_ddl_generated"); scores["governance"]=0
    if "final scd type" in atxt or "use scd type 2" in atxt: crit.append("finalized_scd_without_evidence")
    overall=int(sum(scores.values())/len(scores)); passed=(not crit) and overall>=70
    if not passed: rec.append("Lower confidence and keep human decision gate explicit.")
    return {"case_id":golden.get("case_id","unknown"),"overall_score":overall,"passed":passed,"decision_area_scores":scores,"critical_failures":crit,"warnings":warn,"recommendations":rec}

def compare_files(actual_path:str,golden_path:str)->Dict[str,Any]:
    return compare(json.loads(Path(actual_path).read_text()),json.loads(Path(golden_path).read_text()))
