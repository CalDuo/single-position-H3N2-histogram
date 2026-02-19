# single-position-H3N2-histogram

Python pipeline for automated generation of publication-quality H3N2 HA amino-acid position figures. These scripts are intended for use with chatGPT to generate histograms for figures using the chatGPT5.2 project context feature.

---

# H3N2 Figure Generation Scripts (Reviewer Package)

This repository contains the original manuscript-level scripts used to generate automated H3N2 HA position figures and slide decks.

## Included Scripts

- `render_single_position_histogram_adaptive_COLORLOCKED_v2.py`
- `render_ha_single_position_figures.py`
- `build_histogram_ha_deck_ORDERED_ALIGNED.py`

## Example Outputs

- `Example output position 82.svg`
- `Example output position 83.svg`

No experimental datasets are included.

---

# 1) Single-Position Histogram Renderer

**File**
```
render_single_position_histogram_adaptive_COLORLOCKED_v2.py
```

## Purpose

Generates a complete publication-style multi-panel figure for a single HA amino-acid position.

**Output formats**
- SVG (default, vector)
- PNG (optional)
- Transparent background

---

## Figure Structure (Top → Bottom)

### 1. Stacked Amino-Acid Histogram

- Year range: 1965–2020 (locked)
- Y-axis: Proportion (0–1.0, fixed 0.25 increments)
- Deterministic amino-acid color map (frozen)
- “Other” category automatically collapsed
- Legend titled **Amino Acid**
- Publication-aligned margins

### 2. Antigenic Cluster Strip

Clusters:

HK68 → EN72 → VI75 → TX77 → BK79 → SI87 → BE89 → BE92 → WU95 → SY97 → FU02 → CA04 → WI05 → PE09 → TX12 → HK14

- Horizontally aligned to histogram bins
- Deterministic `tab20` colormap
- Black borders
- Two-digit cluster labels

### 3. Neutralization Matrix

- Rows: mAbs associated with that position
- Columns: Antigenic clusters
- Cell color derived from Excel fill color
- Mutation letters rendered (WT → mutant across cluster boundary)
- Negative mAb IDs treated as equivalent to positive (e.g., `-117 == 117`)
- Adaptive height scaling
- If no mAbs are present: panel collapses with message

### 4. Year Axis Strip

- Tick marks every 5 years
- Vertical year labels
- Bold axis label “Year”
- Locked placement (no stretching)

---

## Required Inputs

User must provide:

- Histogram proportion XLSX  
- Neutralization matrix XLSX  
- Amino-acid mutation table XLSX  
- JSON mapping (position → mAbs)

No data files are bundled in this repository.

---

## Command Example

```bash
python render_single_position_histogram_adaptive_COLORLOCKED_v2.py \
  --position 82 \
  --out position_82.svg \
  --fmt svg \
  --hist_xlsx hist_data.xlsx \
  --neut_xlsx neutralization.xlsx \
  --aa_positions_xlsx aa_positions.xlsx \
  --mapping_json position_mab_map.json
```

---

# 2) HA Head Renderer (Structural Panel)

**File**
```
render_ha_single_position_figures.py
```

## Purpose

Generates HA-head structural PNG renders (single residue highlighted) for integration with histogram slides.

Designed for:

- Transparent background
- Fixed camera angle
- Deterministic coloring
- Compatible sizing for deck builder script

**Output**
```
position_<X>_HA.png
```

---

# 3) PowerPoint Deck Builder

**File**
```
build_histogram_ha_deck_ORDERED_ALIGNED.py
```

## Purpose

Builds a slide deck where each slide contains:

**Left panel**
- Histogram (SVG converted internally to PNG)

**Right panel**
- HA-head PNG render

---

## Slide Layout Rules (Locked)

**Histogram**
- Width: 7.5 inches
- Flush left
- Height auto-scaled proportionally

**HA-head**
- Width: 3.0 inches
- Flush right
- Vertically centered

Slides:
- Ordered descending by numeric position
- Negative IDs treated as positive
- Deterministic alignment

---

## Required Inputs

- ZIP file of histogram SVGs  
- ZIP file of HA-head PNGs  

**Output**
```
Histogram_HA_deck.pptx
```

---

# Reproducibility

Figures are deterministic given:

- Locked year range (1965–2020)
- Frozen amino-acid color map
- Fixed cluster definitions
- Explicit layout constants (inches)
- Neutralization height scaling derived from canonical reference (position 225)

Identical inputs will produce identical figures.

---

# Data Policy

This repository contains **code only**.

No:
- IC50 data
- Raw neutralization tables
- Sequence datasets
- Manuscript figures
- Unpublished results

All experimental data must be supplied locally by the user.
