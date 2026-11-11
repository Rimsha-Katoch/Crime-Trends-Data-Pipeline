
import pandas as pd
from pathlib import Path
from sqlalchemy import text

from crime_pipeline.db import get_engine


def load_data():

    # -----------------------------------
    # 1. Set project paths
    # -----------------------------------

    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root / "data" / "processed"
        / "cambridge_police_log_transformed.csv"
    )

    # -----------------------------------
    # 2. Load transformed CSV
    # -----------------------------------

    df = pd.read_csv(input_file)

    print("Transformed dataset loaded!")
    print("Total records:", len(df))

    # -----------------------------------
    # 3. Prepare data types
    # -----------------------------------

    df["date_time"] = pd.to_datetime(df["date_time"])
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    df["is_weekend"] = df["is_weekend"].astype(bool)

    # -----------------------------------
    # 4. Connect to PostgreSQL
    # -----------------------------------

    engine = get_engine()

    print("\nConnected to PostgreSQL!")

    # -----------------------------------
    # 5. Insert records safely
    # -----------------------------------

    columns = [
        "id", "date_time", "type", "subtype",
        "location", "description", "last_updated",
        "year", "month", "month_name", "day",
        "day_name", "hour", "time_period",
        "year_month", "is_weekend"
    ]

    insert_sql = text("""
        INSERT INTO crime_records (
            id, date_time, type, subtype,
            location, description, last_updated,
            year, month, month_name, day,
            day_name, hour, time_period,
            year_month, is_weekend
        )
        VALUES (
            :id, :date_time, :type, :subtype,
            :location, :description, :last_updated,
            :year, :month, :month_name, :day,
            :day_name, :hour, :time_period,
            :year_month, :is_weekend
        )
        ON CONFLICT (id) DO UPDATE SET
            date_time = EXCLUDED.date_time,
            type = EXCLUDED.type,
            subtype = EXCLUDED.subtype,
            location = EXCLUDED.location,
            description = EXCLUDED.description,
            last_updated = EXCLUDED.last_updated,
            year = EXCLUDED.year,
            month = EXCLUDED.month,
            month_name = EXCLUDED.month_name,
            day = EXCLUDED.day,
            day_name = EXCLUDED.day_name,
            hour = EXCLUDED.hour,
            time_period = EXCLUDED.time_period,
            year_month = EXCLUDED.year_month,
            is_weekend = EXCLUDED.is_weekend
    """)

    records = df[columns].to_dict(orient="records")

    with engine.begin() as connection:
        connection.execute(insert_sql, records)

    print("\nData loading completed successfully!")
    print("Records processed:", len(records))

    # -----------------------------------
    # 6. Verify database record count
    # -----------------------------------

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM crime_records")
        )
        total_records = result.scalar()

    print("Total records in PostgreSQL:", total_records)

    engine.dispose()
    return len(records)


if __name__ == "__main__":
    load_data()
