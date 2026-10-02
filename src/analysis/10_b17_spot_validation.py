"""Small offline source-to-table spot validation for B1.7."""
from pathlib import Path
import csv, re
ROOT=Path(__file__).resolve().parents[2]
targets=['2024-01-01','2025-09-29','2026-09-29']
with open(ROOT/'data/derived/descriptive_temporal.csv',encoding='utf-8-sig',newline='') as f: source={r['snapshot_id']:r for r in csv.DictReader(f)}
rows=[]
for sid in targets:
    text=(ROOT/f'data/historical_acquisition/{sid}/response.html').read_text(encoding='utf-8',errors='replace')
    r=source[sid]
    a=re.search(r"w_a\.png.*?(\d[\d,]*)\s*</div>",text,re.S)
    d=re.search(r"w_d\.png.*?(\d[\d,]*)\s*</div>",text,re.S)
    ca=re.search(r"c_a\.png.*?(\d[\d,]*)\s*</div>",text,re.S)
    cd=re.search(r"c_d\.png.*?(\d[\d,]*)\s*</div>",text,re.S)
    date_ok=f'value="{sid}"' in text
    display_ok=__import__('datetime').datetime.strptime(sid,'%Y-%m-%d').strftime('%d-%b-%Y') in text
    rows += [
        {'snapshot_id':sid,'check':'weekly_case_summary_strip','expected':r['weekly_case_raw'],'observed':a.group(1).replace(',','').strip() if a else 'MISSING','status':'MATCH' if a and a.group(1).replace(',','').strip()==r['weekly_case_raw'] else 'MISMATCH'},
        {'snapshot_id':sid,'check':'weekly_death_summary_strip','expected':r['weekly_death_raw'],'observed':d.group(1).replace(',','').strip() if d else 'MISSING','status':'MATCH' if d and d.group(1).replace(',','').strip()==r['weekly_death_raw'] else 'MISMATCH'},
        {'snapshot_id':sid,'check':'cumulative_case_summary_strip','expected':r['cumulative_case_raw'],'observed':ca.group(1).replace(',','').strip() if ca else 'MISSING','status':'MATCH' if ca and ca.group(1).replace(',','').strip()==r['cumulative_case_raw'] else 'MISMATCH'},
        {'snapshot_id':sid,'check':'cumulative_death_summary_strip','expected':r['cumulative_death_raw'],'observed':cd.group(1).replace(',','').strip() if cd else 'MISSING','status':'MATCH' if cd and cd.group(1).replace(',','').strip()==r['cumulative_death_raw'] else 'MISMATCH'},
        {'snapshot_id':sid,'check':'date_control','expected':sid,'observed':str(date_ok),'status':'MATCH' if date_ok else 'MISMATCH'},
        {'snapshot_id':sid,'check':'displayed_date','expected':sid,'observed':str(display_ok),'status':'MATCH' if display_ok else 'MISMATCH'}]
out=ROOT/'outputs/b17_spot_validation.csv'
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['snapshot_id','check','expected','observed','status']); w.writeheader(); w.writerows(rows)
print(f'B17_SPOT_VALIDATION_ROWS={len(rows)} MISMATCHES={sum(r["status"]!="MATCH" for r in rows)}')
