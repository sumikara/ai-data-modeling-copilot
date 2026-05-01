import json
from pathlib import Path
BAD=["Synthetic scenario for","business process","reference_entity"]
CASE_IDS=['case_01_transaction_line_clear','case_02_order_header_line_mixed','case_03_inventory_snapshot_hybrid','case_04_customer_scd_conflict','case_05_noisy_event_log_uncertain','case_06_accumulating_snapshot_lifecycle','case_07_factless_fact_attendance','case_08_bridge_many_to_many','case_09_degenerate_dimension_invoice','case_10_product_attribute_drift_scd']

def fail(msg):
    print(f"FAIL: {msg}"); raise SystemExit(1)
for cid in CASE_IDS:
    cp=Path(f'test_inputs/semantic_profiling/cases/{cid}.json'); gp=Path(f'test_inputs/semantic_profiling/golden/{cid}_expected.json'); mp=Path(f'docs/evaluation/expected_outputs/{cid}_expected.md')
    if not cp.exists() or not gp.exists() or not mp.exists(): fail(f"missing artifacts for {cid}")
    c=json.loads(cp.read_text()); g=json.loads(gp.read_text())
    for k in ['case_id','domain','case_type','business_scenario','trap_or_ambiguity_note','table_profile','relationship_candidates','domain_pattern_findings','sample_rows']:
        if k not in c: fail(f"{cid} missing {k}")
    txt=json.dumps(c)
    for b in BAD:
        if b in txt: fail(f"{cid} contains placeholder '{b}'")
    if '"notes": "candidate"' in txt: fail(f"{cid} has weak candidate-only note")
    if g.get('case_id')!=cid: fail(f"golden case id mismatch for {cid}")
    if 'expected' not in g or 'critical_failures' not in g: fail(f"golden schema missing for {cid}")
    exp=g['expected']
    if exp.get('requires_human_decision') is not True: fail(f"golden requires_human_decision must be true for {cid}")
    if 'confidence_allowed' not in exp: fail(f"golden confidence_allowed missing for {cid}")
print('PASS: benchmark assets validated')
