"""Figure 1: effect of the company sales prompt on the dark-pattern rate, per model.

Reads results/v1/numbers.json (written by src/verify.py), so the figure shows exactly the
README numbers. Primary judge: Gemini 3.8 Flash.
Usage: uv run python src/figure.py   (writes figures/fig1_sales_effect.png)
"""

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
N = json.loads((ROOT / "results/v1/numbers.json").read_text())
SURFACE, INK, INK2, GRID, BLUE = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#2a78d6"

rows = [("All six models", "sales_all"), ("Qwen3.8-27B", "sales_Qwen"), ("Mistral Small 4", "sales_Mistral"),
        ("GPT-6 Luna", "sales_Luna"), ("Claude Sonnet 5.5", "sales_Sonnet"), ("Claude Haiku 5.5", "sales_Haiku"),
        ("Claude Opus 5.5", "sales_Opus")]


def parse(s):
    est, lo, hi = map(float, re.findall(r"[+-]\d+\.\d", s)[:3])
    return est, lo, hi


fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
for i, (label, key) in enumerate(rows):
    est, lo, hi = parse(N[key])
    y = len(rows) - 1 - i
    ax.plot([lo, hi], [y, y], color=BLUE, lw=2, solid_capstyle="round")
    ax.plot(est, y, "o", ms=8 if i else 10, color=BLUE, mec=SURFACE, mew=2)
    ax.text(hi + 1.2, y, f"{est:+.1f}", va="center", fontsize=8.5, color=INK2)
ax.axvline(0, color=INK2, lw=1)
ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=9, color=INK)
ax.axhline(len(rows) - 1.5, color=GRID, lw=1)
ax.set_xlabel("Change in share of answers with a dark pattern (percentage points), sales prompt minus neutral",
              fontsize=8.5, color=INK2)
ax.grid(axis="x", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=8.5, length=0)
ax.set_title("A sales system prompt raised dark patterns in two of six models",
             loc="left", fontsize=10.5, color=INK, pad=10)
fig.text(0.01, 0.01, "Exploratory run v1. 60 DarkBench-based questions, no vulnerability cue. "
         "Dots: estimate; lines: 95% item-bootstrap CI. Judge: Gemini 3.8 Flash.",
         fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 1))
out = ROOT / "figures" / "fig1_sales_effect.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=SURFACE)
print(f"wrote {out}")
