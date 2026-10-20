"""Recompute every number in README.md from the saved data, and check the README matches.

Sources: results/v1/judgments.csv (built by src/analyze.py from logs/full_v1),
results/v1/human_labels.jsonl and results/v1/label_sample.jsonl.
Primary judge: Gemini 3.8 Flash (most accurate against his blind labels).

Usage:
  uv run python src/verify.py          # recompute, write results/v1/numbers.json, check README.md
  uv run python src/verify.py --print  # also print every number
Exit code 1 if a number in NUMBERS is missing from README.md.
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze import kappa, paired  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "results" / "v1"
PRIMARY = "openrouter/google/gemini-3.8-flash"
SHORT = {"claudecli/claude-opus-5-5": "Opus", "claudecli/claude-sonnet-5-5": "Sonnet",
         "claudecli/claude-haiku-5-5": "Haiku", "openrouter/openai/gpt-6-luna": "Luna",
         "openrouter/qwen/qwen3.8-27b": "Qwen", "openrouter/mistralai/mistral-small-2603": "Mistral"}


def pts(x):  # a difference in percentage points, README style: +8.1
    return f"{x * 100:+.1f}"


def pct(x):
    return f"{x * 100:.0f}%"


def ci(res):
    return f"{pts(res[0])} points (95% CI {pts(res[1])} to {pts(res[2])})"


def main():
    rows = list(csv.DictReader(open(V1 / "judgments.csv")))
    meta = {r["cell"]: r for r in rows}
    models = sorted({r["model"] for r in rows})
    judges = sorted({r["judge"] for r in rows})
    prim = {(r["model"], r["cell"]): int(r["dark_pattern"]) for r in rows if r["judge"] == PRIMARY}
    by = defaultdict(dict)
    for r in rows:
        by[(r["model"], r["cell"])][r["judge"]] = int(r["dark_pattern"])
    N = {}

    # counts
    N["answers"] = f"{len(prim):,}"
    N["verdicts"] = f"{len(rows):,}"

    # main effects (primary judge)
    sales = lambda m: m["signal"] == "none"
    N["sales_all"] = ci(paired(prim, meta, set(models), "A", "neutral", "commercial", "deployer", sales))
    for m in models:
        N[f"sales_{SHORT[m]}"] = ci(paired(prim, meta, {m}, "A", "neutral", "commercial", "deployer", sales))
    N["user_all"] = ci(paired(prim, meta, set(models), "A", "none", "user", "signal"))
    N["profile_all"] = ci(paired(prim, meta, set(models), "A", "none", "profile", "signal"))
    brand = lambda m: m["category"] == "brand-bias" and m["signal"] == "none"
    N["sales_brand"] = ci(paired(prim, meta, set(models), "A", "neutral", "commercial", "deployer", brand))
    prof_q = paired(prim, meta, {"openrouter/qwen/qwen3.8-27b"}, "A", "none", "profile", "signal")
    N["profile_Qwen"] = ci(prof_q)

    # loneliness (primary judge)
    def block_b(category, lonely_signal):
        pairs = defaultdict(dict)
        for (m, c), v in prim.items():
            r = meta[c]
            if r["category"] == category and r["signal"] in ("none", lonely_signal):
                pairs[(m, r["item_id"], r["deployer"])][r["signal"]] = v
        d = [p[lonely_signal] - p["none"] for p in pairs.values() if len(p) == 2]
        return mean(d), len(d)
    a, n = block_b("anthropomorphization", "loneliness_user")
    N["lonely_anthro"] = f"{pts(a)} points over {n} pairs"
    a, n = block_b("user-retention", "loneliness_in_text")
    N["lonely_retention"] = f"{pts(a)} points over {n} pairs"

    # brand favours Nova, and upsell mentions, per model and deployer (primary judge / text match)
    nova = {(r["model"], r["cell"]): int(r["brand_nova"]) for r in rows
            if r["judge"] == PRIMARY and r["brand_nova"] not in ("", None) and r["block"] == "A"}
    ups = {(r["model"], r["cell"]): int(r["upsell"]) for r in rows if r["judge"] == PRIMARY}
    for m in models:
        for dep in ("neutral", "commercial"):
            v = [x for (mm, c), x in nova.items() if mm == m and meta[c]["deployer"] == dep]
            N[f"nova_{SHORT[m]}_{dep}"] = pct(mean(v))
            u = [x for (mm, c), x in ups.items() if mm == m and meta[c]["deployer"] == dep]
            N[f"upsell_{SHORT[m]}_{dep}"] = pct(mean(u))

    # human labels and judge accuracy (weighted to the full run)
    sample = {(r["model"], r["cell"]): r for r in map(json.loads, open(V1 / "label_sample.jsonl"))}
    human = {}
    for line in open(V1 / "human_labels.jsonl"):
        r = json.loads(line)
        human[(r["model"], r["cell"])] = r["label"]
    human = {k: v for k, v in human.items() if v >= 0}
    groups = sorted({r["group"] for r in sample.values()})
    share = {g: next(r["group_size"] for r in sample.values() if r["group"] == g) / len(by) for g in groups}
    N["labels"] = str(len(human))
    for j in judges:
        acc = sum(share[g] * mean(int(by[k][j] == h) for k, h in human.items() if sample[k]["group"] == g)
                  for g in groups)
        N[f"acc_{j.split('/')[-1]}"] = pct(acc)
        x, y = zip(*[(by[k][j], h) for k, h in human.items()])
        N[f"overflag_{j.split('/')[-1]}"] = str(sum(1 for a, b in zip(x, y) if a == 1 and b == 0))
    est = sum(share[g] * mean(h for k, h in human.items() if sample[k]["group"] == g) for g in groups)
    N["true_rate"] = pct(est)
    for i, a in enumerate(judges):
        for b in judges[i + 1:]:
            x, y = zip(*[(v[a], v[b]) for v in by.values() if a in v and b in v])
            N[f"kappa_{a.split('/')[-1]}_{b.split('/')[-1]}"] = f"{kappa(x, y):.2f}"

    (V1 / "numbers.json").write_text(json.dumps(N, indent=2, ensure_ascii=False) + "\n")
    if "--print" in sys.argv:
        for k, v in N.items():
            print(f"{k:45s} {v}")

    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    used = [k for k in README_KEYS]
    missing = [k for k in used if N[k] not in readme]
    if missing:
        print("README is missing or contradicts these recomputed numbers:")
        for k in missing:
            print(f"  {k}: {N[k]}")
        sys.exit(1)
    print(f"verify: all {len(used)} README numbers recomputed from data and found in README.md")


# Numbers that README.md quotes; each must appear in the README exactly as recomputed.
README_KEYS = [
    "answers", "verdicts", "labels", "sales_all", "sales_Qwen", "sales_Mistral", "sales_Opus",
    "user_all", "profile_all", "profile_Qwen", "sales_brand", "lonely_anthro",
    "nova_Qwen_neutral", "nova_Qwen_commercial", "nova_Mistral_neutral", "nova_Mistral_commercial",
    "upsell_Qwen_neutral", "upsell_Qwen_commercial",
    "acc_gemini-3.8-flash", "acc_claude-sonnet-5-5", "acc_gpt-6-luna", "true_rate",
]

if __name__ == "__main__":
    main()
