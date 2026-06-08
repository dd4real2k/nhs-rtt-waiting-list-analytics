import pandas as pd

INPUT_FILE = "data/raw/rtt_incomplete_pathways.xlsx"
OUTPUT_FILE = "data/processed/rtt_incomplete_provider_clean.csv"


def transform_data():
    df = pd.read_excel(
        INPUT_FILE,
        sheet_name="Provider",
        header=13
    )

    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")

    keep_cols = [
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
        "% 52 plus weeks"
    ]

    rtt = df[keep_cols].copy()

    rtt.columns = [
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
        "pct_52_plus"
    ]

    rtt["reporting_month"] = "2026-03"

    rtt.to_csv(OUTPUT_FILE, index=False)

    print("Rows:", len(rtt))
    print("Columns:", len(rtt.columns))
    print(rtt.head())


if __name__ == "__main__":
    transform_data()
