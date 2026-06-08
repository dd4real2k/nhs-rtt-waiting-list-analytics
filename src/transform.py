"""Transform NHS RTT incomplete pathway data into an analysis-ready CSV."""

import pandas as pd

from config import PROCESSED_DATA_PATH
from extract import load_raw_provider_data


KEEP_COLUMNS = [
    "Region Code",
    "Provider Code",
    "Provider Name",
    "Treatment Function Code",
    "Treatment Function",
    "Total number of incomplete pathways",
    "Total within 18 weeks",
    "% within 18 weeks",
    "Average (median) waiting time (in weeks)",
    "92nd percentile waiting time (in weeks)",
    "Total 52 plus weeks",
    "Total 65 plus weeks",
    "Total 78 plus weeks",
    "% 52 plus weeks",
]

RENAMED_COLUMNS = [
    "region_code",
    "provider_code",
    "provider_name",
    "treatment_function_code",
    "treatment_function",
    "total_incomplete_pathways",
    "total_within_18_weeks",
    "pct_within_18_weeks",
    "median_wait_weeks",
    "p92_wait_weeks",
    "total_52_plus",
    "total_65_plus",
    "total_78_plus",
    "pct_52_plus",
]

NUMERIC_COLUMNS = [
    "total_incomplete_pathways",
    "total_within_18_weeks",
    "pct_within_18_weeks",
    "median_wait_weeks",
    "p92_wait_weeks",
    "total_52_plus",
    "total_65_plus",
    "total_78_plus",
    "pct_52_plus",
]


def clean_rtt_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardise raw NHS RTT provider data."""
    df = raw_df.dropna(axis=1, how="all").dropna(axis=0, how="all")

    missing_columns = [col for col in KEEP_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    rtt = df[KEEP_COLUMNS].copy()
    rtt.columns = RENAMED_COLUMNS

    # NHS files use '-' where a waiting-time value is suppressed/not applicable.
    # Convert those to missing values and coerce numeric fields safely.
    for col in NUMERIC_COLUMNS:
        rtt[col] = pd.to_numeric(rtt[col].replace("-", pd.NA), errors="coerce")

    rtt["reporting_month"] = pd.to_datetime("2026-03-01")

    # Remove rows without core identifiers.
    rtt = rtt.dropna(
        subset=["provider_code", "provider_name", "treatment_function_code", "treatment_function"]
    )

    return rtt


def transform_data() -> pd.DataFrame:
    """Run the full transformation and write the cleaned CSV."""
    raw_df = load_raw_provider_data()
    rtt = clean_rtt_data(raw_df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    rtt.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"Cleaned rows: {len(rtt)}")
    print(f"Cleaned columns: {len(rtt.columns)}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")
    print(rtt.head())

    return rtt


if __name__ == "__main__":
    transform_data()
