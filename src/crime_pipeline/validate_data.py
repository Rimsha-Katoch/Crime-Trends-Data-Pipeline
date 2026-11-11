
import pandas as pd
import json
from pathlib import Path

def validate_and_clean_data():
    # -----------------------------------
    # 1. Set project paths
    # -----------------------------------

    project_root = Path(__file__).resolve().parents[2]

    input_file = project_root / "data" / "raw" / "cambridge_police_log_full.csv"

    output_folder = project_root / "data" / "processed"
    output_folder.mkdir(parents=True, exist_ok=True)

    cleaned_file = output_folder / "cambridge_police_log_cleaned.csv"
    report_file = output_folder / "data_quality_report.json"


    # -----------------------------------
    # 2. Load raw dataset
    # -----------------------------------

    df = pd.read_csv(input_file)

    print("Raw dataset loaded successfully!")
    print("Total records:", len(df))


    # -----------------------------------
    # 3. Validate expected columns
    # -----------------------------------

    expected_columns = [
        "date_time",
        "id",
        "type",
        "subtype",
        "location",
        "description",
        "last_updated"
    ]

    missing_columns = [
        col for col in expected_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    print("\nColumn validation passed!")


    # -----------------------------------
    # 4. Check missing values
    # -----------------------------------

    missing_before = df.isnull().sum().to_dict()

    print("\nMissing values before cleaning:")
    print(df.isnull().sum())


    # -----------------------------------
    # 5. Check duplicate IDs
    # -----------------------------------

    duplicate_ids = int(df["id"].duplicated().sum())

    print("\nDuplicate IDs:", duplicate_ids)


    # -----------------------------------
    # 6. Validate date columns
    # -----------------------------------

    df["date_time"] = pd.to_datetime(
        df["date_time"], errors="coerce"
    )

    df["last_updated"] = pd.to_datetime(
        df["last_updated"], errors="coerce"
    )

    invalid_date_time = int(df["date_time"].isnull().sum())
    invalid_last_updated = int(df["last_updated"].isnull().sum())

    print("\nInvalid date_time values:", invalid_date_time)
    print("Invalid last_updated values:", invalid_last_updated)


    # -----------------------------------
    # 7. Handle missing text values
    # -----------------------------------

    missing_subtype = int(df["subtype"].isnull().sum())
    missing_description = int(df["description"].isnull().sum())

    df["subtype"] = df["subtype"].fillna("Unknown")
    df["description"] = df["description"].fillna("Unknown")

    print("\nMissing subtype values replaced:", missing_subtype)
    print("Missing description values replaced:", missing_description)


    # -----------------------------------
    # 8. Check missing values after cleaning
    # -----------------------------------

    missing_after = df.isnull().sum().to_dict()

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())


    # -----------------------------------
    # 9. Save cleaned dataset
    # -----------------------------------

    df.to_csv(cleaned_file, index=False)

    print("\nCleaned dataset saved successfully!")
    print("File:", cleaned_file)


    # -----------------------------------
    # 10. Generate quality report
    # -----------------------------------

    quality_report = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "duplicate_ids": duplicate_ids,
        "missing_values_before_cleaning": missing_before,
        "missing_values_after_cleaning": missing_after,
        "missing_subtype_replaced": missing_subtype,
        "missing_description_replaced": missing_description,
        "invalid_date_time": invalid_date_time,
        "invalid_last_updated": invalid_last_updated
    }

    with open(report_file, "w") as file:
        json.dump(quality_report, file, indent=4)

    print("\nData quality report generated!")
    print("Report:", report_file)

    print("\n========== VALIDATION COMPLETED ==========")

if __name__ == "__main__":
    validate_and_clean_data()