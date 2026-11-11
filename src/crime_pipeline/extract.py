
import requests
import pandas as pd
from pathlib import Path


# Cambridge Police Daily Log API
API_URL = "https://data.cambridgema.gov/resource/3gki-wyrb.json"


def extract_sample_data():

    print("Starting data extraction...")

    # Request the latest 100 records
    params = {
        "$limit": 100,
        "$order": "date_time DESC"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        # Convert JSON response into Python records
        records = response.json()

        if not records:
            print("No records received.")
            return

        # Convert records into a DataFrame
        df = pd.DataFrame(records)

        # Find the main project directory
        project_root = Path(__file__).resolve().parents[2]

        # Create raw data folder if it does not exist
        raw_folder = project_root / "data" / "raw"
        raw_folder.mkdir(parents=True, exist_ok=True)

        # Save the original downloaded data
        output_file = raw_folder / "cambridge_police_log_sample.csv"

        df.to_csv(output_file, index=False)

        print("\nData extraction successful!")
        print("Number of records:", len(df))
        print("Columns:", list(df.columns))
        print("Saved file:", output_file)

        print("\nFirst five records:")
        print(df.head())

    except requests.exceptions.RequestException as error:
        print("API connection failed:", error)


if __name__ == "__main__":
    extract_sample_data()
