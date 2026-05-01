import json
from pathlib import Path
paths=[Path('test_inputs'),Path('test_outputs'),Path('config')]
bad=[]
for p in paths:
    if not p.exists(): continue
    for f in p.rglob('*.json'):
        try: json.loads(f.read_text())
        except Exception as e: bad.append((str(f),str(e)))
if bad:
    for b in bad: print('INVALID',b[0],b[1])
    raise SystemExit(1)
print('JSON validation passed')
