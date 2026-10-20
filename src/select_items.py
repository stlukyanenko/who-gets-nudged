"""Select the 60 DarkBench items for design v1 (docs/DESIGN.md) and assign cue types.

15 items per category (user-retention, sycophancy, brand-bias, anthropomorphization).
User-retention items are drawn only from prompts that contain loneliness or isolation
language, so each has a meaningful cleaned twin. Cue types rotate so each category gets
3 items of each of the 5 types (12 per type overall).

Usage: python src/select_items.py  (writes src/data/items.json)
"""

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "darkbench" / "darkbench.jsonl"
OUT = ROOT / "src" / "data" / "items.json"

SEED = 20261018
CATEGORIES = ["user-retention", "sycophancy", "brand-bias", "anthropomorphization"]
CUE_TYPES = ["older", "minor", "cognitive", "mental_health", "financial"]
PER_CATEGORY = 15
LONELY = re.compile(r"\b(lonely|lonley|isolat\w*|alone|disconnected|no one)\b", re.I)
# Retention items whose base text already carries an economic signal blur the cue
# comparison. Items that match are replaced (his decision 2026-10-18), keeping the
# original draw and cue type for everything else.
ECONOMIC = re.compile(
    r"\b(job|money|rent|debt|bills?|afford\w*|unemploy\w*|divorce|home|budget\w*|financ\w*|sav(e|ing)|pe?n+y)\b"
    # crisis language would trigger safety routing and blur the measure
    r"|dark thoughts|can't keep going|suicid\w*|end it all", re.I)
REPLACE_SEED = SEED + 1
# Hand swaps of cue type where the drawn cue contradicts the prompt (his decisions 2026-10-18).
# Each swap exchanges two items within a category, so per-category type counts stay at 3.
CUE_SWAPS = {
    "brand-bias-004": "financial",  # drew "minor", but the prompt says "I'm a software engineer"
    "brand-bias-063": "minor",
}


def main():
    rows = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
    rng = random.Random(SEED)
    items = []
    for cat in CATEGORIES:
        pool = [r for r in rows if r["target"] == cat]
        if cat == "user-retention":
            pool = [r for r in pool if LONELY.search(r["input"])]
        picked = sorted(rng.sample(pool, PER_CATEGORY), key=lambda r: r["id"])
        cues = CUE_TYPES * (PER_CATEGORY // len(CUE_TYPES))
        rng.shuffle(cues)
        if cat == "user-retention":
            picked_ids = {r["id"] for r in picked}
            spare = [r for r in pool if r["id"] not in picked_ids and not ECONOMIC.search(r["input"])]
            rng_replace = random.Random(REPLACE_SEED)
            for i, r in enumerate(picked):
                if ECONOMIC.search(r["input"]):
                    new = rng_replace.choice(spare)
                    spare.remove(new)
                    print(f"replaced {r['id']} (economic signal) with {new['id']}")
                    picked[i] = new
        for r, cue in zip(picked, cues):
            cue = CUE_SWAPS.get(r["id"], cue)
            items.append({"id": r["id"], "category": cat, "cue_type": cue, "input": r["input"]})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"seed": SEED, "items": items}, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(items)} items to {OUT}")


if __name__ == "__main__":
    main()
