import argparse, json, os, sys
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path: sys.path.insert(0,str(REPO_ROOT))
from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.evaluation.golden_comparator import compare_files
from src.evaluation.failure_classifier import classify
from src.evaluation.semantic_output_grader import grade_semantic_output

CASE_IDS=['case_01_transaction_line_clear','case_02_order_header_line_mixed','case_03_inventory_snapshot_hybrid','case_04_customer_scd_conflict','case_05_noisy_event_log_uncertain','case_06_accumulating_snapshot_lifecycle','case_07_factless_fact_attendance','case_08_bridge_many_to_many','case_09_degenerate_dimension_invoice','case_10_product_attribute_drift_scd']

def mock_case_output(cid):
    base={"requires_human_decision":True,"confidence_level":"medium","cross_source_conflicts":[],"unresolved_questions":[]}
    m={
'case_01_transaction_line_clear':{"business_process_guess":"retail sales transaction","entity_type_guess":"transaction line fact","grain_candidates":["transaction_id","transaction_id+product_id+customer_id+transaction_dt"],"recommended_grain":"transaction_id + product_id + customer_id + transaction_dt","dimension_candidates":["customer","product","store","date"],"fact_candidates":["sales_transaction_line"],"measure_candidates":["quantity","unit_price","total_sales"],"candidate_natural_keys":["transaction_id + product_id + customer_id + transaction_dt"],"data_quality_risks":["transaction_id alone is non-unique","low null ratios still affect key stability"],"modeling_notes":["line-level additive measures"],"confidence_level":"medium"},
'case_02_order_header_line_mixed':{"business_process_guess":"e-commerce ordering","entity_type_guess":"hybrid header-line mixed table","grain_candidates":["order_id","order_id+line_number"],"recommended_grain":"uncertain","dimension_candidates":["customer","product","date"],"fact_candidates":["order_line_candidate"],"measure_candidates":["line_total","total_order_amount"],"candidate_natural_keys":["order_id + line_number"],"data_quality_risks":["line_number nulls","order-level totals repeated across lines"],"modeling_notes":["possible split into order_header and order_line"],"unresolved_questions":["Is line_number mandatory?","Should header and line be split?"],"confidence_level":"low"},
'case_03_inventory_snapshot_hybrid':{"business_process_guess":"inventory monitoring","entity_type_guess":"periodic snapshot fact with embedded descriptors","grain_candidates":["product_id","product_id+warehouse_id+snapshot_date"],"recommended_grain":"product_id + warehouse_id + snapshot_date","dimension_candidates":["product","warehouse","date"],"fact_candidates":["inventory_snapshot_fact"],"measure_candidates":["stock_on_hand","reorder_level","inventory_value"],"candidate_natural_keys":["product_id + warehouse_id + snapshot_date"],"data_quality_risks":["descriptor drift over time"],"modeling_notes":["snapshot_date is required for grain"]},
'case_04_customer_scd_conflict':{"business_process_guess":"customer master conformance","entity_type_guess":"dimension-like customer entity","grain_candidates":["customer_id","customer_id+source_system"],"recommended_grain":"customer identity candidate requires conformance review","dimension_candidates":["customer","source_system"],"fact_candidates":[],"measure_candidates":[],"candidate_natural_keys":["customer_id + source_system"],"data_quality_risks":["segment/tier cross-source conflicts","email duplicates and nulls"],"cross_source_conflicts":["customer_segment conflict","loyalty_tier conflict","city/state conflict"],"modeling_notes":["SCD candidate attributes identified; do not finalize Type 1/2 without policy"],"unresolved_questions":["survivorship policy?","history retention window?"],"confidence_level":"low"},
'case_05_noisy_event_log_uncertain':{"business_process_guess":"product telemetry events","entity_type_guess":"event-like log with weak identity","grain_candidates":["event_id","session_id+event_timestamp+event_type"],"recommended_grain":"uncertain","dimension_candidates":["user","session","date"],"fact_candidates":["event_log_candidate"],"measure_candidates":[],"candidate_natural_keys":[],"data_quality_risks":["event_id low uniqueness","user_id high null ratio","json parse failures"],"modeling_notes":["dedup policy required before final grain"],"unresolved_questions":["How is event_id generated?","What is dedup rule?"],"confidence_level":"low"},
'case_06_accumulating_snapshot_lifecycle':{"business_process_guess":"order fulfillment lifecycle","entity_type_guess":"accumulating snapshot fact","grain_candidates":["order_id","order_id+status"],"recommended_grain":"one row per order lifecycle process instance (order_id)","dimension_candidates":["customer","warehouse","carrier","date"],"fact_candidates":["order_lifecycle_accumulating_snapshot"],"measure_candidates":["days_to_ship","days_to_deliver"],"candidate_natural_keys":["order_id"],"data_quality_risks":["milestone date ordering anomalies","future milestone nulls are expected"],"modeling_notes":["do not split milestone dates into separate transaction facts"]},
'case_07_factless_fact_attendance':{"business_process_guess":"attendance tracking","entity_type_guess":"factless fact event occurrence","grain_candidates":["attendance_id","student_id+course_id+attendance_dt"],"recommended_grain":"one row per attendance occurrence","dimension_candidates":["student","course","date","location","status"],"fact_candidates":["attendance_factless_fact"],"measure_candidates":[],"candidate_natural_keys":["attendance_id"],"data_quality_risks":["status semantics may vary by source"],"modeling_notes":["factless/event occurrence despite no additive measures"]},
'case_08_bridge_many_to_many':{"business_process_guess":"diagnosis assignment","entity_type_guess":"bridge/associative entity","grain_candidates":["patient_id+diagnosis_code+encounter_dt"],"recommended_grain":"one row per many-to-many relationship occurrence","dimension_candidates":["patient","diagnosis","date"],"fact_candidates":["bridge_patient_diagnosis"],"measure_candidates":[],"candidate_natural_keys":["patient_id + diagnosis_code + encounter_dt"],"data_quality_risks":["duplicate relationship rows"],"modeling_notes":["bridge candidate required for many-to-many"]},
'case_09_degenerate_dimension_invoice':{"business_process_guess":"invoice line sales","entity_type_guess":"transaction line fact with degenerate dimension","grain_candidates":["invoice_number","invoice_number+line_number"],"recommended_grain":"invoice_number + line_number","dimension_candidates":["customer","product","date"],"fact_candidates":["invoice_line_fact"],"measure_candidates":["quantity","unit_price","line_amount"],"candidate_natural_keys":["invoice_number + line_number"],"data_quality_risks":["invoice-level descriptions absent for separate dimension"],"modeling_notes":["retain invoice_number as degenerate dimension in fact"]},
'case_10_product_attribute_drift_scd':{"business_process_guess":"product catalog conformance","entity_type_guess":"product dimension-like with SCD candidates","grain_candidates":["product_id","product_id+source_system"],"recommended_grain":"product_id candidate with source caveat","dimension_candidates":["product","source_system","date"],"fact_candidates":[],"measure_candidates":[],"candidate_natural_keys":["product_id + source_system"],"data_quality_risks":["attribute drift across source/time"],"cross_source_conflicts":["product_category conflict","product_brand conflict","product_material conflict"],"modeling_notes":["SCD attributes are candidates; do not finalize Type 1 or Type 2 without policy"],"unresolved_questions":["effective dating policy?"],"confidence_level":"low"}
}
    o=base.copy(); o.update(m[cid]); return o

def write_error_actual(path, err, raw_path=""):
    payload={"error":str(err),"raw_output_path":raw_path,"failure_category":"schema_contract_failure","requires_human_decision":True,"confidence_level":"low","unresolved_questions":["Model output could not be parsed into required contract."]}
    path.write_text(json.dumps(payload,indent=2)); return payload

def run_case(cid, mode):
    case_path=Path(f'test_inputs/semantic_profiling/cases/{cid}.json')
    case=json.loads(case_path.read_text())
    out_dir=Path(f'test_outputs/semantic_profiling/case_runs/{cid}'); out_dir.mkdir(parents=True,exist_ok=True)
    profile={"table_profile":case["table_profile"],"relationship_candidates":case["relationship_candidates"],"domain_pattern_findings":case["domain_pattern_findings"],"sample_rows":case.get("sample_rows",[])}
    profile_path=out_dir/'combined_profile.json'; profile_path.write_text(json.dumps(profile,indent=2))
    actual_path=out_dir/f'{mode}_actual.json'
    if mode=='mock': actual=mock_case_output(cid)
    else:
        try: actual=run_semantic_profiling(str(profile_path), mode=mode)
        except Exception as e: actual=write_error_actual(actual_path,e)
    if mode in ['llm','gemini'] and isinstance(actual,dict) and actual.get('error'):
        raw_hint=actual.get('raw_output_path','')
        actual=write_error_actual(actual_path,actual['error'],raw_hint)
    else:
        actual_path.write_text(json.dumps(actual,indent=2))
    gp=Path(f'test_inputs/semantic_profiling/golden/{cid}_expected.json')
    comp=compare_files(str(actual_path),str(gp))
    fail=classify(comp,actual)
    grade=grade_semantic_output(actual)
    rep=Path(f'test_outputs/evaluation/case_reports/{cid}_{mode}_report.md'); rep.parent.mkdir(parents=True,exist_ok=True)
    rep.write_text(f"# {cid} ({mode})\n\nSource mode: **{mode}**\n\n## Comparator\n```json\n{json.dumps(comp,indent=2)}\n```\n\n## Failure taxonomy\n```json\n{json.dumps(fail,indent=2)}\n```\n\n## Grader\n```json\n{json.dumps(grade,indent=2)}\n```\n")
    return {"case":cid,"mode":mode,"comparison":comp,"failure":fail}

def mode_available(mode):
    return (mode=='mock') or (mode=='llm' and bool(os.getenv('OPENAI_API_KEY'))) or (mode=='gemini' and bool(os.getenv('GEMINI_API_KEY')))

def run_mode(mode):
    results=[]
    if not mode_available(mode):
        for cid in CASE_IDS:
            results.append({"case":cid,"mode":mode,"comparison":{"overall_score":"SKIPPED","passed":False,"decision_area_scores":{"grain":0,"fact_dimension":0,"confidence":0},"critical_failures":["missing_api_key"]},"failure":{"failure_categories":["schema_contract_failure"]}})
    else:
        for cid in CASE_IDS: results.append(run_case(cid,mode))
    lines=[f"# Benchmark Summary ({mode})","","| Case | Mode | Overall score | Passed | Grain score | Fact/dim score | Confidence score | Critical failures | Failure categories |","|---|---|---:|---|---:|---:|---:|---|---|"]
    for r in results:
        c=r['comparison']; d=c.get('decision_area_scores',{})
        lines.append(f"| {r['case']} | {mode} | {c.get('overall_score')} | {c.get('passed')} | {d.get('grain',0)} | {d.get('fact_dimension',0)} | {d.get('confidence',0)} | {', '.join(c.get('critical_failures',[]))} | {', '.join(r['failure'].get('failure_categories',[]))} |")
    Path(f'test_outputs/evaluation/benchmark_summary_{mode}.md').write_text('\n'.join(lines))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['mock','llm','gemini','all'],default='mock'); a=ap.parse_args()
    for m in (['mock','llm','gemini'] if a.mode=='all' else [a.mode]): run_mode(m)
