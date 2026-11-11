
import pandas as pd
from pathlib import Path

def transform_data():

    # -----------------------------------
    # 1. Set project paths
    # -----------------------------------

    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root / "data" / "processed"
        / "cambridge_police_log_cleaned.csv"
    )

    output_file = (
        project_root / "data" / "processed"
        / "cambridge_police_log_transformed.csv"
    )


    # -----------------------------------
    # 2. Load cleaned dataset
    # -----------------------------------

    df = pd.read_csv(input_file)

    print("Cleaned dataset loaded successfully!")
    print("Total records:", len(df))


    # -----------------------------------
    # 3. Convert date_time into datetime
    # -----------------------------------

    df["date_time"] = pd.to_datetime(
        df["date_time"], errors="coerce"
    )


    # -----------------------------------
    # 4. Extract date features
    # -----------------------------------

    df["year"] = df["date_time"].dt.year

    df["month"] = df["date_time"].dt.month

    df["month_name"] = df["date_time"].dt.month_name()

    df["day"] = df["date_time"].dt.day

    df["day_name"] = df["date_time"].dt.day_name()

    df["hour"] = df["date_time"].dt.hour


    # -----------------------------------
    # 5. Create time period column
    # -----------------------------------

    def get_time_period(hour):

        if 5 <= hour < 12:
            return "Morning"

        elif 12 <= hour < 17:
            return "Afternoon"

        elif 17 <= hour < 21:
            return "Evening"

        else:
            return "Night"


    df["time_period"] = df["hour"].apply(get_time_period)


    # -----------------------------------
    # 6. Create year_month column
    # -----------------------------------

    df["year_month"] = df["date_time"].dt.strftime("%Y-%m")


    # -----------------------------------
    # 7. Identify weekends
    # -----------------------------------

    df["is_weekend"] = df["day_name"].isin(
        ["Saturday", "Sunday"]
    )

    # -----------------------------------
    # 8. Save transformed dataset
    # -----------------------------------

    df.to_csv(output_file, index=False)

    print("\nData transformation completed!")

    print("Total records:", len(df))

    print("\nNew columns added:")
    new_columns = [
        "year",
        "month",
        "month_name",
        "day",
        "day_name",
        "hour",
        "time_period",
        "year_month",
        "is_weekend"
    ]

    print(new_columns)
    print("\nTotal columns:", len(df.columns))
    print("\nWeekend distribution:")
    print(df["is_weekend"].value_counts())

    print("\nTime period distribution:")
    print(df["time_period"].value_counts())


    print("\nTransformed dataset preview:")

    print(df[[
        "date_time",
        "year",
        "month_name",
        "day_name",
        "hour",
        "time_period",
        "year_month",
        "is_weekend"
    ]].head())


    print("\nSaved file:", output_file)

if __name__ == "__main__":
    transform_data()