# Data-Pipeline Explanation

## 1. Data acquisition

The project uses the WHOOP API for cycle, recovery, sleep, and workout records. Journal records are handled through exports/imports rather than an assumed journal endpoint. The exact private sync implementation was not inspected; incremental fetching and pagination should be verified against that code before documenting them as implemented.

The public demo does not make external API calls. It reads `data/synthetic_whoop_data.csv`, which has the same general analytical shape without containing personal data.

## 2. Validation and normalization

The included demo checks required columns, parses cycle dates, converts numeric fields, removes rows with invalid dates, sorts records, and removes duplicate cycle dates. Numeric conversion failures become missing values; this is intentionally a small demonstration, not complete production validation. Production data should use authoritative cycle IDs rather than calendar dates for identity.

## 3. Feature engineering

The processed dataset includes derived values used by the dashboard:

- Total sleep duration in hours
- Next-cycle recovery for strain–recovery analysis
- Seven-record rolling recovery and HRV trends
- Date-range filtering

Local bedtime and wake-time analysis belongs to the private project, not this demo dataset. Next-cycle recovery is assigned before filtering, so a plotted strain point can refer to a recovery record outside the selected display range. Synthetic data contains one consecutive record per day; a real pipeline must preserve cycle order and handle gaps explicitly.

## 4. Persistent storage

The private project uses Supabase/PostgreSQL for persistent data and preferences. Table names, conflict keys, row-level policies, and upsert behavior must be checked against the private implementation. The public demo has no database connector and never writes user records.

## 5. Scheduled synchronization

GitHub Actions runs the production synchronization workflow every six hours. The workflow retrieves new data, applies the same validation and transformation rules, and updates the cloud database.

## 6. Visualization

The Streamlit application queries the stored records, applies the selected date filter, calculates summary metrics, and renders interactive Plotly charts for recovery, sleep, strain, and activity analysis.

## 7. Access control

The private project uses Google OAuth for sign-in. Account allowlisting and database authorization are separate controls that must be configured and verified in production. The public demo does not authenticate users and is suitable only for synthetic data.

## Production flow

See the architecture diagram and Mermaid source in README.md. Scheduled ingestion and user sign-in are separate from the data-flow path.

## Privacy controls

- A production implementation should keep credentials in protected secret stores; this package contains placeholders only.
- Personal health data is excluded from this public repository.
- The sample dataset is deterministic and fully synthetic.
- The public application code operates in demo mode only.

Reference: [WHOOP API reference](https://developer.whoop.com/api/).
