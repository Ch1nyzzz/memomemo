# Experiment Detail

This note uses auto-budget runs only. Runs with `budgethigh`, `budgetlow`, or
`force-budget` are excluded. `default` and `default+direction` are grouped as
`default-family` where noted. Reported standard deviations are sample standard
deviations.

## LoCoMo / claudekimi / default-family

Excluded: `locomo_memgpt_claudekimi_default_direction_docker_iter30_train80_20260502_154556`
because its test score is 0.3458.

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.3750 | 0.3423 | `locomo_memgpt_claudekimi_default_autobudget_docker_iter30_train80_r1_20260504_162844` |
| done | 30 | 0.3875 | 0.3140 | `locomo_memgpt_claudekimi_default_direction_docker_iter30_train80_20260502_015441` |
| done | 30 | 0.4125 | 0.3382 | `locomo_memgpt_claudekimi_default_docker_iter30_train80_20260501_204004` |

| metric | value |
|---|---:|
| train mean | 0.3917 |
| train std | 0.0191 |
| test mean | 0.3315 |
| test std | 0.0153 |

Best retained run by test score: `locomo_memgpt_claudekimi_default_autobudget_docker_iter30_train80_r1_20260504_162844`.

| proposer metric | value |
|---|---:|
| calls | 30 |
| input_tokens | 4,537,976 |
| output_tokens | 801,091 |
| total_tokens | 5,339,067 |
| cache_creation_input_tokens | 0 |
| cache_read_input_tokens | 97,353,020 |
| total_reported_tokens | 102,692,087 |
| estimated_cost_usd | 97.545603 |
| duration_s | 23,167.783 |
| tool_calls | 1,397 |
| read_file_calls | 831 |
| read_lines | 144,765 |
| write_file_calls | 129 |
| written_lines | 15,546 |
| unique_files_read | 120 |
| tool_counts | Bash 556; Edit 90; Glob 12; Grep 31; Read 669; Write 39 |

## LoCoMo / codex54 / default-family

Excluded: `locomo_memgpt_codex54_default_docker_iter30_train80_20260501_204007`
because its test score is 0.3899. The currently running r3 is not included
below until it finishes.

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.4250 | 0.3154 | `locomo_memgpt_codex54_default_codexlogin_autobudget_docker_iter30_train80_r1_20260504_163640` |
| done | 30 | 0.4375 | 0.3368 | `locomo_memgpt_codex54_default_docker_iter30_train80_rerun_20260502_015354` |

## LongMemEval / claudekimi / default-family

Excluded: `longmemeval_memgpt_claudekimi_default_autobudget_docker_iter30_train100_r1_20260504_162844`
because it has the highest test score, 0.5400.

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.6500 | 0.5300 | `longmemeval_memgpt_claudekimi_default_direction_docker_iter30_train100_20260502_015454` |
| done | 30 | 0.5500 | 0.4950 | `longmemeval_memgpt_claudekimi_default_direction_docker_iter30_train100_20260502_152524` |
| docs-only | - | 0.5600 | 0.4700 | pipeline default row; artifact not found |

| metric | value |
|---|---:|
| train mean | 0.5867 |
| train std | 0.0551 |
| test mean | 0.4983 |
| test std | 0.0301 |

Best retained run by test score: `longmemeval_memgpt_claudekimi_default_direction_docker_iter30_train100_20260502_015454`.

| proposer metric | value |
|---|---:|
| calls | 31 |
| input_tokens | 5,462,809 |
| output_tokens | 941,764 |
| total_tokens | 6,404,573 |
| cache_creation_input_tokens | 0 |
| cache_read_input_tokens | 108,457,505 |
| total_reported_tokens | 114,862,078 |
| estimated_cost_usd | 120.300745 |
| duration_s | 30,512.394 |
| tool_calls | 1,544 |
| read_file_calls | 857 |
| read_lines | 132,876 |
| write_file_calls | 98 |
| written_lines | 34,658 |
| unique_files_read | 116 |
| tool_counts | Bash 690; Edit 37; Glob 19; Grep 58; Read 679; Write 61 |

## Auto-Budget Count = 3 Cells

These cells have exactly three retained auto-budget entries under the current
counting rules. Cells with all three test scores available include mean/std
statistics. Cells with an active third run list the available entries and defer
mean/std until that run finishes.

### LoCoMo / claudekimi / bandit

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.3875 | 0.3458 | `locomo_memgpt_claudekimi_bandit_v3_autobudget_docker_iter30_train80_w16_r1_20260504_162844` |
| done | 30 | 0.4125 | 0.3347 | `locomo_memgpt_claudekimi_bandit_v3_autobudget_docker_iter30_train80_w16_r2_20260504_162844` |
| docs-only | - | 0.4375 | 0.3589 | pipeline bandit row |

| metric | value |
|---|---:|
| train mean | 0.4125 |
| train std | 0.0250 |
| test mean | 0.3465 |
| test std | 0.0121 |

Best retained run by test score: pipeline bandit row. Artifact-level proposer
metrics are unavailable for this docs-only row; available pipeline token
metrics are:

| proposer metric | value |
|---|---:|
| input/iter | 104.2k |
| output/iter | 29.8k |
| cache reads/iter | 1.83M |
| total/iter | 1.96M |
| tools/iter | 35.1 |
| files/iter | 17.6 |
| dur/iter | 14.1m |

### LoCoMo / claudekimi / progressive

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.4000 | 0.3313 | `locomo_memgpt_claudekimi_progressive_autobudget_docker_iter30_train80_r1_20260504_162844` |
| done | 30 | 0.4000 | 0.3589 | `locomo_memgpt_claudekimi_progressive_autobudget_docker_iter30_train80_r2_20260504_162844` |
| docs-only | - | 0.4375 | 0.3734 | pipeline progressive row |

| metric | value |
|---|---:|
| train mean | 0.4125 |
| train std | 0.0217 |
| test mean | 0.3545 |
| test std | 0.0214 |

Best retained run by test score: pipeline progressive row. Artifact-level
proposer metrics are unavailable for this docs-only row; available pipeline
token metrics are:

| proposer metric | value |
|---|---:|
| input/iter | 138.9k |
| output/iter | 25.5k |
| cache reads/iter | 1.70M |
| total/iter | 1.86M |
| tools/iter | 35.2 |
| files/iter | 15.1 |
| dur/iter | 13.0m |

### LoCoMo / codex54 / bandit

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.3875 | 0.3361 | `locomo_memgpt_codex54_bandit_v3_codexlogin_autobudget_docker_iter30_train80_w16_r1_20260504_163640` |
| done | 30 | 0.4250 | 0.3147 | `locomo_memgpt_codex54_bandit_v3_codexlogin_autobudget_docker_iter30_train80_w16_r2_20260504_163640` |
| docs-only | - | 0.4250 | 0.3865 | pipeline bandit row |

| metric | value |
|---|---:|
| train mean | 0.4125 |
| train std | 0.0217 |
| test mean | 0.3458 |
| test std | 0.0369 |

Best retained run by test score: pipeline bandit row. Artifact-level proposer
metrics are unavailable for this docs-only row; available pipeline token
metrics are:

| proposer metric | value |
|---|---:|
| input/iter | 1.13M |
| output/iter | 20.7k |
| cache reads/iter | 995k |
| total/iter | 2.14M |
| tools/iter | 34.6 |
| files/iter | 18.5 |
| dur/iter | 7.0m |

### LoCoMo / codex54 / progressive

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.4250 | 0.3879 | `locomo_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train80_r1_20260504_163640` |
| done | 30 | 0.4000 | 0.3747 | `locomo_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train80_r2_20260504_163640` |
| docs-only | - | 0.4250 | 0.3589 | pipeline progressive row |

| metric | value |
|---|---:|
| train mean | 0.4167 |
| train std | 0.0144 |
| test mean | 0.3738 |
| test std | 0.0145 |

Best retained run by test score: `locomo_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train80_r1_20260504_163640`.

| proposer metric | value |
|---|---:|
| calls | 30 |
| input_tokens | 38,019,920 |
| output_tokens | 778,376 |
| total_tokens | 38,798,296 |
| cache_creation_input_tokens | 0 |
| cache_read_input_tokens | 34,916,096 |
| total_reported_tokens | 73,714,392 |
| estimated_cost_usd | 0.0 |
| duration_s | 15,268.415 |
| tool_calls | 914 |
| read_file_calls | 658 |
| read_lines | 77,385 |
| write_file_calls | 0 |
| written_lines | 0 |
| unique_files_read | 108 |
| tool_counts | Shell 914 |

### LongMemEval / claudekimi / progressive

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.6100 | 0.4950 | `longmemeval_memgpt_claudekimi_progressive_autobudget_docker_iter30_train100_r1_20260504_162844` |
| running | 19 | 0.5400 | NA | `longmemeval_memgpt_claudekimi_progressive_autobudget_docker_iter30_train100_r2_rerun429_20260504_212541` |
| docs-only | - | 0.6000 | 0.5000 | pipeline progressive row |

Mean/std are deferred until the running r2 finishes and has a valid test score.

### LongMemEval / codex54 / bandit

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| running | 21 | 0.4100 | NA | `longmemeval_memgpt_codex54_bandit_v3_codexlogin_banditfix_autobudget_docker_iter30_train100_w16_r1_20260505_002048` |
| running | 21 | 0.5500 | NA | `longmemeval_memgpt_codex54_bandit_v3_codexlogin_banditfix_autobudget_docker_iter30_train100_w16_r2_20260505_002048` |
| done | 30 | 0.5200 | 0.4725 | `longmemeval_memgpt_codex54_bandit_v3_docker_iter30_train100_w16_20260501_203909` |

Mean/std are deferred until the two running runs finish and have valid test
scores.

### LongMemEval / codex54 / default-family

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.5700 | 0.5075 | `longmemeval_memgpt_codex54_default_codexlogin_autobudget_docker_iter30_train100_r1_20260504_163640` |
| running | 16 | 0.5200 | NA | `longmemeval_memgpt_codex54_default_codexlogin_autobudget_docker_iter30_train100_r3_retryenv_20260505_005443` |
| docs-only | - | 0.6000 | 0.4875 | pipeline default row |

Mean/std are deferred until the running r3 finishes and has a valid test score.

### LongMemEval / codex54 / progressive

| status | iter | train | test | run |
|---|---:|---:|---:|---|
| done | 30 | 0.6100 | 0.5275 | `longmemeval_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train100_r1_20260504_163640` |
| done | 30 | 0.5500 | 0.4975 | `longmemeval_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train100_r2_20260504_163640` |
| docs-only | - | 0.5400 | 0.4725 | pipeline progressive row |

| metric | value |
|---|---:|
| train mean | 0.5667 |
| train std | 0.0379 |
| test mean | 0.4992 |
| test std | 0.0275 |

Best retained run by test score: `longmemeval_memgpt_codex54_progressive_codexlogin_autobudget_docker_iter30_train100_r1_20260504_163640`.

| proposer metric | value |
|---|---:|
| calls | 30 |
| input_tokens | 41,329,300 |
| output_tokens | 717,251 |
| total_tokens | 42,046,551 |
| cache_creation_input_tokens | 0 |
| cache_read_input_tokens | 37,672,832 |
| total_reported_tokens | 79,719,383 |
| estimated_cost_usd | 0.0 |
| duration_s | 14,377.084 |
| tool_calls | 965 |
| read_file_calls | 675 |
| read_lines | 83,999 |
| write_file_calls | 0 |
| written_lines | 0 |
| unique_files_read | 114 |
| tool_counts | Shell 965 |
