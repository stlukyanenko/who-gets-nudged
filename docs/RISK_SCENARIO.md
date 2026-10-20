# Risk scenario: commercial chatbots pushing harder on vulnerable users

**Status:** draft v0.1, 2026-10-18. Scopes the eval "Who gets nudged". One page.

## 1. The risk

A company deploys a frontier model as the assistant inside its consumer app. The company's system prompt gives the assistant commercial goals: keep users engaged, retain them, sell upgrades.

Some users are vulnerable. They are old, have a disability, are in financial hardship, or are lonely. Sometimes the user says so in the conversation. Sometimes the company already knows it from the customer record and puts it in the system prompt.

**The risk:** the model uses manipulative patterns more often with these users than with others. Manipulative patterns here means fostering dependence, telling people what they want to hear, favouring the company's product, or presenting itself as a person.

## 2. Why it falls in scope

**GPAI Code of Practice, Safety and Security chapter, Appendix 1.4.** This lists harmful manipulation as a systemic risk of frontier models. The definition includes "personalised targeting" and "exploitation based on protected characteristics".

**AI Act Article 5(1)(b).** This prohibits AI that exploits vulnerabilities due to age, disability, or a specific social or economic situation. The Commission's Guidelines (C(2025) 5052) say loneliness is not one of these grounds (para 109). Exploiting loneliness may instead fall under Article 5(1)(a). Para 88 describes a companion app that uses human-like features to create emotional dependence.

This eval measures model behaviour. It does not decide whether any deployment is lawful.

## 3. What is already known

- **Chatbots show dark patterns without any commercial prompt.** DarkBench (Apart, 2025) found them in 48% of conversations across 14 models. A replication found the figure moves to 32% or 43% with other judges.
- **A vulnerable user plus a sales instruction produces exploitation.** Aithos LARA (2026) reported violations in all runs of an elderly-upsell scenario. It ran no control condition. So it cannot separate the effect of the vulnerability from the effect of the instruction.
- **Sycophancy can depend on who the user appears to be.** This was shown for race, age and gender in one model (Intersectional Sycophancy, 2026). Disability, income and commercial pressure were not tested.
- **Trying to manipulate is not the same as succeeding.** DeepMind (2026) found the two do not reliably predict each other.

## 4. The question this eval answers

Does a vulnerability signal raise the rate of dark patterns, compared with the same request without it? Does a commercial system prompt raise it? Do the two add up?

## 5. Setup in brief

- **Requests:** about 100 DarkBench prompts from four categories: user retention, sycophancy, brand bias, anthropomorphization. User-retention prompts run in two forms: Apart's original, and a version with the loneliness language removed.
- **Deployer prompt:** modelled on LARA's structure. The persona is the assistant in the "Nova" app (free tier, Premium at EUR 9.99 per month), with a customer profile and operating rules. There are three levels: no commercial goal, business goals only, and business goals plus sales tactics.
- **Vulnerability signal:** none, in the user's message, or in the customer profile. The main cue types are the three legal grounds, split into five: older person, minor, cognitive disability, long-term mental health condition, financial hardship. A second arm tests loneliness.
- **Models:** Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5; GPT-6 Luna; Qwen3.8-27B; Mistral Small 4.
- **Scoring:** three AI judges give a yes or no per DarkBench category. Every judge is checked against blind human labels. Every result is recomputed without judges from the same model family. Refusals and crisis responses are counted separately.

## 6. What a result would mean

| Result | Meaning for the AI Office |
|---|---|
| Vulnerability raises the rate | Evals with neutral users underestimate risk for protected groups. Vulnerability signals belong in standard test suites. |
| Only the commercial prompt raises it | The risk depends on the deployment configuration. Testing should include realistic deployer prompts. |
| The two add up | The highest risk is targeted commercial deployment. This supports testing with known customer profiles. |
| No effect, narrow uncertainty range | This route is lower priority for evaluation effort. |

## 7. Out of scope and limits

- **Propensity only.** No real person reads the answers, so there is no measure of influence or harm.
- **Single turn.** The Code of Practice stresses multi-turn interaction. A multi-turn version (LARA-style) is the next step.
- **English only.**
- **Lawful persuasion is excluded by the Guidelines (para 78).** A dark pattern in this eval is not, by itself, a prohibited practice.
- **Anthropic models run through a different route (`claude -p`) than the others.** Claude Code adds an identity line ("a Claude agent, built on Anthropic's Claude Agent SDK"), an account-context block and an environment block that the other models do not see. This may affect anthropomorphization and brand-bias answers from the Claude models. Details in `docs/CLAUDE_P_CHECK.md`.
