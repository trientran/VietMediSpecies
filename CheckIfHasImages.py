import os
import csv

# --- Update these paths ---
CSV_FILE = 'new_species_list.csv'
SOURCE_ROOT = '/Users/trien.tran/PycharmProjects/PlantClef/plant/merged_images'
OUTPUT_CSV = 'new_species_list_has_images.csv'

# Get all folder names in SOURCE_ROOT as a set for quick lookup
available_folders = {name for name in os.listdir(SOURCE_ROOT) if os.path.isdir(os.path.join(SOURCE_ROOT, name))}

# Open the input CSV and create a new CSV with the "hasImages" column
with open(CSV_FILE, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['hasImages']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        species_key = row['speciesKey'].strip()
        row['hasImages'] = 'yes' if species_key in available_folders else 'no'
        writer.writerow(row)

print("✅ Updated CSV with 'hasImages' column saved to:", OUTPUT_CSV)
