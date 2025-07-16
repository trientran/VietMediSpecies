import os

folder = '/Users/trien.tran/Downloads/dl2/cleaned_dataset2'
subfolders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

print(f"Total subfolders: {len(subfolders)}")
