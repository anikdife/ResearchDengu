from common import *
import shutil
for name in ("snapshot_characteristics.csv","restricted_temporal_description.csv","geographic_composition.csv","demographic_composition.csv","surveillance_quality_summary.csv"):
    shutil.copyfile(ROOT/"outputs"/"b1"/name,TABLES/name)
