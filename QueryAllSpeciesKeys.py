import pandas as pd
import requests
import time
from pathlib import Path

# Input and output file paths
input_csv = "species_keys.csv"  # Your input CSV file (should contain a column named 'speciesKey')
output_csv = "species_metadata.csv"  # Output CSV file with metadata

# Load species keys
species_df = pd.read_csv(input_csv)

# API base URL
base_url = "https://api.gbif.org/v1/species/"

# Store results here
results = []

# Loop through each speciesKey and query the API
for idx, row in species_df.iterrows():
    species_key = row['speciesKey']
    url = f"{base_url}{species_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results.append(data)
        else:
            print(f"[{idx}] Failed for {species_key}: Status {response.status_code}")
            results.append({"speciesKey": species_key, "error": f"HTTP {response.status_code}"})
    except Exception as e:
        print(f"[{idx}] Error for {species_key}: {e}")
        results.append({"speciesKey": species_key, "error": str(e)})

    time.sleep(0.2)  # Avoid overwhelming the API

# Convert list of dicts to DataFrame
results_df = pd.json_normalize(results)

# Save to CSV
results_df.to_csv(output_csv, index=False)

print(f"\n✅ Finished! Metadata written to: {Path(output_csv).resolve()}")
