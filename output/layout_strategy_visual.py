"""
Visual representation of the layout strategy for outfit variation workflow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(20, 10))

# Define colors for data bus lanes
bus_lanes = {
    "MODEL": {"y": -2000, "color": "#FFB6C1"},
    "CLIP": {"y": -1600, "color": "#98D8C8"},
    "VAE": {"y": -1200, "color": "#F7DC6F"},
    "IMAGE": {"y": -800, "color": "#BB8FCE"},
    "LATENT": {"y": -400, "color": "#85C1E2"},
    "CONDITIONING": {"y": 0, "color": "#F8C471"},
    "CONTROL": {"y": 400, "color": "#ABEBC6"}
}

# Define stages
stages = {
    "0_input_loaders": {"x_start": 0, "x_end": 2000, "y_start": -2200, "y_end": 600, "color": "#E8F8F5"},
    "1_lora_stack": {"x_start": 2500, "x_end": 6500, "y_start": -2200, "y_end": -1000, "color": "#FEF9E7"},
    "2_conditioning": {"x_start": 7000, "x_end": 11000, "y_start": -1600, "y_end": 600, "color": "#EBF5FB"},
    "3_image_processing": {"x_start": 11500, "x_end": 15500, "y_start": -1200, "y_end": 1200, "color": "#F4ECF7"},
    "4_generation_control": {"x_start": 16000, "x_end": 20000, "y_start": -800, "y_end": 1600, "color": "#FADBD8"},
    "5_sampling": {"x_start": 20500, "x_end": 24500, "y_start": -1600, "y_end": 800, "color": "#E8F6F3"},
    "6_video_processing": {"x_start": 25000, "x_end": 29000, "y_start": -1200, "y_end": 1200, "color": "#FDF2E9"},
    "7_output": {"x_start": 29500, "x_end": 32500, "y_start": -800, "y_end": 1600, "color": "#EAEDED"}
}

# Draw data bus lanes
for lane_name, lane_info in bus_lanes.items():
    ax.axhline(y=lane_info["y"], color=lane_info["color"], linewidth=4, alpha=0.3, linestyle='--')
    ax.text(-500, lane_info["y"], lane_name, fontsize=10, ha='right', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor=lane_info["color"], alpha=0.5))

# Draw stages
for stage_name, stage_info in stages.items():
    rect = FancyBboxPatch(
        (stage_info["x_start"], stage_info["y_start"]),
        stage_info["x_end"] - stage_info["x_start"],
        stage_info["y_end"] - stage_info["y_start"],
        boxstyle="round,pad=50",
        facecolor=stage_info["color"],
        edgecolor='gray',
        linewidth=2,
        alpha=0.3
    )
    ax.add_patch(rect)
    
    # Add stage label
    stage_label = stage_name.replace('_', ' ').title()
    ax.text(
        (stage_info["x_start"] + stage_info["x_end"]) / 2,
        stage_info["y_end"] + 100,
        stage_label,
        fontsize=12,
        ha='center',
        va='bottom',
        weight='bold'
    )

# Add sample node representations
sample_nodes = [
    {"x": 500, "y": -1800, "label": "UNET\nLoader", "color": "#AED6F1"},
    {"x": 500, "y": -1400, "label": "CLIP\nLoader", "color": "#ABEBC6"},
    {"x": 3500, "y": -1800, "label": "LoRA 1", "color": "#F9E79F"},
    {"x": 5500, "y": -1800, "label": "LoRA 2", "color": "#F9E79F"},
    {"x": 9000, "y": -800, "label": "Text\nEncode", "color": "#FAD7A0"},
    {"x": 13500, "y": 0, "label": "Image\nPrep", "color": "#DDA0DD"},
    {"x": 18000, "y": 800, "label": "Seed\nControl", "color": "#F5B7B1"},
    {"x": 22500, "y": -400, "label": "KSampler", "color": "#A9DFBF"},
    {"x": 27000, "y": 400, "label": "Video\nCombine", "color": "#F8C471"},
    {"x": 31000, "y": 800, "label": "Save\nImage", "color": "#D5DBDB"}
]

for node in sample_nodes:
    rect = FancyBboxPatch(
        (node["x"] - 150, node["y"] - 75),
        300, 150,
        boxstyle="round,pad=10",
        facecolor=node["color"],
        edgecolor='black',
        linewidth=1
    )
    ax.add_patch(rect)
    ax.text(node["x"], node["y"], node["label"], fontsize=10, ha='center', va='center')

# Add flow arrows
flow_arrows = [
    {"start": (650, -1800), "end": (3350, -1800)},  # UNET to LoRA
    {"start": (3650, -1800), "end": (5350, -1800)},  # LoRA chain
    {"start": (5650, -1800), "end": (8850, -800)},   # To conditioning
    {"start": (9150, -800), "end": (13350, 0)},      # To image
    {"start": (13650, 0), "end": (17850, 800)},      # To control
    {"start": (18150, 800), "end": (22350, -400)},   # To sampling
    {"start": (22650, -400), "end": (26850, 400)},   # To video
    {"start": (27150, 400), "end": (30850, 800)}     # To output
]

for arrow in flow_arrows:
    ax.annotate('', xy=arrow["end"], xytext=arrow["start"],
                arrowprops=dict(arrowstyle='->', color='gray', lw=2, alpha=0.6))

# Set axis properties
ax.set_xlim(-2000, 33000)
ax.set_ylim(-2500, 2000)
ax.set_xlabel('Horizontal Position (pixels)', fontsize=12)
ax.set_ylabel('Vertical Position (pixels)', fontsize=12)
ax.set_title('Outfit Variation Workflow - Optimal Layout Strategy\nExtreme Spacing (2000px) with Data Bus Architecture', fontsize=16, weight='bold')

# Add grid
ax.grid(True, alpha=0.2, linestyle=':', linewidth=0.5)

# Add spacing info
spacing_text = """
Spacing Parameters:
• Horizontal: 2000px
• Vertical: 400px
• Group Padding: 120px
• Data Bus Lanes: 150px
• Total Width: ~32,500px
"""
ax.text(32000, 1500, spacing_text, fontsize=10, 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8),
        verticalalignment='top')

plt.tight_layout()
plt.savefig('output/layout_strategy_visualization.png', dpi=150, bbox_inches='tight')
plt.close()

print("Layout strategy visualization saved to: output/layout_strategy_visualization.png")