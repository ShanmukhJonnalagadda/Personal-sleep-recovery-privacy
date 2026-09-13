"""Run data checks and an optional Streamlit application smoke test."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_pipeline import load_demo_data, filter_by_days, summary_metrics

data = load_demo_data(ROOT / "data/synthetic_whoop_data.csv")
assert len(data) == 120
assert data.cycle_date.is_monotonic_increasing
assert data.cycle_date.is_unique
assert data.recovery_score.between(0, 100).all()
assert data.day_strain.between(0, 21).all()
assert data.next_cycle_recovery.isna().sum() == 1
assert data.next_cycle_recovery.iloc[0] == data.recovery_score.iloc[1]
assert len(filter_by_days(data, 30)) == 30
assert len(filter_by_days(data, 90)) == 90
assert len(filter_by_days(data, None)) == 120
assert len(summary_metrics(data)) == 5
print("Data validation passed: 120 synthetic records and date filters.")

from streamlit.testing.v1 import AppTest
app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
assert not app.exception, str(app.exception)
assert len(app.metric) == 5
for selection in ["30 days", "90 days", "All data"]:
    app.selectbox[0].select(selection).run()
    assert not app.exception, str(app.exception)
print("Streamlit smoke test passed: startup, five metrics, three period filters.")
