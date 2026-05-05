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

For example, LoCoMo claudekimi progressive has only one final retained best
candidate, but it had five score-improvement events during training:

| iteration | budget | passrate |
|---:|---|---:|
| 1 | low | 0.3750 |
| 2 | low | 0.3875 |
| 5 | low | 0.4125 |
| 13 | high | 0.4250 |
| 20 | high | 0.4375 |

LoCoMo claudekimi bandit likewise has one final retained best candidate, but
six process breakthroughs:

| iteration | budget | passrate |
|---:|---|---:|
| 1 | low | 0.3000 |
| 2 | medium | 0.3000 |
| 3 | medium | 0.3750 |
| 9 | high | 0.3875 |
| 12 | medium | 0.4125 |
| 22 | high | 0.4375 |

The `iter002` row is counted because `average_score` improved even though the
displayed passrate remained 0.3000.

## Breakthroughs By Budget

Across all retained adaptive runs in `PIPELINE.md`, excluding default and opus,
the process-breakthrough distribution is:

| benchmark | run | low | medium | high | total |
|---|---|---:|---:|---:|---:|
| LoCoMo | claudekimi progressive | 3 | 0 | 2 | 5 |
| LoCoMo | claudekimi bandit | 1 | 3 | 2 | 6 |
| LoCoMo | codex54 progressive | 3 | 0 | 1 | 4 |
| LoCoMo | codex54 bandit | 1 | 2 | 1 | 4 |
| LongMemEval | claudekimi progressive | 2 | 2 | 2 | 6 |
| LongMemEval | claudekimi bandit | 1 | 5 | 1 | 7 |
| LongMemEval | codex54 progressive | 3 | 1 | 2 | 6 |
| LongMemEval | codex54 bandit | 1 | 3 | 1 | 5 |
| SWE-bench mini | mimo progressive | 1 | 0 | 1 | 2 |
| SWE-bench mini | DeepSeek bandit | 1 | 2 | 0 | 3 |
| **total** |  | **17** | **18** | **13** | **48** |

On the full training horizon, low and medium account for most score
improvements. This is the optimistic view of the adaptive policies: narrow
contexts are often enough to find early gains, and medium budget is especially
productive for bandit.

## After Iteration 5

The full-horizon count is biased by the first few iterations. Early candidates
start from a low baseline, so they have more headroom and often improve without
needing much context. A stricter view is to count only breakthroughs after
iteration 5.

Raw breakthrough counts after iteration 5:

| benchmark | run | low | medium | high | total |
|---|---|---:|---:|---:|---:|
| LoCoMo | claudekimi progressive | 0 | 0 | 2 | 2 |
| LoCoMo | claudekimi bandit | 0 | 1 | 2 | 3 |
| LoCoMo | codex54 progressive | 1 | 0 | 1 | 2 |
| LoCoMo | codex54 bandit | 0 | 0 | 1 | 1 |
| LongMemEval | claudekimi progressive | 0 | 2 | 2 | 4 |
| LongMemEval | claudekimi bandit | 0 | 3 | 1 | 4 |
| LongMemEval | codex54 progressive | 1 | 1 | 2 | 4 |
| LongMemEval | codex54 bandit | 0 | 0 | 1 | 1 |
| SWE-bench mini | mimo progressive | 0 | 0 | 1 | 1 |
| SWE-bench mini | DeepSeek bandit | 0 | 0 | 0 | 0 |
| **total** |  | **2** | **7** | **13** | **22** |

However, raw counts are still not enough, because after warm-up the policies
spend many more iterations at `high`. The denominator matters:

| budget | post-5 iterations | post-5 breakthroughs | breakthrough rate |
|---|---:|---:|---:|
| low | 18 | 2 | 11.1% |
| medium | 66 | 7 | 10.6% |
| high | 142 | 13 | 9.2% |
| **total** | **226** | **22** | **9.7%** |

So the post-warm-up distribution changes materially in two different ways:
`high` produces the most absolute breakthroughs, but it also gets by far the
most opportunities. Normalized by how often each budget is used, `high` is not
more efficient per iteration than low or medium in this sample.

Per-run post-5 exposure and breakthrough rates:

| benchmark | run | low | medium | high |
|---|---|---:|---:|---:|
| LoCoMo | claudekimi progressive | 0/3 | 0/3 | 2/18 |
| LoCoMo | claudekimi bandit | 0/0 | 1/13 | 2/12 |
| LoCoMo | codex54 progressive | 1/2 | 0/2 | 1/21 |
| LoCoMo | codex54 bandit | 0/0 | 0/8 | 1/14 |
| LongMemEval | claudekimi progressive | 0/4 | 2/5 | 2/16 |
| LongMemEval | claudekimi bandit | 0/0 | 3/13 | 1/12 |
| LongMemEval | codex54 progressive | 1/4 | 1/4 | 2/17 |
| LongMemEval | codex54 bandit | 0/0 | 0/8 | 1/17 |
| SWE-bench mini | mimo progressive | 0/5 | 0/6 | 1/4 |
| SWE-bench mini | DeepSeek bandit | 0/0 | 0/4 | 0/11 |

The better interpretation is:

- low and medium are useful for early exploration and cheap candidate
  discovery;
- medium remains useful after warm-up, especially for claudekimi bandit on
  LongMemEval;
- high is where most later-stage gains happen in absolute count, mostly because
  the state machines spend far more post-warm-up iterations at high;
- per opportunity, post-warm-up high is not clearly more productive than low or
  medium in the retained runs;
- SWE-bench DeepSeek bandit is an important exception: its best train30
  improvement happens by iteration 5, so the post-5 table shows no additional
  breakthrough even though the medium-budget phase produced the key 0.5333
  train result.

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

The "progressive wins because it sees more useful iteration context, not
because it simply reads more files" hypothesis is supported for the retained
claudekimi memory runs, but not uniformly for every proposer.

On claudekimi memory benchmarks, progressive has both stronger test results
and smaller file/tool footprints than the default-family rows:

| benchmark | policy | test | tools/iter | files/iter | total/iter |
|---|---|---:|---:|---:|---:|
| LoCoMo | default | 0.3382 | 45.8 | 19.9 | 3.13M |
| LoCoMo | default+direction | 0.3458 best frontier | 53.1 | 20.0 | 4.37M |
| LoCoMo | progressive | **0.3734** | **35.2** | **15.1** | **1.86M** |
| LongMemEval | default | 0.4700 | 39.6 | 18.4 | 2.27M |
| LongMemEval | default+direction | 0.4950 rerun | 50.8 | 20.5 | 4.33M |
| LongMemEval | progressive | **0.5000** | **33.6** | **16.3** | **1.86M** |

This is a real behavioral difference: progressive does not win by widening
the file-access surface. It exposes a narrower reference set, selected from
the current optimization state, and the proposer spends its reads on those
state-selected iterations. The later "Reference-Iteration Read Distribution"
section shows the mechanism more directly: when policy-selected best
iterations are labelled, those directories receive ~10-15x more reads per
available slot than unmarked reference dirs.

For codex54 the claim is weaker. LoCoMo codex54 progressive beats default on
test (0.3589 vs 0.3368), but the file count is essentially tied (16.9 vs
16.8 files/iter) and total proposer token volume is higher (4.66M vs 2.80M).
So the robust claim is not "progressive always reads fewer files"; it is
"progressive can improve test performance by routing attention toward
selected best/worst iteration context, and on claudekimi memory runs that also
comes with fewer files and lower gross token volume."

## Budget-Conditioned Proposer Behavior

This section uses artifact-level `agent/tool_access.json` traces from complete
claudekimi memory runs only. Codex54 is excluded because its tool traces do
not preserve the same Read-tool structure, and docs-only rows cannot be
reconstructed per iteration. The auto-budget sample covers 150 proposer
iterations: LoCoMo progressive r1/r2, LoCoMo bandit r1/r2, and LongMemEval
progressive r1. The force-budget sample covers 180 proposer iterations from
the claudekimi `force=low` / `force=high` ablations. The primary table below
combines both sources by **actual budget tier**. Auto-budget rows tell us what
the policy naturally chooses during optimization; force-budget rows add
controlled exposure to a tier. The force rows are evidence about the tier's
behavior, not a replacement for the auto-budget distribution.

Combined auto + force behavior by actual budget:

| policy | budget | iters | tools/propose | reads/propose | lines/propose | unique files/propose | source reads/propose | summary reads/propose | ref reads/propose | ref read share | ref lines/propose | best reads/propose |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit | low | 62 | 37.40 | 21.21 | 2,326.2 | 15.58 | 11.21 | 7.87 | 0.02 | 0.1% | 0.0 | 0.00 |
| bandit | medium | 22 | 49.23 | 27.59 | 3,252.2 | 19.23 | 10.91 | 6.59 | 8.00 | 29.0% | 1,032.6 | 4.86 |
| bandit | high | 96 | 48.83 | 28.14 | 4,087.9 | 20.34 | 10.22 | 5.48 | 10.44 | 37.1% | 1,845.2 | 7.97 |
| progressive | low | 84 | 45.06 | 25.81 | 3,486.7 | 18.36 | 9.70 | 6.62 | 7.38 | 28.6% | 1,350.5 | NA |
| progressive | medium | 8 | 59.50 | 27.62 | 3,585.0 | 19.12 | 11.88 | 5.00 | 8.50 | 30.8% | 1,408.1 | NA |
| progressive | high | 58 | 52.14 | 30.28 | 4,000.8 | 20.60 | 10.19 | 6.10 | 11.86 | 39.2% | 1,846.6 | NA |

The key pattern is that budget mostly changes *reference-history exposure*,
not source-code reading. Source reads stay near 10-12 per propose across
budgets. What changes is the reference-iteration channel: bandit moves from
almost no ref reads at low (0.02/propose) to 8.00 at medium and 10.44 at high;
progressive moves from 7.38 at low to 8.50 at medium and 11.86 at high. The
line volume shows the same pattern. High budget is therefore not merely "more
files"; it is specifically more iteration-history reading.

For bandit, this also directly increases reads of policy-labelled best
iterations: best-iteration reads are 0.00/propose at low, 4.86/propose at
medium, and 7.97/propose at high. This supports the mechanism-level
interpretation that the policy's best-iteration pointers are an attention
prior. The auto-only and force-only splits below show where the combined
numbers come from.

Auto-budget behavior only:

| policy | budget | iters | tools/propose | reads/propose | lines/propose | unique files/propose | source reads/propose | summary reads/propose | ref reads/propose | ref read share | ref lines/propose | best reads/propose |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit | low | 2 | 31.00 | 16.50 | 2,068.0 | 15.50 | 9.50 | 5.50 | 0.00 | 0.0% | 0.0 | 0.00 |
| bandit | medium | 22 | 49.23 | 27.59 | 3,252.2 | 19.23 | 10.91 | 6.59 | 8.00 | 29.0% | 1,032.6 | 4.86 |
| bandit | high | 36 | 50.94 | 29.58 | 4,119.1 | 20.86 | 10.36 | 5.50 | 11.75 | 39.7% | 1,801.6 | 8.53 |
| progressive | low | 24 | 42.00 | 24.58 | 3,157.9 | 18.67 | 10.04 | 5.46 | 6.79 | 27.6% | 1,280.8 | NA |
| progressive | medium | 8 | 59.50 | 27.62 | 3,585.0 | 19.12 | 11.88 | 5.00 | 8.50 | 30.8% | 1,408.1 | NA |
| progressive | high | 58 | 52.14 | 30.28 | 4,000.8 | 20.60 | 10.19 | 6.10 | 11.86 | 39.2% | 1,846.6 | NA |

Force-budget behavior only:

| policy | forced budget | iters | tools/propose | reads/propose | lines/propose | unique files/propose | source reads/propose | summary reads/propose | ref reads/propose | ref read share | ref lines/propose | best reads/propose |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit | low | 60 | 37.62 | 21.37 | 2,334.8 | 15.58 | 11.27 | 7.95 | 0.02 | 0.1% | 0.0 | 0.00 |
| bandit | high | 60 | 47.57 | 27.27 | 4,069.2 | 20.03 | 10.13 | 5.47 | 9.65 | 35.4% | 1,871.3 | 7.63 |
| progressive | low | 60 | 46.28 | 26.30 | 3,618.2 | 18.23 | 9.57 | 7.08 | 7.62 | 29.0% | 1,378.4 | NA |

The auto-only split confirms the same tier ordering while preserving the
natural policy schedule: medium and high expose and attract much more
iteration-history reading than low. The force-only split is the controlled
ablation: bandit `force=low` almost eliminates reference-iteration reads,
while bandit `force=high` opens the iteration-history channel. That behavioral
change matches the result split in `PIPELINE.md`: LoCoMo benefits from
adaptive access to medium/high history, while LongMemEval's best bandit result
comes from keeping the UCB file prior but forcing low budget.

The practical interpretation is budget-dependent:

- low budget is a source/summaries mode; it is cheap and good for local
  candidate edits, but for bandit it largely removes historical iteration
  evidence;
- medium budget is the first tier where bandit best-iteration hints become
  behaviorally active;
- high budget mainly buys more reference-history reading, and especially more
  reads of policy-labelled best iterations;
- progressive's advantage on claudekimi is consistent with getting more value
  from selected iteration context while reading fewer files overall than the
  default-family baselines.

## Workspace Pool Inflates with Budget, Reads Do Not

The "After Iteration 5" view counts breakthroughs but not how much the
proposer has to wade through to find them. This section asks a separate
mechanistic question: when budget escalates from `low` to `high`, does the
agent actually read more files? The answer is that the workspace file pool
grows nearly an order of magnitude, but per-iteration unique-file reads stay
roughly flat. The implication is that adaptive-policy gains come from
*directing* the agent's attention, not from giving it a bigger pile to look
at.

Aggregating `agent/metrics.json` across all retained adaptive runs (6
bandit_v3 + 8 progressive runs, mixed claudekimi and codex54, 420 proposer
iterations total). Because metrics.json fields are populated for both
proposer agents, this slice is not restricted to claudekimi the way the prior
"Budget-Conditioned Proposer Behavior" section is.

| policy | budget | iters | workspace files (mean) | unique files read | read_file_calls | read_lines | duration_s |
|---|---|---:|---:|---:|---:|---:|---:|
| bandit | low    |   6 |  1,222 | 14.7 | 18.5 | 1,965 | 419 |
| bandit | medium |  66 |  5,916 | 18.2 | 24.4 | 2,922 | 597 |
| bandit | high   | 108 | 22,578 | 18.9 | 25.3 | 3,318 | 630 |
| progressive | low    |  59 |  3,166 | 17.8 | 23.1 | 2,857 | 682 |
| progressive | medium |  21 |  6,103 | 20.2 | 26.1 | 3,201 | 853 |
| progressive | high   | 160 | 21,413 | 18.9 | 25.7 | 3,301 | 792 |

The workspace file count is a proxy for what the agent could reach.
Escalating from `low` to `high` inflates the pool ~19x for bandit and ~7x
for progressive. But the agent's `unique_files_read` is essentially flat:
bandit moves from 14.7 to 18.9 (+28%), progressive moves from 17.8 to 18.9
(+6% then back). Read lines grow modestly (bandit +69%, progressive +15%)
and per-iter wall time grows 50% (bandit) or 16% (progressive). The agent
self-throttles to ~18-20 unique reads per iteration regardless of how many
files are physically copied into the workspace.

This is the structural confirmation behind the `Reference-Iteration Read
Distribution` finding below: the agent is not surveying the bigger pool and
picking more sources; it follows the curated menu the policy surfaces (hot
paths, best-iter pointers). The pool growth therefore mostly buys I/O cost
without behavioral change.

### Quality does not track pool size

Reading more does not produce systematically better candidates. Per-budget
mean passrate of *evaluated* candidates in the same 14-run sample:

| policy | low | medium | high |
|---|---:|---:|---:|
| bandit | 0.353 | 0.319 | 0.335 |
| progressive | 0.370 | 0.358 | 0.360 |

For both policies, low-budget candidates have the highest mean quality and
high is comparable to or slightly below low. Where `high` does pay off is
the long tail: the train-best candidate per run lands at `high` in 6/6
bandit runs and 6/8 progressive runs (the other two progressive bests are
at `low`). After base-rate adjustment (`high` occupies 60-67% of iters in
this sample), the relative over-representation of `high` for the run-best
candidate is **1.67x for bandit** and only **1.12x for progressive**.

Iter-position controls clarify the timing. Improvement rate (fraction of
iters whose evaluated passrate strictly exceeded the prior running best),
bucketed by iter range and budget:

| policy | iter range | low | medium | high |
|---|---|---:|---:|---:|
| bandit | 01-10 | 100% (6/6) | 20.0% (7/35) |  5.3% (1/19) |
| bandit | 11-20 |          - |  0.0% (0/21) | 12.8% (5/39) |
| bandit | 21-30 |          - |  0.0% (0/10) |  4.0% (2/50) |
| progressive | 01-10 | 50.0% (23/46) | 11.1% (1/9)  |  8.0% (2/25) |
| progressive | 11-20 | 20.0% (2/10)  |  0.0% (0/9)  |  9.8% (6/61) |
| progressive | 21-30 |  0.0% (0/3)   |  0.0% (0/3)  |  4.1% (3/74) |

These rates are consistent with the post-warm-up summary in `After
Iteration 5` (high ~9% post-5, similar magnitude across our 14-run cut).
Two patterns stand out:

- **Early iters at `low` are the most productive single setting** in the
  whole sample: progressive's 50% improvement rate at iter01-10 / `low` is
  the only cell that even approaches what is conceptually a steep early
  ramp.
- **Late iters (11-30) are dominated by `high`**: `medium` and `low` produce
  almost no breakthroughs after iter 10, while `high` keeps a 4-13%
  per-iter improvement rate. This is the only role where `high` is
  irreplaceable — late-stage stagnation rescue.

### Why this matters: focus is the real lever

Putting `After Iteration 5`, this section, and `Reference-Iteration Read
Distribution` together:

1. Budget controls how many reference-iter directories are physically
   exposed in the workspace (low ~1 to high ~20 dirs), which inflates the
   workspace pool ~19x.
2. The agent does not respond to that inflation. Unique reads per iter stay
   at ~18-20 across all budgets and policies.
3. What the agent does read is overwhelmingly steered by surfaced labels.
   In the next section, bandit-marked best-iter dirs receive ~10-15x more
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
- `medium` is the weakest standalone tier in this sample: 0/31 mid- and
  late-iter improvements for bandit, 0/12 for progressive. Its main
  remaining role appears to be transitional. A binary "stagnated -> high,
  otherwise -> low" policy would lose little observable optimization value
  in the retained runs while removing a tier.

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
how the bandit policy labelled it (`best_iterations`, `worst_iteration`, other
listed reference, or unlisted) and report **reads per available slot** across
the run. The slot normalization removes the confound of "how many iter dirs
were exposed".

### Bandit best-iter hints concentrate attention strongly

Two LongMemEval kimi `bandit_v3` runs, restricted to iterations whose policy
included a non-empty `best_iterations` list:

| run | bucket | slots | reads | reads/slot | lines/slot |
|---|---|---:|---:|---:|---:|
| mixed A | best-iter dirs | 58 | 124 | **2.14** | **513** |
| mixed A | worst-iter dir | 24 | 11 | 0.46 | 87 |
| mixed A | other ref dirs | 232 | 51 | 0.22 | 42 |
| mixed B | best-iter dirs | 77 | 227 | **2.95** | **586** |
| mixed B | worst-iter dir | 15 | 3 | 0.20 | 23 |
| mixed B | other ref dirs | 233 | 47 | 0.20 | 11 |

A `best`-tagged directory receives ~10–15× more Read calls per available slot
than an unmarked reference directory, and ~50× more lines in mixed B. The
`worst` directory is read at roughly the same rate as a random reference
directory; on lines/slot it is *less* read than other refs in mixed B. The
proposer selectively trusts the `best` hint and effectively ignores `worst`.

### Without best/worst hints, attention defaults to recency

For `default+direction` the policy exposes *all* prior iter dirs without any
best/worst label. Bucketing the same reads-per-slot metric by recency of the
exposed iter:

| run | recent (last 3) | middle | early (first 3) |
|---|---:|---:|---:|
| LME default+direction A | 1.79 | 0.26 | 0.03 |
| LME default+direction B | 1.30 | 0.48 | 0.00 |
| LoCoMo default+direction A | 2.06 | 0.26 | 0.04 |

Early iterations are read ~50–70× less often than the most recent three. With
no policy hint, the proposer falls back to a strong recency prior.

### Bandit pulls attention back into early and middle iters

The same recency bucketing applied to LME bandit_v3 mixed B and the matched
`default+direction` baseline:

| bucket | bandit mixed B reads/slot | default+direction A reads/slot |
|---|---:|---:|
| recent (last 3) | 1.68 | 1.79 |
| middle | **0.72** | 0.26 |
| early (first 3) | **0.14** | 0.03 |

Recent-iter coverage is essentially unchanged, but middle iters receive ~2.8×
more reads per slot under bandit, and early iters ~5× more. The bandit's
`best_iterations` list pulls the proposer back to older iterations that the
recency prior would otherwise skip.

### Takeaways

- The adaptive policies' main effect on read behavior is *redistribution*, not
  reduction: total Read calls per iteration are similar to `default+direction`
  (~21–23 reads/iter) but the targets shift.
- The `best_iterations` slot is the primary lever; bandit-marked best dirs
  receive ~10–15× more reads per slot than unmarked refs.
- The `worst_iteration` slot has near-zero observable effect on the proposer's
  read distribution; if a future revision keeps it, the worst summary should be
  surfaced more directly in the prompt rather than only as a referenced dir.
- Without bandit hints, the proposer defaults to strong recency bias and
  almost never re-reads early iterations; this is the failure mode that the
  best-iter pointer corrects.
