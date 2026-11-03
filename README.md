# coding-bench

Can a local or free model replace Claude Code? 23 small but real coding tasks (20 everyday, 3 hard), each graded by
hidden tests the agent never sees. Agents run the real tools (Claude Code, OpenCode), so a score
measures the harness and the model together.

| Agent key | What runs | Cost | Data leaves the laptop |
|---|---|---|---|
| `claude` | Claude Code + Opus 5.5 | Claude subscription | yes (Anthropic) |
| `sonnet` | Claude Code + Sonnet 5.5 | Claude subscription | yes (Anthropic) |
| `qwen` | OpenCode + Qwen3.6-35B-A3B on llama.cpp (port 18434) | free | no |
| `deepseek` | OpenCode + `opencode/deepseek-v4.1-flash-free` (Zen) | free, limited time | yes (OpenCode Zen) |
| `dsh-qwen` | DeepSeek Harness (dsh, headless) + the same local Qwen | free | no |

## Tasks

Bug fixes (01 Elo, 03 privacy regex, 08 CSV import, 15 chunker, 20 failing suite), features
(02 PGN, 04 pace, 05 TTL cache, 06 time-weighted return, 07 SM-2, 10 async retry, 13 vault
links, 14 free calendar slots, 17 schema validator, 18 MoE top-k, 19 migrations), multi-file
refactor (09), debugging a crash from a traceback (11), performance (12), CLI change that must
keep old output (16). Hard tier: 21 chess perft move generator, 22 regex engine checked against
Python's `re`, 23 mini SQL engine checked against sqlite3.

Each `tasks/<id>/` holds `task.md` (the prompt), `repo/` (starting code) and
`grade/test_hidden.py`. `solutions/<id>/` holds a reference solution used only by `--verify`.

## Run

```
python run.py --verify                          # every task: start fails, reference passes
python run.py --agents qwen --only 01,02        # quick try
python run.py --agents claude,qwen,deepseek     # full run -> results/<stamp>.md and .jsonl
```

Work folders and agent logs stay in `%TEMP%\coding-bench-runs\<stamp>\` for inspection. Each
result row records the power state; run local models on AC, or their timings mean little.

## Results (2 to 3 November 2026)

| Agent | Passed | Everyday | Hard | Median time per task |
|---|---|---|---|---|
| Claude Code + Opus 5.5 | 23/23 | 20/20 | 3/3 | 52 s |
| OpenCode + DeepSeek V4.1 Flash (free) | 22/23 | 20/20 | 2/3 | 36 s |
| OpenCode + Qwen3.6-35B-A3B (local) | 17/23 | 16/20 | 1/3 | 195 s |
| DeepSeek Harness + the same Qwen (local) | 14/23 | 14/20 | 0/3 | 138 s |

Raw rows in `results/*.jsonl`. Write-up with charts: https://sergioadan.dev/work/coding-bench

## Running it on your machine

The tool paths at the top of `run.py` (OpenCode, the DeepSeek Harness, the llama.cpp key file) point at my laptop;
change them to yours. Every task folder has `task.md` (the prompt), `repo/` (the starting code) and `grade/`
(hidden tests, copied in only after the agent stops); `solutions/` holds a reference solution per task, and
`python run.py --verify` checks that each task starts failing and passes with its solution.

MIT licence.

