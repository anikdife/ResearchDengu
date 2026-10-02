import csv, json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class B1OfflineTests(unittest.TestCase):
    def test_input_hash_enforcement(self):
        m=json.loads((ROOT/'metadata/b011-derived-dataset-manifest.json').read_text())
        for f in m['derived_files']: self.assertEqual(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest(),f['sha256'])
    def test_prohibited_terms_protocol(self):
        t=(ROOT/'docs/B1-ANALYSIS-PROTOCOL.md').read_text().lower(); self.assertIn('incidence',t); self.assertIn('no p-values',t); self.assertIn('will be produced',t)
    def test_ambiguous_age_exclusion(self):
        rows=list(csv.DictReader((ROOT/'metadata/b011-age-label-map.csv').open())); self.assertTrue(any(r['normalization_status']=='AMBIGUOUS' for r in rows)); self.assertTrue(any(r['normalization_status']=='MALFORMED' for r in rows))
    def test_geographic_terminology(self): self.assertIn('not ruralized',(ROOT/'docs/B1-ANALYSIS-PROTOCOL.md').read_text())
    def test_provenance_completeness(self):
        rows=list(csv.DictReader((ROOT/'outputs/b1/result-provenance.csv').open())); self.assertTrue(rows); self.assertTrue(all(all(v for v in r.values()) for r in rows))
    def test_2026_note(self):
        rows=list(csv.DictReader((ROOT/'outputs/b1/restricted_temporal_description.csv').open())); self.assertTrue(all(r['incomplete_period_note'] for r in rows if r['year']=='2026'))
if __name__=='__main__': unittest.main()
