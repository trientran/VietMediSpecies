import asyncio
import os
from urllib.parse import urlparse
from io import BytesIO

import aiohttp
import pandas as pd
from PIL import Image, ImageOps

# =======================
# Configuration
# =======================
INPUT_CSV = "csv/4799_species_keys.csv"        # CSV file with column 'speciesKey'
OUTPUT_DIR = "all_viet_species"
MAX_IMAGES = 130
CONCURRENT_SPECIES = 1
CONCURRENT_DOWNLOADS = 20
TIMEOUT_SECONDS = 60
RETRIES = 3

# Image resize config
MAX_DIM = 600  # Max width or height, depending on orientation

# Custom headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://quod.lib.umich.edu/"
}

# =======================
# Setup
# =======================
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load species keys
df = pd.read_csv(INPUT_CSV)
if "speciesKey" not in df.columns:
    raise ValueError("CSV must contain a column named 'speciesKey'.")
species_keys = df['speciesKey'].tolist()

# =======================
# Helpers
# =======================
def _resize_bytes_to_max_dim(content: bytes, max_dim: int, out_ext: str) -> bytes:
    """
    Open image bytes, EXIF-correct them, resize to max_dim on the longer edge
    if needed, and return encoded bytes (format derived from out_ext).
    """
    with Image.open(BytesIO(content)) as img:
        # Normalize orientation using EXIF
        img = ImageOps.exif_transpose(img)
        width, height = img.size

        # Decide target size
        if width >= height:
            # Landscape / square treated as width-major
            if width > max_dim:
                new_w = max_dim
                new_h = int((max_dim / width) * height)
                img = img.resize((new_w, new_h), Image.LANCZOS)
            # else: already small; keep as-is
        else:
            # Portrait
            if height > max_dim:
                new_h = max_dim
                new_w = int((max_dim / height) * width)
                img = img.resize((new_w, new_h), Image.LANCZOS)

        # Choose format based on extension
        ext = out_ext.lower()
        if ext in (".jpg", ".jpeg"):
            fmt = "JPEG"
            save_kwargs = dict(format=fmt, quality=85, optimize=True, progressive=True)
        elif ext == ".png":
            fmt = "PNG"
            save_kwargs = dict(format=fmt, optimize=True)
        else:
            # Fallback to JPEG
            fmt = "JPEG"
            save_kwargs = dict(format=fmt, quality=85, optimize=True, progressive=True)

        out = BytesIO()
        # Convert mode if needed for JPEG
        if fmt == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(out, **save_kwargs)
        return out.getvalue()

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

async def download_and_resize(session, url, dest_path, retries=RETRIES):
    """
    Download image bytes with retries, resize in-memory, then save resized bytes to dest_path.
    No large original is stored on disk.
    """
    # Decide output extension from destination filename
    _, ext = os.path.splitext(dest_path)
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=TIMEOUT_SECONDS) as resp:
                if resp.status != 200:
                    print(f"⚠️ Attempt {attempt + 1}: status {resp.status} on {url}")
                else:
                    content = await resp.read()
                    # Offload CPU-bound resize to a thread
                    resized = await asyncio.to_thread(
                        _resize_bytes_to_max_dim, content, MAX_DIM, ext
                    )
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(dest_path, "wb") as f:
                        f.write(resized)
                    return
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

                # Keep extension consistent with source
                if filename.endswith(".jpg"):
                    filename = f"original_{count}.jpg"
                else:
                    filename = f"original_{count}.jpeg"

                dest_path = os.path.join(species_dir, filename)
                tasks.append(download_and_resize(session, img_url, dest_path))
                count += 1

                if count >= MAX_IMAGES:
                    break
            if count >= MAX_IMAGES:
                break

        if tasks:
            await asyncio.gather(*tasks)

        print(f"✅ Finished {species_key}: {count} images (downloaded + resized)")

async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_DOWNLOADS)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    semaphore = asyncio.Semaphore(CONCURRENT_SPECIES)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=HEADERS) as session:
        tasks = [process_species(session, key, semaphore) for key in species_keys]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
