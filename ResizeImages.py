import os
from PIL import Image

# Folder to process
ROOT_DIR = "non_plantae_new"
MAX_DIM = 600  # Max width or height, depending on orientation

count_resized = 0
count_skipped = 0

for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(root, file)

        try:
            with Image.open(path) as img:
                width, height = img.size

                # Determine orientation and new size
                if width > height:
                    # Landscape → scale width to MAX_DIM
                    if width > MAX_DIM:
                        new_height = int((MAX_DIM / width) * height)
                        img = img.resize((MAX_DIM, new_height), Image.LANCZOS)
                    else:
                        count_skipped += 1
                        continue
                else:
                    # Portrait or square → scale height to MAX_DIM
                    if height > MAX_DIM:
                        new_width = int((MAX_DIM / height) * width)
                        img = img.resize((new_width, MAX_DIM), Image.LANCZOS)
                    else:
                        count_skipped += 1
                        continue

                # Overwrite original file
                img.save(path)
                count_resized += 1

        except Exception as e:
            print(f"⚠️ Failed to resize {path}: {e}")

print(f"\n✅ Resizing complete.")
print(f"🖼️ Resized: {count_resized}")
print(f"⏭️ Skipped (already small): {count_skipped}")
