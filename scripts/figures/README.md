# Paper figure sources

`make_figures.py` generates the Experiments-section figures for the CuraHarness
paper. It was recovered from commit `4ead028`, where it lived in `paper/figures/`
before `paper/` was replaced by the standalone
[Cura_paper](https://github.com/Ch1nyzzz/Cura_paper) repository.

It stays on the code side because it depends on this repo, not on the paper:

- `OPTCURVE_RUNS` reads `candidate_score_table.json` and
  `proposer_calls/iter_*/assignment.json` under absolute `runs/` paths.
- Hard-coded numbers are transcribed from `docs/EXPERIMENT_INSIGHTS.md` and
  `docs/experiment_detail.md`.
- `attention_data.json` must sit next to the script (`Path(__file__).with_name`).

## Running

Figures are written to the current working directory, so run it from wherever
the output should land:

```bash
cd paper/figures && python /data/home/yuhan/cura_harness/scripts/figures/make_figures.py
```

## Figure name mapping

The Cura_paper repo renamed the figures during the Overleaf import, and the
committed PDFs there no longer match this script's output names one-to-one:

| `make_figures.py` output      | Cura_paper `figures/`        |
| ----------------------------- | ---------------------------- |
| `optimization_curve.pdf`      | `optimization_curve.pdf`     |
| `attention_heatmap.pdf`       | `heatmap.pdf`                |
| `pareto_small.pdf`            | `pareto_small_fixed_v9.pdf`  |
| `optimization_effect.pdf`     | (unused)                     |
| `pareto_cost_quality*.pdf`    | (unused)                     |
| `read_concentration.pdf`      | (unused)                     |
| —                             | `Pipeline.png` (hand-made)   |

`pareto_small_fixed_v9.pdf` is a later revision whose edits were never folded
back into this script; regenerating `pareto_small.pdf` will not reproduce it.

## Missing

`fig_attention_heatmap` consumes `attention_data.json`, which the docstring says
was produced by `scripts/aggregate_attention.py`. That aggregator was never
committed to this repo, so the heatmap can be re-rendered from the existing JSON
but not re-aggregated from `runs/`.
