# VYŪH Threat Research

**Status:** Initial threat-model foundation

## Purpose

This document records the threat-research assumptions that support VYŪH's temporal fraud-detection approach.

The focus is not to enumerate every form of payment fraud. It is to identify scam behaviours that can plausibly appear as **sequences of related account, device, authentication, beneficiary, and transaction events** and therefore can be represented by VYŪH's workflow-oriented detection model.

Research maturity and implementation maturity are kept separate. A threat pattern documented here does not automatically become a detection rule.

---

## Threat Model Scope

VYŪH currently focuses on five canonical scam workflows:

| ID | Workflow | Core behavioural pattern |
|---|---|---|
| T1 | SIM/Device Takeover + Rapid Transfer | Account/device state changes followed by rapid beneficiary and transfer activity |
| T2 | Remote-Access App + Unauthorized Transfer | Suspicious session/device context followed by unauthorized payment activity |
| T3 | Phishing/Smishing + Credential Compromise | Compromise indicators followed by account access and payment activity |
| T4 | Vishing/Fake Support + Collect Request | Social-engineering interaction followed by a collect-request payment flow |
| T5 | Mule Account + Rapid Dispersal | Funds received into an account followed by rapid onward movement |

These templates define the current research boundary. Additional workflows should be introduced explicitly and evaluated separately rather than silently extending an existing template.

---

## Threat Actors and Abuse Patterns

The current threat model treats the adversary as capable of manipulating or inducing legitimate users and accounts into fraudulent payment workflows.

Relevant abuse patterns include:

- obtaining or abusing access to an account
- changing or introducing a device or authentication context
- inducing credential disclosure or account compromise
- introducing a new beneficiary
- initiating unusual or rapid transfers
- exploiting collect-request or payment-approval flows
- using accounts to receive and rapidly disperse funds
- combining individually plausible events into a fraudulent sequence

The model therefore emphasizes **relationships between events**, not only whether a single transaction looks unusual.

---

## Protected Assets

VYŪH's threat model is concerned with protecting:

- customer funds
- payment-account integrity
- account and authentication integrity
- beneficiary relationships
- transaction trust
- analyst decision quality
- privacy of behavioural and transaction data

The system also treats the integrity of its own risk score and evidence as security-relevant assets. Manipulated inputs or explanations could affect downstream review decisions.

---

## Detection-Relevant Signals

The current VYŪH architecture defines eight signals:

| Signal | Detection purpose |
|---|---|
| **S1 — Behavioral deviation** | Detects deviation from the account's rolling 90-day behavioural baseline |
| **S2 — Device/authentication change** | Detects new devices or unusual authentication context |
| **S3 — Amount anomaly** | Detects transaction amounts that materially differ from normal account behaviour |
| **S4 — Beneficiary novelty** | Detects newly introduced or previously unseen beneficiaries |
| **S5 — Velocity** | Detects unusual transaction activity over 10-minute and 60-minute windows |
| **S6 — Session/context risk** | Captures unusual hour, IP/geo context, and authentication failures |
| **S7 — Template match** | Measures alignment with a known scam workflow |
| **S8 — Destination/network risk** | Captures risk associated with the payment destination or network |

These signals are detection abstractions defined by the VYŪH specification. Their exact raw-feature extraction and normalization logic remains an implementation concern unless explicitly specified elsewhere.

---

## Temporal Threat Model

VYŪH uses multiple time horizons because different threat indicators operate at different temporal scales.

| Window | Purpose |
|---|---|
| **10 minutes** | Primary sequence construction and rapid workflow detection |
| **60 minutes** | Supporting velocity and contextual analysis |
| **90 days** | Account-specific behavioural baseline |

The central threat-model assumption is that fraudulent activity may become distinguishable when individually plausible events are connected within a short temporal sequence.

Example:

```text
Normal transaction
      ↓
New device login
      ↓
New beneficiary
      ↓
Large transfer
      ↓
Rapid additional transfer
```

This sequence can carry more detection value than evaluating any one event independently.

---

## Threat-to-Signal Mapping

| Workflow | High-relevance signals |
|---|---|
| T1 | S1, S2, S3, S4, S5, S6, S7 |
| T2 | S2, S3, S5, S6, S7 |
| T3 | S2, S3, S4, S5, S6, S7 |
| T4 | S3, S4, S6, S7, S8 |
| T5 | S1, S3, S4, S5, S7, S8 |

This mapping is a design hypothesis for organizing detection evidence. It is not evidence that every listed signal will independently distinguish the workflow in real-world data.

---

## False Positives and Benign Counterexamples

A central threat-research problem is distinguishing malicious workflows from legitimate activity that produces similar event sequences.

Potential benign counterexamples include:

- a legitimate new-device login followed by normal payment activity
- a customer making an unusually large legitimate purchase
- a newly added beneficiary for a genuine payment
- several legitimate transfers made within a short period
- travel or network changes causing unusual IP/geo context
- legitimate authentication recovery
- newly created accounts with limited behavioural history

VYŪH therefore treats isolated anomalies as insufficient evidence for an automatic block.

The system's current policy boundary is:

```text
Risk Score
    ↓
Policy Mapper
    ↓
ALLOW
SOFT_PROMPT
STEP_UP_VERIFY
HOLD_FOR_REVIEW
```

No automatic BLOCK action is part of the current scoring architecture.

---

## Adversarial and Noisy Behaviour

Scam sequences should not be assumed to be perfectly ordered or complete.

The VYŪH synthetic-data specification therefore allows:

- missing events
- delayed events
- timing jitter
- amounts closer to normal behaviour
- benign transactions mixed into scam sequences
- altered event ordering

These variations are intended to test whether detection depends too heavily on an idealized sequence.

Real adversarial robustness remains an open research problem and requires further evaluation.

---

## New Accounts and Missing History

New accounts create an important ambiguity: limited historical data can make behavioural deviation difficult to estimate, but lack of history is not itself evidence of fraud.

VYŪH therefore specifies **signal-specific defaults** for accounts younger than seven days rather than applying a blanket suspiciousness value.

The numerical defaults are intentionally not invented here. They should remain configuration until empirically justified.

---

## Trust Boundaries

Important boundaries in the threat model include:

1. **Event source → normalization**
   - Incoming events must be validated before use.

2. **Normalization → detection**
   - Detection logic should operate on a consistent event representation.

3. **Detection → policy**
   - Risk scoring and policy decisions remain separate components.

4. **Policy → human review**
   - Escalated cases require evidence that an analyst can inspect.

5. **Feedback → future evaluation**
   - Reviewer labels should not silently alter scoring logic or evaluation datasets.

6. **Development data → evaluation data**
   - Training/tuning data must remain separated from held-out evaluation data.

These boundaries reduce the risk that malformed inputs, feedback leakage, or undocumented policy changes invalidate the detection process.

---

## Research Questions

The following questions remain open and should be answered through research or controlled evaluation:

- Which raw event features provide the strongest evidence for each signal?
- How stable are behavioural baselines across different customer profiles?
- How much does each signal contribute independently?
- Which benign workflows most frequently resemble each scam template?
- How robust is template matching to missing or reordered events?
- How should thresholds change across different operational environments?
- How does detection performance change under population or behavioural drift?
- Which evidence is most useful to human reviewers?
- What real-world data is required to validate the synthetic assumptions?

Open questions should not be treated as settled design decisions.

---

## Evidence Discipline

Claims in this document should be classified before being used in engineering decisions:

| Type | Meaning |
|---|---|
| **Observed** | Directly supported by a source or measured experiment |
| **Specified** | Defined by the current VYŪH project specification |
| **Hypothesis** | Proposed explanation or detection assumption requiring validation |
| **Inference** | Reasoned conclusion derived from available evidence |
| **Open question** | Not yet sufficiently established |

Where external sources are used, they should be recorded in [references.md](./references.md).

---

## Limitations

This document does not establish:

- real-world prevalence of any scam workflow
- effectiveness of VYŪH on production UPI traffic
- causal attribution between a signal and a scam
- regulatory compliance
- guaranteed fraud-loss reduction
- universal applicability across financial institutions

Those questions require evidence beyond the current project specification and synthetic evaluation framework.

---

## Research Principle

> **A threat pattern becomes a VYŪH detection capability only after its assumptions are explicit and its performance can be evaluated against legitimate counterexamples.**
