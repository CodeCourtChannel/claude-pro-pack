# Pro Pack: a Claude Code setup for the $20 plan

From the CodeCourt video **Master Claude's Tokens in 10 Minutes (Every Setting, Tested)**: 88 measured runs, every coding run graded by hidden tests.

Two files and six habits. Every part is here because a measured test won; the parts that lost are listed at the end.

## Install (2 minutes)

1. Copy `statusline.py` to `~/.claude/statusline.py`:

```sh
mkdir -p ~/.claude && curl -fsSL https://raw.githubusercontent.com/CodeCourtChannel/claude-pro-pack/main/statusline.py -o ~/.claude/statusline.py
```

2. Merge `settings.json` into `~/.claude/settings.json` (create it if it doesn't exist):

```json
{
  "model": "sonnet",
  "statusLine": {"type": "command", "command": "python3 ~/.claude/statusline.py"}
}
```

3. Start a new Claude Code session. The bottom line now shows your five-hour and weekly bars, context size, effort and whether the prompt cache is still warm:

```
5h 23% (2h10m) · 7d 41% · ctx 34k · medium · cache warm 52m · hit 91%
```

## The six habits

| Habit | What we measured |
|---|---|
| **Work on Sonnet, not the default Opus.** | Same 20-request work day: half the cost, the same visible tests passing. On four single tasks Opus cost 2–3× Sonnet for the same hidden-test score. |
| **Switch to Haiku (`/model haiku`) for tasks with a written spec and tests, at the start of a session.** | 5–15× cheaper than Sonnet, same score on every spec'd task. It is slower on hard tasks, and on the work day it left a month-end crash that no test reported in both runs (Sonnet fixed it in 4 of 5 runs, Opus in 2 of 2). |
| **Leave effort on medium.** | Low to max on a hard task: every level passed all 16 hidden tests; max cost 8–12.5× medium and took 11 minutes instead of 1. |
| **Don't switch model in the middle of a session.** | Each model has its own cache: the next message cost 4.5× a normal one. Changing effort mid-session is free. |
| **Don't `/clear` after every small task. Clear every few tasks.** | Clearing after every task cost 2.15× staying in one thread. Clearing every 5 tasks cost about the same as one thread. `/compact` every 5 cost 30 % more. |
| **Back after an hour? The cache is gone.** | A one-word reply after 61 minutes away cost 20× the same reply after 6 minutes. The status line shows `cache cold` with how much the next message re-reads, so you can `/clear` first instead. |

## Tested and left out

- **Subagents** (a Haiku scout under Sonnet, a Sonnet builder under Opus): 1.4–1.6× the cost of one model alone.
- **The advisor** (`--advisor opus`): Haiku + Opus advisor cost 21× Haiku alone; Sonnet never called it.
- **`opusplan`**: 2× plain Opus.
- **A router mod** (Opus for the first request, Haiku for the rest): 5× cheaper than Opus, but 2.4× Haiku alone.
- **A hook that trims long command output**: no measurable gain. Claude already pipes chatty output through `tail` or `grep`, and Claude Code caps long output by itself.

## What the tests don't cover

Costs are the API-equivalent dollar figures Claude Code reports, a proxy: the plan isn't billed this way and Anthropic publishes no token figure for the limits. Tasks were small Python repos with a written spec and tests, two or three runs per setting. Limits and defaults can change; check the plan's current docs.
