"""Project configuration for NHS RTT Waiting List Intelligence."""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "rtt_incomplete_pathways.xlsx"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "rtt_incomplete_provider_clean.csv"

# Example for local PostgreSQL:
# postgresql+psycopg2://postgres:password@localhost:5432/nhs_rtt
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2:///nhs_rtt")
