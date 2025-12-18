import csv
import json
import time
import logging
from typing import List, Dict, Any

import requests

# note that this script will skip species that have no data in the new csv
INPUT_CSV = "csv/4799_species_keys.csv"
OUTPUT_CSV = "csv/gbif_20_species_metadata.csv"
GBIF_SPECIES_URL = "https://api.gbif.org/v1/species/{}"

# Optional: be a good API citizen
REQUEST_DELAY_SECONDS = 0.1  # 100 ms between calls


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def read_species_keys(path: str) -> List[str]:
    """Read speciesKey values from a CSV file with a single column 'speciesKey'."""
    keys = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "speciesKey" not in reader.fieldnames:
            raise ValueError("Input CSV must have a 'speciesKey' column.")
        for row in reader:
            key = row["speciesKey"]
            if key is not None and key != "":
                keys.append(str(key).strip())
    logging.info("Loaded %d speciesKey values from %s", len(keys), path)
    return keys


def fetch_species_detail(species_key: str) -> Dict[str, Any]:
    """Call GBIF Species API for a given speciesKey and return the JSON dict."""
    url = GBIF_SPECIES_URL.format(species_key)
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            logging.warning("Non-200 response for speciesKey %s: %s",
                            species_key, resp.status_code)
            return {}
        return resp.json()
    except requests.RequestException as e:
        logging.error("Request failed for speciesKey %s: %s", species_key, e)
        return {}


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a JSON record so it can be written to CSV.

    - Keep original field names.
    - For non-primitive types (lists/dicts), dump as JSON strings.
    """
    normalized = {}
    for k, v in record.items():
        # Keep None as empty string in CSV
        if v is None:
            normalized[k] = ""
        # Primitive values: str, int, float, bool
        elif isinstance(v, (str, int, float, bool)):
            normalized[k] = v
        # Lists, dicts, or anything else: JSON-encode
        else:
            normalized[k] = json.dumps(v, ensure_ascii=False)
    return normalized


def main():
    species_keys = read_species_keys(INPUT_CSV)

    all_records: List[Dict[str, Any]] = []
    all_fieldnames: set = set()

    for i, sk in enumerate(species_keys, start=1):
        logging.info("Fetching %s (%d/%d)", sk, i, len(species_keys))
        record = fetch_species_detail(sk)
        if not record:
            logging.warning("No data for speciesKey %s, skipping.", sk)
            continue

        normalized = normalize_record(record)
        all_records.append(normalized)
        all_fieldnames.update(normalized.keys())

        time.sleep(REQUEST_DELAY_SECONDS)

    if not all_records:
        logging.warning("No records fetched; nothing to write.")
        return

    # Convert fieldnames set to a sorted list for stable column order
    fieldnames = sorted(all_fieldnames)

    logging.info("Writing %d records with %d fields to %s",
                 len(all_records), len(fieldnames), OUTPUT_CSV)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in all_records:
            writer.writerow(rec)

    logging.info("Done.")


if __name__ == "__main__":
    main()
