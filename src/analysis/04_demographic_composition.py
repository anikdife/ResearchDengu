from common import *
obs=read_csv("data/processed/dghs_research_observations.csv"); age=read_csv("metadata/b011-age-label-map.csv"); out=[]
for family in ("age_by_sex","death_age_by_sex"):
    for r in obs:
        if r["data_family"]==family: out.append({"snapshot_id":r["snapshot_id"],"data_family":family,"availability":r["availability"],"raw_label":r["raw_label"],"safe_category_status":"NOT_ANALYZED","exclusion_reason":"family unavailable in B0.10; no age×sex counts"})
fields=list(out[0]); write_csv("outputs/b1/demographic_composition.csv",out,fields)
write_csv("outputs/b1/age_category_exclusions.csv",[{"raw_label":r["raw_label"],"normalization_status":r["normalization_status"],"reason":r["reason"]} for r in age],["raw_label","normalization_status","reason"])
provenance([{"result_id":"B1-DEM-001","description":"Age×sex availability and exclusion audit","analysis_script":"src/analysis/04_demographic_composition.py","derived_input":"data/processed/dghs_research_observations.csv; metadata/b011-age-label-map.csv","input_hash":sha("data/processed/dghs_research_observations.csv"),"source_rows":str(len(obs)),"source_snapshots":"27","calculation":"availability audit; no category redistribution or demographic composition","output_artifact":"outputs/b1/demographic_composition.csv"}])
