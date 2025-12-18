import csv
import logging

ORIGINAL_KEYS_CSV = "csv/all_viet_species_keys.csv"              # original list
METADATA_CSV = "csv/gbif_4799_species_metadata.csv"         # file generated from GBIF API
OUTPUT_CSV = "csv/merged_species_with_gbif_metadata.csv"      # merged output


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_metadata_by_species_key(path: str):
    """
    Load gbif_species_metadata.csv into a dict keyed by speciesKey.
    Assumes there is a 'speciesKey' column in the metadata CSV.
    """
    meta_by_key = {}
    fieldnames = None

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if "speciesKey" not in fieldnames:
            raise ValueError(
                f"'speciesKey' column not found in metadata file {path}. "
                "Check the header row."
            )

        for row in reader:
            sk = (row.get("speciesKey") or "").strip()
            if sk:
                # last one wins if duplicates, which is fine for our use
                meta_by_key[sk] = row

    logging.info(
        "Loaded %d metadata rows with %d fields from %s",
        len(meta_by_key), len(fieldnames), path
    )
    return meta_by_key, fieldnames


def merge_in_original_order(original_keys_csv: str,
                            metadata_csv: str,
                            output_csv: str):
    # 1. Load metadata indexed by speciesKey
    meta_by_key, meta_fieldnames = load_metadata_by_species_key(metadata_csv)

    # Ensure 'speciesKey' is present and first in the header
    fieldnames = list(meta_fieldnames)
    if "speciesKey" not in fieldnames:
        fieldnames.insert(0, "speciesKey")

    # Optionally, move speciesKey to the front if it's not already
    if fieldnames[0] != "speciesKey":
        fieldnames.remove("speciesKey")
        fieldnames.insert(0, "speciesKey")

    logging.info("Final header will have %d columns.", len(fieldnames))

    # 2. Open original list and create output
    count_total = 0
    count_found = 0
    count_missing = 0

    with open(original_keys_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:

        original_reader = csv.DictReader(fin)
        if "speciesKey" not in original_reader.fieldnames:
            raise ValueError(
                f"'speciesKey' column not found in original file {original_keys_csv}"
            )

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in original_reader:
            count_total += 1
            sk = (row.get("speciesKey") or "").strip()

            meta_row = meta_by_key.get(sk)
            if meta_row is not None:
                # Use metadata row, but ensure speciesKey = original key
                out_row = {field: meta_row.get(field, "") for field in fieldnames}
                out_row["speciesKey"] = sk  # enforce original key just in case
                count_found += 1
            else:
                # Create blank row with only speciesKey filled
                out_row = {field: "" for field in fieldnames}
                out_row["speciesKey"] = sk
                count_missing += 1

            writer.writerow(out_row)

    logging.info(
        "Done. Total: %d | Found in metadata: %d | Missing (blank rows): %d",
        count_total, count_found, count_missing
    )
    logging.info("Output written to %s", output_csv)


if __name__ == "__main__":
    merge_in_original_order(ORIGINAL_KEYS_CSV, METADATA_CSV, OUTPUT_CSV)
