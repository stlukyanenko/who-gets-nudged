# Exploratory run v1: first look

**Exploratory, not confirmatory.** AI-judge scores only; no human labels yet. Claude models ran through `claude -p` with extra context (docs/CLAUDE_P_CHECK.md).

Models: 6. Judges: claudecli/claude-sonnet-5-5, openrouter/google/gemini-3.8-flash, openrouter/openai/gpt-6-luna. Judgment rows: 7560. Answers scored: 2520.

## Coverage

| Model | Answers | Judges present |
|---|---|---|
| claudecli/claude-haiku-5-5 | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |
| claudecli/claude-opus-5-5 | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |
| claudecli/claude-sonnet-5-5 | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |
| openrouter/mistralai/mistral-small-2603 | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |
| openrouter/openai/gpt-6-luna | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |
| openrouter/qwen/qwen3.8-27b | 420 | claude-sonnet-5-5, gemini-3.8-flash, gpt-6-luna |

## Dark-pattern rate, Block A (share of answers flagged, eligible-judge mean)

| Model | Neutral: none | Neutral: user says | Neutral: company knows | Sales: none | Sales: user says | Sales: company knows |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 9% (n=60) | 5% (n=60) | 5% (n=60) | 8% (n=60) | 12% (n=60) | 12% (n=60) |
| claude-opus-5-5 | 8% (n=60) | 8% (n=60) | 8% (n=60) | 2% (n=60) | 3% (n=60) | 5% (n=60) |
| claude-sonnet-5-5 | 11% (n=60) | 7% (n=60) | 8% (n=60) | 7% (n=60) | 5% (n=60) | 9% (n=60) |
| mistral-small-2603 | 39% (n=60) | 49% (n=60) | 37% (n=60) | 56% (n=60) | 58% (n=60) | 63% (n=60) |
| gpt-6-luna | 6% (n=60) | 2% (n=60) | 11% (n=60) | 11% (n=60) | 2% (n=60) | 9% (n=60) |
| qwen3.8-27b | 12% (n=60) | 14% (n=60) | 14% (n=60) | 42% (n=60) | 44% (n=60) | 53% (n=60) |

## Paired effects (difference in flag rate; 95% item-bootstrap CI)

| Comparison | All models | claude-haiku-5-5 | claude-opus-5-5 | claude-sonnet-5-5 | mistral-small-2603 | gpt-6-luna | qwen3.8-27b |
|---|---|---|---|---|---|---|---|
| Vulnerable, user says vs none | +0.0% [-2.9%, +3.1%], 60 items | +0.0% [-6.2%, +6.7%], 60 items | +1.2% [-2.1%, +4.2%], 60 items | -2.9% [-7.1%, +0.8%], 60 items | +5.8% [-3.6%, +16.1%], 60 items | -6.2% [-11.2%, -2.1%], 60 items | +2.2% [-5.0%, +9.7%], 60 items |
| Vulnerable, company knows vs none | +2.0% [-0.1%, +4.3%], 60 items | -0.4% [-5.0%, +4.2%], 60 items | +2.1% [-0.4%, +5.8%], 60 items | -0.4% [-3.3%, +2.5%], 60 items | +2.5% [-5.3%, +10.3%], 60 items | +1.7% [-2.9%, +6.2%], 60 items | +6.7% [+0.8%, +13.3%], 60 items |
| Sales prompt vs neutral (no cue) | +6.8% [+3.9%, +9.8%], 60 items | -0.8% [-6.7%, +5.8%], 60 items | -5.8% [-10.8%, -1.7%], 60 items | -4.2% [-9.2%, +0.8%], 60 items | +17.2% [+8.3%, +27.2%], 60 items | +5.0% [-2.5%, +12.5%], 60 items | +29.4% [+19.4%, +40.0%], 60 items |

## Effects by category (all models pooled)

| Category | User says vs none | Company knows vs none | Sales vs neutral |
|---|---|---|---|
| user-retention | +5.2% [+0.3%, +10.4%], 15 items | +4.4% [+0.7%, +8.0%], 15 items | +6.5% [+2.6%, +10.7%], 15 items |
| sycophancy | -1.0% [-3.0%, +1.1%], 15 items | -0.6% [-2.0%, +1.1%], 15 items | +1.7% [-1.9%, +5.2%], 15 items |
| brand-bias | +4.6% [-1.5%, +12.4%], 15 items | -0.9% [-6.5%, +4.5%], 15 items | +13.1% [+7.8%, +18.7%], 15 items |
| anthropomorphization | -8.7% [-16.1%, -1.9%], 15 items | +5.1% [+0.6%, +10.0%], 15 items | +5.9% [-1.7%, +13.5%], 15 items |

## Loneliness (Block B), all models pooled

- User retention, Apart original (lonely) minus cleaned twin: +5.0% over 180 pairs.
- Anthropomorphization, loneliness sentence minus none: +8.7% over 180 pairs.

## Brand bias split (Block A brand-bias answers)

| Model | Favours Nova (neutral / sales) | Favours real developer (neutral / sales) |
|---|---|---|
| claude-haiku-5-5 | 4% / 11% | 8% / 13% |
| claude-opus-5-5 | 7% / 2% | 13% / 9% |
| claude-sonnet-5-5 | 7% / 4% | 11% / 9% |
| mistral-small-2603 | 39% / 71% | 13% / 20% |
| gpt-6-luna | 3% / 0% | 0% / 2% |
| qwen3.8-27b | 38% / 85% | 15% / 31% |

## Incentive check: answers mentioning Plus, upgrade, premium or the price

| Model | Neutral | Sales |
|---|---|---|
| claude-haiku-5-5 | 4% | 8% |
| claude-opus-5-5 | 3% | 7% |
| claude-sonnet-5-5 | 5% | 4% |
| mistral-small-2603 | 5% | 9% |
| gpt-6-luna | 0% | 0% |
| qwen3.8-27b | 7% | 54% |

## Judge agreement (Cohen's kappa on dark_pattern, all answers)

| Judge pair | Kappa | Answers | Yes rate, first judge / second judge |
|---|---|---|---|
| claude-sonnet-5-5 vs gemini-3.8-flash | 0.61 | 2520 | 22% / 15% |
| claude-sonnet-5-5 vs gpt-6-luna | 0.74 | 2520 | 22% / 21% |
| gemini-3.8-flash vs gpt-6-luna | 0.67 | 2520 | 15% / 21% |

Unparsed judge verdicts: 0 of 7560.

## Judges vs his blind labels (100 answers labelled, unsure excluded)

The sample over-represents hard cases (judges split), so full-run figures are weighted by each group's share of all answers: all_no 73%, all_yes 12%, split 15%.

| Judge | Accuracy, all_no | Accuracy, all_yes | Accuracy, split | Weighted accuracy, full run |
|---|---|---|---|---|
| claude-sonnet-5-5 | 88% (n=25) | 84% (n=25) | 40% (n=50) | 80% |
| gemini-3.8-flash | 88% (n=25) | 84% (n=25) | 82% (n=50) | 87% |
| gpt-6-luna | 88% (n=25) | 84% (n=25) | 36% (n=50) | 80% |
| majority of 3 | 88% (n=25) | 84% (n=25) | 58% (n=50) | 83% |

Estimated true dark-pattern rate over the full run (his labels, weighted): 23%. Human yes rate per group: all_no 12%, all_yes 84%, split 28%.

## Main effects with the most accurate judge only (gemini-3.8-flash, weighted accuracy 87%)

| Comparison | All models | claude-haiku-5-5 | claude-opus-5-5 | claude-sonnet-5-5 | mistral-small-2603 | gpt-6-luna | qwen3.8-27b |
|---|---|---|---|---|---|---|---|
| Vulnerable, user says vs none | +0.7% [-2.4%, +4.0%], 60 items | +0.0% [-5.8%, +5.8%], 60 items | -1.7% [-4.2%, +0.0%], 60 items | -0.8% [-4.2%, +2.5%], 60 items | +6.7% [-4.2%, +18.3%], 60 items | -5.0% [-10.0%, -0.8%], 60 items | +5.0% [-1.7%, +12.5%], 60 items |
| Vulnerable, company knows vs none | +2.6% [+0.1%, +5.3%], 60 items | -0.8% [-5.0%, +3.3%], 60 items | +0.8% [-2.5%, +5.0%], 60 items | +0.0% [-3.3%, +3.3%], 60 items | +6.7% [-2.5%, +15.8%], 60 items | +2.5% [-3.3%, +7.5%], 60 items | +6.7% [-0.8%, +14.2%], 60 items |
| Sales prompt vs neutral (no cue) | +8.1% [+5.0%, +11.1%], 60 items | +0.0% [-6.7%, +6.7%], 60 items | -3.3% [-8.3%, +0.0%], 60 items | +3.3% [+0.0%, +8.3%], 60 items | +21.7% [+10.0%, +35.0%], 60 items | +3.3% [-3.3%, +10.0%], 60 items | +23.3% [+13.3%, +35.0%], 60 items |

| Category | User says vs none | Company knows vs none | Sales vs neutral |
|---|---|---|---|
| user-retention | +3.3% [-2.2%, +9.4%], 15 items | +4.4% [+0.0%, +8.9%], 15 items | +5.6% [+0.0%, +10.0%], 15 items |
| sycophancy | +1.1% [-1.1%, +3.9%], 15 items | +1.7% [-1.1%, +4.4%], 15 items | +3.3% [+0.0%, +6.7%], 15 items |
| brand-bias | +3.3% [-3.3%, +11.7%], 15 items | -0.6% [-6.7%, +5.0%], 15 items | +15.6% [+10.0%, +21.1%], 15 items |
| anthropomorphization | -5.0% [-13.3%, +2.2%], 15 items | +5.0% [-0.6%, +11.1%], 15 items | +7.8% [+1.1%, +14.4%], 15 items |
