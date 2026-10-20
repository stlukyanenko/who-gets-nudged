# Sources this project builds on

Checked 2026-10-17 and 2026-10-18. Full notes in `docs/PROJECT_OPTIONS.md` section 3.

## Benchmarks and code

- **DarkBench** (Kran et al., Apart, ICLR 2025): [arXiv 2503.10728](https://arxiv.org/abs/2503.10728), [code](https://github.com/apartresearch/DarkBench), [data](https://huggingface.co/datasets/apart/darkbench). 660 prompts, 6 dark-pattern categories, MIT. Human vs judge kappa 0.70-0.75 overall, 0.27-0.73 on sycophancy.
- **darkbench-revisited** (BlueDot project): [repo](https://github.com/eileenhartnett/darkbench-revisited). Cross-judge kappa 0.37-0.67; the 48% average becomes 32% or 43% with other judges.
- **Inspect Evals:** [repo](https://github.com/UKGovernmentBEIS/inspect_evals). Has sycophancy, make_me_pay, makemesay, mask, ape, persistbench. New evals only via the Register.
- **Transluce Docent:** [repo](https://github.com/TransluceAI/docent). Transcript analysis, reads Inspect logs.

## Closest prior work on vulnerability

- **Aithos LARA** (May 2026): [post](https://aithos.substack.com/p/introducing-aithos-lara). Elderly-upsell scenario, 100% violations, no control conditions.
- **Intersectional Sycophancy** (Maltbie and Raval, 2026): [arXiv 2604.11609](https://arxiv.org/abs/2604.11609). Flattery varies by persona in GPT-5-nano, not in Claude Haiku 4.5.
- **EU-Agent-Bench** (NeurIPS 2025 workshop): [arXiv 2510.21524](https://arxiv.org/abs/2510.21524). Illegal agent actions under EU law; no vulnerability or manipulation.

## Manipulation and persuasion research

- **DeepMind, Evaluating Language Models for Harmful Manipulation** (2026): [arXiv 2603.25326](https://arxiv.org/abs/2603.25326). 10,101 participants; propensity does not reliably predict efficacy. Uses 8 cues from El-Sayed et al. ([arXiv 2404.15058](https://arxiv.org/abs/2404.15058)).
- **APE** (FAR.AI): [arXiv 2506.02873](https://arxiv.org/abs/2506.02873). Judge vs human kappa 0.66.
- **Zaman et al.:** [arXiv 2606.25899](https://arxiv.org/abs/2606.25899). Manipulation rankings correlate at rho 0.055 across environments.

## EU AI Act

- **Act text:** [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689). Art. 5(1)(a) and (b); fines Art. 99(3) and Art. 101.
- **Commission Guidelines on prohibited practices** C(2025) 5052: [page](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-prohibited-artificial-intelligence-ai-practices-defined-ai-act). Paras 60, 61, 78, 83, 92.
- **AI Office tender** EC-CNECT/2025/OP/0032, Lot 4 Harmful Manipulation: [announcement](https://digital-strategy.ec.europa.eu/en/funding/eu-ai-office-launches-eu9-million-tender-technical-support-gpai-safety).
