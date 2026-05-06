# Experiment Insights

This note captures cross-run observations that are not visible from the
headline result tables alone. The scope is the retained experiments in
`docs/PIPELINE.md`, with the following exclusions for budget-stage analysis:

- default and default+direction are excluded because every iteration is fixed
  `high`;
- claude opus is excluded because there is no retained v3 bandit comparison;
- text classification is excluded from budget-stage comparisons because no
  bandit result is retained.

Unless otherwise stated, a breakthrough means a training iteration whose
candidate score improved over all earlier candidates in that same run. Score is
ordered by `passrate`, then `average_score`; equal-score ties are not counted
as new breakthroughs.

## Final Frontier vs Process Breakthroughs

Do not infer where optimization happens from `best_candidates.json` alone.
That file records the candidates left on the final frontier, so it can collapse
many earlier improvements into one or two retained candidates.

For example, `locomo_memgpt_claudekimi_bandit_v4_autobudget_..._r1_20260505_040626`
(the LoCoMo·kimi/bandit "best by test" run cited in `experiment_detail.md`)
has only one final retained best candidate (iter011, test 0.3616), but it
had four process-breakthrough events during training:

| iteration | budget | passrate | average_score |
|---:|---|---:|---:|
| 2 | medium | 0.3750 | 0.5397 |
| 3 | medium | 0.4250 | 0.5531 |
| 11 | high | 0.4375 | 0.5855 |
| 30 | high | 0.4750 | 0.5971 |

Note that the train-best (0.4750 at iter 30) was *not* the held-out
test-best — the iter011 candidate generalized better to the held-out
set. This is the typical pattern across the experiment_detail set: train
passrate climbs across the run while the test-leading iter is often
mid-run, which is why per-iter test eval is needed to surface the right
candidate.

## Breakthroughs By Budget

Across the 17 bandit and progressive auto-budget runs cited at the artifact
level in `docs/experiment_detail.md` (default-family excluded because every
iter is fixed `high` by construction), the process-breakthrough distribution
aggregated by (benchmark, proposer, policy) cell:

| benchmark | proposer | policy | n runs | low | medium | high | total |
|---|---|---|---:|---:|---:|---:|---:|
| LoCoMo | claudekimi | bandit | 2 | 0 | 2 | 6 | 8 |
| LoCoMo | claudekimi | progressive | 2 | 3 | 1 | 3 | 7 |
| LoCoMo | codex54 | bandit | 2 | 0 | 3 | 4 | 7 |
| LoCoMo | codex54 | progressive | 2 | 4 | 0 | 1 | 5 |
| LongMemEval | claudekimi | bandit | 3 | 2 | 6 | 7 | 15 |
| LongMemEval | claudekimi | progressive | 1 | 7 | 0 | 1 | 8 |
| LongMemEval | codex54 | bandit | 3 | 1 | 7 | 5 | 13 |
| LongMemEval | codex54 | progressive | 2 | 5 | 0 | 4 | 9 |
| **subtotal (auto-budget)** |  |  | **17** | **22** | **19** | **31** | **72** |

SWE-bench mini retained artifacts are all single-tier (force=high or
default+direction at high). Including them for completeness, all
breakthroughs land at high by construction:

| benchmark | proposer | policy | n runs | low | medium | high | total |
|---|---|---|---:|---:|---:|---:|---:|
| SWE-bench mini | claudekimi | default+direction | 1 | 0 | 0 | 1 | 1 |
| SWE-bench mini | claudekimi | bandit_v3 budgethigh | 3 | 0 | 0 | 2 | 2 |

The PIPELINE.md docs-only SWE-bench rows (`default` train 0.5000,
`progressive` train 0.5333, `bandit (fixedsource)` train 0.5333,
verified-set 0.4580 / 0.6200 / 0.6400) are not aggregated here because
their per-iter breakthrough sequences are not retained in
`runs/`; see `docs/PIPELINE.md` Section 5.3 for the headline numbers.

On the full training horizon, in the adaptive (auto-budget) cells low+medium
together account for 41/72 = 57% of breakthroughs, and high alone for
31/72 = 43%. This is the optimistic view of the adaptive policies: narrow
contexts find a meaningful fraction of the early gains, and medium budget
is especially productive for bandit on LongMemEval (6 medium breakthroughs
across 3 kimi-bandit runs, 7 across 3 codex-bandit runs).

## After Iteration 5

The full-horizon count is biased by the first few iterations. Early candidates
start from a low baseline, so they have more headroom and often improve without
needing much context. A stricter view is to count only breakthroughs after
iteration 5.

Raw breakthrough counts and exposure after iteration 5, restricted to the
17 bandit/progressive runs in `docs/experiment_detail.md`:

| benchmark | proposer | policy | n | iters L/M/H | breakthroughs L/M/H |
|---|---|---|---:|---|---|
| LoCoMo | claudekimi | bandit | 2 | 0 / 16 / 34 | 0 / 0 / 6 |
| LoCoMo | claudekimi | progressive | 2 | 4 / 6 / 40 | 0 / 1 / 3 |
| LoCoMo | codex54 | bandit | 2 | 0 / 19 / 31 | 0 / 1 / 4 |
| LoCoMo | codex54 | progressive | 2 | 2 / 3 / 45 | 0 / 0 / 1 |
| LongMemEval | claudekimi | bandit | 3 | 0 / 38 / 37 | 0 / 1 / 7 |
| LongMemEval | claudekimi | progressive | 1 | 5 / 2 / 18 | 3 / 0 / 1 |
| LongMemEval | codex54 | bandit | 3 | 0 / 25 / 50 | 0 / 1 / 5 |
| LongMemEval | codex54 | progressive | 2 | 6 / 7 / 37 | 0 / 0 / 4 |
| **total** |  |  | **17** | **17 / 116 / 292** | **3 / 4 / 31** |

Aggregated by budget:

| budget | post-5 iterations | post-5 breakthroughs | breakthrough rate |
|---|---:|---:|---:|
| low | 17 | 3 | 17.6% |
| medium | 116 | 4 | 3.4% |
| high | 292 | 31 | 10.6% |
| **total** | **425** | **38** | **8.9%** |

The picture is clearer than before: high captures **31/38 = 81.6% of
post-iter-5 breakthroughs in absolute count**, and per-iter rate (10.6%)
is materially higher than medium (3.4%). Low has the highest rate (17.6%)
but only 17 post-5 opportunities (longmemeval claudekimi progressive
contributes 5/17 of those), so the denominator is too small to draw a
strong claim. The interpretation:

- low and medium remain useful for early exploration and cheap candidate
  discovery within the first 5 iters (covered in `Breakthroughs By
  Budget` above);
- after iter 5, medium becomes the weakest tier (only 4/116 = 3.4% rate)
  — most policies do not productively spend medium late in a run;
- high is where the late-stage rescue work happens — both in absolute
  count (31) and per-iter rate (10.6%);
- LongMemEval claudekimi progressive r1 is unusual: 3 of the 5 post-5
  low-budget breakthroughs in the entire sample come from this single
  run, where the proposer kept finding gains at low budget through iter
  17 (see Section 1 / experiment_detail.md for the per-iter sequence).

## Token Trend Context

The budget-stage breakthrough counts should be read alongside proposer-token
curves:

- bandit usually ramps up: `low` is cheap, `medium` is moderate, and `high`
  approaches default-like context cost;
- progressive does not always save tokens. It saves clearly for claudekimi
  memory runs, but can be flat or more expensive for codex54 and SWE-bench
  mini because the proposer may compensate for smaller granted context by
  reading fewer but larger or more information-dense files;
- default should not be mixed into budget-stage breakthrough counts, because
  default has no budget transition. Its breakthroughs are all `default-high`
  by construction.

## Progressive Advantage: Fewer Files, Better Iteration Routing

The headline claim is that adaptive policies (bandit, progressive) sit on
a Pareto frontier with default: **comparable or lower per-propose cost
AND comparable or higher test score**. We use two run-selection rules
deliberately:

- **Test-score columns** report mean ± std across all retained runs in
  the cell (the way accuracy is reported in the rest of `docs/experiment_detail.md`),
  because a single best-test run is statistically thin for an accuracy
  claim.
- **Per-propose cost columns** are taken from the best-by-test single
  run in each cell (matching `Per-Propose Token Cost Across Policies`
  above), because cost is measured on the run we are actually proposing
  as the cell's representative result.

Restricted to the claudekimi cells in `docs/experiment_detail.md`:

| benchmark | policy | n | test mean ± std | best test | tools/iter (best-run) | unique_files/iter (best-run) | total/iter (best-run) |
|---|---|---:|---|---:|---:|---:|---:|
| LoCoMo | default-family | 3 | 0.3315 ± 0.0153 | 0.3423 | 46.6 | 4.0 | 3.42M |
| LoCoMo | bandit | 2 done + 1 docs | 0.3554 ± 0.0084 | 0.3616 | 41.8 | 3.0 | 2.63M |
| LoCoMo | progressive | 2 done + 1 docs | 0.3545 ± 0.0214 | **0.3734** | **35.2** | 15.1* | **1.86M** |
| LongMemEval | default-family | 2 done + 1 docs | 0.4983 ± 0.0301 | 0.5300 | 49.8 | 3.7 | 3.71M |
| LongMemEval | bandit | 3 | **0.5100 ± 0.0378** | **0.5450** | **38.2** | **3.3** | **2.55M** |
| LongMemEval | progressive | 2 done + 1 docs | 0.5050 ± 0.0132 | 0.5200 | 47.3 | 3.8 | 3.37M |

*The LoCoMo progressive `unique_files/iter` of 15.1 comes from
`PIPELINE.md`'s `files/iter` column on the docs-only pipeline progressive
row, which uses a different definition (workspace files touched per
iter) than the artifact-derived `unique_files_read` in the other rows.
Treat it as a different metric.

**Mean-test reading** (across all retained runs in each cell):

- LoCoMo: bandit mean 0.3554 ≈ progressive mean 0.3545, both **clear of
  default's 0.3315 by ~2.3 ppt** (default-family std 0.0153, so the gap
  is ~1.5σ). Adaptive policies' mean test is materially above default's
  mean.
- LongMemEval: bandit mean 0.5100 > progressive mean 0.5050 > default
  mean 0.4983. Smaller margins (~1-1.2 ppt), all within std overlap, so
  the per-cell mean ranking is suggestive rather than significant on
  this benchmark.

**Best-test reading** (single run per cell, used for cost):

- LoCoMo: **progressive Pareto-dominates** — best test 0.3734 (highest
  in the cell) at 1.86M total/iter (lowest cost) and 35.2 tools/iter
  (lowest tool count).
- LongMemEval: **bandit Pareto-dominates** — best test 0.5450 (highest
  in the cell) at 2.55M total/iter (lowest cost) and 38.2 tools/iter
  (lowest tool count).

So the cost-quality picture is Pareto-favorable across both run-selection
rules: mean test confirms the adaptive policies sit at or above default
for accuracy, and best-test cost confirms they do so without paying more
per-propose. The Pareto reading is robust to which rule is used for
accuracy reporting; only the cost column requires picking a specific
run.

The mechanism-level claim — that best/worst iteration labels concentrate
the proposer's reads on a small subset of available iter dirs — is
verified against current bandit artifacts in the
`Reference-Iteration Read Distribution` section below (14-22x reads/slot
concentration on best-tagged dirs).

This is presented as a Pareto trade-off rather than a strict ordering:
not every retained adaptive run beats default on cost or test (e.g.
LoCoMo bandit_v3 r1 test 0.3458 / per-iter 4.24M is below the default
best-test on accuracy and above on cost). The claim is that the
*best-by-test* adaptive run from each cell sits at or below the
default-family baseline on cost, while the *cell mean* test is at or
above default's mean. Cheaper operating points at lower test scores
(e.g. bandit force=low at LongMemEval, train 0.6300 / test 0.4550) are
explored in the `Force-Budget Ablation` subsection later.

## Per-Propose Token Cost Across Policies

This section compares default, bandit, and progressive at per-propose
granularity for all four (benchmark, proposer) cells, using the
"best retained run by test score" rows in `docs/experiment_detail.md`.
It extends `Progressive Advantage` above by including bandit and codex54,
and adds a mechanistic decomposition of why a longer initial prompt produces
lower total token consumption per propose.

### Cross-cell summary table

| cell | policy | input | output | cache_read | total | tools | read_files | read_lines | best test |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LoCoMo claudekimi | default | 151.3k | 26.7k | 3.25M | **3.42M** | 46.6 | 27.7 | 4,825.5 | 0.3423 |
|  | bandit | 156.9k | 21.1k | 2.45M | **2.63M** (-23%) | 41.8 | 26.3 | 3,970.3 | 0.3616 |
|  | progressive | 138.9k | 25.5k | 1.70M | **1.86M** (-46%) | 35.2 | NA | NA | **0.3734** |
| LoCoMo codex54 | default | 1.79M | 25.7k | 1.61M | **3.42M** | 37.1 | 23.0 | 2,893.3 | 0.3402 |
|  | bandit | 1.13M | 20.7k | 0.995M | **2.14M** (-37%) | 34.6 | NA | NA | 0.3865 |
|  | progressive | 1.27M | 25.9k | 1.16M | **2.46M** (-28%) | 30.5 | 21.9 | 2,579.5 | **0.3879** |
| LongMemEval claudekimi | default | 176.2k | 30.4k | 3.50M | **3.71M** | 49.8 | 27.6 | 4,286.3 | 0.5300 |
|  | bandit | 209.5k | 18.7k | 2.32M | **2.55M** (-31%) | 38.2 | 23.8 | 3,526.7 | **0.5450** |
|  | progressive | 177.7k | 28.4k | 3.16M | **3.37M** (-9%) | 47.3 | 28.8 | 3,772.8 | 0.5200 |
| LongMemEval codex54 | default | 1.51M | 25.3k | 1.39M | **2.93M** | 33.9 | 22.5 | 2,487.0 | 0.5075 |
|  | bandit | 1.13M | 24.6k | 1.03M | **2.18M** (-26%) | 34.8 | 24.7 | 2,879.6 | 0.4725 |
|  | progressive | 1.38M | 23.9k | 1.26M | **2.66M** (-9%) | 32.2 | 22.5 | 2,800.0 | **0.5275** |

The two NA rows (LoCoMo claudekimi progressive, LoCoMo codex54 bandit) are
docs-only entries: their best retained run was rolled up into `PIPELINE.md`
but the artifact directory is no longer on disk, so per-iteration
`metrics.json` cannot be re-aggregated. PIPELINE.md only stores seven
aggregate fields for those rows (`input/iter`, `output/iter`,
`cache reads/iter`, `total/iter`, `tools/iter`, `files/iter`, `dur/iter`),
which is why `read_files/propose` and `read_lines/propose` are unavailable.
Note the docs-only `unique_files/propose` value reported in
`docs/experiment_detail.md` (15.1 for LoCoMo kimi progressive, 18.5 for
LoCoMo codex bandit) uses a different definition than the artifact-derived
rows: PIPELINE's `files/iter` counts workspace files touched per iter,
while artifact rows count distinct files read via the Read tool. The
two columns are not directly comparable, so we omit `unique_files/propose`
from the summary table.

### Headline observations

1. **Default is always the most expensive policy on `total/propose`** in this
   four-cell view. Savings vs default range from -9% (LongMemEval, both
   proposers, progressive) to -46% (LoCoMo claudekimi, progressive).
2. **The cheapest policy outscores default on test in three of four cells**.
   LoCoMo claudekimi has progressive winning both cost and test
   (0.3423 -> 0.3734); LoCoMo codex54 has bandit cheapest at test 0.3865
   vs default 0.3402 (with progressive marginally higher at 0.3879);
   LongMemEval claudekimi has bandit winning both (0.5300 -> 0.5450).
   Only LongMemEval codex54 inverts: bandit is cheapest but its test
   0.4725 is below default 0.5075, while progressive 0.5275 is the
   higher-scoring option.
3. **Bandit is the most reliable cost-saver**: -23% to -37% vs default
   across all four cells. Progressive saves 28-46% on LoCoMo cells and only
   9% on LongMemEval cells; its state machine is benchmark-sensitive.

### Why a longer initial prompt produces lower total tokens

Initial prompt sizes (claudekimi LoCoMo, `prompt.md` median bytes across the
retained training runs):

| policy | prompt.md median | rel to default |
|---|---:|---:|
| default | 6.68 KB | 1.00x |
| progressive | 8.05 KB | 1.20x |
| bandit | 9.97 KB | 1.49x |

Both bandit and progressive carry a longer initial prompt than default
(bandit ~50% larger, progressive ~20% larger) and yet both produce lower
per-propose totals. The reason is that per-propose total decomposes as

```
total ~= initial_prompt * turns * cache_amplification
       + sum_t (per-turn intermediate output + tool output)
       + final output
```

The longer prompt is a fixed cost paid once per propose. The reference
content it carries (best/worst iteration digests for bandit, state-machine
direction for progressive) substitutes for a much larger amount of
exploration cost in the variable sum_t term. Cross-cell decomposition of
the bandit-vs-default delta on the kimi side, where the per-turn prefix
re-read makes the effect easiest to read:

| dimension | LoCoMo bandit delta | LongMemEval bandit delta |
|---|---:|---:|
| input/propose | +4% | +19% |
| output/propose | -21% | -38% |
| tools/propose | -10% | -23% |
| read_lines/propose | -18% | -18% |
| cache_read/propose | -25% | -34% |
| **total/propose** | **-23%** | **-31%** |

Per-turn fresh input grows on LongMemEval (+19% from the +1k initial-prompt
token increase being re-counted across ~38 turns) and stays nearly flat on
LoCoMo. The dominant savings come from output (-21 to -38%), tool turns
(-10 to -23%), and cache_read (-25 to -34%). cache_read declines because
both the per-turn prefix and the turn count fall: the proposer no longer
enumerates exploratory thinking, so per-turn intermediate output is shorter,
and fewer turns are needed because the policy already named the directions
to try.

For codex54 the same direction holds but the accounting differs: codex's
`input_tokens` includes the cached portion (OpenAI Responses convention),
so input and cache_read move together. LoCoMo codex54 bandit shows
input -37% / cache -38%; LongMemEval codex54 bandit shows input -25% /
cache -26%. Codex saves through a smaller final-turn cumulative prefix
(shorter conversation tail) rather than fewer accumulated turns.

A back-of-envelope reconciliation for LoCoMo claudekimi bandit: the longer
initial prompt adds ~1k tokens, re-read across 41.8 turns contributes
~+42k accumulated cache_read. Tool turns drop by 4.8 (46.6 to 41.8), and
each turn's prefix averages ~70k, removing ~336k cache_read. Per-turn
intermediate output also shrinks because the proposer no longer enumerates
options, removing roughly another ~400k cache_read. Net: +42k - 336k - 400k
~ -694k, about -21% of the 3.25M default cache_read. This is in line with
the measured -25% cache_read drop and the headline -23% total drop.

### Progressive vs bandit: state machine fragility on larger codebases

Progressive's mechanism is more aggressive than bandit: bandit surfaces a
menu of best-k and worst-k digests and the proposer picks a direction;
progressive's state machine prescribes the direction directly. The
state-machine constraint translates into fewer tool turns *only when the
candidate codebase is small enough that direct prescription replaces a
localization scan*:

| cell | progressive tools/propose | bandit tools/propose | default tools/propose |
|---|---:|---:|---:|
| LoCoMo claudekimi | 35.2 | 41.8 | 46.6 |
| LoCoMo codex54 | 30.5 | 34.6 | 37.1 |
| LongMemEval claudekimi | 47.3 | 38.2 | 49.8 |
| LongMemEval codex54 | 32.2 | 34.8 | 33.9 |

On LoCoMo (smaller candidate code) progressive's state machine succeeds:
tool turns drop 18-24% below default and below bandit. On LongMemEval
(larger candidate code) progressive's tool count returns to near-default
(47.3 vs 49.8 on kimi); the state machine cannot constrain enough to skip
the localization scan, and bandit's anchor-based hints become more
effective. This is consistent with the divergence in the per-cell summary
table above: progressive saves 28-46% on LoCoMo and only 9% on LongMemEval,
while bandit's saving stays in the -23% to -37% band across all four cells.

The practical heuristic: progressive scales with the codebase size for
which its state machine can substitute for exploration. For larger
codebases, anchor-based hints (bandit) are more robust because they tell
the proposer "look here" instead of "do this".

### Headline cost-vs-score per cell

| cell | cheapest policy | savings vs default | best-test policy |
|---|---|---:|---|
| LoCoMo claudekimi | progressive (1.86M) | -46% | progressive (0.3734) |
| LoCoMo codex54 | bandit (2.14M) | -37% | progressive (0.3879) |
| LongMemEval claudekimi | bandit (2.55M) | -31% | bandit (0.5450) |
| LongMemEval codex54 | bandit (2.18M) | -26% | progressive (0.5275) |

Default is consistently the most expensive policy in this slice. Bandit is
the universal cost-saver. Progressive saves 28-46% on LoCoMo and 9% on
LongMemEval, which is consistent with the state-machine-fragility finding
above; progressive should be paired with smaller candidate codebases, or
its state machine widened for larger ones.

## Budget-Conditioned Proposer Behavior

This section uses artifact-level `agent/tool_access.json` traces from the
8 claudekimi memory runs in `docs/experiment_detail.md` (5 bandit + 3
progressive, 240 iterations total). Codex54 is excluded because its tool
traces do not preserve the same Read-tool structure (all calls are bucketed
under `Shell`), and `docs/experiment_detail.md` docs-only rows cannot be
reconstructed per iteration. The earlier `force=low` / `force=high`
ablation runs are also excluded because they are not in
`docs/experiment_detail.md`.

Auto-budget behavior by actual budget tier:

| policy | budget | iters | tools/propose | reads/propose | lines/propose | unique files/propose | source reads/propose | summary reads/propose | ref reads/propose | ref read share | ref lines/propose | best reads/propose |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit | low |  5 | 37.40 | 19.60 | 2,176 | 16.00 | 12.00 | 5.60 |  0.00 |  0.0% |   0.0 | 0.00 |
| bandit | medium | 74 | 41.65 | 23.14 | 3,225 | 17.70 |  8.86 | 5.93 |  7.23 | 31.2% | 426.6 | 6.21 |
| bandit | high | 71 | 43.77 | 26.27 | 4,233 | 20.48 |  8.37 | 5.37 | 12.30 | 46.8% | 703.2 | 9.25 |
| progressive | low | 24 | 40.25 | 22.88 | 3,179 | 18.29 |  9.25 | 5.50 |  6.96 | 30.4% | 826.2 | NA |
| progressive | medium |  8 | 59.50 | 27.25 | 3,442 | 19.62 | 12.00 | 4.88 |  9.00 | 33.0% | 683.1 | NA |
| progressive | high | 58 | 50.26 | 27.52 | 3,925 | 19.97 |  9.28 | 6.14 | 11.95 | 43.4% | 960.8 | NA |

`best reads/propose` for bandit is averaged only over iterations whose
policy state had a non-empty `best_iterations` list (otherwise the metric is
not defined). Progressive does not surface `best_iterations` directly to the
proposer, so the column is NA.

The key pattern is that budget mostly changes *reference-history exposure*,
not source-code reading. Source reads stay in a 8-12 / propose band across
all (policy, budget) cells, with no clear monotone trend. What changes is
the reference-iteration channel: bandit moves from 0.00 ref reads/propose
at low (small n=5 sample, but matches the 0.00 force=low result from the
earlier ablation) to 7.23 at medium and 12.30 at high; progressive moves
from 6.96 at low to 9.00 at medium and 11.95 at high. The line volume
shows the same pattern. High budget is therefore not merely "more files";
it is specifically more iteration-history reading.

For bandit, this also directly increases reads of policy-labelled best
iterations: best-iteration reads/propose are 0.00 at low (no best refs
surfaced), 6.21 at medium, and 9.25 at high. This supports the
mechanism-level interpretation that the policy's best-iteration pointers
are an attention prior; the next section
(`Reference-Iteration Read Distribution`) shows the same effect at
slot-normalized resolution.

The bandit `low` cell here only has 5 iterations because the bandit policy
naturally schedules low almost exclusively in the warm-up phase, and most
runs in the experiment_detail set then escalate. The qualitative claim
that low budget effectively removes the reference-iteration channel was
also confirmed by the earlier force=low ablation runs (60 iters, 0.02
ref reads/propose), which are no longer in `docs/experiment_detail.md`
but are kept in `PIPELINE.md` as supporting evidence.

The practical interpretation is budget-dependent:

- low budget is a source/summaries mode; it is cheap and good for local
  candidate edits, but for bandit it largely removes historical iteration
  evidence;
- medium budget is the first tier where bandit best-iteration hints become
  behaviorally active;
- high budget mainly buys more reference-history reading, and especially
  more reads of policy-labelled best iterations.

### Force-Budget Ablation

The auto-budget table above lets the policy choose its tier each iter, so
the bandit `low` row in particular has only n=5 (the policy almost
immediately escalates). To get a clean tier comparison we use the six
claudekimi force-budget runs cataloged in
`docs/experiment_detail.md` (`Ablation: Force-Budget Runs`). These pin
every iter to a single budget so behavioral signatures are not confounded
with the natural escalation schedule. Per-iter means across 60 iters per
(policy, forced-tier) cell:

| policy | forced | iters | tools/propose | reads/propose | lines/propose | unique files/propose | source reads | summary reads | ref reads | ref read share | ref lines | best reads/propose |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit | high | 60 | 47.50 | 26.33 | 4,041 | 20.03 |  9.90 | 5.43 | **9.58** | **36.4%** | 724.9 | **7.84** |
| bandit | low  | 60 | 37.08 | 20.52 | 2,361 | 15.65 | 10.93 | 7.93 | **0.02** | **0.1%** | 0.0 | **0.00** |
| progressive | low | 60 | 43.67 | 24.35 | 3,638 | 17.80 |  8.77 | 6.95 | 7.42 | 30.5% | 652.4 | NA |

Two clean ablation findings:

- **bandit force=low almost completely removes the reference-iteration
  channel** (0.02 ref reads / propose, 0 best-iter reads), while
  force=high opens it (9.58 / 7.84). The 0.0 ref_lines confirms the
  reads aren't even partial — bandit at low is a pure source/summaries
  proposer with no history exposure. This is the controlled-ablation
  evidence that the policy's best-iteration pointers, not just budget
  tier, are what drives the iteration-history reading we measure in the
  auto-budget table.
- **progressive at force=low still does ref reading** (7.42 ref reads,
  30.5% share) — unlike bandit, progressive surfaces a small reference
  set even at the lowest tier (the state-machine direction is encoded
  through reference iters). So "low budget = no history" is a bandit
  property, not a policy-agnostic one.

This also reconciles with `docs/PIPELINE.md` results: LongMemEval bandit
force=low scores train 0.6300 (the highest train passrate on
LongMemEval claudekimi bandit), so removing the ref channel does *not*
destroy bandit on LongMemEval; the file-prior alone via UCB hot-files is
sufficient for that benchmark. On LoCoMo the force=low bandit lands at
train 0.3875, modestly below force=high's 0.4000 — the ref channel is
more useful for LoCoMo than for LongMemEval. The Pareto trade is
benchmark-conditional, not absolute.

## Workspace Pool Inflates with Budget, Reads Do Not

The "After Iteration 5" view counts breakthroughs but not how much the
proposer has to wade through to find them. This section asks a separate
mechanistic question: when budget escalates from `low` to `high`, does the
agent actually read more files? The answer is that the workspace file pool
grows nearly an order of magnitude, but per-iteration unique-file reads stay
roughly flat. The implication is that adaptive-policy gains come from
*directing* the agent's attention, not from giving it a bigger pile to look
at.

Aggregating `agent/metrics.json` across all bandit and progressive runs
explicitly cited at the artifact level in `docs/experiment_detail.md`
(10 bandit + 7 progressive runs, mixed claudekimi and codex54,
510 proposer iterations total). Because metrics.json fields are populated
for both proposer agents, this slice is not restricted to claudekimi the
way the prior "Budget-Conditioned Proposer Behavior" section is.

| policy | budget | iters | workspace files (mean) | unique files read | read_file_calls | read_lines | duration_s |
|---|---|---:|---:|---:|---:|---:|---:|
| bandit | low    |  10 |  1,222 | 15.9 | 20.7 | 2,314 | 781 |
| bandit | medium | 138 |  6,191 | 17.9 | 23.7 | 2,975 | 923 |
| bandit | high   | 152 | 21,648 | 19.2 | 25.3 | 3,472 | 917 |
| progressive | low    |  52 |  3,170 | 17.5 | 22.3 | 2,847 | 615 |
| progressive | medium |  18 |  6,102 | 20.2 | 26.1 | 3,230 | 743 |
| progressive | high   | 140 | 21,790 | 18.7 | 25.3 | 3,204 | 709 |

The workspace file count is a proxy for what the agent could reach.
Escalating from `low` to `high` inflates the pool ~17.7x for bandit and
~6.9x for progressive. But the agent's `unique_files_read` is essentially
flat: bandit moves from 15.9 to 19.2 (+21%), progressive moves from 17.5
to 18.7 (+7%, with a peak at 20.2 in medium). Read lines grow modestly
(bandit +50%, progressive +13%) and per-iter wall time grows 17% for
bandit and 15% for progressive. The agent self-throttles to ~18-20
unique reads per iteration regardless of how many files are physically
copied into the workspace.

This is the structural confirmation behind the `Reference-Iteration Read
Distribution` finding below: the agent is not surveying the bigger pool and
picking more sources; it follows the curated menu the policy surfaces (hot
paths, best-iter pointers). The pool growth therefore mostly buys I/O cost
without behavioral change.

### Quality vs budget: Pareto trade-off, not a free lunch

Per-budget mean passrate of *successfully-evaluated* candidates, restricted
to the 17 auto-budget runs in `docs/experiment_detail.md`:

| policy | low n | low pass | medium n | medium pass | high n | high pass |
|---|---:|---:|---:|---:|---:|---:|
| bandit | 9 | 0.255 | 121 | 0.357 | 134 | **0.378** |
| progressive | 50 | **0.369** | 17 | 0.346 | 127 | 0.355 |

The two policies show different but mutually consistent shapes. **Bandit's
mean passrate is monotonic in budget** (low < medium < high) — more
context, higher mean candidate quality, exactly the cost-quality
trade-off you would expect when budget is the only knob being changed.
**Progressive's low tier has the highest mean passrate** (0.369) but its
high tier (0.355) is only slightly behind, with medium between — the
state machine constrains the search direction enough that smaller
budgets are not losing much candidate quality.

The bandit `low` cell is small (n=9, almost entirely warm-up
iterations), so the 0.255 mean should be read as a weak signal rather
than a stable estimate; the medium and high cells are the ones to trust
for budget comparison. Either way, the headline framing is
**"bandit can pay more budget for marginally higher mean candidate
quality"** and **"progressive's quality is roughly tier-insensitive at
similar absolute level"**. Neither is a free lunch; both are
points on a Pareto curve where the user picks an operating point.

Where `high` does pay off is the long tail: the train-best candidate per
run lands at `high` in 9/10 bandit runs and 5/7 progressive runs (the
other 2 progressive bests are at `low`, both LongMemEval r1 / r2 from the
LongMemEval claudekimi cell). After base-rate adjustment — `high`
occupies 50.8% of evaluated iters for bandit and 65.5% for progressive —
the relative over-representation of `high` for the run-best candidate is
**1.77x for bandit** and only **1.09x for progressive**. Bandit clearly
prefers high for its train-best; progressive's preference is essentially
no preference once you control for tier exposure.

Iter-position controls clarify the timing. Improvement rate (fraction of
iters whose evaluated passrate strictly exceeded the prior running best),
bucketed by iter range and budget:

| policy | iter range | low | medium | high |
|---|---|---:|---:|---:|
| bandit | 01-10 | 30.0% (3/10) | 21.3% (16/75) | 20.0% (3/15) |
| bandit | 11-20 |            - | 0.0% (0/36) | 14.1% (9/64) |
| bandit | 21-30 |            - | 3.7% (1/27) |  9.6% (7/73) |
| progressive | 01-10 | 35.0% (14/40) | 12.5% (1/8)  |  4.5% (1/22) |
| progressive | 11-20 | 22.2% (2/9)   |  0.0% (0/7)  |  9.3% (5/54) |
| progressive | 21-30 |  0.0% (0/3)   |  0.0% (0/3)  |  4.7% (3/64) |

Two patterns stand out:

- **Early iters at `low` are the most productive single setting**:
  progressive's 35% improvement rate at iter01-10 / `low` and bandit's
  30% are the highest cells in their respective rows. This is consistent
  with the warm-up phase finding cheap improvements before the candidate
  approaches the easy ceiling.
- **Late iters (11-30) are dominated by `high`**: `medium` and `low`
  produce almost no improvements after iter 10 (0/36 + 1/27 for bandit
  medium; 0/9 + 0/3 for progressive medium; 0/3 for progressive late
  low), while `high` keeps a 4.7-14.1% per-iter improvement rate. This
  is the role where `high` is irreplaceable — late-stage stagnation
  rescue.

### Why this matters: focus is the real lever

Putting `After Iteration 5`, this section, and `Reference-Iteration Read
Distribution` together:

1. Budget controls how many reference-iter directories are physically
   exposed in the workspace (low ~1 to high ~20 dirs), which inflates the
   workspace pool ~17.7x for bandit and ~6.9x for progressive.
2. The agent does not respond to that inflation. Unique reads per iter stay
   at ~18-20 across all budgets and policies.
3. What the agent does read is overwhelmingly steered by surfaced labels.
   In the next section, bandit-marked best-iter dirs receive 14-22x more
   Read calls per available slot than unmarked refs; without policy hints,
   the proposer falls back to a strong recency prior.
4. Therefore the marginal quality benefit from `high` (the late-iter
   rescue) comes from *which* iters are pointed to as best/worst, not from
   piling more iter dirs into the workspace.

Two design implications follow:

- A `high`-budget cap on `reference_iterations` (e.g., 8-10 instead of full
  history) should preserve the late-stage rescue role of `high` while
  cutting workspace I/O roughly 2x. The change is low-risk because the
  agent was already not reading the extra dirs. v4's ref-iter selection
  rewrite is in this direction (best-3 + worst, capped at 5 for medium and
  3 for low, full history at high); a `high` cap would close the loop.
- `medium` is the weakest standalone tier in this sample: 1/63 mid- and
  late-iter improvements for bandit (only 1 improvement in 36+27 medium
  iters from iter 11 onward), 0/10 for progressive. Its main remaining
  role appears to be transitional. A binary "stagnated -> high, otherwise
  -> low" policy would lose little observable optimization value in the
  retained runs while removing a tier.

## Reference-Iteration Read Distribution

The adaptive policies do not always read fewer files than `default+direction`
(see "Token Trend Context" above), but they redistribute *which* iteration
directories the proposer attends to. This section quantifies that shift using
the per-iteration `tool_access.json` traces from the kimi proposer runs on
LongMemEval and LoCoMo. Codex5.4 runs are excluded because tool_uses are not
logged for that proposer.

Methodology. For every iteration we count, per Read tool call, which
`reference_iterations/iter_NNN/` directory it lands in (if any). Each call also
exposes a set of *available* `iter_NNN` directories under
`workspace/reference_iterations/`. We then bucket each available directory by
how the bandit policy labelled it **at that specific iteration**
(`bandit_policy.best_iterations`, `bandit_policy.worst_iteration`, other
listed `reference_iterations`, or unlisted) and report **reads per available
slot** across the run. The slot normalization removes the confound of
"how many iter dirs were exposed". Note: `best_iterations` is per-iteration
state — at iteration N the policy can only point to iters whose evaluation
finished before N, so labels evolve along the run. Slots and reads are
bucketed against the policy state used in *that* iteration's prompt.

### Bandit best-iter hints concentrate attention strongly

Three LongMemEval kimi bandit runs cited in `docs/experiment_detail.md`,
restricted to iterations whose policy included a non-empty `best_iterations`
list:

| run | iters w/ best | bucket | slots | reads | reads/slot | lines/slot |
|---|---:|---|---:|---:|---:|---:|
| bandit_v3_banditfix r1 | 27 | best-iter dirs | 63 | 231 | **3.67** | **258.9** |
|  |  | worst-iter dir | 24 | 3 | 0.12 | 0.0 |
|  |  | other ref dirs | 131 | 22 | 0.17 | 4.8 |
| bandit_v3_banditfix r2 | 29 | best-iter dirs | 74 | 200 | **2.70** | **180.1** |
|  |  | worst-iter dir | 18 | 4 | 0.22 | 0.0 |
|  |  | other ref dirs | 166 | 21 | 0.13 | 10.5 |
| bandit_v4 r1 | 29 | best-iter dirs | 71 | 245 | **3.45** | **133.9** |
|  |  | worst-iter dir | 18 | 8 | 0.44 | 0.0 |
|  |  | other ref dirs | 183 | 45 | 0.25 | 9.1 |

A `best`-tagged directory receives **14-22x more Read calls per available
slot** than an unmarked reference directory across all three runs, and
**15-54x more lines per slot**. The `worst` directory is read at the same
rate as or below a random reference directory (0.12-0.44 reads/slot), and
zero lines in all three runs — the proposer selectively trusts the `best`
hint and effectively ignores `worst`.

### Without best/worst hints, attention defaults to recency

For `default+direction` the policy exposes *all* prior iter dirs without any
best/worst label. Bucketing the same reads-per-slot metric by recency of the
exposed iter, recomputed against the three default+direction runs in
`docs/experiment_detail.md`:

| run | recent (last 3) | middle | early (first 3) |
|---|---:|---:|---:|
| LME default+direction (015454) | 2.24 | 0.31 | 0.04 |
| LME default+direction (152524) | 2.23 | 0.68 | 0.01 |
| LoCoMo default+direction (015441) | 2.93 | 0.39 | 0.09 |

Early iterations are read 30-220x less often than the most recent three.
With no policy hint, the proposer falls back to a strong recency prior.

### Bandit pulls attention back into early and middle iters

The same recency bucketing applied to LongMemEval bandit_v3_banditfix r1
versus the matched LME default+direction (015454):

| bucket | bandit (banditfix r1) reads/slot | default+direction (015454) reads/slot |
|---|---:|---:|
| recent (last 3) | 2.27 | 2.24 |
| middle | **0.71** | 0.31 |
| early (first 3) | **0.18** | 0.04 |

Recent-iter coverage is essentially unchanged, but middle iters receive ~2.3x
more reads per slot under bandit, and early iters ~4.5x more. The bandit's
`best_iterations` list pulls the proposer back to older iterations that the
recency prior would otherwise skip.

### Takeaways

- The adaptive policies' main effect on read behavior is *redistribution*, not
  reduction: total Read calls per iteration are similar to `default+direction`
  (~21–23 reads/iter) but the targets shift.
- The `best_iterations` slot is the primary lever; bandit-marked best dirs
  receive **14-22x** more reads per slot than unmarked refs across the three
  retained LongMemEval bandit runs.
- The `worst_iteration` slot has near-zero observable effect on the proposer's
  read distribution; if a future revision keeps it, the worst summary should be
  surfaced more directly in the prompt rather than only as a referenced dir.
- Without bandit hints, the proposer defaults to strong recency bias and
  almost never re-reads early iterations; this is the failure mode that the
  best-iter pointer corrects.
