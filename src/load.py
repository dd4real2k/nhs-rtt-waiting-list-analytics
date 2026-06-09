"""Load cleaned NHS RTT data into PostgreSQL."""

import pandas as pd
from sqlalchemy import create_engine, text

from config import DATABASE_URL, PROCESSED_DATA_PATH


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


def load_to_postgres() -> None:
    """Load processed RTT data into the rtt_waiting_list table."""
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed file not found at {PROCESSED_DATA_PATH}. "
            "Run python src/transform.py first."
        )

    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["reporting_month"])

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col].replace("-", pd.NA), errors="coerce")

    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM rtt_waiting_list WHERE reporting_month = :reporting_month"),
            {"reporting_month": df["reporting_month"].iloc[0].date()},
        )

        df.to_sql(
            "rtt_waiting_list",
            connection,
            if_exists="append",
            index=False,
        )

    print(f"Loaded {len(df)} rows into rtt_waiting_list")


if __name__ == "__main__":
    load_to_postgres()
