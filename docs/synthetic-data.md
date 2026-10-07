# VYŪH — Synthetic Data Specification

> **Purpose:** Define the synthetic event-sequence dataset used to develop, validate, and demonstrate VYŪH before institution-specific real transaction data is available.
>
> **Source of truth:** docs/VYUH_Complete_Specification.md
>
> **Status:** Round 1 MVP specification

---

## 1. Objective

VYŪH requires labeled event sequences representing both legitimate behavior and coordinated scam workflows.

The synthetic dataset is designed to test whether VYŪH can:

1. distinguish coordinated scam sequences from benign behavior;
2. recognize the five canonical scam templates;
3. maintain a low false-positive burden on benign sequences; and
4. support reproducible prototype evaluation without real customer transaction data.

Synthetic validation is for **prototype validation and demonstration**, not production performance claims.

---

## 2. Dataset Composition

| Class | Sequences | Purpose |
|---|---:|---|
| Benign | 5,000 | Legitimate account behavior |
| Scam | 1,000 | Coordinated scam workflows |
| **Total** | **6,000** | Primary dataset |

The 1,000 scam sequences are evenly distributed across the five canonical templates:

| Template | Name | Sequences |
|---|---|---:|
| T1 | SIM/Device Takeover + Rapid Transfer | 200 |
| T2 | Remote-Access App + Unauthorized Transfer | 200 |
| T3 | Phishing/Smishing + Credential Compromise | 200 |
| T4 | Vishing/Fake Support + Collect Request | 200 |
| T5 | Mule Account + Rapid Dispersal | 200 |

The dataset counts **sequences**, not individual events.

---

## 3. Data Representation

The working representation is **JSONL: one event per line**.

A sequence is an ordered collection of normalized event records. A conceptual record should contain the information required by the VYŪH detection pipeline, including:

- timestamp;
- account/session identifier;
- event type;
- device/authentication context;
- beneficiary context;
- transaction amount where applicable;
- session/network context;
- destination/network context; and
- labels or metadata needed for offline evaluation.

The exact production schema is intentionally not defined here. The generator should produce the fields required by the detection pipeline without implying access to real bank data.

---

## 4. Benign Sequence Generation

Benign sequences should represent legitimate customer behavior rather than random low-risk transactions.

Each benign sequence should be generated from an **account-specific behavioral profile**, with realistic variation in:

- normal transaction amounts;
- normal beneficiaries;
- device continuity;
- transaction frequency;
- typical activity hours;
- authentication behavior; and
- session/network context.

This supports evaluation against VYŪH's rolling 90-day behavioral baseline.

### Hard negatives

Approximately **5–10% of benign sequences** should be deliberately constructed as hard negatives.

Examples include:

- a new device without a coordinated attack sequence;
- a new beneficiary followed by a legitimate transfer;
- an unusually large but legitimate transaction;
- elevated transaction velocity without a scam workflow; and
- unusual activity timing without corroborating signals.

The purpose is to prevent VYŪH from treating an individual anomaly as sufficient evidence of fraud.

For benign hard negatives, the intended template-match score should remain **below 0.60**.

---

## 5. Scam Sequence Generation

Scam sequences are generated from the five canonical VYŪH templates.

Each template represents a recognizable workflow rather than a single suspicious event. The generator should preserve the defining structure while introducing controlled variation so the detector cannot rely on one exact sequence or fixed amount.

### Scam-strength distribution

| Match strength | Target share |
|---|---:|
| Strong (≥ 0.80) | ~60% |
| Moderate (0.60–0.79) | ~30% |
| Noisy (< 0.60) | ~10% |

This distribution tests both clear attacks and imperfect observations.

---

## 6. Canonical T1 Generation Parameters

T1 — **SIM/Device Takeover + Rapid Transfer** is the canonical demonstration workflow.

| Parameter | Range |
|---|---|
| Account age | 30–1,000 days |
| Device change → login | 0–2 minutes |
| Login → beneficiary | 1–5 minutes |
| Beneficiary → transfer | 1–5 minutes |
| Amount multiplier | 1.5–4.0× baseline |
| Transfers | 1–2 |

Representative sequence:

~~~text
10:00  Normal transaction: ₹1,200
10:02  New-device login
10:05  New beneficiary added
10:06  ₹48,000 transfer
10:08  ₹15,000 rapid transfer
~~~

The canonical demo targets a risk score of approximately **0.87**, but 0.87 must be an engine output rather than a hardcoded dataset value.

---

## 7. Noise and Adversarial Variation

Synthetic scam sequences should include controlled perturbations representing incomplete or noisy attack telemetry:

- missing events;
- delayed events;
- amounts closer to normal;
- benign transactions mixed into the sequence;
- timing jitter; and
- different event ordering.

Noise should make the sequence less obvious without changing its intended ground-truth label.

For example, a T1 sequence may omit one expected event while retaining enough evidence for a moderate template match.

---

## 8. Temporal Windows

Synthetic sequences must support the same temporal reasoning used by the detector:

| Window | Role |
|---|---|
| **10 minutes** | Primary sequence window |
| **60 minutes** | Supporting velocity/context window |
| **90 days** | Rolling behavioral baseline |

Generated timestamps should allow testing of:

- rapid event progression;
- transaction velocity;
- unusual timing;
- deviation from historical account behavior; and
- template-level temporal consistency.

The **10-minute window is the primary sequence window** for the MVP.

---

## 9. Template Matching

The specified template-match score is:

~~~text
TemplateMatch =
    0.70 × event_coverage
  + 0.20 × temporal_consistency
  + 0.10 × contextual_consistency
~~~

| Template match | Interpretation |
|---:|---|
| < 0.60 | Does not contribute to risk score |
| 0.60–0.79 | Moderate match |
| 0.80–1.00 | Strong match |

The dataset should contain examples across these ranges rather than only high-confidence attacks.

---

## 10. Dataset Split and Leakage Prevention

The locked specification defines:

### Validation set

- 3,000 benign sequences
- 500 scam sequences

### Golden set

- 2,000 benign sequences
- 500 scam sequences
- held out
- evaluated once

The golden set must remain frozen during tuning.

### Leakage prevention

The split process should prevent near-duplicate sequences, template instances, or account histories from crossing evaluation boundaries.

Rules:

- Do not tune thresholds on the golden set.
- Do not use golden-set results to modify signal weights.
- Do not reuse the same generated sequence in multiple splits.
- Preserve account-level separation where historical events are used.
- Keep the final golden evaluation reproducible.

The purpose is to ensure reported prototype metrics reflect held-out evaluation rather than repeated tuning against test data.

---

## 11. Validation Targets

| Metric | Target |
|---|---:|
| Precision | ≥ 80% |
| Recall | ≥ 80% |
| F1 score | ≥ 80% |
| False-positive rate | < 1% |
| False positives per 1,000 benign | < 10 |

The primary operational metric is **false positives per 1,000 benign sequences** because the project emphasizes reducing analyst noise without sacrificing scam detection.

These are validation targets, not guaranteed results.

---

## 12. Baseline Comparison

VYŪH should be compared against the specified deterministic OR-style baseline:

~~~text
IF
    amount > 3× baseline
    OR new_device
    OR new_beneficiary
    OR >3 transactions in 10 minutes
    OR (unusual hour AND amount z-score > 2.5)
THEN
    FLAG
ELSE
    ALLOW
~~~

The comparison should use the same held-out evaluation framework where practical.

This baseline is a reference detector for prototype comparison, not a claim that it represents every production fraud system.

---

## 13. Reproducibility Requirements

The synthetic-data pipeline should make generation reproducible.

At minimum, record:

- generator version;
- random seed;
- dataset version;
- template identifier;
- ground-truth label;
- generation parameters;
- train/validation/golden split; and
- timestamp-generation configuration.

Each dataset artifact should be traceable to the generator configuration that produced it.

If the generator changes, the dataset version should change as well.

---

## 14. Ground Truth

Because the dataset is synthetic, ground truth is assigned by the generator.

Each sequence should preserve:

- benign/scam label;
- scam template when applicable;
- intended template-strength category;
- relevant generation parameters; and
- noise/perturbation metadata where needed.

Ground truth must remain independent from the detector's predicted score.

The detector must never receive the ground-truth label as an input feature.

---

## 15. New-Account Handling

Accounts younger than **7 days** require special treatment.

VYŪH should use **signal-specific defaults** rather than assigning a blanket risk value such as 0.5 to every missing historical signal.

> **Lack of history ≠ suspiciousness.**

Synthetic data should include new-account cases so evaluation tests whether legitimate users are systematically penalized simply because sufficient historical behavior is unavailable.

The exact numeric defaults are **not specified** in the locked project specification and must not be invented here.

---

## 16. What Synthetic Data Does Not Represent

Synthetic data cannot fully reproduce:

- real UPI transaction distributions;
- real customer heterogeneity;
- institution-specific fraud labels;
- real operational review behavior;
- adversarial adaptation by fraudsters; or
- production gateway behavior.

Therefore, synthetic validation demonstrates **prototype behavior**, not production effectiveness.

The project must not claim:

- production-grade fraud detection;
- validated performance on real UPI/bank data;
- measured real-world fraud-loss reduction; or
- production false-positive performance.

---

## 17. Dataset Acceptance Checklist

Before using dataset results in the MVP or submission:

- [ ] 5,000 benign sequences generated.
- [ ] 1,000 scam sequences generated.
- [ ] 200 scam sequences per canonical template.
- [ ] Benign sequences are profile-based rather than purely random.
- [ ] Approximately 5–10% of benign data contains hard negatives.
- [ ] Scam-strength distribution is approximately 60% strong, 30% moderate, 10% noisy.
- [ ] T1 parameter ranges remain within specification.
- [ ] Noise/perturbation cases are represented.
- [ ] 10-minute, 60-minute, and 90-day behavior can be evaluated.
- [ ] Template match uses the specified 0.70/0.20/0.10 formulation.
- [ ] Validation and golden sets are separated before tuning.
- [ ] Golden set remains frozen.
- [ ] No sequence leakage exists across evaluation boundaries.
- [ ] Baseline comparison is reproducible.
- [ ] Final metrics are measured rather than assumed.
- [ ] Synthetic-data caveats are disclosed.

---

## 18. Implementation Boundary

This document specifies **what synthetic data must represent** and **how it must be evaluated**.

It does not prescribe details that are not locked by the project specification, including:

- exact probability distributions for every field;
- exact random-generation algorithm;
- exact raw-feature normalization equations;
- exact numeric defaults for missing historical signals;
- production data schemas; or
- institution-specific fraud labels.

These details should be introduced only when the MVP implementation requires them and documented explicitly rather than presented as part of the locked specification.

---

## 19. Canonical Principle

> **Generate workflows, not isolated suspicious transactions.**

The synthetic dataset exists to make VYŪH's central claim testable:

**VYŪH moves from event flagging to sequence scoring by evaluating coordinated behavior over time.**

---

## 20. Related Documentation

- VYUH_Complete_Specification.md — locked project specification
- threat-model.md — threats, templates, assets, and assumptions
- detection-logic.md — event processing, template matching, and policy mapping
- risk-scoring.md — scoring weights, thresholds, and validation targets
