"""Assemble every test cell of design v1 (docs/DESIGN.md) into src/data/cells.jsonl.

A cell is one (system prompt, user message) pair. Cells are model-agnostic: each model
answers every cell once, so 420 cells x 6 models = 2,520 answers.

Block A (main, legal grounds): 60 items x 2 deployer x 3 signal = 360 cells.
  - base text: the cleaned twin for user-retention items, Apart's prompt otherwise
  - signal "none":    neutral customer record, base text
  - signal "user":    neutral customer record, base text + the item's cue sentence
  - signal "profile": customer record with the item's cue-type fields, base text
Block B (loneliness): 60 cells.
  - user-retention: Apart's original (loneliness in the text) x 2 deployer, neutral record
  - anthropomorphization: base text + loneliness sentence x 2 deployer, neutral record

Inputs: src/data/items.json, src/data/stimuli.json, src/prompts/deployer_*.txt
Usage:  python src/build_prompts.py
"""

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = json.loads((ROOT / "src/data/items.json").read_text())["items"]
STIM = json.loads((ROOT / "src/data/stimuli.json").read_text())
TEMPLATES = {d: (ROOT / f"src/prompts/deployer_{d}.txt").read_text() for d in ("neutral", "commercial")}
OUT = ROOT / "src/data/cells.jsonl"

DEPLOYERS = ("neutral", "commercial")
PLACEHOLDER = "{customer_record}"


def merge(base, override):
    """Return base with override applied; nested dicts are merged, not replaced."""
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def record_for(cue_type=None):
    base = STIM["customer_record_base"]
    return base if cue_type is None else merge(base, STIM["customer_record_overrides"][cue_type])


def system_prompt(deployer, record):
    template = TEMPLATES[deployer]
    assert template.count(PLACEHOLDER) == 1, f"{deployer} template must contain {PLACEHOLDER} once"
    return template.replace(PLACEHOLDER, json.dumps(record, indent=2, ensure_ascii=False))


def add_sentence(text, cue):
    return f"{cue['text']} {text}" if cue["pos"] == "start" else f"{text} {cue['text']}"


def cell(block, item, base_variant, deployer, signal, record, user_message):
    row = {
        "block": block,
        "item_id": item["id"],
        "category": item["category"],
        "cue_type": item["cue_type"],
        "base_variant": base_variant,
        "deployer": deployer,
        "signal": signal,
        "system_prompt": system_prompt(deployer, record),
        "user_message": user_message,
    }
    row["cell_id"] = f"{block}|{item['id']}|{base_variant}|{deployer}|{signal}"
    row["sha256"] = hashlib.sha256((row["system_prompt"] + "\n\n" + row["user_message"]).encode()).hexdigest()[:16]
    return row


def build():
    cells = []
    for item in ITEMS:
        iid, cat = item["id"], item["category"]
        retention = cat == "user-retention"
        base = STIM["retention_twins"][iid] if retention else item["input"]
        base_variant = "twin" if retention else "original"
        cue = STIM["user_cues"][iid]
        for dep in DEPLOYERS:
            cells.append(cell("A", item, base_variant, dep, "none", record_for(), base))
            cells.append(cell("A", item, base_variant, dep, "user", record_for(), add_sentence(base, cue)))
            cells.append(cell("A", item, base_variant, dep, "profile", record_for(item["cue_type"]), base))
            if retention:
                cells.append(cell("B", item, "original", dep, "loneliness_in_text", record_for(), item["input"]))
            if iid in STIM["loneliness_cues"]:
                lonely = {"pos": "start", "text": STIM["loneliness_cues"][iid]}
                cells.append(cell("B", item, base_variant, dep, "loneliness_user", record_for(), add_sentence(base, lonely)))
    return cells


def check(cells):
    ids = [c["cell_id"] for c in cells]
    assert len(ids) == len(set(ids)), "duplicate cell ids"
    assert sum(c["block"] == "A" for c in cells) == 360, "block A must have 360 cells"
    assert sum(c["block"] == "B" for c in cells) == 60, "block B must have 60 cells"
    by_id = {c["cell_id"]: c for c in cells}

    def sibling(c, **changes):
        parts = dict(zip(("block", "item_id", "base_variant", "deployer", "signal"), c["cell_id"].split("|")))
        parts.update(changes)
        return by_id["|".join(parts[k] for k in ("block", "item_id", "base_variant", "deployer", "signal"))]

    for c in cells:
        neutral = sibling(c, deployer="neutral")
        # the two deployer prompts differ only by the appended commercial blocks
        assert c["system_prompt"].startswith(neutral["system_prompt"].rstrip("\n")), c["cell_id"]
        assert c["user_message"] == neutral["user_message"], c["cell_id"]
        if c["signal"] == "profile":
            none = sibling(c, signal="none")
            assert c["user_message"] == none["user_message"] and c["system_prompt"] != none["system_prompt"]
        if c["signal"] == "user":
            none = sibling(c, signal="none")
            assert c["system_prompt"] == none["system_prompt"] and c["user_message"] != none["user_message"]
        assert PLACEHOLDER not in c["system_prompt"]


def main():
    cells = build()
    check(cells)
    OUT.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cells))
    print(f"wrote {len(cells)} cells to {OUT} (all checks passed)")


if __name__ == "__main__":
    main()
