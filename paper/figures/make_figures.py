"""Generate Experiment-section figures for CuraHarness paper.

All numbers are pulled verbatim from
    docs/EXPERIMENT_INSIGHTS.md
    docs/experiment_detail.md
of the MemoMemo repo (see paper README for the docs commit pinned).

Three figures:
    pareto_cost_quality.pdf   -- 2x2 cost-vs-test scatter
    breakthrough_rate.pdf     -- per-iter breakthrough rate by budget tier
    read_concentration.pdf    -- read distribution (bandit vs default+direction)
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# --- Nature-leaning rcParams: sans-serif, editable text, vector PDFs ---------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.linewidth"] = 0.7
plt.rcParams["axes.labelsize"] = 9
plt.rcParams["axes.titlesize"] = 10
plt.rcParams["xtick.labelsize"] = 8
plt.rcParams["ytick.labelsize"] = 8
plt.rcParams["legend.fontsize"] = 8
plt.rcParams["legend.frameon"] = False
plt.rcParams["figure.dpi"] = 150

# Okabe-Ito colorblind-safe palette
C_DEFAULT = "#3a3a3a"      # dark grey for default
C_BANDIT = "#0072B2"        # blue
C_PROGRESSIVE = "#D55E00"   # vermilion
C_RECENT = "#56B4E9"        # sky-blue
C_MIDDLE = "#009E73"        # bluish-green
C_EARLY = "#CC79A7"         # mauve


# ============================================================================
# Figure 1: Pareto cost vs quality
# ============================================================================
def fig_pareto():
    """4-panel scatter of total/propose vs best test, one per (bench, proposer)."""
    # (cell name, [(policy, total_per_propose_M, best_test)])
    cells = [
        ("LoCoMo / claudekimi", [
            ("default", 3.42, 0.3423),
            ("bandit", 2.63, 0.3616),
            ("progressive", 1.86, 0.3734),
        ]),
        ("LoCoMo / codex54", [
            ("default", 3.42, 0.3402),
            ("bandit", 2.14, 0.3865),
            ("progressive", 2.46, 0.3879),
        ]),
        ("LongMemEval / claudekimi", [
            ("default", 3.71, 0.5300),
            ("bandit", 2.55, 0.5450),
            ("progressive", 3.37, 0.5200),
        ]),
        ("LongMemEval / codex54", [
            ("default", 2.93, 0.5075),
            ("bandit", 2.18, 0.4725),
            ("progressive", 2.66, 0.5275),
        ]),
    ]

    style = {
        "default": dict(color=C_DEFAULT, marker="s", label="Full-context (default)",
                         short="default"),
        "progressive": dict(color=C_PROGRESSIVE, marker="o", label="Progressive (iter axis)",
                             short="Progressive"),
        "bandit": dict(color=C_BANDIT, marker="^", label="CuraHarness (iter + file)",
                        short="CuraHarness"),
    }

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.0), sharex=False, sharey=False)
    for ax, (title, points) in zip(axes.flat, cells):
        # arrow showing "favourable" direction (upper-left)
        for policy, x, y in points:
            s = style[policy]
            ax.scatter(x, y, s=85, edgecolor="black", linewidths=0.6,
                       zorder=3, color=s["color"], marker=s["marker"])
            ax.annotate(s["short"], xy=(x, y), xytext=(4, 4),
                        textcoords="offset points", fontsize=7,
                        color=s["color"])
        # find pareto frontier among the three points
        xs = [p[1] for p in points]
        ys = [p[2] for p in points]
        # compute pareto-favorable corner (lowest x, highest y of the 3)
        pareto_x = min(xs) - 0.15
        pareto_y = max(ys) + 0.005
        ax.annotate("", xy=(pareto_x, pareto_y),
                    xytext=(pareto_x + 0.7, pareto_y - 0.01),
                    arrowprops=dict(arrowstyle="->", color="grey",
                                    lw=0.8, alpha=0.7))
        ax.text(pareto_x + 0.05, pareto_y - 0.005, "Pareto-favourable",
                fontsize=6.5, color="grey", style="italic")

        ax.set_title(title, fontsize=9, pad=4)
        ax.set_xlabel("Tokens per propose  (M)")
        ax.set_ylabel("Best test passrate")
        ax.grid(True, ls=":", lw=0.4, color="grey", alpha=0.5)
        ax.set_xlim(min(xs) - 0.5, max(xs) + 0.6)
        ax.set_ylim(min(ys) - 0.02, max(ys) + 0.02)
        ax.tick_params(axis="both", which="both", length=2.5)

    handles = [Line2D([0], [0], marker=s["marker"], color="w",
                       markerfacecolor=s["color"], markeredgecolor="black",
                       markersize=8, label=s["label"])
               for s in style.values()
               if "label" in s]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, -0.02), fontsize=8)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig("pareto_cost_quality.pdf", bbox_inches="tight")
    fig.savefig("pareto_cost_quality.svg", bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Figure 2: Breakthrough rate by budget x iter range
# ============================================================================
def fig_breakthrough_rate():
    """Grouped bar chart: warm-up (iters 1-5) vs late (iters 6-30) breakthrough rates."""
    # Counts derived from EXPERIMENT_INSIGHTS:
    #   full horizon by tier (auto-budget, n=17): low 22, med 19, high 31 (total 72)
    #     iters by tier (auto-budget): low 62, med 156, high 292 (total 510)
    #   post-iter-5 by tier: brk 3/4/31 over 17/116/292 iters
    #   warm-up by tier (full - post5): brk 19/15/0 over 45/40/0 iters
    groups = {
        "Warm-up\n(iters 1-5)": {
            "low": (19, 45),
            "medium": (15, 40),
            "high": (0, 0),     # no exposure
        },
        "Late horizon\n(iters 6-30)": {
            "low": (3, 17),
            "medium": (4, 116),
            "high": (31, 292),
        },
    }
    tiers = ["low", "medium", "high"]
    colors = {
        "low":     "#9ecae1",
        "medium":  "#4292c6",
        "high":    "#08519c",
    }

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    width = 0.24
    xs = np.arange(len(groups))
    for i, tier in enumerate(tiers):
        rates = []
        labels = []
        for grp, vals in groups.items():
            brk, n = vals[tier]
            rate = (brk / n * 100) if n > 0 else np.nan
            rates.append(rate)
            labels.append(f"{brk}/{n}")
        offset = (i - 1) * width
        bars = ax.bar(xs + offset, rates, width=width,
                       color=colors[tier], edgecolor="black",
                       linewidth=0.5, label=tier)
        # annotate counts above bars; for NaN show "no exp."
        for j, (b, lbl, r) in enumerate(zip(bars, labels, rates)):
            if np.isnan(r):
                ax.text(b.get_x() + b.get_width() / 2, 1.0,
                        "no\nexposure", ha="center", va="bottom",
                        fontsize=6.5, color="grey", style="italic")
            else:
                ax.text(b.get_x() + b.get_width() / 2, r + 0.6,
                        lbl, ha="center", va="bottom", fontsize=6.5,
                        color="black")

    ax.set_xticks(xs)
    ax.set_xticklabels(list(groups.keys()))
    ax.set_ylabel("Per-iter breakthrough rate  (%)")
    ax.set_ylim(0, max(50, ax.get_ylim()[1]))
    ax.legend(title="Budget tier", loc="upper right",
              ncol=1, fontsize=7.5, title_fontsize=8)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig("breakthrough_rate.pdf", bbox_inches="tight")
    fig.savefig("breakthrough_rate.svg", bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Figure 3: Read concentration -- bandit best/worst/other vs default+dir recency
# ============================================================================
def fig_read_concentration():
    """Two-panel grouped bar: bandit best-tag concentration | default+dir recency bias."""
    # Left panel: bandit reads/slot by bucket per run
    bandit_runs = ["banditfix\nr1", "banditfix\nr2", "v4\nr1"]
    bandit_data = {
        "best-iter dirs":  [3.67, 2.70, 3.45],
        "worst-iter dir":  [0.12, 0.22, 0.44],
        "other ref dirs":  [0.17, 0.13, 0.25],
    }
    # Right panel: default+direction reads/slot by recency bucket per run
    dd_runs = ["LME\n(015454)", "LME\n(152524)", "LoCoMo\n(015441)"]
    dd_data = {
        "recent (last 3)":  [2.24, 2.23, 2.93],
        "middle":           [0.31, 0.68, 0.39],
        "early (first 3)":  [0.04, 0.01, 0.09],
    }

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.3), sharey=True)

    # Left
    ax = axes[0]
    width = 0.25
    xs = np.arange(len(bandit_runs))
    bandit_colors = {
        "best-iter dirs":  C_BANDIT,
        "worst-iter dir":  "#9bbcd1",
        "other ref dirs":  "#cccccc",
    }
    for i, (label, vals) in enumerate(bandit_data.items()):
        offset = (i - 1) * width
        bars = ax.bar(xs + offset, vals, width=width,
                       color=bandit_colors[label], edgecolor="black",
                       linewidth=0.5, label=label)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.06,
                    f"{v:.2f}", ha="center", va="bottom",
                    fontsize=6.5, color="black")
    ax.set_xticks(xs)
    ax.set_xticklabels(bandit_runs)
    ax.set_ylabel("Reads per available slot")
    ax.set_title("Bandit (LongMemEval, claudekimi)", fontsize=9, pad=4)
    ax.legend(loc="upper right", fontsize=7)
    ax.set_ylim(0, 4.3)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.5)
    ax.set_axisbelow(True)

    # Right
    ax = axes[1]
    xs = np.arange(len(dd_runs))
    dd_colors = {
        "recent (last 3)":  C_RECENT,
        "middle":           C_MIDDLE,
        "early (first 3)":  C_EARLY,
    }
    for i, (label, vals) in enumerate(dd_data.items()):
        offset = (i - 1) * width
        bars = ax.bar(xs + offset, vals, width=width,
                       color=dd_colors[label], edgecolor="black",
                       linewidth=0.5, label=label)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.06,
                    f"{v:.2f}", ha="center", va="bottom",
                    fontsize=6.5, color="black")
    ax.set_xticks(xs)
    ax.set_xticklabels(dd_runs)
    ax.set_title("Default+direction (no labels)", fontsize=9, pad=4)
    ax.legend(loc="upper right", fontsize=7)
    ax.set_ylim(0, 4.3)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.5)
    ax.set_axisbelow(True)

    fig.suptitle("Reads per available reference-iter slot", fontsize=10, y=1.02)
    fig.tight_layout()
    fig.savefig("read_concentration.pdf", bbox_inches="tight")
    fig.savefig("read_concentration.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_pareto()
    fig_read_concentration()
    # fig_breakthrough_rate() retained for reference but not referenced in
    # the current Experiments section -- the warm-up vs late narrative was
    # dropped because data does not support a "low/medium still useful
    # after iter 5" claim (medium hits 3.4% post-iter-5).
    print("Generated: pareto_cost_quality.pdf, read_concentration.pdf")
