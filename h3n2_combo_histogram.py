Always show details
import os, pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import warnings, logging

warnings.filterwarnings("ignore")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

# ---- Locked combo-hist template params (match v9) ----
class Cfg:
    font_family="DejaVu Sans"
    base_fontsize=11.0
    hist_axis_w_in=6.0
    hist_axis_h_in=2.0
    fig_w_in=8.0
    fig_h_in=6.4
    left_frac=0.08
    bottom_frac=0.20
    legend_gap_in=0.03
    legend_w_in=1.44
    year_min=1965
    year_max=2020
    year_step=5
    prop_ticks=(1.00,0.75,0.50,0.25,0.00)
    tick_len=8.0
    tick_w=1.6
    grid_ls=":"
    grid_lw=0.8
    cluster_strip_h_in=0.25
    cluster_fontsize=10.0
    cluster_fontweight="normal"
cfg = Cfg()

plt.rcParams.update({
    "font.family": cfg.font_family,
    "font.size": cfg.base_fontsize,
    "axes.titlesize": cfg.base_fontsize + 3,
    "axes.titleweight": "bold",
    "svg.fonttype": "none",
})

CLUSTERS = [
    ("HK68",1968,1972),("EN72",1972,1975),("VI75",1975,1977),("TX77",1977,1979),
    ("BK79",1979,1987),("SI87",1987,1989),("BE89",1989,1992),("BE92",1992,1995),
    ("WU95",1995,1997),("SY97",1997,2002),("FU02",2002,2004),("CA04",2004,2005),
    ("WI05",2005,2009),("PE09",2009,2012),("TX12",2012,2014),("HK14",2014,2015),
]

# ---- Data ----
xlsx = "/mnt/data/Human_H3N2_Set3_aa_proportions_combined_wide.xlsx"
df = pd.read_excel(xlsx)

posA, posB = 158, 160
dfA = df[df["Position"] == posA]
dfB = df[df["Position"] == posB]

years_present = [c for c in df.columns if isinstance(c, int)]
THRESH = 0.05

records = []
for y in years_present:
    combos = {}
    for _, rA in dfA.iterrows():
        pA = float(rA[y])
        if pA < THRESH:
            continue
        for _, rB in dfB.iterrows():
            pB = float(rB[y])
            if pB < THRESH:
                continue
            combo = f"{rA['Amino acid']}/{rB['Amino acid']}"
            combos[combo] = combos.get(combo, 0.0) + min(pA, pB)
    if combos:
        tot = sum(combos.values())
        records.append({"year": y, **{k: v / tot for k, v in combos.items()}})
    else:
        records.append({"year": y, "Other": 1.0})

combo_df = pd.DataFrame(records).fillna(0).set_index("year")

# Deterministic colors (stable per run)
np.random.seed(1)
colors = {c: ("#B0B0B0" if c == "Other" else to_hex(np.random.rand(3)))
          for c in combo_df.columns}

# ---- Figure ----
fig = plt.figure(figsize=(cfg.fig_w_in, cfg.fig_h_in))
fig_w, fig_h = fig.get_size_inches()
hist_w_frac = cfg.hist_axis_w_in / fig_w
hist_h_frac = cfg.hist_axis_h_in / fig_h
strip_h_frac = cfg.cluster_strip_h_in / fig_h

# Histogram axis placement (same as v9)
hist_bottom = max(0.34, cfg.bottom_frac + strip_h_frac + 0.08)
ax = fig.add_axes([cfg.left_frac, hist_bottom, hist_w_frac, hist_h_frac])

bottom = np.zeros(len(combo_df))
x = combo_df.index.values
for c in combo_df.columns:
    vals = combo_df[c].values.astype(float)
    if np.allclose(vals, 0):
        continue
    ax.bar(x, vals, bottom=bottom, width=0.9,
           color=colors[c], linewidth=0, align="center", label=c)
    bottom += vals

ax.set_ylim(0, 1.0)
ax.set_yticks(list(cfg.prop_ticks))
ax.set_yticklabels([f"{t:.2f}" for t in cfg.prop_ticks])

ax.set_xlim(cfg.year_min - 0.5, cfg.year_max + 0.5)
ticks = np.arange(cfg.year_min, cfg.year_max + 1, cfg.year_step)
ax.set_xticks(ticks)
ax.set_xticklabels([str(y) for y in ticks], rotation=90)

ax.tick_params(axis="x", direction="in", length=cfg.tick_len, width=cfg.tick_w, pad=36)
ax.tick_params(axis="y", direction="in", length=cfg.tick_len, width=cfg.tick_w)
ax.grid(True, axis="y", linestyle=cfg.grid_ls, linewidth=cfg.grid_lw)
ax.grid(True, axis="x", linestyle=cfg.grid_ls, linewidth=cfg.grid_lw)

ax.set_title(f"{posA}/{posB}", pad=14)

# Legend placement (same as v9)
leg_left = cfg.left_frac + hist_w_frac + (cfg.legend_gap_in / fig_w)
leg_w = cfg.legend_w_in / fig_w
ax_leg = fig.add_axes([leg_left, hist_bottom, leg_w, hist_h_frac])
ax_leg.axis("off")
h, l = ax.get_legend_handles_labels()
leg = ax_leg.legend(h, l, loc="upper left", frameon=False,
                    fontsize=cfg.base_fontsize - 3, title="Amino Acid")
leg.get_title().set_fontweight("bold")

# Cluster strip: exactly 0.4" below X axis (locked)
strip_bottom = hist_bottom - (0.4 / fig_h)
ax_strip = fig.add_axes([cfg.left_frac, strip_bottom, hist_w_frac, strip_h_frac])
ax_strip.set_xlim(cfg.year_min, cfg.year_max)
ax_strip.set_ylim(0, 1)
ax_strip.axis("off")

cmap = plt.get_cmap("tab20")
for i, (name, start, end) in enumerate(CLUSTERS):
    s = max(cfg.year_min, start)
    e = min(cfg.year_max, end)
    if e <= s:
        continue
    ax_strip.add_patch(
        plt.Rectangle((s, 0), e - s, 1,
                      facecolor=cmap(i),
                      edgecolor="black", linewidth=0.8)
    )
    label = str(start)[-2:]
    cx = (s + e) / 2
    block = max(1, e - s)
    fs = min(cfg.cluster_fontsize,
             max(6.0, cfg.cluster_fontsize * (block / 4.0)))
    ax_strip.text(cx, 0.5, label, ha="center", va="center",
                  fontsize=fs, fontweight=cfg.cluster_fontweight)

out = "/mnt/data/histogram_158_160_combination_5pct_lockedstyle_v9.png"
fig.savefig(out, dpi=200, transparent=True)
plt.close(fig)

out
