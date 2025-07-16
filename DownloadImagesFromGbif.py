import asyncio
import os
from urllib.parse import urlparse

import aiohttp
import pandas as pd

# Configuration
INPUT_CSV = "species_keys.csv"  # CSV file with column 'speciesKey'
OUTPUT_DIR = "fungi_bacteria_chromita_only"
MAX_IMAGES = 130
CONCURRENT_SPECIES = 1
CONCURRENT_DOWNLOADS = 20
TIMEOUT_SECONDS = 60
RETRIES = 3

# Custom User-Agent header (mimics Chrome on macOS)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://quod.lib.umich.edu/"
}


# Prepare output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load species keys
df = pd.read_csv(INPUT_CSV)
if "speciesKey" not in df.columns:
    raise ValueError("CSV must contain a column named 'speciesKey'.")
species_keys = df['speciesKey'].tolist()


async def fetch_occurrences(session, species_key):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "taxonKey": species_key,
        "mediaType": "StillImage",
        "limit": MAX_IMAGES
    }
    try:
        async with session.get(url, params=params, timeout=TIMEOUT_SECONDS) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("results", [])
    except Exception as e:
        print(f"❌ Failed to fetch metadata for speciesKey {species_key}: {e}")
        return []


async def download_image(session, url, dest_path, retries=RETRIES):
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=TIMEOUT_SECONDS) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    with open(dest_path, "wb") as f:
                        f.write(content)
                    return
                else:
                    print(f"⚠️ Attempt {attempt + 1}: status {resp.status} on {url}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"⚠️ Attempt {attempt + 1}: error fetching {url}: {e}")
        await asyncio.sleep(1)
    print(f"❌ Gave up downloading {url} after {retries} attempts")


async def process_species(session, species_key, semaphore):
    async with semaphore:
        print(f"🔍 Processing speciesKey: {species_key}")
        species_dir = os.path.join(OUTPUT_DIR, str(species_key))
        os.makedirs(species_dir, exist_ok=True)

        occurrences = await fetch_occurrences(session, species_key)
        tasks = []
        count = 0

        for occ in occurrences:
            media_items = occ.get("media", [])
            for media in media_items:
                img_url = media.get("identifier")
                if not img_url:
                    continue

                parsed = urlparse(img_url)
                filename = os.path.basename(parsed.path).lower()

                # ✅ Only download images named exactly "original.jpg" or "original.jpeg"
                if filename not in {"original.jpg", "original.jpeg"}:
                    continue

                filename = f"original_{count}.jpg" if filename.endswith(".jpg") else f"original_{count}.jpeg"
                dest_path = os.path.join(species_dir, filename)
                tasks.append(download_image(session, img_url, dest_path))
                count += 1

                if count >= MAX_IMAGES:
                    break
            if count >= MAX_IMAGES:
                break

        await asyncio.gather(*tasks)
        print(f"✅ Finished {species_key}: {count} images")


async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_DOWNLOADS)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    semaphore = asyncio.Semaphore(CONCURRENT_SPECIES)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=HEADERS) as session:
        tasks = [process_species(session, key, semaphore) for key in species_keys]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
