# Features and Technical Stack

Scope: this feature inventory describes the private project as discussed, not a source-code audit. The public demo implements only the metrics, three charts, and 30/90/all-data filters described in README.md. Mobile optimization, user isolation, and forecasting are not demonstrated by this demo.

## Analytics features

### Overview

- Summary metrics for recovery, HRV, resting heart rate, sleep performance, day strain, and workouts
- Configurable 30-day, 90-day, custom, and complete-history filters
- Timezone-aware timestamps for local bedtime and wake-time analysis

### Recovery analysis

- Recovery-score trends across the selected period
- HRV and resting-heart-rate time series
- Recovery-band comparisons and longer-term physiological patterns

### Sleep analysis

- Sleep duration versus recovery comparison
- Average sleep-stage composition
- Sleep-quality and sleep-performance trends
- Typical bedtime and wake time
- Bedtime and wake-time variability
- Comparison with a saved WHOOP-recommended bedtime (not assumed to be a public API field)

### Strain and activity analysis

- Personal strain overview
- Primary activity summaries by cycle
- Daily strain versus next-cycle recovery
- Workout frequency and strain trends

### Journal analysis

- Integration of exported/imported journal behaviors with cycle-level data
- Evaluation of relationships between journal behaviors, sleep, and recovery

## Engineering features

- WHOOP API integration in the private production system
- Data cleaning, normalization, deduplication, and enrichment with Python/Pandas
- Persistent storage in Supabase/PostgreSQL
- Scheduled synchronization every six hours with GitHub Actions
- Interactive Plotly visualizations in Streamlit
- Google OAuth access control
- Persistent user preferences and date selections
- Streamlit Community Cloud deployment

## Technical stack

| Category | Technologies | Purpose |
|---|---|---|
| Language | Python | Data processing and application logic |
| Data processing | Pandas, NumPy | Cleaning, transformation, and feature generation |
| Visualization | Plotly | Interactive charts and trend exploration |
| Web application | Streamlit | Dashboard interface and deployment |
| API | WHOOP API | Wearable sleep, recovery, strain, and workout data |
| Database | Supabase, PostgreSQL | Persistent data and preference storage |
| Authentication | Google OAuth | Controlled application access |
| Automation | GitHub Actions | Scheduled six-hour synchronization |
| Version control | Git, GitHub | Source management and automation |
