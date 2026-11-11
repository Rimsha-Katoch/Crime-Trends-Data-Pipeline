
from datetime import datetime

from prefect import flow, task
from prefect.client.schemas.schedules import CronSchedule
from sqlalchemy import text

from crime_pipeline.db import get_engine
from crime_pipeline.extract_full_data import extract_full_dataset
from crime_pipeline.validate_data import validate_and_clean_data
from crime_pipeline.transform_data import transform_data
from crime_pipeline.load_data import load_data


def save_pipeline_run(
    start_time,
    end_time,
    status,
    records_processed=0,
    error_message=None
):
    engine = get_engine()

    try:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO pipeline_runs (
                        start_time,
                        end_time,
                        status,
                        records_processed,
                        error_message
                    )
                    VALUES (
                        :start_time,
                        :end_time,
                        :status,
                        :records_processed,
                        :error_message
                    )
                """),
                {
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": status,
                    "records_processed": records_processed,
                    "error_message": error_message
                }
            )
    finally:
        engine.dispose()


@task(name="Extract Data", retries=2, retry_delay_seconds=5)
def extraction_task():
    print("Starting data extraction...")
    extract_full_dataset()


@task(name="Validate and Clean Data", retries=2, retry_delay_seconds=5)
def validation_task():
    print("Starting data validation and cleaning...")
    validate_and_clean_data()


@task(name="Transform Data", retries=2, retry_delay_seconds=5)
def transformation_task():
    print("Starting data transformation...")
    transform_data()


@task(name="Load Data into PostgreSQL", retries=2, retry_delay_seconds=5)
def loading_task():
    print("Starting database loading...")
    return load_data()


@flow(name="Crime Trends Data Pipeline")
def crime_data_pipeline():

    start_time = datetime.now()
    records_processed = 0
    status = "Failed"
    error_message = None

    try:
        extraction_task()
        validation_task()
        transformation_task()

        records_processed = loading_task()

        status = "Success"

    except Exception as exc:
        error_message = str(exc)
        raise

    finally:
        end_time = datetime.now()

        save_pipeline_run(
            start_time=start_time,
            end_time=end_time,
            status=status,
            records_processed=records_processed,
            error_message=error_message
        )


if __name__ == "__main__":
    crime_data_pipeline.serve(
        name="daily-crime-trends",
        schedules=[
            CronSchedule(
                cron="0 8 * * *",
                timezone="Asia/Kolkata"
            )
        ],
        tags=["crime-trends", "daily"],
        description="Daily automated Cambridge Police Log data pipeline."
    )
