"""
PyMOL HA Single-Position Renderer
----------------------------------

Generates publication-style HA-head figures with:

• Fixed camera
• Transparent background
• Base HA coloring
• RBS highlighted (yellow)
• Position colored by category:
    - Gain   : red
    - Loss   : blue
    - Mixed  : purple
    - Ferret : green
• Residue label
• PNG output

No data included. User provides:
- PDB file
- Position lists (gain/loss/mixed/ferret)
"""

from pymol import cmd
import os

# ------------------------------
# USER SETTINGS
# ------------------------------

PDB_PATH = "your_structure.pdb"
CHAIN = "A"
OUTPUT_DIR = "ha_single_outputs"

GAIN_POSITIONS   = [8, 50, 83, 135, 144, 172, 192, 196, 198, 222, 223]
LOSS_POSITIONS   = [3, 78, 82, 124, 128, 158, 160, 183, 242, 277]
MIXED_POSITIONS  = [122, 138, 145, 155, 159, 186, 188, 193, 225]
FERRET_POSITIONS = [145, 155, 156, 158, 159, 189, 193]

RBS_POSITIONS = [98, 134, 135, 136, 137, 153, 155, 183, 190, 194, 195, 196, 198, 222, 225]

IMAGE_WIDTH = 2400
IMAGE_HEIGHT = 2400

# ------------------------------
# COLORS
# ------------------------------

COLOR_GAIN   = "red"
COLOR_LOSS   = "blue"
COLOR_MIXED  = "purple"
COLOR_FERRET = "green"
COLOR_RBS    = "yellow"
COLOR_BASE   = "gray80"

# ------------------------------
# SETUP
# ------------------------------

def setup_structure():
    cmd.load(PDB_PATH, "ha")
    cmd.remove("solvent")
    cmd.bg_color("white")
    cmd.set("ray_opaque_background", 0)
    cmd.hide("everything")
    cmd.show("cartoon", "ha")
    cmd.color(COLOR_BASE, "ha")

    # RBS
    rbs_sel = f"chain {CHAIN} and resi " + "+".join(map(str, RBS_POSITIONS))
    cmd.color(COLOR_RBS, rbs_sel)

    # Fixed camera (replace with your saved view if needed)
    cmd.orient("ha")
    cmd.zoom("ha", 5)

def color_position(pos):
    sel = f"chain {CHAIN} and resi {pos}"

    if pos in FERRET_POSITIONS:
        cmd.color(COLOR_FERRET, sel)
    elif pos in GAIN_POSITIONS:
        cmd.color(COLOR_GAIN, sel)
    elif pos in LOSS_POSITIONS:
        cmd.color(COLOR_LOSS, sel)
    elif pos in MIXED_POSITIONS:
        cmd.color(COLOR_MIXED, sel)

    cmd.show("sticks", sel)
    cmd.set("stick_radius", 0.3)
    cmd.label(sel + " and name CA", f'"{pos}"')

def render_position(pos):
    cmd.reinitialize()
    setup_structure()
    color_position(pos)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    out_path = os.path.join(OUTPUT_DIR, f"HA_pos_{pos}.png")
    cmd.png(out_path, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, ray=1)
    print(f"Saved: {out_path}")

# ------------------------------
# MAIN
# ------------------------------

def render_all():
    all_positions = sorted(set(
        GAIN_POSITIONS +
        LOSS_POSITIONS +
        MIXED_POSITIONS +
        FERRET_POSITIONS
    ))

    for pos in all_positions:
        render_position(pos)

# Run in PyMOL with:
# run render_ha_single_position_figures.py
# render_all()
