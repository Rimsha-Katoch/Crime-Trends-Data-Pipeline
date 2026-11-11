
import requests
import pandas as pd
from pathlib import Path
import time
import os
from dotenv import load_dotenv

load_dotenv()
#API_URL = "https://invalid.example.com/crime-data.json"
API_URL = "https://data.cambridgema.gov/resource/3gki-wyrb.json"
BATCH_SIZE = 1000


def extract_full_dataset():

    project_root = Path(__file__).resolve().parents[2]

    raw_folder = project_root / "data" / "raw"
    raw_folder.mkdir(parents=True, exist_ok=True)

    output_file = raw_folder / "cambridge_police_log_full.csv"

    data_source = os.getenv("DATA_SOURCE", "local").lower()

    # -----------------------------------
    # LOCAL MODE
    # -----------------------------------

    if data_source == "local":

        if not output_file.exists():
            raise FileNotFoundError(
                f"Local dataset not found: {output_file}"
            )

        df = pd.read_csv(output_file)

        actual_source = "local"

        print("Using existing local dataset.")
        print("Internet connection is not required.")

    # -----------------------------------
    # ONLINE MODE WITH AUTOMATIC FALLBACK
    # -----------------------------------

    elif data_source == "api":

        print("Starting online data extraction...")

        all_records = []
        offset = 0

        try:

            while True:

                params = {
                    "$limit": BATCH_SIZE,
                    "$offset": offset,
                    "$order": "date_time ASC"
                }

                response = requests.get(
                    API_URL,
                    params=params,
                    timeout=60
                )

                response.raise_for_status()

                records = response.json()

                if not records:
                    break

                all_records.extend(records)

                print(
                    f"Downloaded {len(records)} records. "
                    f"Total: {len(all_records)}"
                )

                offset += BATCH_SIZE

                if len(records) < BATCH_SIZE:
                    break

                time.sleep(0.2)

            if not all_records:
                raise ValueError(
                    "No records downloaded from API."
                )

            df = pd.DataFrame(all_records)

            # Save only after the complete download succeeds
            temp_file = output_file.with_suffix(".tmp")

            df.to_csv(temp_file, index=False)
            os.replace(temp_file, output_file)

            actual_source = "api"

            print("Online dataset downloaded successfully.")
            print("Updated local CSV backup.")

        except (requests.RequestException, ValueError) as error:

            print("\nAPI extraction failed:", error)
            print("Attempting to use local CSV fallback...")

            if not output_file.exists():
                raise RuntimeError(
                    "API failed and local CSV is unavailable."
                ) from error

            df = pd.read_csv(output_file)

            actual_source = "local_fallback"

            print("Using previously saved local dataset.")
            print("Warning: This data may not be the latest.")

    else:

        raise ValueError(
            "Invalid DATA_SOURCE. Use 'local' or 'api'."
        )

    print("\n========== EXTRACTION SUMMARY ==========")

    print("Total records:", len(df))
    print("Total columns:", len(df.columns))
    print("Columns:", df.columns.tolist())
    print("Requested data source:", data_source)
    print("Actual data source:", actual_source)
    print("Dataset:", output_file)

    print("\nExtraction completed successfully!")

    return df


if __name__ == "__main__":
    extract_full_dataset()
