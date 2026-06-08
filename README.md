# NHS RTT Waiting List Intelligence

End-to-end NHS Referral to Treatment (RTT) waiting list analytics project using SQL, Python, data quality checks, and dashboards.

## Project Aim

This project analyses NHS RTT incomplete pathway data at provider and treatment-function level. The goal is to demonstrate how raw healthcare operational data can be cleaned, validated, modelled, and converted into clear insights for service planning and performance improvement.

## Business Problem

NHS Trusts need reliable intelligence to monitor elective waiting lists, identify specialties under pressure, track long-wait patients, and support evidence-based operational decisions. This project uses publicly available NHS England RTT data to create a reproducible analytics workflow.

## Dataset

Primary dataset for Phase 1:

- NHS England Referral to Treatment Waiting Times
- Provider-level incomplete pathways
- Reporting period: March 2026

The raw Excel file should be stored locally in:

```text
data/raw/rtt_incomplete_pathways.xlsx
```

Raw and processed data files are not committed to GitHub.

## Skills Demonstrated

- Python data extraction and cleaning
- Structured healthcare dataset transformation
- Data quality validation
- SQL table design
- Complex SQL queries
- KPI development
- Reproducible project structure
- Healthcare operational analysis

## Project Structure

```text
nhs-rtt-waiting-list-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
├── src/
├── dashboard/
├── models/
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

1. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Place the raw Excel file here:

```text
data/raw/rtt_incomplete_pathways.xlsx
```

4. Transform the raw NHS RTT file.

```bash
python src/transform.py
```

This creates:

```text
data/processed/rtt_incomplete_provider_clean.csv
```

5. Create the PostgreSQL database.

```bash
createdb nhs_rtt
psql nhs_rtt < sql/01_create_tables.sql
```

6. Load the clean data into PostgreSQL.

```bash
python src/load.py
```

7. Run the SQL analysis queries.

```bash
psql nhs_rtt < sql/03_analysis_queries.sql
```

## Key Metrics Created

- Total incomplete pathways
- Total within 18 weeks
- Percentage within 18 weeks
- Median waiting time in weeks
- 92nd percentile waiting time in weeks
- Total 52+ week waits
- Total 65+ week waits
- Total 78+ week waits
- Percentage 52+ week waits

## Phases

- Phase 1: Clean raw RTT provider data
- Phase 2: Load cleaned data into PostgreSQL
- Phase 3: Build SQL data quality checks
- Phase 4: Create insight queries and KPI report
- Phase 5: Build Streamlit dashboard
- Phase 6: Add historical data and forecasting model
