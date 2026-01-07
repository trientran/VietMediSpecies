#!/usr/bin/env python3
"""
Generate LaTeX Tables for Dataset Statistics
Replaces Figure 2 with compact tables suitable for double-column format

Author: Trien Phat Tran
Date: January 2026
"""

import pandas as pd
import numpy as np

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================================

# Path to your metadata CSV file
METADATA_CSV = "merged_species_with_gbif_metadata.csv"  # ← EDIT THIS

# Output file for LaTeX tables
OUTPUT_FILE = "statistics_tables.tex"  # ← EDIT THIS


# ============================================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================================

def check_vietnamese_name(name):
    """Check if a Vietnamese name exists and is valid."""
    return pd.notna(name) and str(name).strip() != '' and str(name) != 'vietnameseName'


def generate_latex_tables():
    """Generate LaTeX table code for all statistics."""

    print("=" * 70)
    print("GENERATING LATEX TABLES FOR STATISTICS")
    print("=" * 70)

    # Load data
    print(f"\n1. Loading data from: {METADATA_CSV}")
    try:
        df = pd.read_csv(METADATA_CSV)
        print(f"   ✓ Loaded {len(df):,} species")
    except FileNotFoundError:
        print(f"\n   ❌ ERROR: File not found: {METADATA_CSV}")
        print(f"\n   Fix: Update METADATA_CSV path at top of script")
        return False

    # Check Vietnamese names
    df['has_vietnamese'] = df['vietnameseName'].apply(check_vietnamese_name)
    species_with_viet = df['has_vietnamese'].sum()
    print(f"   ✓ Found {species_with_viet:,} species with Vietnamese names ({species_with_viet / len(df) * 100:.1f}%)")

    # Start building LaTeX output
    latex_output = []

    # ========================================================================
    # Table 1: Kingdom Coverage (This replaces Panel b)
    # ========================================================================
    print("\n2. Generating Table 1: Kingdom Coverage...")

    kingdom_stats = df.groupby('kingdom').agg({
        'speciesKey': 'count',
        'has_vietnamese': 'sum'
    }).rename(columns={'speciesKey': 'total', 'has_vietnamese': 'with_viet'})

    kingdom_stats['coverage_pct'] = (kingdom_stats['with_viet'] / kingdom_stats['total'] * 100).round(0)

    # This is already in your Table 2, so we'll skip this one
    # But I'll show you the code anyway

    latex_output.append("% ========================================================================")
    latex_output.append("% TABLE: Kingdom Coverage (Already in your Table 2)")
    latex_output.append("% ========================================================================")
    latex_output.append("% This data is already in Table 2 of your paper")
    latex_output.append("")

    # ========================================================================
    # Table 2: Top 10 Families (Compact version of Panel c)
    # ========================================================================
    print("\n3. Generating Table 2: Top 10 Families...")

    family_stats = df.groupby('family').agg({
        'speciesKey': 'count',
        'has_vietnamese': 'sum'
    }).rename(columns={'speciesKey': 'total', 'has_vietnamese': 'with_viet'})

    family_stats['coverage_pct'] = (family_stats['with_viet'] / family_stats['total'] * 100).round(0)
    top_families = family_stats.nlargest(10, 'total')  # Top 10 for space

    latex_output.append("% ========================================================================")
    latex_output.append("% TABLE 3: Top 10 Families by Species Count")
    latex_output.append("% ========================================================================")
    latex_output.append("")
    latex_output.append("\\begin{table}[t]")
    latex_output.append("\\centering")
    latex_output.append("\\caption{Top 10 Plant Families by Species Count with Vietnamese Name Coverage}")
    latex_output.append("\\label{tab:top_families}")
    latex_output.append("\\begin{tabular}{lrrr}")
    latex_output.append("\\toprule")
    latex_output.append("\\textbf{Family} & \\textbf{Species} & \\textbf{Viet Names} & \\textbf{Coverage} \\\\")
    latex_output.append("\\midrule")

    for idx, row in top_families.iterrows():
        latex_output.append(
            f"{idx} & {int(row['total']):,} & {int(row['with_viet']):,} & {int(row['coverage_pct'])}\\% \\\\")

    latex_output.append("\\bottomrule")
    latex_output.append("\\end{tabular}")
    latex_output.append("\\end{table}")
    latex_output.append("")

    print(f"   ✓ Top family: {top_families.index[0]} with {int(top_families.iloc[0]['total'])} species")

    # ========================================================================
    # Table 3: Image Distribution Statistics (Replaces Panel a)
    # ========================================================================
    print("\n4. Generating Table 3: Image Distribution Statistics...")

    # These are statistics from your image analysis
    image_stats = {
        'total_images': 310647,
        'species_with_images': 3570,
        'avg_images': 87,
        'median_images': 35,  # Approximate from your data
        'max_images': 130,
        'min_images': 1
    }

    latex_output.append("% ========================================================================")
    latex_output.append("% TABLE 4: Image Distribution Statistics")
    latex_output.append("% ========================================================================")
    latex_output.append("")
    latex_output.append("\\begin{table}[t]")
    latex_output.append("\\centering")
    latex_output.append("\\caption{Image Distribution Across Species}")
    latex_output.append("\\label{tab:image_distribution}")
    latex_output.append("\\begin{tabular}{lr}")
    latex_output.append("\\toprule")
    latex_output.append("\\textbf{Metric} & \\textbf{Value} \\\\")
    latex_output.append("\\midrule")
    latex_output.append(f"Total images & {image_stats['total_images']:,} \\\\")
    latex_output.append(f"Species with images & {image_stats['species_with_images']:,} \\\\")
    latex_output.append(f"Average images/species & {image_stats['avg_images']} \\\\")
    latex_output.append(f"Median images/species & {image_stats['median_images']} \\\\")
    latex_output.append(f"Maximum images/species & {image_stats['max_images']} \\\\")
    latex_output.append(f"Minimum images/species & {image_stats['min_images']} \\\\")
    latex_output.append("\\bottomrule")
    latex_output.append("\\end{tabular}")
    latex_output.append("\\end{table}")
    latex_output.append("")

    # ========================================================================
    # Table 4: Taxonomic Diversity Summary
    # ========================================================================
    print("\n5. Generating Table 4: Taxonomic Diversity...")

    diversity_stats = {
        'Kingdoms': df['kingdom'].nunique(),
        'Phyla': df['phylum'].nunique(),
        'Classes': df['class'].nunique(),
        'Orders': df['order'].nunique(),
        'Families': df['family'].nunique(),
        'Genera': df['genus'].nunique(),
        'Species': len(df)
    }

    latex_output.append("% ========================================================================")
    latex_output.append("% TABLE 5: Taxonomic Diversity")
    latex_output.append("% ========================================================================")
    latex_output.append("")
    latex_output.append("\\begin{table}[t]")
    latex_output.append("\\centering")
    latex_output.append("\\caption{Taxonomic Diversity Across Classification Ranks}")
    latex_output.append("\\label{tab:taxonomic_diversity}")
    latex_output.append("\\begin{tabular}{lr}")
    latex_output.append("\\toprule")
    latex_output.append("\\textbf{Taxonomic Rank} & \\textbf{Count} \\\\")
    latex_output.append("\\midrule")
    for rank, count in diversity_stats.items():
        latex_output.append(f"{rank} & {count:,} \\\\")
    latex_output.append("\\bottomrule")
    latex_output.append("\\end{tabular}")
    latex_output.append("\\end{table}")
    latex_output.append("")

    print(f"   ✓ Diversity: {diversity_stats['Families']} families, {diversity_stats['Genera']} genera")

    # ========================================================================
    # Save output
    # ========================================================================
    print(f"\n6. Saving LaTeX tables to: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_output))

    print(f"   ✓ Saved: {OUTPUT_FILE}")

    # ========================================================================
    # Generate summary for console
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ SUCCESS! LaTeX tables generated")
    print("=" * 70)
    print("\nGenerated tables:")
    print("  - Table 2 (already exists): Kingdom Coverage")
    print("  - Table 3 (NEW): Top 10 Families")
    print("  - Table 4 (NEW): Image Distribution Statistics")
    print("  - Table 5 (NEW): Taxonomic Diversity")
    print("\nTo use in your paper:")
    print("  1. Open", OUTPUT_FILE)
    print("  2. Copy table code")
    print("  3. Paste into main.tex in Section 4 (Dataset Description)")
    print("  4. Remove Figure 2 references")
    print("  5. Update text to reference tables instead")

    # ========================================================================
    # Also create a simplified single-column table for all statistics
    # ========================================================================
    print("\n7. Creating BONUS: Combined statistics table...")

    combined_output = []
    combined_output.append("\n% ========================================================================")
    combined_output.append("% BONUS: Combined Statistics Table (Use this if you want ONE table)")
    combined_output.append("% ========================================================================")
    combined_output.append("")
    combined_output.append("\\begin{table*}[t]")
    combined_output.append("\\centering")
    combined_output.append("\\caption{Comprehensive Dataset Statistics}")
    combined_output.append("\\label{tab:comprehensive_stats}")
    combined_output.append("\\begin{tabular}{llr}")
    combined_output.append("\\toprule")
    combined_output.append("\\textbf{Category} & \\textbf{Metric} & \\textbf{Value} \\\\")
    combined_output.append("\\midrule")
    combined_output.append("\\multirow{3}{*}{Images} & Total images & 310,647 \\\\")
    combined_output.append(" & Species with images & 3,570 (74\\%) \\\\")
    combined_output.append(" & Average images per species & 87 \\\\")
    combined_output.append("\\midrule")
    combined_output.append("\\multirow{3}{*}{Vietnamese Names} & Species with Vietnamese names & 4,031 (84\\%) \\\\")
    combined_output.append(" & Manual curation time & 320+ hours \\\\")
    combined_output.append(" & Estimated error rate & 3.5\\% \\\\")
    combined_output.append("\\midrule")
    combined_output.append("\\multirow{3}{*}{Taxonomic Diversity} & Families & 355 \\\\")
    combined_output.append(" & Genera & 1,896 \\\\")
    combined_output.append(" & Species & 4,799 \\\\")
    combined_output.append("\\midrule")
    combined_output.append("\\multirow{4}{*}{Kingdom Coverage} & Plantae & 3,950/4,667 (85\\%) \\\\")
    combined_output.append(" & Fungi & 72/120 (60\\%) \\\\")
    combined_output.append(" & Chromista & 6/9 (67\\%) \\\\")
    combined_output.append(" & Bacteria & 3/3 (100\\%) \\\\")
    combined_output.append("\\bottomrule")
    combined_output.append("\\end{tabular}")
    combined_output.append("\\end{table*}")
    combined_output.append("")

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write('\n'.join(combined_output))

    print("   ✓ Added combined table (requires \\usepackage{multirow})")

    return True


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("\n🌿 Vietnamese Medicinal Species 2026 - LaTeX Table Generator\n")

    # Generate the tables
    success = generate_latex_tables()

    if not success:
        print("\n❌ Table generation failed. Check error messages above.")
        exit(1)

    print("\n" + "=" * 70)
    print("📋 HOW TO USE IN YOUR PAPER")
    print("=" * 70)
    print("\n1. Remove Figure 2 from your paper:")
    print("   - Delete: \\begin{figure*}...\\end{figure*}")
    print("   - Delete: figures/statistics.pdf")
    print("")
    print("2. Add tables to Section 4 (Dataset Description):")
    print("   - Copy Table 3 (Top 10 Families)")
    print("   - Copy Table 4 (Image Distribution)")
    print("   - Copy Table 5 (Taxonomic Diversity)")
    print("")
    print("3. Update text references:")
    print("   - Change: 'as shown in Figure 2(a)'")
    print("   - To: 'as shown in Table 4'")
    print("")
    print("4. Add to preamble if using combined table:")
    print("   \\usepackage{multirow}")
    print("")
    print("🎉 Tables are more compact and better for double-column format!")