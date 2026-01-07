import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# Define box parameters
box_width = 2.2
box_height = 1.4
y_line1 = 7
y_line2 = 2.5

# Color scheme
box_color = '#E3F2FD'  # Light blue
border_color = '#1976D2'  # Darker blue
final_box_color = '#2d5a3f'  # Dark green
arrow_color = '#424242'  # Dark gray
vertical_arrow_color = '#D32F2F'  # Red

# Line 1 boxes
boxes_line1 = [
    (1, y_line1, "Vietnamese\nCatalogue"),
    (4.5, y_line1, "GBIF\nMatch"),
    (8, y_line1, "Image\nDownload")
]

# Line 2 boxes
boxes_line2 = [
    (1, y_line2, "Add Vietnamese\nNames"),
    (4.5, y_line2, "Quality\nControl"),
    (8, y_line2, "Final\nDataset")
]


def draw_box(ax, x, y, width, height, text, facecolor, edgecolor, textcolor='black', fontweight='bold'):
    """Draw a rounded box with shadow effect"""
    # Shadow
    shadow = FancyBboxPatch((x + 0.05, y - 0.05), width, height,
                            boxstyle="round,pad=0.15",
                            edgecolor='none', facecolor='gray', alpha=0.3, linewidth=0)
    ax.add_patch(shadow)

    # Main box
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.15",
                         edgecolor=edgecolor, facecolor=facecolor, linewidth=2.5)
    ax.add_patch(box)

    # Text with much bigger font size
    ax.text(x + width / 2, y + height / 2, text,
            ha='center', va='center', fontsize=16, weight=fontweight, color=textcolor)


def draw_arrow(ax, x1, y1, x2, y2, color, linewidth=2.5):
    """Draw a straight arrow"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='->', mutation_scale=25,
                            linewidth=linewidth, color=color,
                            connectionstyle="arc3,rad=0")
    ax.add_patch(arrow)


# Draw Line 1 boxes and arrows
for i, (x, y, text) in enumerate(boxes_line1):
    draw_box(ax, x, y, box_width, box_height, text, box_color, border_color)

    # Draw horizontal arrow to next box
    if i < len(boxes_line1) - 1:
        draw_arrow(ax, x + box_width + 0.1, y + box_height / 2,
                   boxes_line1[i + 1][0] - 0.1, y + box_height / 2, arrow_color)

# Draw straight vertical arrow from last box of line 1 to first box of line 2
x_middle = 6  # Center position between the two lines
y_start = boxes_line1[-1][1] - 0.1
y_end = boxes_line2[0][1] + box_height + 0.1

arrow_v = FancyArrowPatch((x_middle, y_start), (x_middle, y_end),
                          arrowstyle='->', mutation_scale=30,
                          linewidth=3.5, color=vertical_arrow_color,
                          connectionstyle="arc3,rad=0")  # rad=0 makes it straight
ax.add_patch(arrow_v)

# Draw Line 2 boxes and arrows
for i, (x, y, text) in enumerate(boxes_line2):
    # Special styling for final box
    if i == len(boxes_line2) - 1:
        draw_box(ax, x, y, box_width, box_height, text,
                 final_box_color, final_box_color, textcolor='white', fontweight='bold')
    else:
        draw_box(ax, x, y, box_width, box_height, text, box_color, border_color)

    # Draw horizontal arrow to next box
    if i < len(boxes_line2) - 1:
        draw_arrow(ax, x + box_width + 0.1, y + box_height / 2,
                   boxes_line2[i + 1][0] - 0.1, y + box_height / 2, arrow_color)

plt.tight_layout()
plt.savefig('flowchart_pretty.pdf', bbox_inches='tight', facecolor='white')
plt.show()