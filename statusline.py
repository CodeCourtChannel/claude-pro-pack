#!/usr/bin/env python3
"""Pro Pack status line: plan bars, context size, effort and the prompt cache, from the JSON Claude Code sends on stdin.
   5h 23% (2h10m) · 7d 41% · ctx 34k · high · cache warm 52m · hit 91%
settings.json: "statusLine": {"type": "command", "command": "python3 ~/.claude/statusline.py"}"""
import json, sys, time

d = json.load(sys.stdin)
now, out = time.time(), []


def left(ts):
    s = max(0, int(ts - now))
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m"


rl = d.get("rate_limits") or {}
for k, lab in (("five_hour", "5h"), ("seven_day", "7d")):
    w = rl.get(k) or {}
    if w.get("used_percentage") is not None:
        out.append(f"{lab} {w['used_percentage']:.0f}%" + (f" ({left(w['resets_at'])})" if k == "five_hour" and w.get("resets_at") else ""))
cw = d.get("context_window") or {}
if cw.get("total_input_tokens") is not None:
    out.append(f"ctx {cw['total_input_tokens'] / 1000:.0f}k")
if (d.get("effort") or {}).get("level"):
    out.append(d["effort"]["level"])
pc = d.get("prompt_cache")
if pc:
    if pc.get("warm") and pc.get("expires_at"):
        out.append(f"cache warm {left(pc['expires_at'])}")
    else:
        out.append(f"cache cold: next message re-reads {pc.get('recache_tokens_if_cold', 0) / 1000:.0f}k" if pc.get("recache_tokens_if_cold") else "cache cold")
    if pc.get("hit_ratio") is not None:
        out.append(f"hit {pc['hit_ratio'] * 100:.0f}%")
print(" · ".join(out) or (d.get("model") or {}).get("display_name", ""))
