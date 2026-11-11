
import pandas as pd
from pathlib import Path

# Locate the project directory
project_root = Path(__file__).resolve().parents[2]

# Read the downloaded CSV
file_path = project_root / "data" / "raw" / "cambridge_police_log_full.csv"

df = pd.read_csv(file_path)

print("\n========== DATA OVERVIEW ==========")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())


# Check missing values
print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


# Check duplicate IDs
print("\n========== DUPLICATE RECORDS ==========")

print("Duplicate IDs:", df["id"].duplicated().sum())


# Check activity types
print("\n========== ACTIVITY TYPES ==========")

print(df["type"].value_counts(dropna=False))


# Check most common subtypes
print("\n========== TOP 10 SUBTYPES ==========")

print(df["subtype"].value_counts(dropna=False).head(10))


# Check date range
print("\n========== DATE RANGE ==========")

df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

print("Earliest date:", df["date_time"].min())
print("Latest date:", df["date_time"].max())

print("\nData profiling completed!")
