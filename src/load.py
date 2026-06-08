"""Load cleaned NHS RTT data into PostgreSQL."""

import pandas as pd
from sqlalchemy import create_engine, text

from config import DATABASE_URL, PROCESSED_DATA_PATH


def load_to_postgres() -> None:
    """Load processed RTT data into the rtt_waiting_list table."""
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed file not found at {PROCESSED_DATA_PATH}. "
            "Run python src/transform.py first."
        )

    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["reporting_month"])

    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        # Prevent duplicate loads for the same reporting month.
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
