import os
import csv

# === CONFIGURATION ===
# The root directory containing subfolders named by speciesKey
IMAGE_ROOT_DIR = "non_plantae"

# The source CSV file from GBIF
INPUT_CSV = '/Users/trien.tran/Downloads/gbif_species_match_results - conference.csv'

# The new file that will be created with the added count column
OUTPUT_CSV = "all_image_count_2.csv"

# --- SCRIPT START ---

def run_image_count_processor():
    """
    Counts images in subfolders, reads the input CSV, and writes a new
    CSV with an 'image_count' column appended.
    """
    print(f"🔍 Step 1: Counting images in subfolders of '{IMAGE_ROOT_DIR}'...")

    # Create a dictionary to map speciesKey (folder name) to its image count
    image_count_map = {}
    try:
        for folder_name in os.listdir(IMAGE_ROOT_DIR):
            folder_path = os.path.join(IMAGE_ROOT_DIR, folder_name)
            if os.path.isdir(folder_path):
                # Count valid image files in the subfolder
                image_files = [
                    f for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f))
                    and f.lower().endswith(('.jpg', '.jpeg', '.png'))
                ]
                image_count_map[folder_name] = len(image_files)
    except FileNotFoundError:
        print(f"❌ ERROR: The directory '{IMAGE_ROOT_DIR}' was not found. Please check the path.")
        return

    print(f"✅ Found image counts for {len(image_count_map)} species folders.")
    print("-" * 30)
    print(f"🔄 Step 2: Processing '{INPUT_CSV}' to add image counts...")

    try:
        # Open the input and output files
        with open(INPUT_CSV, mode='r', newline='', encoding='utf-8') as infile, \
             open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Read the header from the input file
            header = next(reader)

            # Find the column index for 'speciesKey' to make the script robust
            try:
                species_key_index = header.index('speciesKey')
            except ValueError:
                print(f"❌ ERROR: 'speciesKey' column not found in '{INPUT_CSV}'.")
                return

            # Write the new header to the output file
            writer.writerow(header + ['image_count'])

            # Process each row in the input CSV
            processed_rows = 0
            for row in reader:
                if not row:  # Skip empty rows
                    continue

                # Get the speciesKey from the row
                species_key = row[species_key_index]

                # Look up the image count using the speciesKey. Default to 0 if not found.
                image_count = image_count_map.get(species_key, 0)

                # Append the count to the row and write it to the new file
                writer.writerow(row + [image_count])
                processed_rows += 1

    except FileNotFoundError:
        print(f"❌ ERROR: The input file '{INPUT_CSV}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    print(f"✅ Processed {processed_rows} rows.")
    print(f"🎉 Success! New file with image counts is saved as '{OUTPUT_CSV}'.")

# === EXECUTE SCRIPT ===
if __name__ == "__main__":
    run_image_count_processor()