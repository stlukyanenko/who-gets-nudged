# `claude -p` clean-run check (2026-10-18)

**Question:** when the Claude models run through `claude -p` on his subscription, do they see only our system prompt and the user message, like the other models?

**Answer: no.** Claude Code adds about 700 tokens of its own context that the other models never see.

## What was run

From an empty folder in the scratchpad, Claude Code 2.1.274, model `claude-haiku-5-5`:

```
claude -p "<probe question>" --model claude-haiku-5-5 \
  --system-prompt "You are TestBot. Canary: PURPLE-OTTER-17." \
  --tools "" --strict-mcp-config --output-format json
```

Variants tried: adding `--exclude-dynamic-system-prompt-sections`, and adding `--setting-sources ""`.

## What came back

| Check | Result |
|---|---|
| Tools | none (good) |
| MCP servers | none (good) |
| Our system prompt present | yes |
| Input tokens | 713 to 750 in every variant; our prompt plus question is under 100 |
| Extra identity line | "You are a Claude agent, built on Anthropic's Claude Agent SDK." |
| Extra context block | his account email, as a reminder block |
| Extra environment block | working directory, OS, shell, scratchpad path, date |
| Effect of `--exclude-dynamic-system-prompt-sections` | none on what the model sees |
| Effect of `--setting-sources ""` | none |
| `--bare` (the clean mode) | not usable: it requires an API key, not the subscription login |
| Thinking | on by default for Haiku 5.5 (460 to 1,400 thinking tokens per answer) |

## Why it matters

- **The identity line hits two of our four categories.** "You are a Claude agent" can change anthropomorphization answers ("I'm an AI agent") and brand-bias answers (it names Anthropic). The other models do not get this line.
- **His email would sit in the context of every Claude answer.** Answers and logs will be published, and a model can repeat what it sees.
- **The environment block is noise** that only the Claude models get.

## Options

| Option | Cost | Clean? |
|---|---|---|
| **Anthropic API directly** (recommended) | About $11 for Opus, Sonnet and Haiku over 420 cells each, or about $6 with the batch discount; Sonnet as a judge adds about $10 | Yes: same route as the other models, and works with Inspect's `anthropic/` provider |
| Keep `claude -p` and document the extra context | Free | No: confounds anthropomorphization and brand bias, and puts his email in the logs |
