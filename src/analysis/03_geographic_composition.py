from common import *
obs=read_csv("data/processed/dghs_research_observations.csv"); out=[]
for family in ("division_data","division_by_epi_week","city_corporation_data"):
    for r in obs:
        if r["data_family"]==family: out.append({"snapshot_id":r["snapshot_id"],"data_family":family,"availability":r["availability"],"raw_label":r["raw_label"],"denominator_compatibility":"NOT_ESTABLISHED","interpretation":"source geographic label only; no residence/rural inference"})
fields=list(out[0]); write_csv("outputs/b1/geographic_composition.csv",out,fields)
provenance([{"result_id":"B1-GEO-001","description":"Geographic family availability and raw labels","analysis_script":"src/analysis/03_geographic_composition.py","derived_input":"data/processed/dghs_research_observations.csv","input_hash":sha("data/processed/dghs_research_observations.csv"),"source_rows":str(len(obs)),"source_snapshots":"27","calculation":"family-level availability and raw-label selection; no incompatible proportions","output_artifact":"outputs/b1/geographic_composition.csv"}])
