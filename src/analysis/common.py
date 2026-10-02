"""Shared offline utilities for restricted B1; no network access."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "b1"; TABLES = ROOT / "data" / "derived" / "b1_tables"; FIGURES = ROOT / "data" / "derived" / "b1_figures"
for p in (OUT, TABLES, FIGURES): p.mkdir(parents=True, exist_ok=True)
def read_csv(path):
    with open(ROOT / path, newline="", encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def write_csv(path, rows, fields):
    path=ROOT/path; path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def sha(path):
    h=hashlib.sha256()
    with open(ROOT/path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def provenance(rows):
    fields=["result_id","description","analysis_script","derived_input","input_hash","source_rows","source_snapshots","calculation","output_artifact"]
    path=ROOT/"outputs/b1/result-provenance.csv"; prior=list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
    write_csv("outputs/b1/result-provenance.csv",prior+rows,fields)
