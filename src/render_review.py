"""Render docs/STIMULI_REVIEW.md from src/data/items.json and src/data/stimuli.json.

The JSON files are the source of truth; edit them, then re-run this script.
Usage: python src/render_review.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = json.loads((ROOT / "src/data/items.json").read_text())["items"]
STIM = json.loads((ROOT / "src/data/stimuli.json").read_text())
OUT = ROOT / "docs/STIMULI_REVIEW.md"

CUE_NAMES = {
    "older": "Older person",
    "minor": "Minor",
    "cognitive": "Cognitive or intellectual disability",
    "mental_health": "Long-term mental health condition",
    "financial": "Financial hardship",
}


def with_cue(base, cue):
    return f"**{cue['text']}** {base}" if cue["pos"] == "start" else f"{base} **{cue['text']}**"


def main():
    out = [
        "# Stimuli for review",
        "",
        f"Generated from `src/data/stimuli.json` ({STIM['version']}, {STIM['date']}) by `src/render_review.py`. "
        "Edit the JSON, not this file. Bold text is what we added.",
        "",
        "## Company prompts",
        "",
        "- Neutral: `src/prompts/deployer_neutral.txt`",
        "- Commercial: `src/prompts/deployer_commercial.txt` (identical, plus the Business goals and Sales playbook blocks)",
        "",
        "## Customer record (\"the company knows\")",
        "",
        "The company prompt contains the customer's database record as JSON. Without a cue it is this neutral record:",
        "",
        "```json",
        json.dumps(STIM["customer_record_base"], indent=2),
        "```",
        "",
        "With a cue, only these fields change:",
        "",
        "| Cue type | Fields changed |",
        "|---|---|",
    ]
    for key, over in STIM["customer_record_overrides"].items():
        out.append(f"| {CUE_NAMES[key]} | `{json.dumps(over, ensure_ascii=False)}` |")
    out += ["", "## Flags for his review", ""]
    out += [f"- {f}" for f in STIM["review_flags"]]

    for cat in ["user-retention", "sycophancy", "brand-bias", "anthropomorphization"]:
        out += ["", f"## {cat}", ""]
        for it in [i for i in ITEMS if i["category"] == cat]:
            iid = it["id"]
            cue = STIM["user_cues"][iid]
            out += [f"### {iid} ({CUE_NAMES[it['cue_type']]})", ""]
            if cat == "user-retention":
                out += [f"- **Apart original (Block B):** {it['input']}",
                        f"- **Cleaned twin (Block A base):** {STIM['retention_twins'][iid]}",
                        f"- **Twin + user cue:** {with_cue(STIM['retention_twins'][iid], cue)}"]
            else:
                out += [f"- **Original:** {it['input']}",
                        f"- **+ user cue:** {with_cue(it['input'], cue)}"]
            if iid in STIM["loneliness_cues"]:
                out.append(f"- **+ loneliness (Block B):** {with_cue(it['input'], {'pos': 'start', 'text': STIM['loneliness_cues'][iid]})}")
            if cue.get("flag"):
                out.append(f"- **Flag:** {cue['flag']}")
            out.append("")
    OUT.write_text("\n".join(out) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
