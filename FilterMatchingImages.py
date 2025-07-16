import os
import csv
import shutil

# --- Update these paths ---
CSV_FILE = 'new_species_list.csv'
SOURCE_ROOT = '/Users/trien.tran/PycharmProjects/PlantClef/plant/merged_images'  # The folder with thousands of speciesKey-named subfolders
DEST_ROOT = '/Users/trien.tran/Downloads/dl2/cleaned_dataset2'  # New folder to copy matched folders into

# Create the destination folder if it doesn't exist
os.makedirs(DEST_ROOT, exist_ok=True)

# Step 1: Read all speciesKeys from the CSV
with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    species_keys = {row['speciesKey'].strip() for row in reader if row['speciesKey'].strip()}

# Step 2: Loop through all subfolders in the source directory
for folder_name in os.listdir(SOURCE_ROOT):
    folder_path = os.path.join(SOURCE_ROOT, folder_name)

    if os.path.isdir(folder_path) and folder_name in species_keys:
        dest_path = os.path.join(DEST_ROOT, folder_name)

        # Copy the entire folder (overwrite if exists)
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)

        shutil.copytree(folder_path, dest_path)
        print(f"✅ Copied folder: {folder_name}")

print("\n🎉 Done! Matched folders copied to 'cleaned_dataset'.")
