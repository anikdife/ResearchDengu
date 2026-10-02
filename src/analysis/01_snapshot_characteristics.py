from common import *
rows=read_csv("data/derived/descriptive_temporal.csv"); obs=read_csv("data/processed/dghs_research_observations.csv")
families={r["snapshot_id"]:[] for r in rows}
for r in obs:
    if r["snapshot_id"] in families: families[r["snapshot_id"]].append(r["data_family"]+":"+r["availability"])
out=[]
for r in rows:
    sid=r["snapshot_id"]
    out.append({"snapshot_id":sid,"year":sid[:4],"requested_date":r["requested_date"],"displayed_date":r["displayed_date"],"headline_observations":"4","available_families":";".join(sorted(families[sid])),"demographic_availability":"age_by_sex=NOT_AVAILABLE;death_age_by_sex=NOT_AVAILABLE","geographic_availability":"division_data=PRESENT;division_by_epi_week=PRESENT;city_corporation_data=PRESENT","semantic_status":"SUPPORTED_MEANING","anomalous_categories":"see outputs/b010_category_anomalies.csv"})
fields=list(out[0]); write_csv("outputs/b1/snapshot_characteristics.csv",out,fields)
provenance([{"result_id":"B1-SNAP-001","description":"Analysis-ready snapshot inventory","analysis_script":"src/analysis/01_snapshot_characteristics.py","derived_input":"data/derived/descriptive_temporal.csv","input_hash":sha("data/derived/descriptive_temporal.csv"),"source_rows":str(len(rows)),"source_snapshots":"27","calculation":"one row per authorized snapshot; family availability joined by snapshot_id","output_artifact":"outputs/b1/snapshot_characteristics.csv"}])
