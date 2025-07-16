import os
import csv

# === CONFIGURATION ===
root_dir = "all_species"  # Replace with your actual folder path
output_csv = "image_counts.csv"

# === IMAGE COUNT FUNCTION ===
def count_images_by_subfolder(root):
    results = []
    for subfolder in os.listdir(root):
        subfolder_path = os.path.join(root, subfolder)
        if os.path.isdir(subfolder_path):
            image_files = [
                f for f in os.listdir(subfolder_path)
                if os.path.isfile(os.path.join(subfolder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]
            results.append((subfolder, len(image_files)))
    return results

# === MAIN SCRIPT ===
image_counts = count_images_by_subfolder(root_dir)

# === WRITE TO CSV ===
with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["folder_name", "image_count"])  # Header
    writer.writerows(image_counts)

print(f"Image counts written to {output_csv}")
