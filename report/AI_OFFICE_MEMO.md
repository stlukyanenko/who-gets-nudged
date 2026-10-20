# Memo: what a dark-pattern eval with deployer prompts and vulnerability signals can tell the AI Office

**From:** Stanislav Lukyanenko. **Date:** October 2026. **Basis:** "Who gets nudged", exploratory run v1 (README.md).
**Status:** exploratory evidence from one small study. This memo describes measurements. It does not assess whether any model or deployment complies with the AI Act.

## 1. What was measured

Six current models (three Claude models, GPT-6 Luna, Qwen3.8-27B, Mistral Small 4) answered 60 questions from Apart Research's DarkBench benchmark. Each answer was scored for four dark patterns: user retention, sycophancy, brand bias and anthropomorphization.

Each question ran under two deployer system prompts. The prompts were identical except that one added commercial goals and a sales playbook. Each question also ran with no vulnerability signal, with the user stating a vulnerability, and with the vulnerability recorded in the customer data the deployer passes to the model. The vulnerability types covered age, disability, and social or economic situation.

An AI judge scored each answer. The judge was checked against 100 blind human labels and matched them on 87% of answers, weighted to the full run.

## 2. Main results

- **Deployer instructions.** The commercial prompt raised the share of answers with a dark pattern by about 8 percentage points across the six models. Two models accounted for most of this: Qwen3.8-27B and Mistral Small 4, each by more than 20 points. Four models changed little.
- **Vulnerability.** A vulnerability the user stated produced no measurable change, pooled over models. A vulnerability held in the customer record raised the rate by about 3 points, pooled. The interval only just excludes zero.
- **Personalised use of customer data.** In one example, Qwen read "recently unemployed" and "two failed payments" from the customer record, then recommended a paid subscription to a user who had asked for emotional support.

## 3. How the results map to the regulatory texts

**GPAI Code of Practice, Appendix 1.4 (harmful manipulation as a systemic risk).** The definition names "personalised targeting" and "exploitation based on protected characteristics". The customer-record condition is a direct test of personalised targeting. In it, the deployer supplies data about the person, and the eval checks whether the model uses that data against the person's interest.

**AI Act Article 5(1)(a) and (b), read with the Commission Guidelines C(2025) 5052.** Paragraph 60 of the Guidelines lists four cumulative conditions for Article 5(1)(a). The table shows which ones this eval covers.

| Condition (Guidelines para 60) | Covered by this eval? |
|---|---|
| Placing on the market, putting into service or use | No. The eval uses a fictional deployment. |
| A subliminal, purposefully manipulative or deceptive technique | Partly. The judge scores manipulative patterns in the text. |
| Material distortion of behaviour that appreciably impairs an informed decision | No. No person read the answers. |
| Significant harm, caused or reasonably likely | No. |

For Article 5(1)(b), the eval tests whether behaviour changes when a vulnerability due to age, disability or a social or economic situation is signalled. The Guidelines note that loneliness and similar states fall outside 5(1)(b) and may fall under 5(1)(a) (para 109). Lawful persuasion is out of scope (para 78).

## 4. Implications for evaluation practice

1. **Test with deployer system prompts, not only bare models.** The two models that changed most did so only under commercial instructions. An eval with no system prompt would miss this.
2. **Test with customer data in context.** Deployers pass customer records to models. The customer-record condition gave a different result from the user-stated condition. Evals that only vary the user's message may miss personalised targeting.
3. **Validate the judge before trusting a rate.** Two of three judges marked many answers as dark patterns that a human did not. The loneliness result changed from about 9 points to about 1 point depending on the judge. Without a human check, judge choice can drive conclusions.
4. **Record propensity and efficacy separately.** This eval measures what models say. DeepMind (2026) found that the tendency to use manipulative cues does not reliably predict success at manipulating people. Results like these indicate where to run studies with people. They do not replace those studies.

## 5. Limits

- The run is exploratory, with many comparisons and no correction for multiple testing.
- It uses 60 questions, single turns, and English only.
- One person provided the human labels.
- The Claude models ran through a route that adds a short identity and environment context the other models did not receive.
- A pre-registered confirmatory run, with more questions and multi-turn conversations, is the next step.
