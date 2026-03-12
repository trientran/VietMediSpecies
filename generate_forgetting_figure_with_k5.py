import json
import matplotlib.pyplot as plt
import numpy as np
import os

# =============================================================================
# CONFIGURATION - Update these paths to match your file locations
# =============================================================================

# K=2 experiments (two seeds for averaging)
SEED_42_K2_FILE = 'seed42_k2/paper1_curves_and_sequences.json'
SEED_123_K2_FILE = 'seed123_k2/paper1_curves_and_sequences.json'

# K=5 experiment (single seed)
SEED_42_K5_FILE = 'seed42_k5/paper1_curves_and_sequences.json'

# =============================================================================
# LOAD DATA FROM JSON FILES
# =============================================================================

def load_forgetting_data(filepath):
    """Load forgetting curves from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return {
        'naive': np.array(data['naive_forgets']),
        'replay': np.array(data['replay_forgets']),
        'lwf': np.array(data['lwf_forgets'])
    }

# =============================================================================
# MAIN PLOTTING FUNCTION - K=2 averaged + K=5
# =============================================================================

def plot_forgetting_curves_all(seed1_k2_file, seed2_k2_file, seed_k5_file, 
                                output_name='forgetting_comparison'):
    """
    Generate forgetting curves plot with:
    - K=2: averaged values with error bands (seeds 42 and 123)
    - K=5: single seed results (seed 42)
    
    Parameters:
    - seed1_k2_file: Path to first K=2 seed's JSON file
    - seed2_k2_file: Path to second K=2 seed's JSON file
    - seed_k5_file: Path to K=5 seed's JSON file
    - output_name: Base name for output files (without extension)
    """
    
    # Load data
    print(f"Loading K=2 Seed 1: {seed1_k2_file}")
    seed1_k2 = load_forgetting_data(seed1_k2_file)
    
    print(f"Loading K=2 Seed 2: {seed2_k2_file}")
    seed2_k2 = load_forgetting_data(seed2_k2_file)
    
    print(f"Loading K=5: {seed_k5_file}")
    seed_k5 = load_forgetting_data(seed_k5_file)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # X-axis: increment steps
    x = np.arange(len(seed1_k2['naive']))
    
    # Define colors for each strategy
    colors = {'naive': 'blue', 'replay': 'red', 'lwf': 'green'}
    markers_k2 = {'naive': 'o', 'replay': 's', 'lwf': '^'}
    markers_k5 = {'naive': 'D', 'replay': 'p', 'lwf': 'v'}
    
    labels = {'naive': 'Naïve', 'replay': 'Replay', 'lwf': 'LwF'}
    
    # Plot K=2 results (averaged with error bands)
    for strategy in ['naive', 'replay', 'lwf']:
        y1 = seed1_k2[strategy]
        y2 = seed2_k2[strategy]
        
        # Calculate mean and range
        y_mean = (y1 + y2) / 2
        y_min = np.minimum(y1, y2)
        y_max = np.maximum(y1, y2)
        
        # Plot mean line with markers (solid line for K=2)
        ax.plot(x, y_mean, f'-{markers_k2[strategy]}', color=colors[strategy], 
                linewidth=2, markersize=6, 
                label=f'{labels[strategy]} (K=2, avg)')
        
        # Plot shaded error band
        ax.fill_between(x, y_min, y_max, alpha=0.15, color=colors[strategy])
    
    # Plot K=5 results (single seed, dashed lines)
    for strategy in ['naive', 'replay', 'lwf']:
        y = seed_k5[strategy]
        
        # Plot with dashed line for K=5
        ax.plot(x, y, f'--{markers_k5[strategy]}', color=colors[strategy], 
                linewidth=2, markersize=5, alpha=0.7,
                label=f'{labels[strategy]} (K=5)')
    
    # Formatting
    ax.set_xlabel('Increment Step (0 = after base training)', fontsize=12)
    ax.set_ylabel('Forgetting (negative = improvement)', fontsize=12)
    ax.set_title('Forgetting Curves: Effect of Retraining Frequency\n'
                 'K=2 (solid, averaged across seeds) vs K=5 (dashed, 80% compute reduction)', 
                 fontsize=13)
    
    # Reference line at y=0
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Set axis limits
    all_k2 = np.concatenate([seed1_k2['naive'], seed1_k2['replay'], seed1_k2['lwf'],
                             seed2_k2['naive'], seed2_k2['replay'], seed2_k2['lwf']])
    all_k5 = np.concatenate([seed_k5['naive'], seed_k5['replay'], seed_k5['lwf']])
    y_min_limit = min(np.min(all_k2), np.min(all_k5)) - 0.02
    ax.set_ylim(y_min_limit, 0.03)
    ax.set_xlim(-0.5, len(x) - 0.5)
    
    # Legend - arrange in two columns
    ax.legend(loc='lower left', fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3)
    
    # Add note
    ax.text(0.98, 0.98, 'Shaded bands show range\nbetween seeds (K=2 only)',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            horizontalalignment='right', style='italic', color='gray')
    
    plt.tight_layout()
    
    # Save as PDF and PNG
    plt.savefig(f'{output_name}.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
    
    print(f"\nSaved: {output_name}.pdf")
    print(f"Saved: {output_name}.png")
    
    plt.show()
    
    # Print summary statistics
    print_summary_statistics(seed1_k2, seed2_k2, seed_k5)


def print_summary_statistics(seed1_k2, seed2_k2, seed_k5):
    """Print summary statistics for manuscript."""
    print("\n" + "="*70)
    print("SUMMARY STATISTICS FOR MANUSCRIPT")
    print("="*70)
    
    strategies = ['naive', 'replay', 'lwf']
    labels = {'naive': 'Naïve Fine-tuning', 'replay': 'Experience Replay', 'lwf': 'LwF'}
    
    print("\n--- K=2 Results (Averaged across seeds 42 and 123) ---")
    for strategy in strategies:
        y1 = seed1_k2[strategy]
        y2 = seed2_k2[strategy]
        y_mean = (y1 + y2) / 2
        
        print(f"\n{labels[strategy]}:")
        print(f"  Seed 42 final:  {y1[-1]*100:+.2f}%")
        print(f"  Seed 123 final: {y2[-1]*100:+.2f}%")
        print(f"  Average final:  {y_mean[-1]*100:+.2f}%")
        print(f"  Average mean:   {np.mean(y_mean)*100:+.2f}%")
    
    print("\n--- K=5 Results (Seed 42 only, 80% compute reduction) ---")
    for strategy in strategies:
        y = seed_k5[strategy]
        print(f"\n{labels[strategy]}:")
        print(f"  Final forgetting: {y[-1]*100:+.2f}%")
        print(f"  Mean forgetting:  {np.mean(y)*100:+.2f}%")
    
    print("\n" + "="*70)
    print("KEY FINDINGS:")
    print("="*70)
    
    # K=2 averages
    naive_k2_final = (seed1_k2['naive'][-1] + seed2_k2['naive'][-1]) / 2
    replay_k2_final = (seed1_k2['replay'][-1] + seed2_k2['replay'][-1]) / 2
    lwf_k2_final = (seed1_k2['lwf'][-1] + seed2_k2['lwf'][-1]) / 2
    
    print(f"\nK=2 Final Forgetting (averaged):")
    print(f"  Naïve:  {naive_k2_final*100:+.2f}%")
    print(f"  Replay: {replay_k2_final*100:+.2f}%")
    print(f"  LwF:    {lwf_k2_final*100:+.2f}%")
    
    print(f"\nK=5 Final Forgetting:")
    print(f"  Naïve:  {seed_k5['naive'][-1]*100:+.2f}%")
    print(f"  Replay: {seed_k5['replay'][-1]*100:+.2f}%")
    print(f"  LwF:    {seed_k5['lwf'][-1]*100:+.2f}%")
    
    print(f"\nAll values are negative = IMPROVEMENT (not forgetting)")


# =============================================================================
# ALTERNATIVE: Two-panel figure (K=2 and K=5 side by side)
# =============================================================================

def plot_two_panels(seed1_k2_file, seed2_k2_file, seed_k5_file, 
                    output_name='forgetting_comparison_panels'):
    """Generate a two-panel figure: K=2 (left) and K=5 (right)."""
    
    # Load data
    seed1_k2 = load_forgetting_data(seed1_k2_file)
    seed2_k2 = load_forgetting_data(seed2_k2_file)
    seed_k5 = load_forgetting_data(seed_k5_file)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    x = np.arange(len(seed1_k2['naive']))
    colors = {'naive': 'blue', 'replay': 'red', 'lwf': 'green'}
    markers = {'naive': 'o', 'replay': 's', 'lwf': '^'}
    labels = {'naive': 'Naïve', 'replay': 'Replay', 'lwf': 'LwF'}
    
    # Panel A: K=2 (averaged with error bands)
    ax = axes[0]
    for strategy in ['naive', 'replay', 'lwf']:
        y1 = seed1_k2[strategy]
        y2 = seed2_k2[strategy]
        y_mean = (y1 + y2) / 2
        y_min = np.minimum(y1, y2)
        y_max = np.maximum(y1, y2)
        
        ax.plot(x, y_mean, f'-{markers[strategy]}', color=colors[strategy], 
                linewidth=2, markersize=5, label=labels[strategy])
        ax.fill_between(x, y_min, y_max, alpha=0.2, color=colors[strategy])
    
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Increment Step', fontsize=11)
    ax.set_ylabel('Forgetting (negative = improvement)', fontsize=11)
    ax.set_title('(A) K=2: Retrain every 2nd increment\n(50% compute reduction, averaged across seeds)', fontsize=12)
    ax.set_ylim(-0.14, 0.02)
    ax.legend(loc='lower left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Panel B: K=5
    ax = axes[1]
    for strategy in ['naive', 'replay', 'lwf']:
        ax.plot(x, seed_k5[strategy], f'-{markers[strategy]}', color=colors[strategy], 
                linewidth=2, markersize=5, label=labels[strategy])
    
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Increment Step', fontsize=11)
    ax.set_ylabel('Forgetting (negative = improvement)', fontsize=11)
    ax.set_title('(B) K=5: Retrain every 5th increment\n(80% compute reduction)', fontsize=12)
    ax.set_ylim(-0.14, 0.02)
    ax.legend(loc='lower left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_name}.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_name}.pdf and .png")
    plt.show()


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    # Check if all JSON files exist
    files_exist = (os.path.exists(SEED_42_K2_FILE) and 
                   os.path.exists(SEED_123_K2_FILE) and 
                   os.path.exists(SEED_42_K5_FILE))
    
    if files_exist:
        print("="*60)
        print("Generating forgetting curves figure...")
        print("="*60)
        
        # Generate main figure (all on one plot)
        plot_forgetting_curves_all(SEED_42_K2_FILE, SEED_123_K2_FILE, SEED_42_K5_FILE,
                                   output_name='forgetting_comparison')
        
        # Optionally generate two-panel figure
        print("\n" + "="*60)
        print("Generating two-panel figure...")
        print("="*60)
        plot_two_panels(SEED_42_K2_FILE, SEED_123_K2_FILE, SEED_42_K5_FILE,
                        output_name='forgetting_comparison_panels')
        
    else:
        print("="*60)
        print("JSON files not found at specified paths!")
        print("="*60)
        print(f"\nExpected files:")
        print(f"  - {SEED_42_K2_FILE}")
        print(f"  - {SEED_123_K2_FILE}")
        print(f"  - {SEED_42_K5_FILE}")
        print(f"\nPlease update the file paths at the top of this script.")
        print(f"\nExample folder structure:")
        print(f"  your_project/")
        print(f"  ├── seed42_k2/")
        print(f"  │   └── paper1_curves_and_sequences.json")
        print(f"  ├── seed123_k2/")
        print(f"  │   └── paper1_curves_and_sequences.json")
        print(f"  ├── seed42_k5/")
        print(f"  │   └── paper1_curves_and_sequences.json")
        print(f"  └── generate_forgetting_figure.py")
