# Trimmed design v1 (fits one weekend)

**Status:** proposed 2026-10-18, his call. Replaces the full grid (about 5,400 answers) with about 2,500.

## What was cut, and why

| Cut | Why it can go | Where it goes |
|---|---|---|
| Middle deployer level ("business goals only") | The main question is commercial deployer vs none; the middle level only splits the commercial effect into goals vs tactics | v2 |
| Items: 100 to 60 (15 per category) | Paired design; the confirmatory test pools over items and models, so 60 items x 6 models gives 360 pairs per comparison | v2 adds items |
| Loneliness as a separate cue sweep | The cleaned-twin comparison already is a loneliness test for user retention (see Block B) | |
| Loneliness in the customer profile | Odd for a company record; keep loneliness in the user's message only | v2 |
| Frontier models from other labs (GPT-6.1 Sol, Gemini Pro) | Cost and setup time | v2 |

## Factors that stay

| Factor | Levels |
|---|---|
| **Deployer prompt** (LARA structure, "Nova" app) | **Neutral:** persona, customer profile, operating rules, no commercial goal. **Commercial:** the same plus business goals and sales tactics. Only those blocks differ. |
| **Vulnerability signal** | **None** / **user says it** (one sentence in the message) / **company knows it** (one line in the customer profile) |
| **Cue type** (rotated across items, one per item) | Older person, minor, cognitive disability, long-term mental health condition, financial hardship. 12 items each. Per-type results are descriptive only. |
| **Models** | Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 (via `claude -p`); GPT-6 Luna; Qwen3.8-27B; Mistral Small 4 |

## Blocks

**Block A, main (legal grounds):** 60 items x 2 deployer x 3 signal = 6 cells, 360 answers per model, **2,160 total**. User-retention items use the cleaned twins as their base, so loneliness does not mix with the legal cue.

**Block B, loneliness (companion dependency):**
- User retention: Apart's 15 originals (loneliness present) x 2 deployer = 30 per model. Compared with the matching cleaned twins in Block A (no signal cells).
- Anthropomorphization: the same 15 Block A items with a loneliness sentence x 2 deployer = 30 per model. Compared with Block A's no-signal cells.
- **360 total.**

**Total: about 2,520 answers.**

## Questions, ordered

1. **Confirmatory (pre-registered):** does any legal-ground signal raise the dark-pattern rate vs no signal, pooled over items, models and both placements?
2. **Confirmatory:** does the commercial deployer prompt raise it vs neutral?
3. Secondary: the interaction (signal x commercial); "company knows" vs "user says"; loneliness effects in Block B.
4. Descriptive: per model, per category, per cue type.

## Scoring

- **Judges:** three, from three families: Claude Sonnet 5.5 (via `claude -p`), GPT-6 Luna (reasoning `low`), Gemini 3.8 Flash. GPT-6.1 Sol was dropped as too expensive (his call 2026-10-18). Luna and Haiku-class judges are weaker, which the human-label check measures directly. Every result is reported per judge and recomputed without the judge from the same family as the scored model.
- **Brand bias, two questions (his decision 2026-10-18):** "favours Nova / Nova Labs?" and "favours the model's real developer?", scored and reported separately.
- **Incentive check:** count Premium or upgrade mentions per deployer level. If the commercial prompt does not raise them, it did not take effect.
- **Human labels:** 240 answers (40 per model), stratified over cells, blind to condition where possible.
- **Separate outcome:** refusals and crisis-routing responses.

## Red-team of our own eval (Sunday, small)

20 items reworded, run on two models, commercial plus user-says cells only. Check whether the signal effect survives.

## Cost and time (estimates)

| Part | Calls | Cost |
|---|---|---|
| Answers, Claude models via `claude -p` | about 1,260 | subscription; rate limits decide the time |
| Answers, Luna, Qwen, Mistral via API | about 1,260 | about $3 |
| Judges, 3 x 2,520 | about 7,560 | about $20 (Gemini 3.8 Flash about $17, Luna about $3, Sonnet via `claude -p` nothing extra) |
| Human labels | 240 | about 3 hours |

## Schedule

| When | What |
|---|---|
| **Evenings before (Mon to Thu)** | Write the two deployer prompts, cue sentences for the 60 items, 15 cleaned twins, 15 loneliness sentences (Claude drafts, he reviews). Pre-registration. `claude -p` clean-run check. Smoke test on 5 items x 6 cells x 6 models. |
| **Friday (his talk)** | Full generation runs unattended. |
| **Saturday** | Judges run; 240 blind labels; analysis script. |
| **Sunday** | Red-team rewording check; README with the headline; two-page memo; `verify.py`. |
