from common import *
rows=read_csv("data/derived/descriptive_temporal.csv")
fields=["snapshot_id","year","displayed_date","weekly_case_raw","weekly_death_raw","cumulative_case_raw","cumulative_death_raw","semantic_status","incomplete_period_note"]
out=[]
for r in rows:
    out.append({"snapshot_id":r["snapshot_id"],"year":r["snapshot_id"][:4],"displayed_date":r["displayed_date"],"weekly_case_raw":r["weekly_case_raw"],"weekly_death_raw":r["weekly_death_raw"],"cumulative_case_raw":r["cumulative_case_raw"],"cumulative_death_raw":r["cumulative_death_raw"],"semantic_status":"SUPPORTED_MEANING","incomplete_period_note":"2026 incomplete follow-up; not equivalent to completed annual totals" if r["snapshot_id"].startswith("2026") else ""})
write_csv("outputs/b1/restricted_temporal_description.csv",out,fields)
provenance([{"result_id":"B1-TEMP-001","description":"Source-reported headline observations by snapshot","analysis_script":"src/analysis/02_restricted_temporal_description.py","derived_input":"data/derived/descriptive_temporal.csv","input_hash":sha("data/derived/descriptive_temporal.csv"),"source_rows":str(len(rows)),"source_snapshots":"27","calculation":"direct field selection; no trend model or inferential comparison","output_artifact":"outputs/b1/restricted_temporal_description.csv"}])
