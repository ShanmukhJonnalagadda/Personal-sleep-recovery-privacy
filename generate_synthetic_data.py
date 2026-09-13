"""Generate deterministic synthetic WHOOP-style data for the public demo."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "synthetic_whoop_data.csv"


def main() -> None:
    rng = np.random.default_rng(625)
    days = 120
    dates = pd.date_range(end="2026-09-12", periods=days, freq="D")

    sleep_minutes = np.clip(rng.normal(450, 50, days), 300, 570)
    sleep_performance = np.clip((sleep_minutes / 510) * 100 + rng.normal(0, 5, days), 55, 100)
    day_strain = np.clip(rng.normal(11.8, 3.0, days), 4.0, 19.0)
    recovery = np.clip(
        42 + 0.075 * sleep_minutes - 0.7 * np.roll(day_strain, 1) + rng.normal(0, 11, days),
        20,
        98,
    )
    recovery[0] = 70

    frame = pd.DataFrame(
        {
            "cycle_date": dates.date,
            "recovery_score": recovery.round(0).astype(int),
            "hrv_ms": np.clip(48 + (recovery - 60) * 0.28 + rng.normal(0, 6, days), 25, 85).round(1),
            "resting_hr_bpm": np.clip(61 - (recovery - 60) * 0.08 + rng.normal(0, 2, days), 48, 72).round(1),
            "sleep_performance_pct": sleep_performance.round(0).astype(int),
            "sleep_duration_min": sleep_minutes.round(0).astype(int),
            "day_strain": day_strain.round(1),
            "workout_strain": np.clip(day_strain - rng.uniform(1, 7, days), 0, 18).round(1),
            "primary_activity": rng.choice(
                ["Running", "Weightlifting", "Cricket", "Walking", "Rest"],
                size=days,
                p=[0.18, 0.22, 0.10, 0.30, 0.20],
            ),
        }
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)
    print(f"Created {OUTPUT} with {len(frame)} synthetic records")


if __name__ == "__main__":
    main()

