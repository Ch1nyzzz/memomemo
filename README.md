# CuraHarness

CuraHarness is a meta-agent optimization harness and the evidence corpus behind an
ongoing mechanism study of **how LLM meta-agents actually optimize agent scaffolds**.

An LLM proposer (Claude / Kimi / Codex) iteratively rewrites memory-agent scaffolds
against conversational-memory benchmarks (LOCOMO, LongMemEval), with every
iteration's workspace, prompt, diff, and evaluation archived for post-hoc analysis.
The harness exists both to optimize and to *observe the optimizer*: which evidence
it reads, where its edits land, and what it never touches.

## Research findings (the short version)

Optimization by meta-agents is bounded on both ends, and the boundary is set by
what the proposer conditions on — not by permissions or capability:

- **Reading is bounded** (accessible ≠ inspected): exposed iteration histories are
  mostly never opened; replicated across all runs in the frozen analysis set.
- **Editing is bounded** (editable ≠ edited): edits concentrate on prompts and
  point fixes; LLM-call topology stays frozen in 15/17 runs; of ~1.7k functions
  added by proposers, ~1% contain an LLM call.
- **Defining dimensions as explicit affordances widens exploration**: a controlled
  bare-vs-afford intervention (2 proposers × 3 domains, 12 runs on a unified
  substrate) shifts edits into structural dimensions, replicated across proposers.

Where to read more:

| Document | Content |
|---|---|
| `docs/AFFORDANCE_INTERVENTION.md` | Intervention experiment: design, 12-run results, held-out scores, unified narrative |
| `docs/EXPERIMENT_INSIGHTS.md` | Accumulated observations from harness runs |
| `docs/PIPELINE.md` | How the optimization pipeline works end to end |
| `analysis/` | Frozen-set measurement scripts and probe outputs |
| `AGENTS.md` | Operational recipes (docker images, credentials, test evaluation) |

The paper lives in the standalone `Cura_paper` repo; the self-contained
intervention codebase lives outside this repo (see the intervention doc).

## The harness

`memomemo optimize` runs the loop:

1. iteration 0 evaluates seed scaffolds (or loads precomputed baselines);
2. the proposer CLI is invoked in a Docker sandbox with a scoped workspace
   (source snapshot, cumulative summaries, reference iterations);
3. the proposer writes one candidate plus `pending_eval.json`;
4. the harness evaluates it and updates `best_candidates.json` / the Pareto
   frontier over `passrate` (up) and `token_consuming` (down).

Seed scaffold families under `src/memomemo/scaffolds/`: `bm25` (lexical
baseline), `mem0_source`, `memgpt_source`, `membank_source` (source-informed
reimplementations of mem0 / MemGPT / MemoryBank). Selection policies include
fixed-budget, progressive context escalation, and bandit.

Every proposer session archives `meta.json`, `tool_access.json`, and
`metrics.json` (tokens, cost, per-file read/write counts) — this instrumentation
is what makes the read/edit-boundary analysis possible.

## Quickstart

```bash
python -m pip install -e '.[dev]'          # add ,source for mem0/MemGPT/MemoryBank deps
scripts/fetch_reference_repos.sh           # optional upstream reference checkouts
pytest -q
```

Prepare data:

```bash
memomemo locomo prepare                    # add --allow-download without a local cache
memomemo longmemeval prepare --variant s --allow-download
```

Smoke test the loop:

```bash
memomemo optimize --run-id smoke_opt --iterations 1 --limit 3 --dry-run \
  --scaffold-extra-json @configs/source_memory.example.json
```

Real run (Claude proposer, Docker sandbox):

```bash
set -a && source .env && set +a
python -m memomemo.cli optimize --locomo \
  --run-id locomo_opt --iterations 20 --split train \
  --baseline-dir runs/baselines \
  --scaffold-extra-json @configs/source_memory.example.json \
  --model /data/home/yuhan/model_zoo/Qwen3-8B \
  --base-url http://127.0.0.1:8000/v1 \
  --proposer-agent claude --proposer-sandbox docker \
  --proposer-docker-image docker-claude:latest \
  --proposer-docker-home /home/yuhan \
  --proposer-docker-mount /data/home/yuhan/.claude:/home/yuhan/.claude:ro \
  --proposer-docker-mount /data/home/yuhan/.claude.json:/home/yuhan/.claude.json:ro
```

For the Kimi proposer use `--proposer-agent kimi` with
`--proposer-docker-image docker-claude-kimi:latest --proposer-docker-home /tmp
--proposer-docker-env KIMI_API_KEY` (never `docker-claude:latest` for Kimi —
see `AGENTS.md` for why, plus the held-out test-evaluation recipe via
`scripts/evaluate_candidate_json.py`).

Long jobs should be detached with `setsid ... < /dev/null &` so they survive
the launching session.

## Run artifacts

Each run directory under `runs/<run-id>/` contains:

- `evolution_summary.jsonl`, `best_candidates.json`, `candidate_score_table.json`
- `proposer_calls/iter_<NNN>/{workspace,source_snapshot,eval}/` — the exact
  material the proposer saw, and what it did with it
- `generated/` — proposer-written candidate code
- `reports/`, `candidate_results/`, `trace_slices/`, `iteration_index.json`,
  `diff_summary.jsonl`

Treat run outputs as data, not source; they are the raw material for `analysis/`.

## Repository layout

```
src/memomemo/        core package (optimizer loop, scaffolds, CLI)
src/optiharness/     legacy package name kept for compatibility
scripts/             launch, evaluation, and figure scripts
configs/             example scaffold/LLM configuration
analysis/            frozen-set measurements and trajectory probes
docs/                pipeline docs, experiment insights, intervention results
paper/               figure sources (paper text moved to Cura_paper repo)
tests/               pytest suite (`pytest -q`)
runs/, logs/         run artifacts (not source)
references/          upstream reference checkouts (vendor/)
```
