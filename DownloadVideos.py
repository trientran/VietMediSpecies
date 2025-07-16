import requests

# Base URL
base_url = "https://cloud1.toomva.com/825kmp111/phimbo/once-upon-a-time/Once-upon-a-time-S01E{:02d}.mp4"

# Folder to save videos (make sure the folder exists or create it)
save_path = "./once_upon_a_time/"

# Ensure directory exists
import os

os.makedirs(save_path, exist_ok=True)

# Download episodes
for episode in range(10, 23):  # 1 to 22 inclusive
    url = base_url.format(episode)
    filename = f"{save_path}Once-upon-a-time-S01E{episode:02d}.mp4"
    print(f"Downloading {url} -> {filename}")

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Episode {episode:02d} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download Episode {episode:02d}: {e}")
