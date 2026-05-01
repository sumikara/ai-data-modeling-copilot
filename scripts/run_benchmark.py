import argparse, json, os
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from src.evaluation.golden_comparator import compare_files
from src.evaluation.failure_classifier import classify
from src.evaluation.semantic_output_grader import grade_semantic_output


def mock_semantic_output(case):
    cid=case['case_id']
    return {"case_id":cid,"entity_type_guess":"uncertain semantic entity","recommended_grain":"uncertain","grain_candidates":[],"dimension_candidates":["date"],"fact_candidates":[],"measure_candidates":case.get('table_profile',{}).get('measure_candidates',[]),"candidate_natural_keys":[],"data_quality_risks":["null","uniqueness"],"modeling_notes":["human decision required"],"confidence_level":"low","requires_human_decision":True,"unresolved_questions":["Confirm business grain policy"]}

def run_mode(mode):
    case_ids=['case_01_transaction_line_clear','case_02_order_header_line_mixed','case_03_inventory_snapshot_hybrid','case_04_customer_scd_conflict','case_05_noisy_event_log_uncertain','case_06_accumulating_snapshot_lifecycle','case_07_factless_fact_attendance','case_08_bridge_many_to_many','case_09_degenerate_dimension_invoice','case_10_product_attribute_drift_scd']
    cases=[Path(f'test_inputs/semantic_profiling/cases/{c}.json') for c in case_ids]
    results=[]
    for cp in cases:
        case=json.loads(cp.read_text()); cid=case['case_id']
        if mode in ['llm','gemini'] and not os.getenv('OPENAI_API_KEY' if mode=='llm' else 'GEMINI_API_KEY'):
            results.append({"case":cid,"mode":mode,"status":"SKIPPED","comparison":{"overall_score":"SKIPPED","passed":False,"decision_area_scores":{"grain":0,"fact_dimension":0,"confidence":0},"critical_failures":["missing_api_key"]},"failure":{"failure_categories":["schema_contract_failure"]}}); continue
        actual=mock_semantic_output(case)
        out_dir=Path(f'test_outputs/semantic_profiling/case_runs/{cid}'); out_dir.mkdir(parents=True,exist_ok=True)
        ap=out_dir/f'{mode}_actual.json'; ap.write_text(json.dumps(actual,indent=2))
        gp=Path(f'test_inputs/semantic_profiling/golden/{cid}_expected.json')
        comp=compare_files(str(ap),str(gp))
        fail=classify(comp,actual)
        grade=grade_semantic_output(actual)
        rep=Path(f'test_outputs/evaluation/case_reports/{cid}_{mode}_report.md'); rep.parent.mkdir(parents=True,exist_ok=True)
        rep.write_text(f"# {cid} ({mode})\n\n## Comparator\n```json\n{json.dumps(comp,indent=2)}\n```\n\n## Failure taxonomy\n```json\n{json.dumps(fail,indent=2)}\n```\n\n## Grader\n```json\n{json.dumps(grade,indent=2)}\n```\n")
        results.append({"case":cid,"mode":mode,"status":"OK","comparison":comp,"failure":fail})
    lines=[f"# Benchmark Summary ({mode})","","| Case | Mode | Overall score | Passed | Grain score | Fact/dim score | Confidence score | Critical failures | Failure categories |","|---|---|---:|---|---:|---:|---:|---|---|"]
    for r in results:
        c=r['comparison']; d=c.get('decision_area_scores',{})
        lines.append(f"| {r['case']} | {r['mode']} | {c.get('overall_score')} | {c.get('passed')} | {d.get('grain',0)} | {d.get('fact_dimension',0)} | {d.get('confidence',0)} | {', '.join(c.get('critical_failures',[]))} | {', '.join(r['failure'].get('failure_categories',[]))} |")
    Path(f'test_outputs/evaluation/benchmark_summary_{mode}.md').write_text('\n'.join(lines))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['mock','llm','gemini','all'],default='mock'); a=ap.parse_args()
    if a.mode=='all':
        for m in ['mock','llm','gemini']: run_mode(m)
    else:
        run_mode(a.mode)
