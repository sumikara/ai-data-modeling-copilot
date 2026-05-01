from pathlib import Path
req=[
'docs/architecture/technical-flow.md','docs/profiling/profile-artifact-schema.md','docs/evaluation/benchmark-methodology.md','docs/evidence/evidence-package.md',
'test_inputs/semantic_profiling/cases','test_inputs/semantic_profiling/golden','docs/evaluation/expected_outputs'
]
missing=[r for r in req if not Path(r).exists()]
if missing:
    print('Missing artifacts:');[print('-',m) for m in missing];raise SystemExit(1)
print('Required artifacts present')
