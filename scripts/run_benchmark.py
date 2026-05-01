import argparse, json, os, sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.evaluation.semantic_output_grader import grade_semantic_output
from src.evaluation.golden_comparator import compare_files
from src.evaluation.failure_classifier import classify

MODES=["mock","llm","gemini","anthropic"]

def run_case(case_path:Path, mode:str):
    case=json.loads(case_path.read_text()); case_id=case.get("case_id",case_path.stem)
    combined={
        "table_profile":{"table_name":case.get("table_name"),"row_count":case.get("row_count"),"columns":case.get("columns",{})},
        "relationship_candidates":case.get("relationship_candidates",[]),
        "domain_pattern_findings":case.get("domain_pattern_findings",{}),
        "sample_rows":case.get("sample_rows",[])
    }
    out_dir=Path(f"test_outputs/semantic_profiling/case_runs/{case_id}"); out_dir.mkdir(parents=True,exist_ok=True)
    combined_path=out_dir/"combined_profile.json"; combined_path.write_text(json.dumps(combined,indent=2))
    actual=run_semantic_profiling(str(combined_path), mode=mode)
    actual_path=out_dir/f"{mode}_actual.json"; actual_path.write_text(json.dumps(actual,indent=2))
    grade=grade_semantic_output(actual)
    golden_path=Path(f"test_inputs/semantic_profiling/golden/{case_id}_golden.json")
    comp=compare_files(str(actual_path),str(golden_path)) if golden_path.exists() else {"case_id":case_id,"passed":False,"critical_failures":["missing_golden"]}
    fails=classify(comp, actual)
    rep=Path(f"test_outputs/evaluation/case_reports/{case_id}_{mode}_report.md"); rep.parent.mkdir(parents=True,exist_ok=True)
    rep.write_text(f"# {case_id} ({mode})\n\n## Grade\n```json\n{json.dumps(grade,indent=2)}\n```\n\n## Golden\n```json\n{json.dumps(comp,indent=2)}\n```\n\n## Failure categories\n- "+"\n- ".join(fails))
    return {"case_id":case_id,"mode":mode,"grade":grade,"comparison":comp,"failures":fails}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',default='mock',choices=['mock','llm','gemini','anthropic','all']); a=ap.parse_args()
    modes=MODES if a.mode=='all' else [a.mode]
    cases=sorted(Path('test_inputs/semantic_profiling/cases').glob('*.json'))
    summary=[]
    for m in modes:
        if m!='mock' and ((m=='llm' and not os.getenv('OPENAI_API_KEY')) or (m=='gemini' and not os.getenv('GEMINI_API_KEY')) or (m=='anthropic' and not os.getenv('ANTHROPIC_API_KEY'))):
            print(f"Skipping {m}: missing API key")
            continue
        for c in cases: summary.append(run_case(c,m))
        out=Path(f"test_outputs/evaluation/benchmark_summary_{m}.md"); out.parent.mkdir(parents=True,exist_ok=True)
        lines=[f"# Benchmark Summary ({m})","","| Case | Passed | Score | Failures |","|---|---|---:|---|"]
        for s in [x for x in summary if x['mode']==m]:
            lines.append(f"| {s['case_id']} | {s['comparison'].get('passed')} | {s['comparison'].get('overall_score','n/a')} | {', '.join(s['failures'])} |")
        out.write_text('\n'.join(lines))

if __name__=='__main__': main()
