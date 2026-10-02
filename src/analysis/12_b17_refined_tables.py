"""Package only existing B1 tables into a paper-facing table set."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/derived/b17_tables'; OUT.mkdir(parents=True,exist_ok=True)
def rows(path):
    with open(ROOT/path,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write(name,data,fields):
    with open(OUT/name,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(data)
obs=rows('data/processed/dghs_research_observations.csv'); families=[]
for family in sorted({r['data_family'] for r in obs}):
    rs=[r for r in obs if r['data_family']==family]; families.append({'data_family':family,'snapshot_count':len(rs),'present_count':sum(r['availability']=='PRESENT' for r in rs),'not_available_count':sum(r['availability']=='NOT_AVAILABLE' for r in rs),'semantic_status':'RESTRICTED_SOURCE_LABEL_ONLY'})
write('table1_data_family_semantic_status.csv',families,list(families[0]))
snap=rows('outputs/b1/snapshot_characteristics.csv')
write('table2_snapshot_reproducibility.csv',snap,['snapshot_id','year','requested_date','displayed_date','headline_observations','semantic_status'])
q=rows('outputs/b1/surveillance_quality_summary.csv'); write('table3_quality_findings.csv',q,list(q[0]))
t=rows('outputs/b1/restricted_temporal_description.csv'); write('table4_restricted_descriptive_observations.csv',t,list(t[0]))
registry=[{'artifact':'outputs/b15_finding_registry.csv','role':'full finding registry'},{'artifact':'outputs/b15_result_verification.csv','role':'independent numeric verification'},{'artifact':'outputs/b15_prior_art_collision_matrix.csv','role':'prior-art collision matrix'},{'artifact':'outputs/b16_finding_to_paper_matrix.csv','role':'finding-to-paper classification'},{'artifact':'outputs/b011_revision_audit.csv','role':'supplementary revision audit'},{'artifact':'outputs/b011_reconciliation_failure_classification.csv','role':'supplementary reconciliation classifications'},{'artifact':'outputs/b010_category_anomalies.csv','role':'supplementary category anomaly register'},{'artifact':'outputs/b010_reconciliation_tests.csv','role':'supplementary reconciliation register'},{'artifact':'outputs/b1/result-provenance.csv','role':'result provenance'}]
write('supplementary_registry_index.csv',registry,['artifact','role'])
print('B17_REFINED_TABLES=5')
