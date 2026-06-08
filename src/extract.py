"""Extract raw NHS RTT provider data from the Excel workbook."""

import pandas as pd

from config import RAW_DATA_PATH


def load_raw_provider_data() -> pd.DataFrame:
    """Load the Provider sheet from the raw NHS RTT Excel file."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found at {RAW_DATA_PATH}. "
            "Place rtt_incomplete_pathways.xlsx in data/raw/."
        )

    return pd.read_excel(
        RAW_DATA_PATH,
        sheet_name="Provider",
        header=13,
    )


if __name__ == "__main__":
    raw_df = load_raw_provider_data()
    print(raw_df.shape)
    print(raw_df.head())
