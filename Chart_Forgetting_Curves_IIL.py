import json
import matplotlib.pyplot as plt
import numpy as np

# Load data directly from JSON file
with open('paper1_curves_and_sequences.json', 'r') as f:
    data = json.load(f)

# Extract forgetting curves
naive_forgets = data['naive_forgets']
replay_forgets = data['replay_forgets']
lwf_forgets = data['lwf_forgets']

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(naive_forgets))

ax.plot(x, naive_forgets, 'b-o', linewidth=2, markersize=6, label='Naïve Fine-tuning')
ax.plot(x, replay_forgets, 'r-s', linewidth=2, markersize=6, label='Experience Replay')
ax.plot(x, lwf_forgets, 'g-^', linewidth=2, markersize=6, label='LwF')

ax.set_xlabel('Increment Step (0 = after base training)', fontsize=12)
ax.set_ylabel('Forgetting (drop in base-eval accuracy)', fontsize=12)
ax.set_title('Forgetting Curves: Comparison of Continual Learning Strategies\n(Periodic Retraining with K=2)', fontsize=14)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_ylim(-0.12, 0.02)
ax.set_xlim(-0.5, len(naive_forgets) - 0.5)

ax.legend(loc='lower left', fontsize=11)
ax.grid(True, alpha=0.3)

# Add annotations for final values
ax.annotate(f'Final: {naive_forgets[-1]*100:.2f}%',
            xy=(len(naive_forgets)-1, naive_forgets[-1]), xytext=(7.5, -0.04),
            fontsize=9, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7))
ax.annotate(f'Final: {replay_forgets[-1]*100:.2f}%',
            xy=(len(replay_forgets)-1, replay_forgets[-1]), xytext=(7.5, -0.10),
            fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', alpha=0.7))
ax.annotate(f'Final: {lwf_forgets[-1]*100:.2f}%',
            xy=(len(lwf_forgets)-1, lwf_forgets[-1]), xytext=(6.5, -0.07),
            fontsize=9, color='green',
            arrowprops=dict(arrowstyle='->', color='green', alpha=0.7))

plt.tight_layout()

# Save as PDF and PNG
plt.savefig('forgetting_comparison.pdf', dpi=300, bbox_inches='tight')
plt.savefig('forgetting_comparison.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

print("Saved: forgetting_comparison.pdf and forgetting_comparison.png")