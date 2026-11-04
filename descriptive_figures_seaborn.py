import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns


# 1. SETTINGS
#####################################################################################################
# every number below is copied from core_descriptives.log (Stata run of rq1_core_descriptives.do, estimation sample of the main logit, N = 8,204)
# the figures are written next to this file: one PDF with all of them and one PNG per figure in figures_color/
OUT = Path(__file__).resolve().parent
(OUT / "figures_color").mkdir(exist_ok=True)
# colours of the Data Lab template (Argumentative Fallacy): cream background, navy ink, light blue and beige, plus three darker shades of the same family
CREAM, NAVY, SKY, BEIGE = "#F2EEE7", "#19233A", "#E1EAF0", "#DFCCB3"
STEEL, MIST, TAN, RUST, MUTED = "#4F6D8F", "#9DB6CC", "#B08A5B", "#A4573A", "#5F6572"
# template fonts: Gilda Display for titles, Gideon Roman for text (free Google fonts); the script looks for the .ttf files next to it, in fonts/ and in ~/.fonts, and falls back to a serif font
for d in [OUT, OUT / "fonts", Path.home() / ".fonts", Path.home() / "Library" / "Fonts"]:
    for f in list(d.glob("GildaDisplay*.ttf")) + list(d.glob("GideonRoman*.ttf")): font_manager.fontManager.addfont(str(f))
have = {f.name for f in font_manager.fontManager.ttflist}
TITLE_FONT = "Gilda Display" if "Gilda Display" in have else "serif"
BODY_FONT = "Gideon Roman" if "Gideon Roman" in have else "serif"
sns.set_theme(style="ticks", context="paper", font_scale=1.15)
plt.rcParams.update({"font.family": BODY_FONT, "axes.unicode_minus": True, "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
                     "axes.edgecolor": NAVY, "axes.labelcolor": NAVY, "xtick.color": NAVY, "ytick.color": NAVY, "text.color": NAVY,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.titlecolor": NAVY, "pdf.fonttype": 42})
# sequential map light blue to navy (rates) and diverging map rust to cream to navy (signed correlations)
SEQ = LinearSegmentedColormap.from_list("seq", [SKY, MIST, STEEL, NAVY])
DIV = LinearSegmentedColormap.from_list("div", [RUST, TAN, BEIGE, CREAM, SKY, STEEL, NAVY])
N_EST = 8204
EXIT_ALL = 12.80


# 2. HELPERS
#####################################################################################################
# rounding half up, as Stata displays, with a real minus sign
def num(x, d=2): return str(Decimal(str(x)).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)).replace("-", "−")
def thousands(n): return f"{int(round(n)):,}"
# significance stars for a correlation: two-sided test of r = 0 (the test pwcorr uses); with over 7,800 df the normal tail equals the t tail
def stars(r, n):
    p = math.erfc(abs(r * math.sqrt((n - 2) / (1 - r * r))) / math.sqrt(2))
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
# each figure gets a numbered title in the template's title font, a beige rule under it and a note at the bottom
FIGS = []
def finish(fig, name, caption, note):
    fig.suptitle(f"Figure {len(FIGS) + 1}: {caption}", fontsize=16, y=0.985, fontfamily=TITLE_FONT, color=NAVY)
    fig.add_artist(plt.Line2D([0.03, 0.97], [0.935, 0.935], color=BEIGE, linewidth=2.5, transform=fig.transFigure))
    fig.text(0.015, 0.008, note, fontsize=9, ha="left", va="bottom", color=MUTED, wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 0.93))
    fig.savefig(OUT / "figures_color" / f"{name}.png", dpi=200)
    FIGS.append(fig)
# bar labels: the value on top of each bar
def label_bars(ax, fmt, pad=3, **kw):
    for c in ax.containers: ax.bar_label(c, labels=[fmt(v) for v in c.datavalues], padding=pad, fontsize=9, color=NAVY, **kw)
# overall exit rate as a rust dashed line with a legend entry
def overall(ax, vertical=False, loc="upper right"):
    (ax.axvline if vertical else ax.axhline)(EXIT_ALL, color=RUST, linestyle="--", linewidth=1.3, label="All startups (12.80%)")
    ax.legend(frameon=False, loc=loc, fontsize=9)
EDGE = {"edgecolor": NAVY, "linewidth": 0.6}


# 3. DATA FROM THE LOG
#####################################################################################################
# sample (section 1 of the do-file)
sample = pd.DataFrame({"step": ["Two VC rounds, valid gap", "Full 3-year window", "Estimation sample (logit)"], "n": [18248, 9301, 8204]})
# summary statistics (section 2): mean, sd, p25, median, p75, min, max
summ = pd.DataFrame([["Gap in months", 16.760, 10.736, 9.363, 14.602, 22.076, 0.033, 84.166],
                     ["ln(1 + gap in months)", 2.683, 0.668, 2.338, 2.747, 3.139, 0.032, 4.445],
                     ["Heat", -0.091, 0.922, -0.636, -0.314, 0.697, -1.875, 3.002],
                     ["ln(1 + round-1 size, \\$M)", 1.083, 0.815, 0.470, 0.920, 1.474, 0.001, 6.986],
                     ["Deal number of round 1", 1.414, 0.817, 1, 1, 2, 1, 10],
                     ["Startup age at round 1, years", 1.171, 1.145, 0, 1, 2, 0, 6]],
                    columns=["var", "mean", "sd", "p25", "p50", "p75", "min", "max"])
rates = pd.DataFrame({"outcome": ["Exit", "Failure", "Round 3"], "pct": [12.8, 5.7, 61.3]})
# exit by gap quintile (section 3)
gapq = pd.DataFrame({"q": ["Q1\nfastest", "Q2", "Q3", "Q4", "Q5\nslowest"], "n": [1641, 1642, 1642, 1640, 1639],
                     "gap": [4.88, 10.35, 14.64, 20.37, 33.58], "lo": [0.03, 8.11, 12.42, 17.05, 24.18], "hi": [8.08, 12.39, 17.02, 24.15, 84.17],
                     "exit": [13.22, 11.69, 13.89, 12.62, 12.57]})
# exit by gap quintile and heat tercile (section 4): rate in percent and number of startups
cross_exit = pd.DataFrame([[11.21, 14.22, 14.31], [11.50, 13.88, 10.23], [15.29, 12.88, 13.08], [11.69, 13.29, 13.26], [14.19, 12.35, 10.57]],
                          index=["Q1 fastest", "Q2", "Q3", "Q4", "Q5 slowest"], columns=["Cold", "Middle", "Hot"])
cross_n = pd.DataFrame([[562, 443, 636], [565, 461, 616], [641, 458, 543], [676, 504, 460], [613, 591, 435]], index=cross_exit.index, columns=cross_exit.columns)
# heat terciles (section 4)
heatt = pd.DataFrame({"t": ["Cold", "Middle", "Hot"], "n": [3057, 2457, 2690], "heat": [-1.04, -0.05, 0.95], "gap": [17.10, 17.83, 15.40], "exit": [12.82, 13.27, 12.34]})
# by year of round 2 (section 5)
year = pd.DataFrame({"year": list(range(2012, 2020)), "n": [25, 356, 803, 1111, 1316, 1591, 1868, 1134],
                     "exit": [12.00, 16.57, 11.96, 13.68, 11.85, 12.19, 12.85, 13.23], "heat": [-0.03, 0.89, 0.48, -0.15, -0.19, 0.01, -0.43, -0.21],
                     "gap": [4.76, 9.11, 11.96, 13.95, 16.67, 19.00, 19.06, 18.74]})
# by sector (sections 4 and 5)
sector = pd.DataFrame({"sector": ["Information Technology", "Healthcare", "Consumer Products and Services (B2C)", "Business Products and Services (B2B)",
                                  "Financial Services", "Materials and Resources", "Energy"],
                       "n": [3853, 1559, 1495, 941, 204, 89, 63], "exit": [13.76, 14.88, 10.77, 11.26, 7.35, 5.62, 1.59]})
# correlations (section 6): lower triangles with pairwise N
main_names = ["Exit within 3 years", "ln(1 + gap)", "Heat", "ln(1 + round-1 size)", "Deal number, round 1", "Startup age, round 1"]
main_r = [[1], [-0.0046, 1], [0.0106, -0.0860, 1], [0.1455, 0.0249, -0.0202, 1], [-0.0416, -0.0283, -0.0242, -0.0943, 1], [-0.0025, -0.0603, -0.0688, 0.1218, 0.3327, 1]]
main_n = [[N_EST] * (i + 1) for i in range(6)]
hype_names = ["Heat (main)", "Heat, past years only", "Heat, quarterly", "Entry z, lagged", "Hype index", "Sector VC share"]
hype_r = [[1], [0.7019, 1], [0.5936, 0.3855, 1], [0.1592, -0.0301, 0.1496, 1], [0.8256, 0.4870, 0.5221, 0.6884, 1], [-0.1724, -0.4150, -0.0440, -0.0395, -0.1521, 1]]
hype_n = [[8204], [7823, 7823], [8204, 7823, 8204], [8179, 7823, 8179, 8179], [8179, 7823, 8179, 8179, 8179], [8204, 7823, 8204, 8179, 8179, 8204]]


# 4. FIGURE 1: SAMPLE
#####################################################################################################
fig, ax = plt.subplots(figsize=(8.3, 3.6))
sns.barplot(data=sample, y="step", x="n", hue="step", palette=[MIST, STEEL, NAVY], legend=False, ax=ax, **EDGE)
label_bars(ax, thousands)
ax.set(xlabel="Startups", ylabel="", xlim=(0, 21000))
finish(fig, "fig1_sample", "Sample", "1,097 startups of the window sample are not in the logit (missing covariate or fixed-effect cell with no exit). Their exit rate is 11.94% against 12.80%.")


# 5. FIGURE 2: SUMMARY STATISTICS
#####################################################################################################
# one box per variable built from the quartiles in the log: box = p25 to p75, line = median, whiskers = min and max, diamond = mean
BOX = [STEEL, MIST, NAVY, TAN, BEIGE, RUST]
fig, axes = plt.subplots(2, 4, figsize=(11.7, 6.4))
for ax, (_, r), col in zip(axes.flat[:6], summ.iterrows(), BOX):
    ax.bxp([{"med": r.p50, "q1": r.p25, "q3": r.p75, "whislo": r["min"], "whishi": r["max"], "mean": r["mean"], "fliers": [], "label": ""}], showmeans=True, widths=0.5,
           patch_artist=True, boxprops={"facecolor": col, "edgecolor": NAVY}, medianprops={"color": CREAM if col in (NAVY, STEEL, RUST) else NAVY, "linewidth": 1.8},
           whiskerprops={"color": NAVY}, capprops={"color": NAVY}, meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": NAVY, "markersize": 6})
    ax.set_title(r["var"], fontsize=12, fontfamily=TITLE_FONT)
    ax.text(0.97, 0.97, f"mean {num(r['mean'])}\nSD {num(r.sd)}", transform=ax.transAxes, ha="right", va="top", fontsize=9, color=MUTED)
    ax.set_xticks([])
# the binary outcomes as rates
ax = axes.flat[6]
sns.barplot(data=rates, x="outcome", y="pct", hue="outcome", palette=[NAVY, RUST, TAN], legend=False, ax=ax, **EDGE)
label_bars(ax, lambda v: num(v, 1))
ax.set(xlabel="", ylabel="Within 3 years (%)", ylim=(0, 72))
ax.set_title("Outcomes", fontsize=12, fontfamily=TITLE_FONT)
axes.flat[7].axis("off")
finish(fig, "fig2_summary", "Summary statistics", "Box: 25th to 75th percentile; line: median; whiskers: minimum and maximum; diamond: mean. Lead investor of round 1: none identified 56.5%, Venture Capital 31.2%, 11 other types 12.3%.")


# 6. FIGURE 3: EXIT RATE BY GAP QUINTILE
#####################################################################################################
# bars go from light (fastest) to dark (slowest)
fig, ax = plt.subplots(figsize=(8.3, 4.8))
sns.barplot(data=gapq, x="q", y="exit", hue="q", palette=[SKY, MIST, STEEL, "#34496A", NAVY], legend=False, ax=ax, **EDGE)
label_bars(ax, lambda v: num(v))
overall(ax)
ax.set_xticks(range(5), [f"{q}\n{num(lo)} to {num(hi)} months\nN = {thousands(n)}" for q, lo, hi, n in zip(gapq.q, gapq.lo, gapq.hi, gapq.n)], fontsize=9)
ax.set(xlabel="Gap quintile", ylabel="Exit within 3 years (%)", ylim=(0, 17))
finish(fig, "fig3_exit_by_gap", "Exit rate by fundraising speed", "Quintiles of the gap between the 1st and 2nd VC round, cut on the estimation sample. Raw rates without controls or fixed effects.")


# 7. FIGURE 4: EXIT RATE BY GAP QUINTILE AND HEAT TERCILE
#####################################################################################################
# left: heatmap of the rates; right: the same rates as lines, one per heat tercile (cold = steel blue, middle = tan, hot = rust)
fig, axes = plt.subplots(1, 2, figsize=(11.7, 5.0), gridspec_kw={"width_ratios": [1.05, 1]})
annot = np.array([[f"{num(cross_exit.iat[i, j])}\n({thousands(cross_n.iat[i, j])})" for j in range(3)] for i in range(5)])
sns.heatmap(cross_exit, annot=annot, fmt="", cmap=SEQ, vmin=9, vmax=16, linewidths=1.5, linecolor=CREAM,
            cbar_kws={"label": "Exit within 3 years (%)"}, annot_kws={"fontsize": 10}, ax=axes[0])
axes[0].set(xlabel="Heat tercile", ylabel="Gap quintile")
axes[0].tick_params(axis="y", rotation=0, length=0)
axes[0].tick_params(axis="x", length=0)
TERC = {"Cold": STEEL, "Middle": TAN, "Hot": RUST}
long = cross_exit.reset_index(names="q").melt(id_vars="q", var_name="tercile", value_name="exit")
sns.lineplot(data=long, x="q", y="exit", hue="tercile", palette=TERC, marker="o", markersize=8, linewidth=2.2, sort=False, ax=axes[1])
axes[1].axhline(EXIT_ALL, color=MUTED, linestyle=":", linewidth=1)
axes[1].set(xlabel="Gap quintile", ylabel="Exit within 3 years (%)", ylim=(8, 17))
axes[1].legend(title="Heat tercile", frameon=False, fontsize=9, title_fontsize=9, ncols=3, loc="upper center")
finish(fig, "fig4_exit_gap_heat", "Exit rate by gap quintile and heat tercile", "Cell: exit within 3 years (%), startups in parentheses. Mean heat: cold −1.04, middle −0.05, hot 0.95. Raw rates without controls or fixed effects; the raw counterpart of the interaction log gap × heat. Dotted line: all startups.")


# 8. FIGURE 5: HEAT TERCILES
#####################################################################################################
fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2))
for ax, col, lab, ylim in [(axes[0], "gap", "Mean gap (months)", (0, 21)), (axes[1], "exit", "Exit within 3 years (%)", (0, 16))]:
    sns.barplot(data=heatt, x="t", y=col, hue="t", palette=TERC, legend=False, ax=ax, **EDGE)
    label_bars(ax, lambda v: num(v))
    ax.set_xticks(range(3), [f"{t}\nN = {thousands(n)}" for t, n in zip(heatt.t, heatt.n)])
    ax.set(xlabel="Heat tercile", ylabel=lab, ylim=ylim)
finish(fig, "fig5_heat_terciles", "Fundraising speed and exit by heat tercile", "Heat takes one value per sector and year of round 2 (54 sector-years, the clusters of the main model). Terciles cut on the estimation sample.")


# 9. FIGURE 6: BY YEAR OF ROUND 2
#####################################################################################################
fig, axes = plt.subplots(3, 1, figsize=(8.3, 8.6), sharex=True)
sns.barplot(data=year, x="year", y="n", color=MIST, ax=axes[0], **EDGE)
label_bars(axes[0], thousands)
axes[0].set(ylabel="Startups", ylim=(0, 2200), xlabel="")
# exit bars above the overall rate in navy, below it in beige
sns.barplot(data=year, x="year", y="exit", hue=np.where(year.exit >= EXIT_ALL, "above", "below"), palette={"above": NAVY, "below": BEIGE}, legend=False, ax=axes[1], **EDGE)
for c in axes[1].containers:
    for bar, v in zip(c, c.datavalues):
        if not np.isnan(v): axes[1].text(bar.get_x() + bar.get_width() / 2, v / 2, num(v, 1), ha="center", va="center", fontsize=9, color=CREAM if v >= EXIT_ALL else NAVY)
overall(axes[1])
axes[1].set(ylabel="Exit within 3 years (%)", ylim=(0, 20), xlabel="")
# mean gap (left axis, navy) and mean heat (right axis, rust)
ax = axes[2]
ax.plot(range(8), year.gap, color=NAVY, marker="o", linewidth=2.2, label="Mean gap (months, left)")
ax.set(ylabel="Mean gap (months)", ylim=(0, 22), xlabel="Year of round 2")
ax2 = ax.twinx()
ax2.spines["right"].set_visible(True)
ax2.axhspan(0, 1.2, color=SKY, alpha=0.6, zorder=0)
ax2.plot(range(8), year.heat, color=RUST, marker="^", linewidth=2.2, linestyle="--", label="Mean heat (right)")
ax2.axhline(0, color=MUTED, linewidth=0.6)
ax2.set(ylabel="Mean heat", ylim=(-1, 1.2))
# draw the gap axis on top of the heat axis, so the shaded band does not cover the gap line
ax.set_zorder(ax2.get_zorder() + 1)
ax.patch.set_visible(False)
ax.legend(handles=ax.get_lines() + ax2.get_lines()[:1], frameon=False, loc="lower right", fontsize=9)
finish(fig, "fig6_by_year", "Startups, exits, gap and heat by year of round 2", "Shaded band in the bottom panel: heat above the sector mean. The rise of the mean gap probably reflects the cohort design: startups founded 2012 to 2019 can have long gaps only in later years.")


# 10. FIGURE 7: BY SECTOR
#####################################################################################################
fig, ax = plt.subplots(figsize=(8.3, 4.6))
s = sector.sort_values("exit", ascending=False)
s = s.assign(label=[f"{sec} (N = {thousands(n)})" for sec, n in zip(s.sector, s.n)])
sns.barplot(data=s, y="label", x="exit", hue="label", palette=[NAVY, STEEL, MIST, BEIGE, TAN, RUST, MUTED], legend=False, ax=ax, **EDGE)
label_bars(ax, lambda v: num(v))
overall(ax, vertical=True, loc="lower right")
ax.set(xlabel="Exit within 3 years (%)", ylabel="", xlim=(0, 18))
finish(fig, "fig7_by_sector", "Exit rate by sector", "The sector fixed effects absorb these differences in the main model.")


# 11. FIGURES 8 AND 9: CORRELATIONS
#####################################################################################################
# lower triangle only; colour = signed correlation (rust negative, navy positive), text = correlation with stars; the diagonal is left cream
def corr_fig(names, R, N, name, caption, note):
    k = len(names)
    M = np.full((k, k), np.nan)
    A = np.full((k, k), "", dtype=object)
    for i in range(k):
        for j in range(i + 1):
            M[i, j] = 0 if i == j else R[i][j]
            A[i, j] = "1" if i == j else num(R[i][j], 3) + stars(R[i][j], N[i][j])
    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    sns.heatmap(pd.DataFrame(M, index=names, columns=[f"({j + 1})" for j in range(k)]), annot=A, fmt="", cmap=DIV, vmin=-1, vmax=1, center=0,
                mask=np.isnan(M), linewidths=1.5, linecolor=CREAM, cbar_kws={"label": "Correlation"}, annot_kws={"fontsize": 10}, ax=ax)
    ax.set_yticks(np.arange(k) + 0.5, [f"({i + 1}) {n}" for i, n in enumerate(names)], rotation=0)
    ax.tick_params(length=0)
    finish(fig, name, caption, note)
SN = "*** p < 0.01, ** p < 0.05, * p < 0.10 (two-sided test of zero correlation)."
corr_fig(main_names, main_r, main_n, "fig8_corr_main", "Correlations of the main variables", "Pairwise Pearson correlations on the estimation sample (N = 8,204). " + SN)
corr_fig(hype_names, hype_r, hype_n, "fig9_corr_hype", "Correlations of the hype measures", "Pairwise correlations; the past-years heat has 7,823 startups, the lagged entry z and the hype index 8,179. " + SN)


# 12. SAVE
#####################################################################################################
with PdfPages(OUT / "rq1_descriptive_figures_color.pdf") as pdf:
    for f in FIGS: pdf.savefig(f)
print(f"{len(FIGS)} figures written to {OUT} (fonts: {TITLE_FONT}, {BODY_FONT})")
