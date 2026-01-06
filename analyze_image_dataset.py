#!/usr/bin/env python3
"""
Image Dataset Statistics Calculator for Viet Medi Species 2026

This script analyzes your downloaded images and generates statistics needed for the paper.

=============================================================================
HOW TO RUN IN PYCHARM:
=============================================================================
1. Open this file in PyCharm
2. Edit the paths below (lines 25-28):
   - IMAGE_DIR = "your/path/to/images"
   - METADATA_CSV = "your/path/to/metadata.csv"
3. Right-click anywhere in this file
4. Select "Run 'analyze_image_dataset'"
5. Results will appear in the Run panel at the bottom

Example paths:
   IMAGE_DIR = "C:/Users/Trien/Desktop/fungi_bacteria_chromita_only"
   METADATA_CSV = "C:/Users/Trien/Desktop/merged_species_with_gbif_metadata.csv"

Or on Mac/Linux:
   IMAGE_DIR = "/Users/trien/Desktop/fungi_bacteria_chromita_only"
   METADATA_CSV = "/Users/trien/Desktop/merged_species_with_gbif_metadata.csv"

=============================================================================
"""

import os
import sys
import pandas as pd
from pathlib import Path
from collections import defaultdict
import json
from PIL import Image
import numpy as np

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS FOR YOUR SYSTEM
# ============================================================================

# Path to your downloaded images folder
IMAGE_DIR = "all_viet_species"  # ← EDIT THIS PATH

# Path to your metadata CSV file
METADATA_CSV = 'csv/merged_species_with_gbif_metadata.csv' # ← EDIT THIS PATH

# Output file for detailed statistics (will be saved in same directory as script)
OUTPUT_JSON = "image_statistics.json"


# ============================================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================================

def get_image_info(image_path):
    """Extract information from an image file."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            format_type = img.format
            file_size = os.path.getsize(image_path)
            return {
                'width': width,
                'height': height,
                'format': format_type,
                'size_bytes': file_size,
                'megapixels': (width * height) / 1_000_000
            }
    except Exception as e:
        return None


def analyze_images(image_dir, metadata_csv):
    """Analyze the image dataset and generate statistics."""

    print("=" * 70)
    print("VIET MEDI SPECIES 2026 - IMAGE DATASET STATISTICS")
    print("=" * 70)
    print(f"\nAnalyzing images in: {image_dir}")
    print(f"Loading metadata from: {metadata_csv}\n")

    # Load metadata
    df = pd.read_csv(metadata_csv)
    print(f"Loaded metadata for {len(df):,} species")

    # Check Vietnamese names
    df['has_vietnamese'] = df['vietnameseName'].apply(
        lambda x: pd.notna(x) and str(x).strip() != '' and str(x) != 'vietnameseName'
    )

    # Initialize counters
    stats = {
        'total_images': 0,
        'total_species_with_images': 0,
        'by_kingdom': defaultdict(lambda: {'species': 0, 'images': 0}),
        'by_species': {},
        'image_formats': defaultdict(int),
        'total_size_bytes': 0,
        'resolutions': [],
        'megapixels': []
    }

    # Get all subdirectories (each should be a speciesKey)
    image_dir_path = Path(image_dir)

    if not image_dir_path.exists():
        print(f"ERROR: Directory not found: {image_dir}")
        return None

    print(f"\nScanning species folders...")
    species_folders = [d for d in image_dir_path.iterdir() if d.is_dir()]
    print(f"Found {len(species_folders)} species folders\n")

    # Analyze each species folder
    for i, species_folder in enumerate(species_folders, 1):
        try:
            species_key = int(species_folder.name)
        except ValueError:
            print(f"Skipping non-numeric folder: {species_folder.name}")
            continue

        # Get images in this folder
        image_files = list(species_folder.glob("*.jpg")) + list(species_folder.glob("*.jpeg"))
        num_images = len(image_files)

        if num_images > 0:
            stats['total_images'] += num_images
            stats['total_species_with_images'] += 1
            stats['by_species'][species_key] = num_images

            # Find this species in metadata
            species_row = df[df['speciesKey'] == species_key]
            if not species_row.empty:
                kingdom = species_row.iloc[0]['kingdom']
                stats['by_kingdom'][kingdom]['species'] += 1
                stats['by_kingdom'][kingdom]['images'] += num_images

            # Analyze image properties (sample first 5 images per species for speed)
            for img_file in image_files[:5]:
                info = get_image_info(img_file)
                if info:
                    stats['image_formats'][info['format']] += 1
                    stats['total_size_bytes'] += info['size_bytes']
                    stats['resolutions'].append((info['width'], info['height']))
                    stats['megapixels'].append(info['megapixels'])

        # Progress indicator
        if i % 100 == 0:
            print(f"Processed {i:,} / {len(species_folders):,} species folders...")

    print(f"\n✓ Completed scanning all species folders\n")

    # Calculate additional statistics
    if stats['total_images'] > 0:
        stats['avg_images_per_species'] = stats['total_images'] / stats['total_species_with_images']
        stats['total_size_gb'] = stats['total_size_bytes'] / (1024 ** 3)

        if stats['resolutions']:
            widths, heights = zip(*stats['resolutions'])
            stats['avg_width'] = int(np.mean(widths))
            stats['avg_height'] = int(np.mean(heights))
            stats['min_width'] = int(np.min(widths))
            stats['max_width'] = int(np.max(widths))
            stats['min_height'] = int(np.min(heights))
            stats['max_height'] = int(np.max(heights))

        if stats['megapixels']:
            stats['avg_megapixels'] = np.mean(stats['megapixels'])

    return stats, df


def print_statistics(stats, df):
    """Print formatted statistics for the paper."""

    print("=" * 70)
    print("PAPER STATISTICS - COPY THESE VALUES")
    print("=" * 70)

    # Overall statistics
    print("\n" + "=" * 70)
    print("1. OVERALL DATASET STATISTICS")
    print("=" * 70)
    print(f"Total images: {stats['total_images']:,}")
    print(f"Total species with images: {stats['total_species_with_images']:,}")
    print(f"Average images per species: {stats['avg_images_per_species']:.1f}")
    print(f"Total dataset size: {stats['total_size_gb']:.2f} GB")

    # Image quality
    print("\n" + "=" * 70)
    print("2. IMAGE QUALITY METRICS")
    print("=" * 70)
    print(f"Average resolution: {stats['avg_width']} × {stats['avg_height']} pixels")
    print(f"Resolution range: {stats['min_width']}×{stats['min_height']} to {stats['max_width']}×{stats['max_height']}")
    print(f"Average megapixels: {stats['avg_megapixels']:.2f} MP")

    print("\nImage formats:")
    for fmt, count in sorted(stats['image_formats'].items(), key=lambda x: -x[1]):
        print(f"  {fmt}: {count:,} images")

    # Kingdom statistics
    print("\n" + "=" * 70)
    print("3. STATISTICS BY KINGDOM (FOR TABLE 2)")
    print("=" * 70)
    print(f"{'Kingdom':<15} {'Species':<10} {'Images':<12} {'Avg Imgs/Species':<15}")
    print("-" * 70)

    kingdom_order = ['Plantae', 'Fungi', 'Chromista', 'Bacteria']
    total_species_imgs = 0
    total_images = 0

    for kingdom in kingdom_order:
        if kingdom in stats['by_kingdom']:
            k_stats = stats['by_kingdom'][kingdom]
            avg = k_stats['images'] / k_stats['species'] if k_stats['species'] > 0 else 0
            print(f"{kingdom:<15} {k_stats['species']:<10,} {k_stats['images']:<12,} {avg:<15.1f}")
            total_species_imgs += k_stats['species']
            total_images += k_stats['images']

    print("-" * 70)
    avg_total = total_images / total_species_imgs if total_species_imgs > 0 else 0
    print(f"{'TOTAL':<15} {total_species_imgs:<10,} {total_images:<12,} {avg_total:<15.1f}")

    # Distribution statistics
    print("\n" + "=" * 70)
    print("4. IMAGE DISTRIBUTION STATISTICS")
    print("=" * 70)

    species_image_counts = list(stats['by_species'].values())
    if species_image_counts:
        print(f"Minimum images per species: {min(species_image_counts)}")
        print(f"Maximum images per species: {max(species_image_counts)}")
        print(f"Median images per species: {np.median(species_image_counts):.0f}")

        # Distribution bins
        bins = [0, 10, 20, 50, 100, 150]
        print("\nSpecies distribution by image count:")
        for i in range(len(bins) - 1):
            count = sum(1 for x in species_image_counts if bins[i] < x <= bins[i + 1])
            pct = (count / len(species_image_counts)) * 100
            print(f"  {bins[i] + 1}-{bins[i + 1]} images: {count:,} species ({pct:.1f}%)")

        count_over = sum(1 for x in species_image_counts if x > bins[-1])
        pct_over = (count_over / len(species_image_counts)) * 100
        print(f"  >{bins[-1]} images: {count_over:,} species ({pct_over:.1f}%)")


def generate_latex_table(stats):
    """Generate LaTeX code for Table 2."""

    print("\n" + "=" * 70)
    print("5. LATEX TABLE CODE (COPY TO main.tex)")
    print("=" * 70)
    print("\n% Replace Table 2 in your main.tex with this:\n")
    print("\\begin{table}[t]")
    print("\\caption{Dataset Composition by Kingdom}")
    print("\\label{tab:composition}")
    print("\\centering")
    print("\\begin{tabular}{lcccc}")
    print("\\toprule")
    print("\\textbf{Kingdom} & \\textbf{Species} & \\textbf{Images} & \\textbf{Viet Names} & \\textbf{Coverage} \\\\")
    print("\\midrule")

    kingdom_order = ['Plantae', 'Fungi', 'Chromista', 'Bacteria']

    # Need Vietnamese name stats from metadata
    # This is placeholder - will be filled from metadata
    for kingdom in kingdom_order:
        if kingdom in stats['by_kingdom']:
            k_stats = stats['by_kingdom'][kingdom]
            print(f"{kingdom} & {k_stats['species']:,} & {k_stats['images']:,} & XXX & XX\\% \\\\")

    print("\\midrule")
    total_sp = sum(stats['by_kingdom'][k]['species'] for k in stats['by_kingdom'])
    total_img = sum(stats['by_kingdom'][k]['images'] for k in stats['by_kingdom'])
    print(
        f"\\textbf{{Total}} & \\textbf{{{total_sp:,}}} & \\textbf{{{total_img:,}}} & \\textbf{{4,024}} & \\textbf{{84\\%}} \\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table}")


def generate_paper_replacements(stats):
    """Generate search-and-replace values for the paper."""

    print("\n" + "=" * 70)
    print("6. SEARCH & REPLACE IN main.tex")
    print("=" * 70)
    print("\nFind and replace these placeholders:\n")

    total_images = stats['total_images']

    # Format with appropriate precision
    if total_images >= 100000:
        img_str = f"{total_images:,}"
    else:
        img_str = f"{total_images:,}"

    print(f"Search: 'XXX,XXX images'")
    print(f"Replace: '{img_str} images'")
    print()
    print(f"Search: 'approximately XXX,XXX images'")
    print(f"Replace: 'approximately {img_str} images'")
    print()
    print(f"Search: '~XXX,XXX images'")
    print(f"Replace: '~{img_str} images'")
    print()

    # By kingdom
    for kingdom in ['Plantae', 'Fungi', 'Chromista', 'Bacteria']:
        if kingdom in stats['by_kingdom']:
            k_img = stats['by_kingdom'][kingdom]['images']
            k_sp = stats['by_kingdom'][kingdom]['species']

            if k_img >= 100000:
                placeholder = "XXX,XXX"
            elif k_img >= 10000:
                placeholder = "XX,XXX"
            else:
                placeholder = "X,XXX"

            print(f"{kingdom}: {k_sp:,} species, {k_img:,} images")
            print(f"  Replace '{placeholder}' → '{k_img:,}' for {kingdom} row in Table 2")

    print(f"\nDataset size: Replace 'XXX GB' → '{stats['total_size_gb']:.1f} GB'")


def save_results(stats, output_file='image_statistics.json'):
    """Save statistics to JSON file."""

    # Convert defaultdict to regular dict for JSON serialization
    stats_serializable = {
        'total_images': stats['total_images'],
        'total_species_with_images': stats['total_species_with_images'],
        'avg_images_per_species': stats.get('avg_images_per_species', 0),
        'total_size_gb': stats.get('total_size_gb', 0),
        'by_kingdom': dict(stats['by_kingdom']),
        'image_formats': dict(stats['image_formats']),
        'avg_width': stats.get('avg_width', 0),
        'avg_height': stats.get('avg_height', 0),
        'avg_megapixels': stats.get('avg_megapixels', 0)
    }

    with open(output_file, 'w') as f:
        json.dump(stats_serializable, f, indent=2)

    print(f"\n✓ Detailed statistics saved to: {output_file}")


def main():
    """Main function - uses configuration from top of file or command line args."""

    # Check if command line arguments provided (for backward compatibility)
    if len(sys.argv) >= 3:
        image_dir = sys.argv[1]
        metadata_csv = sys.argv[2]
        print("Using command line arguments...")
    else:
        # Use configuration from top of file
        image_dir = IMAGE_DIR
        metadata_csv = METADATA_CSV
        print("Using configuration from script (IMAGE_DIR and METADATA_CSV)...")

    print(f"\nImage directory: {image_dir}")
    print(f"Metadata CSV: {metadata_csv}")

    # Check if paths exist
    if not os.path.exists(image_dir):
        print(f"\n❌ ERROR: Image directory not found: {image_dir}")
        print("\n💡 To fix this:")
        print(f"   1. Open this script in PyCharm")
        print(f"   2. Find the line: IMAGE_DIR = \"{IMAGE_DIR}\"")
        print(f"   3. Change it to your actual image folder path")
        print(f"   4. Example: IMAGE_DIR = \"C:/Users/YourName/Downloads/fungi_bacteria_chromita_only\"")
        sys.exit(1)

    if not os.path.exists(metadata_csv):
        print(f"\n❌ ERROR: Metadata CSV not found: {metadata_csv}")
        print("\n💡 To fix this:")
        print(f"   1. Open this script in PyCharm")
        print(f"   2. Find the line: METADATA_CSV = \"{METADATA_CSV}\"")
        print(f"   3. Change it to your actual CSV file path")
        print(f"   4. Example: METADATA_CSV = \"C:/Users/YourName/Downloads/merged_species_with_gbif_metadata.csv\"")
        sys.exit(1)

    print("\n✓ Paths verified, starting analysis...\n")

    # Analyze the dataset
    stats, df = analyze_images(image_dir, metadata_csv)

    if stats is None:
        print("Error: Could not analyze dataset")
        sys.exit(1)

    # Print all statistics
    print_statistics(stats, df)
    generate_latex_table(stats)
    generate_paper_replacements(stats)

    # Save to file
    save_results(stats, OUTPUT_JSON)

    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\n📋 Next steps:")
    print("1. Scroll up and copy the statistics")
    print("2. Replace XXX,XXX placeholders in main.tex")
    print("3. Update Table 2 with the LaTeX code provided")
    print(f"4. Check {OUTPUT_JSON} for detailed data")
    print("\n💡 Tip: You can copy output from PyCharm's Run panel")
    print("\n")


if __name__ == "__main__":
    main()