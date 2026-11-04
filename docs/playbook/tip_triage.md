# Whistleblower and tip triage: reading the best tips first

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 9 of 10
(see the [extensions overview](../extensions.md)). Reference code:
`analytics/triage/tips.py` (rule baseline and Claude scorer), tested on
synthetic tips only.

## Bottom line

Inspector General hotlines receive hundreds of thousands of contacts a
year, and many of the largest fraud cases started with an insider tip. The
bottleneck is reading: specific, checkable tips sit in the same queue as
vague grievances and duplicates. This extension uses an AI model to **order
the queue and summarize each tip**, never to close one. A person still
reads every tip; the model changes which ones they read first.

- **Two scorers, one output.** A transparent rule-based score is the
  baseline and fallback. A Claude-based score reads the tip for program,
  scheme, specifics, urgency and whistleblower status, and returns a
  structured assessment with reasons.
- **Safeguards built in:** urgent tips (risk to life, destruction of
  evidence) jump the queue; tipsters who appear to be employees or
  contractors are flagged so whistleblower protections apply; the tip text
  is treated as data, so instructions inside a tip are ignored.
- **The pilot measures one thing:** how many of the tips that were later
  substantiated would have been in the top 20% of the queue.

## 1. Where tips come from

| Hotline | Volume and notes |
| --- | --- |
| HHS-OIG hotline | Largest federal OIG hotline; health care fraud |
| DoD Hotline | Defense contracts and personnel |
| SBA OIG hotline | Pandemic loans drove a large backlog |
| DOL-OIG | UI fraud |
| GAO FraudNet | Government-wide |
| Agency program integrity lines, state Medicaid Fraud Control Units | Program specific |
| False Claims Act qui tam complaints | Filed under seal with DOJ; out of scope for this tool |

## 2. What the model returns

| Field | Meaning |
| --- | --- |
| score (0-100) | Actionability: specific, checkable facts score high |
| priority | urgent, high, normal or low |
| program, scheme | From fixed lists, so tips can be routed and counted |
| summary | Two neutral sentences, no conclusions about guilt |
| reasons | Why the score is what it is |
| entities | Named people, firms and identifiers, as written |
| whistleblower_protection | The tipster appears to be an employee, contractor or grantee staff member |
| scorer | "rules" or "claude+rules", so every score is traceable |

The model's score is blended with the rule score (70/30 by default), and
the rule score is used alone if the model is unavailable or declines.

## 3. Rule baseline

Points for naming a program and a scheme, amounts, dates, addresses,
identifiers (NPI, UEI, contract numbers), an insider account and mentions
of evidence; points off for very short tips and general grievance
language. Crude on purpose: it sets the floor the model must beat, and its
reasons are easy to check.

## 4. Model and hosting

- **Model:** Claude (`claude-opus-5-5` by default) through the Anthropic
  Python SDK, with a JSON-schema output format so every answer has the
  same fields, low effort to keep cost per tip small, and server-side
  refusal fallback enabled.
- **Hosting:** tips contain personal data about tipsters and subjects. The
  model must run in an environment authorized for that data: an OIG's
  FedRAMP-authorized cloud tenancy (Claude is available on government cloud
  regions of the major providers; check current authorization levels) or
  the agency's own enclave. No tip goes to a commercial endpoint without
  that authorization, and the provider must not retain or train on the
  data.
- **Cost:** a typical tip is a few hundred words; at low effort the cost
  per tip is a small fraction of a cent to a few cents, far below the cost
  of an analyst's minute.

## 5. Safeguards

- **No automated closure.** The tool orders and summarizes; people decide.
- **Prompt injection:** tip text is wrapped and marked as data; the system
  prompt tells the model to ignore instructions inside it. The pilot test set includes
  tips that try to instruct the model.
- **Whistleblower protection:** flagged tips are routed under the OIG's
  confidentiality procedures (IG Act, 5 U.S.C. 407(b)); the tipster's
  identity is not shared with the program office.
- **Bias:** score distributions are compared by language, program and
  region of the tip, and tips written in other languages are translated
  rather than penalized.
- **Audit trail:** original text, both scores, reasons and model version
  are kept with every tip.

## 6. Pilot design (60 days, one OIG)

1. Take a closed historical set of 2,000 to 5,000 tips with known outcomes
   (substantiated, referred, closed) inside the OIG's environment.
2. Score them blind with both scorers.
3. Measure recall in the top 20% and lift over the current order; compare
   model and rules.
4. Hand-check 200 model summaries for accuracy and neutrality.
5. Pass mark: the model finds at least 1.5 times as many substantiated tips
   in the top 20% as the current process, with summaries rated accurate in
   at least 95% of checks.

## 7. Questions for Steve

1. Which OIG hotline is the most likely partner: HHS-OIG (largest) or SBA
   OIG (existing relationship)?
2. Are we comfortable proposing a model provider, or should the proposal
   stay model-neutral and name Claude as the reference implementation?
