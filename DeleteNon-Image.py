import os

from PIL import Image

# Root image dataset directory
ROOT_DIR = "gbif_images"

# Count stats
total_checked = 0
total_deleted = 0
valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

for root, _, files in os.walk(ROOT_DIR):
    for filename in files:
        file_path = os.path.join(root, filename)
        total_checked += 1

        # Optional: skip if extension looks good (but still check with PIL)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext not in valid_extensions:
            print(f"❌ Unusual extension: {file_path}")

        try:
            # Try opening the file as an image
            with Image.open(file_path) as img:
                img.verify()  # Check if it's a valid image
        except Exception as e:
            print(f"🗑️ Deleting non-image file: {file_path} ({e})")
            os.remove(file_path)
            total_deleted += 1

print(f"\n✅ Done. Checked {total_checked} files, deleted {total_deleted} invalid ones.")
