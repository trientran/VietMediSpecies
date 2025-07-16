import os
import shutil

# Path to your parent folder
parent_dir = '/Users/trien.tran/PycharmProjects/PlantClef/plant'

# Merged output folder
output_dir = os.path.join(parent_dir, 'merged_images')
os.makedirs(output_dir, exist_ok=True)

print("Scanning folders in:", parent_dir)

for folder_name in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, folder_name)

    if os.path.isdir(folder_path) and folder_name.startswith('image'):
        print(f"📁 Merging contents of: {folder_name}")

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Add prefix to preserve where it came from
            new_item_name = f"{folder_name}_{item}"
            destination_path = os.path.join(output_dir, new_item_name)

            if os.path.isdir(item_path):
                shutil.copytree(item_path, destination_path, dirs_exist_ok=True)
                print(f"📦 Copied folder: {item_path} → {destination_path}")
            else:
                shutil.copy2(item_path, destination_path)
                print(f"📄 Copied file: {item_path} → {destination_path}")
    else:
        print(f"⏭ Skipping: {folder_name}")

print("✅ All contents merged into:", output_dir)
