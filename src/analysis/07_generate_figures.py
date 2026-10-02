from common import *
import html
rows=read_csv("data/derived/descriptive_temporal.csv")
def svg(filename,title,values):
    w,h=1000,420; maxv=max(values) or 1; bw=max(4,(w-80)//len(values)-2); bars=[]
    for i,(r,val) in enumerate(zip(rows,values)):
        x=40+i*((w-80)//len(rows)); bh=int(300*val/maxv); bars.append(f'<rect x="{x}" y="{350-bh}" width="{bw}" height="{bh}" fill="#3366aa"><title>{html.escape(r["snapshot_id"])}: {val}</title></rect>')
    (FIGURES/filename).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><text x="40" y="28" font-size="20">{html.escape(title)}</text>{"".join(bars)}<text x="40" y="400" font-size="12">Snapshot date; source-reported value; no inferential trend</text></svg>',encoding="utf-8")
svg("headline_weekly_cases.svg","DGHS-reported weekly headline observations by snapshot",[int(r["weekly_case_raw"]) for r in rows])
svg("headline_cumulative_cases.svg","DGHS-reported cumulative headline observations by snapshot",[int(r["cumulative_case_raw"]) for r in rows])
