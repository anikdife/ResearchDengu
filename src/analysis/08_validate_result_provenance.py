from common import *
import sys
path=ROOT/"outputs/b1/result-provenance.csv"; rows=list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
required=["result_id","description","analysis_script","derived_input","input_hash","source_rows","source_snapshots","calculation","output_artifact"]
ok=bool(rows) and all(all(r.get(k) for k in required) for r in rows) and len({r["result_id"] for r in rows})==len(rows)
if not ok: raise SystemExit("RESULT_PROVENANCE_FAIL")
print(f"RESULT_PROVENANCE_PASS {len(rows)}")
