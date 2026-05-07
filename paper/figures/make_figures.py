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
    """Three-bar mirror chart per cell.

    Upper half (left y-axis): mean test passrate, bars going up.
    Lower half (right y-axis): token consumption per propose (M tokens),
    bars going down.

    Three policies side-by-side: full-context baseline, Progressive,
    CuraHarness. Both axes share y=0 so the same vertical strip shows
    quality on top and cost on bottom for the same (cell, policy).
    """
    cells = [
        "LoCoMo\n/kimi",
        "LoCoMo\n/codex",
        "LongMem\n/kimi",
        "LongMem\n/codex",
        "SWE\n/kimi",
    ]
    # Mean test passrate per cell (default-family / progressive / cura mean
    # across retained runs). Source: docs/experiment_detail.md.
    # SWE row is single docs-only run (mean = the single value).
    baseline_test    = np.array([0.3315, 0.3308, 0.4883, 0.4867, 0.4580])
    progressive_test = np.array([0.3545, 0.3738, 0.5050, 0.4992, 0.6200])
    cura_test        = np.array([0.3554, 0.3554, 0.5100, 0.4625, 0.6400])

    # Token consumption per propose (M tokens), best-by-test row per cell.
    baseline_tok    = np.array([3.42, 3.42, 3.71, 2.93, 3.22])
    progressive_tok = np.array([1.86, 2.46, 3.37, 2.66, 3.78])
    cura_tok        = np.array([2.63, 2.14, 2.55, 2.18, 3.51])

    xs = np.arange(len(cells))
    width = 0.26
    offsets = np.array([-width, 0.0, +width])

    # Local palette for this figure: muted Tol-light trio, colorblind-safe
    # and softer than the global vermilion/blue used in the Pareto figure.
    col_baseline = "#BBBBBB"   # soft cool grey
    col_prog     = "#EE8866"   # warm coral
    col_cura     = "#4477AA"   # muted steel blue

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax2 = ax.twinx()

    # Upper half: mean test passrate
    bars_b = ax.bar(xs + offsets[0], baseline_test, width,
                    color=col_baseline, edgecolor="black", linewidth=0.5,
                    label="Full-context baseline")
    bars_p = ax.bar(xs + offsets[1], progressive_test, width,
                    color=col_prog, edgecolor="black", linewidth=0.5,
                    label="Progressive")
    bars_c = ax.bar(xs + offsets[2], cura_test, width,
                    color=col_cura, edgecolor="black", linewidth=0.5,
                    label="CuraHarness")

    # Lower half: token consumption (drawn as negative on ax2 so bars go down)
    ax2.bar(xs + offsets[0], -baseline_tok, width,
            color=col_baseline, edgecolor="black", linewidth=0.5, alpha=0.85)
    ax2.bar(xs + offsets[1], -progressive_tok, width,
            color=col_prog, edgecolor="black", linewidth=0.5, alpha=0.85)
    ax2.bar(xs + offsets[2], -cura_tok, width,
            color=col_cura, edgecolor="black", linewidth=0.5, alpha=0.85)

    # Symmetric limits sharing y=0
    ax.set_ylim(-0.80, 0.80)
    ax2.set_ylim(-4.5, 4.5)  # in M tokens; 0 aligned with ax

    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(cells, fontsize=10)
    ax.set_ylabel("Mean test passrate                                   ",
                  fontsize=11)
    ax2.set_ylabel("                                   Token consumption (M / propose)",
                   fontsize=11)
    ax.tick_params(axis="y", labelsize=9.5)
    ax2.tick_params(axis="y", labelsize=9.5)
    ax.grid(True, axis="y", ls=":", lw=0.4, color="grey", alpha=0.45)
    ax.set_axisbelow(True)

    # Hide negative y-tick labels on ax (lower half belongs to ax2)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8])
    # Hide positive y-tick labels on ax2 (upper half belongs to ax); show
    # token magnitudes as positive numbers in lower half.
    ax2.set_yticks([-4, -3, -2, -1, 0])
    ax2.set_yticklabels(["4", "3", "2", "1", "0"])

    # Value labels
    for offset, vals in zip(offsets, (baseline_test, progressive_test, cura_test)):
        for x, v in zip(xs + offset, vals):
            ax.text(x, v + 0.012, f"{v:.2f}",
                    ha="center", va="bottom", fontsize=8.2)
    for offset, vals in zip(offsets, (baseline_tok, progressive_tok, cura_tok)):
        for x, v in zip(xs + offset, vals):
            ax2.text(x, -v - 0.08, f"{v:.2f}",
                     ha="center", va="top", fontsize=8.2)

    # Section labels on the y-axis
    ax.text(-0.55, 0.40, "quality ↑", rotation=90, va="center", ha="center",
            fontsize=9.5, color="#444444", style="italic")
    ax.text(-0.55, -0.40, "cost ↓ (better)", rotation=90, va="center",
            ha="center", fontsize=9.5, color="#444444", style="italic")

    ax.legend(handles=[bars_b, bars_p, bars_c],
              loc="upper right", ncol=3, fontsize=9.5)

    fig.tight_layout()
    fig.savefig("optimization_effect.pdf", bbox_inches="tight")
    fig.savefig("optimization_effect.svg", bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Figure 1: Cost--quality shifts as arrows from full-context baseline
# ============================================================================
# Shared data table. Each row: bench, proposer, policy, dcost%, dtest_pp,
# computed against each cell's default-family best-by-test run.
PARETO_POINTS = [
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

# Proposer marker (open vs filled head differentiates proposers within a panel)
PROP_MARKER = {"claudekimi": "o", "codex54": "s"}
PROP_LABEL  = {"claudekimi": "kimi", "codex54": "codex"}
POLICY_COLOR = {"Progressive": C_PROGRESSIVE, "Bandit": C_BANDIT}
POLICY_LABEL = {"Progressive": "Stage 1: CuraHarness-Iter",
                "Bandit":      "Stage 2: CuraHarness-Full"}

BENCH_TAG = {"LoCoMo": "Lo", "LongMemEval": "LME", "SWE-bench": "SWE"}


def _draw_frame(ax, xlim, ylim, show_quadrant_labels=True,
                pareto_label_pos="top-left"):
    """Soft upper-left wash + zero axes; only two corner labels."""
    x0, x1 = xlim
    y0, y1 = ylim
    if x0 < 0:
        ax.add_patch(Rectangle((x0, 0), -x0, y1,
                               facecolor=C_PAREGION, alpha=0.45,
                               edgecolor="none", zorder=0))
    ax.axhline(0, color="grey", lw=0.5, ls="--", alpha=0.55, zorder=1)
    ax.axvline(0, color="grey", lw=0.5, ls="--", alpha=0.55, zorder=1)
    if show_quadrant_labels:
        pad_x = 0.02 * (x1 - x0)
        pad_y = 0.03 * (y1 - y0)
        if x0 < 0:
            if pareto_label_pos == "bottom-left":
                # Inside the Pareto-improving (upper-left) region but at its
                # bottom edge so it sits above y=0 yet below the Stage legend.
                ax.text(x0 + pad_x, 0 + pad_y, "Pareto-improving region",
                        ha="left", va="bottom",
                        fontsize=9.5, color="#3d6f4d", style="italic",
                        alpha=0.85)
            else:
                ax.text(x0 + pad_x, y1 - pad_y, "Pareto-improving",
                        ha="left", va="top",
                        fontsize=9.5, color="#3d6f4d", style="italic",
                        alpha=0.85)
        if x1 > 0:
            ax.text(x1 - pad_x, y1 - pad_y, "Quality--cost trade-off",
                    ha="right", va="top",
                    fontsize=9.5, color="#7a5a18", style="italic", alpha=0.75)


def _draw_point(ax, dx, dy, color, marker, label=None):
    """Light grey guide line from origin + the point."""
    ax.plot([0, dx], [0, dy], color="0.78", lw=0.7, alpha=0.7, zorder=1)
    ax.scatter(dx, dy, marker=marker, s=85, color=color,
               edgecolor="black", linewidths=0.6, zorder=4)
    if label is not None:
        ax.annotate(label, xy=(dx, dy), xytext=(6, 5),
                    textcoords="offset points",
                    fontsize=8.5, color="#333333")


def _draw_origin(ax):
    ax.scatter(0, 0, marker="X", s=85, color=C_DEFAULT,
               edgecolor="black", linewidths=0.6, zorder=5)


def _pareto_frontier(points):
    """Return non-dominated points (upper-left preferred: smaller x, larger y).

    Includes the origin (0, 0) so the frontier is always anchored.
    """
    pts = sorted(points + [(0.0, 0.0)], key=lambda p: (p[0], -p[1]))
    frontier = []
    best_y = -float("inf")
    for x, y in pts:
        if y > best_y:
            frontier.append((x, y))
            best_y = y
    return frontier


def _draw_frontier(ax, xy_pairs):
    front = _pareto_frontier(xy_pairs)
    if len(front) >= 2:
        xs = [p[0] for p in front]
        ys = [p[1] for p in front]
        ax.plot(xs, ys, color="black", lw=0.9, ls="--",
                alpha=0.55, zorder=2)


def _panel(ax, rows, xlim, ylim, title, show_ylabel,
           label_each_point=False, draw_frontier=True,
           frontier_per_bench=True, pareto_label_pos="top-left"):
    _draw_frame(ax, xlim, ylim, pareto_label_pos=pareto_label_pos)
    by_bench = {}
    for bench, prop, policy, dx, dy in rows:
        lab = BENCH_TAG[bench] if label_each_point else None
        _draw_point(ax, dx, dy,
                    color=POLICY_COLOR[policy],
                    marker=PROP_MARKER[prop],
                    label=lab)
        by_bench.setdefault(bench, []).append((dx, dy))
    if draw_frontier:
        if frontier_per_bench:
            for _bench, xy in by_bench.items():
                _draw_frontier(ax, xy)
        else:
            _draw_frontier(ax, [p for xy in by_bench.values() for p in xy])
    _draw_origin(ax)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(r"$\Delta$ tokens / propose vs full-context (%)",
                  fontsize=11)
    if show_ylabel:
        ax.set_ylabel(r"$\Delta$ best test passrate (pp)", fontsize=11)
    ax.set_title(title, fontsize=12, pad=5)
    ax.tick_params(axis="both", which="both", length=3, labelsize=10)
    ax.grid(True, ls=":", lw=0.4, color="grey", alpha=0.3)
    ax.set_axisbelow(True)


def _stage_legend_handles():
    return [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=POLICY_COLOR["Progressive"],
               markeredgecolor="black", markersize=9,
               label=POLICY_LABEL["Progressive"]),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=POLICY_COLOR["Bandit"],
               markeredgecolor="black", markersize=9,
               label=POLICY_LABEL["Bandit"]),
    ]


def _marker_legend_handles():
    return [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=9, label="kimi"),
        Line2D([0], [0], marker="s", color="w",
               markerfacecolor="lightgrey", markeredgecolor="black",
               markersize=9, label="codex"),
        Line2D([0], [0], marker="X", color="w",
               markerfacecolor=C_DEFAULT, markeredgecolor="black",
               markersize=9, label="full-context"),
    ]


def _add_in_axes_stage_legend(ax, loc="upper left",
                              bbox=(0.012, 0.985)):
    leg = ax.legend(handles=_stage_legend_handles(),
                    loc=loc, bbox_to_anchor=bbox,
                    title="Stage", title_fontsize=10, fontsize=9.5,
                    frameon=True, framealpha=0.9, edgecolor="0.7",
                    borderaxespad=0)
    leg.set_zorder(6)
    ax.add_artist(leg)


def fig_pareto_two_panel():
    """Two-panel Pareto figure: (a) memory benchmarks, (b) SWE-bench."""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6),
                             gridspec_kw=dict(width_ratios=[1.25, 1.0]))

    mem_rows = [r for r in PARETO_POINTS if r[0] in ("LoCoMo", "LongMemEval")]
    swe_rows = [r for r in PARETO_POINTS if r[0] == "SWE-bench"]

    _panel(axes[0], mem_rows,
           xlim=(-55, 6), ylim=(-6, 8),
           title="(a) Memory benchmarks",
           show_ylabel=True, label_each_point=True,
           draw_frontier=True, frontier_per_bench=True,
           pareto_label_pos="bottom-left")
    _panel(axes[1], swe_rows,
           xlim=(-4, 24), ylim=(-2, 22),
           title="(b) SWE-bench Verified",
           show_ylabel=False, label_each_point=False,
           draw_frontier=True, frontier_per_bench=True)

    # Stage legend: upper-left of memory panel; lower-right of SWE panel
    # (memory's upper-left is empty space; SWE's upper-left is where the
    # Stage 2 point sits, so the legend goes to the lower-right corner).
    _add_in_axes_stage_legend(axes[0], loc="upper left",
                              bbox=(0.012, 0.985))
    _add_in_axes_stage_legend(axes[1], loc="lower right",
                              bbox=(0.985, 0.015))

    # Marker legend at the bottom of the figure.
    fig.legend(handles=_marker_legend_handles(), loc="lower center",
               bbox_to_anchor=(0.5, -0.04), ncol=3,
               title="Marker", title_fontsize=10, fontsize=9.5,
               frameon=False, borderaxespad=0)

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig("pareto_cost_quality.pdf", bbox_inches="tight")
    fig.savefig("pareto_cost_quality.svg", bbox_inches="tight")
    plt.close(fig)


def fig_pareto_single():
    """Compact single-panel version (slides / single column).

    Note: frontier is drawn per-benchmark to avoid mixing different
    benchmarks' passrate scales.
    """
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    xlim = (-55, 24)
    ylim = (-7, 22)
    _panel(ax, PARETO_POINTS, xlim=xlim, ylim=ylim,
           title="", show_ylabel=True,
           label_each_point=True,
           draw_frontier=True, frontier_per_bench=True)

    _add_in_axes_stage_legend(ax)
    ax.legend(handles=_marker_legend_handles(), loc="upper left",
              bbox_to_anchor=(1.02, 1.0),
              title="Marker", title_fontsize=10, fontsize=9.5,
              frameon=False, borderaxespad=0)

    fig.tight_layout(rect=[0, 0, 0.82, 1])
    fig.savefig("pareto_cost_quality_single.pdf", bbox_inches="tight")
    fig.savefig("pareto_cost_quality_single.svg", bbox_inches="tight")
    plt.close(fig)


def fig_pareto():
    fig_pareto_two_panel()
    fig_pareto_single()


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


# ============================================================================
# Figure 3: Attention heatmap (baseline / Stage1 / Stage2)
# ============================================================================
# Single representative LoCoMo / claudekimi run per stage. Aggregated via
# scripts/aggregate_attention.py into attention_data.json (committed alongside
# this file). Each (N, M) cell counts Read tool calls in proposer iter N
# whose target was reference_iterations/iter_M/. Top-1 marker uses the
# earliest-tie-break post-hoc top-1 (earliest iter with the highest
# candidate-passrate among iter < N).
ATTENTION_RUNS = [
    ("Full-context baseline",
     "locomo_memgpt_claudekimi_default_direction_docker_iter30_train80_20260502_015441"),
    ("Stage 1: CuraHarness-Iter",
     "locomo_memgpt_claudekimi_progressive_autobudget_docker_iter30_train80_r1_20260504_162844"),
    ("Stage 2: CuraHarness-Full",
     "locomo_memgpt_claudekimi_bandit_v4_autobudget_docker_iter30_train80_w16_r1_20260505_040626"),
]


def _load_attention_data():
    import json
    from pathlib import Path
    p = Path(__file__).with_name("attention_data.json")
    raw = json.loads(p.read_text())
    by_short = {}
    for full_path, payload in raw.items():
        by_short[Path(full_path).name] = payload
    return by_short


def _build_grid(payload, y_mode):
    """Return (Z, n_max, y_max, top1_xy, best_xy, worst_xy).

    y_mode='recency': y = N - M (1 = most recent prior iter).
    y_mode='absolute': y = M (absolute iter index).
    """
    import numpy as np
    n_max = payload["n_max"]
    y_max = n_max - 1 if y_mode == "recency" else payload["m_max"]
    Z = np.zeros((y_max + 1, n_max + 1), dtype=float)
    for c in payload["cells"]:
        N, M, r = c["N"], c["M"], c["reads"]
        y = (N - M) if y_mode == "recency" else M
        if 1 <= N <= n_max and 0 <= y <= y_max:
            Z[y, N] += r
    top1_xy = []
    for N_str, M in payload["top1_per_N"].items():
        N = int(N_str)
        if N < 1 or N > n_max: continue
        y = (N - M) if y_mode == "recency" else M
        top1_xy.append((N, y))
    best_xy, worst_xy = [], []
    for N_str, pol in payload["policy_per_N"].items():
        N = int(N_str)
        if N < 1 or N > n_max: continue
        for M in pol.get("best") or []:
            y = (N - M) if y_mode == "recency" else M
            best_xy.append((N, y))
        wm = pol.get("worst")
        if wm is not None:
            y = (N - wm) if y_mode == "recency" else wm
            worst_xy.append((N, y))
    return Z, n_max, y_max, top1_xy, best_xy, worst_xy


def fig_attention_heatmap():
    """Three-stage attention heatmap, two y-axis encodings stacked.

    Top row: y = N - M (recency offset; 1 = most recent prior iter).
    Bottom row: y = M (absolute prior-iter index).
    Color = number of Read tool calls landing on iter M during step N
            (= depth of revisit on the same iter dir). log1p scale,
            shared vmax across all six panels for cross-panel comparison.
    Filled star = post-hoc top-1 (earliest iter with the highest passrate
                  among iter < N).
    Open red square = bandit policy's best_iterations slot (Stage 2 only).
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    data = _load_attention_data()
    grids = {}
    for label, key in ATTENTION_RUNS:
        payload = data[key]
        grids[label] = {
            "recency":  _build_grid(payload, "recency"),
            "absolute": _build_grid(payload, "absolute"),
        }

    # shared colour scale (over both rows + all stages)
    vmax = max(g["recency"][0].max() for g in grids.values())
    vmax = max(vmax, max(g["absolute"][0].max() for g in grids.values()))

    # 1 row x 3 cols of (heatmap + marginal-bar) pairs.
    # Each "column" of the layout is two sub-columns: heatmap (wide) +
    # row-sum bar (narrow, sharey with heatmap).
    fig = plt.figure(figsize=(13.5, 4.2))
    outer = fig.add_gridspec(
        1, 3, wspace=0.30, left=0.07, right=0.92,
        top=0.86, bottom=0.18,
    )

    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_under("#f5f5f5")

    rowsum_max = max(grids[label]["absolute"][0].sum(axis=1).max()
                     for label in grids)

    panel_letters = ["A", "B", "C"]
    last_im = None
    for col, (label, _key) in enumerate(ATTENTION_RUNS):
        inner = outer[0, col].subgridspec(
            1, 2, width_ratios=[5, 1], wspace=0.06,
        )
        ax = fig.add_subplot(inner[0, 0])
        ax_bar = fig.add_subplot(inner[0, 1], sharey=ax)

        Z, n_max, y_max, top1_xy, _best, _worst = grids[label]["absolute"]
        y0, y1 = 0, y_max
        im = ax.imshow(
            Z[y0:y1 + 1, 1:n_max + 1],
            aspect="auto", origin="lower",
            extent=(0.5, n_max + 0.5, y0 - 0.5, y1 + 0.5),
            cmap=cmap, norm=LogNorm(vmin=0.5, vmax=max(vmax, 1)),
        )
        last_im = im
        if top1_xy:
            xs, ys = zip(*top1_xy)
            ax.scatter(xs, ys, marker="*", s=72,
                       facecolor="#1b3a6b", edgecolor="white",
                       linewidths=0.5, zorder=4, label="post-hoc top-1")

        ys = np.arange(y0, y1 + 1)
        rs = Z[y0:y1 + 1, 1:n_max + 1].sum(axis=1)
        ax_bar.barh(ys, rs, height=0.85,
                    color="#7a3a1a", edgecolor="none", alpha=0.85)
        ax_bar.set_xlim(0, rowsum_max * 1.05)
        ax_bar.tick_params(axis="y", left=False, labelleft=False)
        ax_bar.tick_params(axis="x", labelsize=10, length=2.5)
        ax_bar.set_xlabel(r"$\Sigma_N$ reads", fontsize=11, labelpad=2)
        for s in ("top", "right"): ax_bar.spines[s].set_visible(False)
        ax_bar.grid(True, axis="x", ls=":", lw=0.4,
                    color="grey", alpha=0.4)
        ax_bar.set_axisbelow(True)

        ax.set_title(f"{panel_letters[col]}. {label}", fontsize=12.5, pad=6)
        if col == 0:
            ax.set_ylabel("Prior iter $M$ (absolute)", fontsize=12)
        ax.set_xlabel("Proposer iter $N$", fontsize=12)
        ax.tick_params(axis="both", labelsize=10, length=2.5)
        ax.grid(True, ls=":", lw=0.4, color="grey", alpha=0.35)
        ax.set_axisbelow(True)

    cbar_ax = fig.add_axes([0.935, 0.20, 0.011, 0.62])
    cbar = fig.colorbar(last_im, cax=cbar_ax)
    cbar.set_label("Reads on (N, M)  (revisits to same iter dir)",
                   fontsize=11)
    cbar.ax.tick_params(labelsize=10)

    fig.legend(
        handles=[plt.Line2D([0], [0], marker="*", linestyle="",
                            markerfacecolor="#1b3a6b",
                            markeredgecolor="white", markersize=12,
                            label=r"post-hoc top-1 iter at step $N$")],
        loc="lower center", bbox_to_anchor=(0.5, 0.005),
        fontsize=11, frameon=False,
    )
    fig.savefig("attention_heatmap.pdf", bbox_inches="tight")
    fig.savefig("attention_heatmap.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_optimization_effect()
    fig_pareto()
    fig_attention_heatmap()
    print("Generated: optimization_effect.{pdf,svg}, "
          "pareto_cost_quality.{pdf,svg}, attention_heatmap.{pdf,svg}")
