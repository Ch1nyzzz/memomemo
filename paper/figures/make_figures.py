"""Generate Experiment-section figures for CuraHarness paper.

All numbers are pulled verbatim from
    docs/EXPERIMENT_INSIGHTS.md
    docs/experiment_detail.md
of the MemoMemo repo (see paper README for the docs commit pinned).

Two active figures, each defending one experimental claim of Experiments.tex:

    optimization_effect.{pdf,svg}
        Grouped bars of held-out passrate gain relative to full-context.

    pareto_cost_quality.{pdf,svg}
        Single-panel scatter of (delta cost %, delta test pp) versus
        the default-family baseline. Each marker = one (benchmark,
        proposer, policy) triple, taken from the single best-by-test
        retained run in that cell. Default sits at the origin.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

# ------------------------------------------------------------------
# Nature-leaning rcParams: editable text, restrained spines/grids.
# ------------------------------------------------------------------
plt.rcParams.update({
    "font.family":          "sans-serif",
    "font.sans-serif":      ["Arial", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype":         "none",
    "pdf.fonttype":         42,
    "ps.fonttype":          42,
    "axes.spines.top":      False,
    "axes.spines.right":    False,
    "axes.linewidth":       0.7,
    "axes.labelsize":       8.5,
    "axes.titlesize":       9,
    "xtick.labelsize":      7.5,
    "ytick.labelsize":      7.5,
    "legend.fontsize":      7.5,
    "legend.frameon":       False,
    "figure.dpi":           150,
})

# Restrained palette: one neutral family for default, one signal
# family for the two adaptive policies. Okabe-Ito-derived, accessible.
C_DEFAULT     = "#3a3a3a"     # neutral grey for the default origin marker
C_PROGRESSIVE = "#D55E00"     # vermilion for iter-axis only
C_BANDIT      = "#0072B2"     # blue for iter+file (CuraHarness)
C_RECENT      = "#56B4E9"     # sky for default+direction recency bucket
C_PAREGION    = "#e8f4ea"     # very pale green wash for Pareto-favorable region


# ============================================================================
# Figure 0: Optimization effect, grouped bars
# ============================================================================
def fig_optimization_effect():
    """Grouped bars: Δmean test pp (left axis) + token savings % (right axis).

    Both axes are oriented so that higher = better, so a cell where a
    policy beats default on both quality and cost shows two markers above
    zero on the same vertical strip.
    """
    cells = [
        "LoCoMo\n/kimi",
        "LoCoMo\n/codex",
        "LongMem\n/kimi",
        "LongMem\n/codex",
        "SWE\n/kimi",
    ]
    # Δ mean test pp (cell mean across retained runs - default-family mean).
    # Source: docs/experiment_detail.md per-cell test mean rows.
    progressive_test = np.array([+2.30, +4.30, +0.67, +0.25, +16.20])
    cura_test        = np.array([+2.39, +2.46, +1.17, -3.42, +18.20])

    # Token savings % vs default-family best-by-test total/propose
    # (positive = cheaper). Sign-flipped from pareto figure's dcost%.
    progressive_save = np.array([+45.6, +28.1, +9.2, +9.2, -17.4])
    cura_save        = np.array([+23.1, +37.4, +31.3, +25.6, -9.0])

    xs = np.arange(len(cells))
    width = 0.36
    fig, ax = plt.subplots(figsize=(6.0, 3.4))

    bars_p = ax.bar(
        xs - width / 2,
        progressive_test,
        width,
        color=C_PROGRESSIVE,
        edgecolor="black",
        linewidth=0.5,
        label="Progressive",
    )
    bars_c = ax.bar(
        xs + width / 2,
        cura_test,
        width,
        color=C_BANDIT,
        edgecolor="black",
        linewidth=0.5,
        label="CuraHarness",
    )

    ax.axhline(0, color="grey", lw=0.7, ls="--", alpha=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels(cells)
    ax.set_ylabel(r"$\Delta$ mean test passrate vs full-context (pp)")
    ax.set_ylim(-5.5, 21)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.45)
    ax.set_axisbelow(True)

    for bars in (bars_p, bars_c):
        for bar in bars:
            value = bar.get_height()
            va = "bottom" if value >= 0 else "top"
            dy = 0.45 if value >= 0 else -0.45
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + dy,
                f"{value:+.1f}",
                ha="center",
                va=va,
                fontsize=6.8,
            )

    # Right axis: token savings % (positive = cheaper than full-context).
    ax2 = ax.twinx()
    ax2.spines["top"].set_visible(False)
    ax2.set_ylabel("Token savings vs full-context (%)")
    ax2.set_ylim(-30, 60)

    ax2.scatter(
        xs - width / 2,
        progressive_save,
        marker="D",
        s=34,
        facecolor="white",
        edgecolor=C_PROGRESSIVE,
        linewidth=1.1,
        zorder=5,
        label="Progressive savings",
    )
    ax2.scatter(
        xs + width / 2,
        cura_save,
        marker="D",
        s=34,
        facecolor="white",
        edgecolor=C_BANDIT,
        linewidth=1.1,
        zorder=5,
        label="CuraHarness savings",
    )

    for x, v in zip(xs - width / 2, progressive_save):
        ax2.text(x, v + (1.6 if v >= 0 else -1.6), f"{v:+.0f}%",
                 ha="center", va="bottom" if v >= 0 else "top",
                 fontsize=6.4, color=C_PROGRESSIVE)
    for x, v in zip(xs + width / 2, cura_save):
        ax2.text(x, v + (1.6 if v >= 0 else -1.6), f"{v:+.0f}%",
                 ha="center", va="bottom" if v >= 0 else "top",
                 fontsize=6.4, color=C_BANDIT)

    # Combined legend: bar handles for test-pp, marker handles for savings.
    save_p = Line2D([0], [0], marker="D", color=C_PROGRESSIVE,
                    markerfacecolor="white", markersize=6, linewidth=0,
                    label="Progressive savings")
    save_c = Line2D([0], [0], marker="D", color=C_BANDIT,
                    markerfacecolor="white", markersize=6, linewidth=0,
                    label="CuraHarness savings")
    ax.legend(handles=[bars_p, bars_c, save_p, save_c],
              loc="upper left", ncol=2, fontsize=7)

    fig.tight_layout()
    fig.savefig("optimization_effect.pdf", bbox_inches="tight")
    fig.savefig("optimization_effect.svg", bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Figure 1: Pareto cost vs quality, single panel, delta-vs-default coords
# ============================================================================
def fig_pareto():
    """Single panel scatter on (delta cost %, delta best-test pp) coords."""
    # ----- data -----------------------------------------------------------
    # Each row: cell, proposer-suffix, policy, dcost%, dtest_pp.
    # Numbers are computed from EXPERIMENT_INSIGHTS / experiment_detail
    # against each cell's default-family best-by-test row.
    points = [
        # LoCoMo / claudekimi:  default 3.42M, 0.342
        ("LoCoMo",       "claudekimi", "Progressive",  -45.6, +3.1),
        ("LoCoMo",       "claudekimi", "Bandit",       -23.1, +2.0),
        # LoCoMo / codex54:     default 3.42M, 0.340
        ("LoCoMo",       "codex54",    "Progressive",  -28.1, +4.8),
        ("LoCoMo",       "codex54",    "Bandit",       -37.4, +4.7),
        # LongMemEval / claudekimi: default 3.71M, 0.530
        ("LongMemEval",  "claudekimi", "Progressive",   -9.2, -1.0),
        ("LongMemEval",  "claudekimi", "Bandit",       -31.3, +1.5),
        # LongMemEval / codex54:    default 2.93M, 0.508
        ("LongMemEval",  "codex54",    "Progressive",   -9.2, +2.0),
        ("LongMemEval",  "codex54",    "Bandit",       -25.6, -3.5),
        # SWE-bench Verified / claudekimi: default 3.22M, 0.458 verified
        ("SWE-bench",    "claudekimi", "Progressive",  +17.4, +16.2),
        ("SWE-bench",    "claudekimi", "Bandit",        +9.0, +18.2),
    ]

    # marker shape encodes (benchmark, proposer); color encodes policy
    marker_for = {
        ("LoCoMo",      "claudekimi"): "o",
        ("LoCoMo",      "codex54"):    "s",
        ("LongMemEval", "claudekimi"): "D",
        ("LongMemEval", "codex54"):    "^",
        ("SWE-bench",   "claudekimi"): "*",
    }
    color_for = {
        "Progressive": C_PROGRESSIVE,
        "Bandit":      C_BANDIT,
    }

    fig, ax = plt.subplots(figsize=(5.5, 3.6))

    # ----- background regions -------------------------------------------
    # Pareto-favorable = upper-left (delta cost <= 0, delta test >= 0).
    ax.axhspan(-100, 100, xmin=0, xmax=0.5, facecolor=C_PAREGION,
               alpha=0.0)  # placeholder so shading respects later xlim
    # we draw the actual rectangle after lim is set, see below

    # zero crosshairs through the default origin
    ax.axhline(0, color="grey", lw=0.7, ls="--", alpha=0.6, zorder=1)
    ax.axvline(0, color="grey", lw=0.7, ls="--", alpha=0.6, zorder=1)

    # ----- scatter ------------------------------------------------------
    for bench, prop, policy, dx, dy in points:
        m = marker_for[(bench, prop)]
        c = color_for[policy]
        # SWE-bench gets a slightly larger * marker since the shape
        # is visually thinner than D / ^ at equal s value
        s = 110 if m == "*" else 70
        ax.scatter(dx, dy, marker=m, s=s, color=c,
                   edgecolor="black", linewidths=0.55, zorder=4)

    # default origin marker (the baseline anchor)
    ax.scatter(0, 0, marker="X", s=80, color=C_DEFAULT,
               edgecolor="black", linewidths=0.6, zorder=5)
    ax.annotate("default\n(baseline)", xy=(0, 0), xytext=(6, 6),
                textcoords="offset points", fontsize=7.0,
                color=C_DEFAULT)

    # ----- annotate one cell label per (bench, proposer) pair -----------
    # Pick the geometrically more visible point of the two policies in
    # each cell so the label sits cleanly. Cell color = neutral grey
    # because the label refers to the cell, not to a single policy.
    cell_label_anchor = {
        # (bench, proposer): which policy point to anchor on, plus
        # (dx_pt, dy_pt, ha) text offset.
        ("LoCoMo",      "claudekimi"): ("Progressive",  +6, +6, "left"),
        ("LoCoMo",      "codex54"):    ("Bandit",       -5, +6, "right"),
        ("LongMemEval", "claudekimi"): ("Bandit",       -5, +5, "right"),
        ("LongMemEval", "codex54"):    ("Bandit",       +5, -8, "left"),
        ("SWE-bench",   "claudekimi"): ("Bandit",      +10, +2, "left"),
    }
    points_by_key = {(b, p, pol): (dx, dy)
                     for b, p, pol, dx, dy in points}
    for (bench, prop), (anchor_pol, ox, oy, ha) in cell_label_anchor.items():
        dx, dy = points_by_key[(bench, prop, anchor_pol)]
        short = {"claudekimi": "/kimi", "codex54": "/codex"}[prop]
        ax.annotate(f"{bench}{short}", xy=(dx, dy),
                    xytext=(ox, oy), textcoords="offset points",
                    fontsize=6.6, color="#444444", ha=ha)

    # axis range and Pareto-favorable wash --------------------------------
    ax.set_xlim(-52, 28)
    ax.set_ylim(-7.0, 23)
    # Now that lim is fixed, draw the Pareto-favorable rectangle
    ax.add_patch(Rectangle((-52, 0), 52, 23,
                            facecolor=C_PAREGION, alpha=0.7,
                            edgecolor="none", zorder=0))
    ax.text(-50, 22, "Pareto-favorable (less cost, higher score)",
            fontsize=6.4, color="#3d6f4d", style="italic",
            ha="left", va="top")

    # axes / labels ------------------------------------------------------
    ax.set_xlabel(r"$\Delta$ tokens per propose vs default  (%)")
    ax.set_ylabel(r"$\Delta$ best test passrate vs default  (pp)")
    ax.tick_params(axis="both", which="both", length=2.5)
    ax.grid(True, ls=":", lw=0.4, color="grey", alpha=0.4)
    ax.set_axisbelow(True)

    # legend: split into two stacked groups (policy color + cell shape) --
    policy_handles = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=C_PROGRESSIVE, markeredgecolor="black",
               markersize=7, label="Progressive (iter axis)"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=C_BANDIT, markeredgecolor="black",
               markersize=7, label="CuraHarness (iter + file)"),
        Line2D([0], [0], marker="X", color="w",
               markerfacecolor=C_DEFAULT, markeredgecolor="black",
               markersize=7, label="default-family"),
    ]
    cell_handles = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=7, label="LoCoMo / kimi"),
        Line2D([0], [0], marker="s", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=7, label="LoCoMo / codex"),
        Line2D([0], [0], marker="D", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=6.5, label="LongMemEval / kimi"),
        Line2D([0], [0], marker="^", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=7, label="LongMemEval / codex"),
        Line2D([0], [0], marker="*", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=9, label="SWE-bench / kimi"),
    ]
    leg1 = ax.legend(handles=policy_handles, loc="lower left",
                      bbox_to_anchor=(1.01, 0.55), title="Policy",
                      title_fontsize=8, fontsize=7.2, borderaxespad=0)
    ax.add_artist(leg1)
    ax.legend(handles=cell_handles, loc="lower left",
              bbox_to_anchor=(1.01, 0.0), title="Benchmark / proposer",
              title_fontsize=8, fontsize=7.2, borderaxespad=0)

    fig.tight_layout(rect=[0, 0, 0.78, 1])
    fig.savefig("pareto_cost_quality.pdf", bbox_inches="tight")
    fig.savefig("pareto_cost_quality.svg", bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Figure 2: Read concentration -- bandit best/worst/other vs default recency
# ============================================================================
def fig_read_concentration():
    """Single-panel grouped bar with bandit and default+dir on same Y axis.

    All numbers are mean across three retained runs per policy
    (EXPERIMENT_INSIGHTS Reference-Iteration Read Distribution).
    """
    # bandit (3 runs): bandit_v3_banditfix r1/r2 + bandit_v4 r1
    bandit_best  = np.mean([3.67, 2.70, 3.45])    # 3.273
    bandit_worst = np.mean([0.12, 0.22, 0.44])    # 0.260
    bandit_other = np.mean([0.17, 0.13, 0.25])    # 0.183
    # default+direction (3 runs): LME 015454 / 152524 + LoCoMo 015441
    dd_recent  = np.mean([2.24, 2.23, 2.93])      # 2.467
    dd_middle  = np.mean([0.31, 0.68, 0.39])      # 0.460
    dd_early   = np.mean([0.04, 0.01, 0.09])      # 0.047

    # report range as error bars to show run-to-run spread
    bandit_best_err  = np.array([[3.273 - 2.70], [3.67 - 3.273]])
    bandit_worst_err = np.array([[0.260 - 0.12], [0.44 - 0.260]])
    bandit_other_err = np.array([[0.183 - 0.13], [0.25 - 0.183]])
    dd_recent_err    = np.array([[2.467 - 2.23], [2.93 - 2.467]])
    dd_middle_err    = np.array([[0.460 - 0.31], [0.68 - 0.460]])
    dd_early_err     = np.array([[0.047 - 0.01], [0.09 - 0.047]])

    fig, ax = plt.subplots(figsize=(6.0, 3.5))

    # 6 bars on a shared X axis, grouped into two policy clusters
    labels = [
        "best\n(labelled)",
        "worst\n(labelled)",
        "other\n(unlabelled)",
        "recent\n(last 3)",
        "middle\n(iters 4-N-3)",
        "early\n(first 3)",
    ]
    values = [bandit_best, bandit_worst, bandit_other,
              dd_recent, dd_middle, dd_early]
    errs = np.hstack([bandit_best_err, bandit_worst_err, bandit_other_err,
                       dd_recent_err, dd_middle_err, dd_early_err])
    colors = [C_BANDIT, "#9bbcd1", "#cccccc",
              C_RECENT, "#9dd2bf", "#e1c4d4"]

    xs = np.arange(len(labels))
    bars = ax.bar(xs, values, yerr=errs, capsize=2.5,
                   color=colors, edgecolor="black", linewidth=0.5,
                   error_kw=dict(elinewidth=0.6, ecolor="black"))

    # value annotations
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.08,
                f"{v:.2f}", ha="center", va="bottom",
                fontsize=6.8, color="black")

    # group separator + group titles, sitting just above the plot area
    ax.axvline(2.5, color="grey", lw=0.6, ls=":", alpha=0.7, zorder=1)
    ax.text(1.0, 4.65, "CuraHarness (bandit)",
            ha="center", va="bottom", fontsize=8.0, color=C_BANDIT,
            fontweight="bold")
    ax.text(1.0, 4.42, "bucket by policy label",
            ha="center", va="bottom", fontsize=6.8, color=C_BANDIT,
            style="italic")
    ax.text(4.0, 4.65, "default+direction",
            ha="center", va="bottom", fontsize=8.0, color="#1f6e9c",
            fontweight="bold")
    ax.text(4.0, 4.42, "bucket by recency",
            ha="center", va="bottom", fontsize=6.8, color="#1f6e9c",
            style="italic")

    # the headline 14-22x annotation, anchored on the bandit-best bar
    ax.annotate(
        "best dirs absorb 14--22x more\nreads/slot than unlabelled refs",
        xy=(0.4, bandit_best), xytext=(1.05, 3.30),
        fontsize=6.8, color=C_BANDIT,
        ha="left", va="top",
        arrowprops=dict(arrowstyle="-", color=C_BANDIT, lw=0.6, alpha=0.7),
    )

    # axes
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=6.8)
    ax.set_ylabel("Reads per available reference-iter slot")
    ax.set_ylim(0, 5.0)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", which="both", length=0)
    ax.tick_params(axis="y", which="both", length=2.5)

    fig.tight_layout()
    fig.savefig("read_concentration.pdf", bbox_inches="tight")
    fig.savefig("read_concentration.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_optimization_effect()
    fig_pareto()
    print("Generated: optimization_effect.{pdf,svg}, pareto_cost_quality.{pdf,svg}")
