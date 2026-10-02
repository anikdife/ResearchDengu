from pathlib import Path


def test_stage_a_report_stops_before_stage_b():
    report = Path("docs/STAGE-A-REPORT.md").read_text(encoding="utf-8")
    assert "STAGE_A_COMPLETE" in report
    assert "STAGE_B_NOT_STARTED" in report
