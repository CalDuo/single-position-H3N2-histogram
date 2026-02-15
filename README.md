# single-position-H3N2-histogram
Python pipeline for automated generation of influenza antigenic histograms (Single potitions)

# H3N2 Figure Generation Scripts (Reviewer Package)

This repository contains the **original, manuscript-level scripts** used to generate publication-style figures for H3N2 analysis.

The package includes:

1. `render_single_position_histogram_adaptive_COLORLOCKED_v2.py`
2. `build_histogram_ha_deck_ORDERED_ALIGNED.py`

No experimental data are included in this package.

---

# 1) Single-Position Histogram Renderer

File:
```
render_single_position_histogram_adaptive_COLORLOCKED_v2.py
```

## Purpose

Generates a full publication-style multi-panel figure for a single HA amino-acid position including:

• Stacked amino-acid proportion histogram (1965–2020)  
• Antigenic cluster strip  
• Neutralization matrix (per mAb × cluster)  
• Mutation transition letters (WT → mutant across clusters)  
• Adaptive layout scaling based on number of associated mAbs  
• Locked amino-acid color logic  

Output format: SVG (vector), optionally PNG

---

## Figure Layout (Top → Bottom)

### 1. Histogram Panel
- X-axis: Year (1965–2020)
- Y-axis: Proportion (0–1.0)
- Stacked bars representing amino-acid frequencies per year
- Locked amino-acid color map
- Legend labeled “Amino Acid”
- Transparent background
- Publication-aligned margins

### 2. Antigenic Cluster Strip
Horizontal block strip aligned to histogram X-axis.

Clusters included:
HK68 → EN72 → VI75 → TX77 → BK79 → SI87 → BE89 → BE92 → WU95 → SY97 → FU02 → CA04 → WI05 → PE09 → TX12 → HK14

Each cluster:
- Spans its historical year interval
- Uses deterministic colormap assignment
- Labeled by last two digits
- Black border

### 3. Neutralization Matrix
Grid of:
- Rows: mAbs associated with that position
- Columns: antigenic clusters
- Cell color: derived from neutralization Excel fill color
- Mutation letters:
    - Wild-type letter shown in cluster of emergence
    - Mutant letter shown in next cluster
- Negative mAb IDs (e.g., -117) treated as positive equivalents

If no mAbs are associated:
- Panel height collapses
- “No associated mAbs” displayed

### 4. Year Axis Strip
- Tick marks every 5 years
- Vertical year labels
- Bold axis label “Year”

---

## Required Inputs

The script expects the following inputs:

• Histogram proportion XLSX  
• Neutralization matrix XLSX  
• AA mutation position table XLSX  
• JSON mapping of position → mAbs  

These must be provided locally by the user.

No data are bundled in this repository.

---

## Output

Produces:
```
position_<X>.svg
```
or
```
position_<X>.png
```

Vector output suitable for publication.

---

# 2) PPT Deck Builder

File:
```
build_histogram_ha_deck_ORDERED_ALIGNED.py
```

## Purpose

Builds a PowerPoint deck where each slide contains:

• Left: Histogram SVG (converted internally to PNG)
• Right: HA-head PyMOL figure PNG
• Positions ordered descending (numeric)
• Negative IDs treated as positive
• Strict slide layout rules

---

## Slide Layout Specifications

Histogram:
- Width: 7.5 inches
- Left edge flush with slide boundary
- Height auto-scaled proportionally

HA-head:
- Width: 3.0 inches
- Right edge flush with slide boundary
- Vertically centered relative to histogram

Both elements:
- Centered vertically on slide
- Consistent scaling across slides

---

## Required Inputs

• ZIP file of histogram SVGs  
• ZIP file of HA-head PNGs  

---

## Output

Produces:
```
Histogram_HA_deck.pptx
```

Slides ordered in descending position number.

---

# Data Policy

This repository contains **code only**.

No experimental data, no manuscript tables, no IC50 values, and no unpublished datasets are included.

Users must provide their own local data files.

---

# Reproducibility

Figures are deterministic given:
- Fixed cluster definitions
- Locked amino-acid color map
- Defined year range (1965–2020)
- Explicit layout parameters

This ensures reproducibility across systems.

---

# Contact

These scripts were developed for automated generation of publication-quality H3N2 HA position figures.
