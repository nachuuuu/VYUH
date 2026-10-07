# VYŪH Risk Scoring

**Status:** Round 1 Submission Locked  
**Scope:** Weighted workflow-level risk scoring and policy mapping

This document defines the scoring framework used by VYŪH after event normalization, session construction, signal extraction, and scam-template matching.

> **Scoring discipline:** Exact weights, thresholds, windows, and safety boundaries are taken from the locked VYŪH specification. Where the specification does not define a numeric transformation, this document does not invent one.

---

## 1. Scoring Objective

The VYŪH score represents the degree to which an observed event sequence is consistent with suspicious behavior and known scam workflows.

The score is intended to combine multiple forms of evidence rather than allowing a single anomaly to determine the highest-risk action.

The scoring layer sits between signal extraction/template matching and policy mapping:

```text
Events
  ↓
Signals + Template Matches
  ↓
Weighted Risk Score
  ↓
Policy Mapper
  ↓
Action
```

---

## 2. Score Range

The VYŪH risk score is represented on a normalized **0.00–1.00** scale.

| Range | Interpretation |
|---:|---|
| **0.00** | Lowest modeled risk |
| **1.00** | Highest modeled risk |

The score is a risk assessment, not a probability claim unless a future calibration study explicitly establishes probabilistic calibration.

---

## 3. Eight Scoring Signals

VYŪH combines eight signals:

| ID | Signal | Specification basis | Weight |
|---|---|---|---:|
| **S1** | Behavioral deviation | Rolling 90-day MAD baseline | **20%** |
| **S2** | Device/authentication change | New device, unusual authentication method | **20%** |
| **S3** | Amount anomaly | Transaction amount deviation | **15%** |
| **S4** | Beneficiary novelty | New/rare beneficiary | **15%** |
| **S5** | Velocity | 10-minute + 60-minute windows | **10%** |
| **S6** | Session/context risk | Unusual hour, IP/geo, authentication failures | **10%** |
| **S7** | Template match | Known scam-workflow correspondence | **5%** |
| **S8** | Destination/network risk | High-risk payment-network context | **5%** |
| **Total** | | | **100%** |

These weights are the weighting presentation specified in the locked VYŪH design brief.

---

## 4. Weighted Score

At the conceptual level, the final score is a weighted combination of the eight normalized signals:

```text
Risk Score =
    0.20 × S1
  + 0.20 × S2
  + 0.15 × S3
  + 0.15 × S4
  + 0.10 × S5
  + 0.10 × S6
  + 0.05 × S7
  + 0.05 × S8
```

The weights sum to 1.00.

### Important implementation boundary

The locked specification does **not** define the exact normalization formula for every signal.

Therefore, an implementation must separately specify how each raw feature becomes a normalized signal value in the 0–1 range. Those transformations should be documented, tested, and calibrated against the validation set.

This distinction matters because the weights are specified, while the internal feature-to-signal transformations are not fully specified.

---

## 5. Signal Interpretation

### S1 — Behavioral Deviation

Measures deviation from the account's rolling 90-day behavioral baseline.

The specification identifies **MAD (median absolute deviation)** as the baseline method.

```text
Historical behavior → 90-day baseline → current deviation → S1
```

### S2 — Device / Authentication Change

Captures evidence such as:
- New device
- Unusual authentication method

This signal is particularly relevant to T1 and T3 workflows.

### S3 — Amount Anomaly

Measures how unusual the current transaction amount is relative to the account's established behavior.

The specification also uses an amount multiplier in T1 synthetic-data generation and a z-score condition in the transparent baseline detector. These are validation/data-generation constructs and should not automatically be treated as the final VYŪH S3 formula.

### S4 — Beneficiary Novelty

Captures whether the destination beneficiary is new or rarely used.

### S5 — Velocity

Measures transaction activity over:
- 10 minutes
- 60 minutes

Rapid successive transfers are important evidence in T1 and T5 workflows.

### S6 — Session / Context Risk

Considers:
- Unusual hour
- IP/geo context
- Authentication failures

### S7 — Template Match

Measures correspondence between the observed sequence and the five known scam workflows.

Template matching is itself explicitly defined:

```text
TemplateMatch =
    0.70 × event_coverage
  + 0.20 × temporal_consistency
  + 0.10 × contextual_consistency
```

### S8 — Destination / Network Risk

Captures high-risk payment-network context associated with the destination.

---

## 6. Template Match Contribution

Template matches use a thresholded contribution model:

| Template match | Scoring treatment |
|---:|---|
| **< 0.60** | Contributes **0** to final score |
| **0.60–0.79** | Moderate contribution |
| **0.80–1.00** | Strong contribution |

This prevents weak template correspondence from being treated as strong workflow evidence.

### Template score formula

```text
T = 0.70 × event_coverage
  + 0.20 × temporal_consistency
  + 0.10 × contextual_consistency
```

where:

- `event_coverage` represents how much of the expected workflow is observed.
- `temporal_consistency` represents how closely event timing follows the workflow.
- `contextual_consistency` represents compatibility of surrounding context with the workflow.

The specification does not provide further numeric definitions for these three components.

---

## 7. Policy Thresholds

The final weighted score is mapped to four MVP actions:

| Risk score | Action |
|---:|---|
| **0.00–0.29** | `ALLOW` |
| **0.30–0.59** | `SOFT_PROMPT` |
| **0.60–0.79** | `STEP_UP_VERIFY` |
| **0.80–1.00** | `HOLD_FOR_REVIEW` |

### Boundary table

The intended boundary behavior is:

| Score | Expected action |
|---:|---|
| `0.29` | `ALLOW` |
| `0.30` | `SOFT_PROMPT` |
| `0.59` | `SOFT_PROMPT` |
| `0.60` | `STEP_UP_VERIFY` |
| `0.79` | `STEP_UP_VERIFY` |
| `0.80` | `HOLD_FOR_REVIEW` |

These boundaries should be explicitly covered by unit tests.

---

## 8. No Automatic BLOCK

**`BLOCK` is not part of the MVP scoring action set.**

The highest automated action produced by the policy mapper is:

```text
HOLD_FOR_REVIEW
```

The architecture also specifies:
- Scoring engine cannot directly call the transaction gateway.
- Policy mapping is separated from scoring logic.
- Unit tests validate action boundaries.

This is a deliberate safety boundary, not a missing feature.

---

## 9. Canonical T1 Score

The canonical demonstration sequence is:

| Time | Event |
|---|---|
| 10:00 | Normal transaction — ₹1,200, old device, existing beneficiary |
| 10:02 | New device login |
| 10:05 | New beneficiary added |
| 10:06 | ₹48,000 transfer to new beneficiary |
| 10:08 | ₹15,000 rapid transfer |

The specification gives the expected demonstration result as approximately:

```text
Template: T1
Risk: ≈ 0.87
Action: HOLD_FOR_REVIEW
```

**The value 0.87 must not be hardcoded.** The actual implementation must calculate the score from the event sequence.

The canonical score is therefore a demonstration target, not a claim that every implementation will produce exactly 0.87.

---

## 10. New-Account Scoring

For accounts with **less than seven days of history**, the specification requires signal-specific defaults.

```text
Do not use a blanket 0.5 default.
```

The absence of behavioral history must not itself be interpreted as suspiciousness.

The locked specification does not define the numeric default for each individual signal. Those values must be treated as implementation parameters and evaluated during validation.

---

## 11. Calibration Dataset

Threshold tuning uses the specified validation set:

| Set | Composition | Purpose |
|---|---|---|
| Development generation | 5,000 benign + 1,000 scam | Build/test detector behavior |
| Validation | 3,000 benign + 500 scam | Threshold tuning |
| Golden test | 2,000 benign + 500 scam | Held-out final evaluation |

### Data separation rules

- Generation and evaluation sets are separated to prevent leakage.
- The golden test set is frozen before threshold tuning.
- No test data is used for model development.

---

## 12. Target Metrics

VYŪH's synthetic evaluation targets are:

| Metric | Target |
|---|---:|
| Precision | **≥ 80%** |
| Recall | **≥ 80%** |
| F1 | **≥ 80%** |
| False-positive rate | **< 1%** |

The primary operational metric is:

**False positives per 1,000 benign sequences.**

That metric is intended to make alert burden directly interpretable.

### Reporting requirement

Evaluation should report:
- Precision
- Recall
- F1
- False-positive rate
- False positives per 1,000 benign sequences
- Confusion matrix
- Actual measured results

Targets must not be presented as measured performance.

---

## 13. Baseline Comparison

The project defines a transparent baseline detector:

```text
IF (amount > 3× account baseline)
   OR (new device)
   OR (new beneficiary)
   OR (>3 transactions in 10 min)
   OR (unusual hour AND amount z-score > 2.5)
THEN FLAG
ELSE ALLOW
```

This baseline uses OR logic and evaluates individual anomalies independently.

VYŪH differs by combining eight signals with temporal sequence and template context.

Therefore, the comparison should focus on whether VYŪH improves sequence-level discrimination and reduces false-positive burden under the same evaluation conditions.

---

## 14. Hard-Negative Scoring

The synthetic benign set includes approximately **5–10% hard negatives**.

Examples include:
- Legitimate device changes
- High-value family payments
- Short legitimate transaction bursts

These cases are important because the detector must distinguish unusual-but-legitimate activity from coordinated scam sequences.

A benign hard negative should not receive a high score merely because one or more individual signals are elevated.

---

## 15. Score Explainability

A risk score must be accompanied by evidence rather than presented as an opaque number.

The MVP evidence output should expose:
- Overall risk score
- Individual signal scores/contributions
- Matched template
- Event timeline
- Final policy action

The evidence card supports analyst review and later error analysis.

---

## 16. Feedback and Offline Calibration

Analyst feedback is logged with:
- `case_id`
- `decision`
- `risk_score`
- `template`
- `signal_scores`
- `analyst_id`
- `timestamp`
- `reason`

Supported review outcomes include:
- `RELEASE`
- `ESCALATE`
- `FALSE_POSITIVE`

These labels can support:
- Offline threshold calibration
- Error analysis
- Future model updates

**Online retraining is explicitly excluded from the MVP.**

---

## 17. Calibration Principles

Threshold calibration should prioritize the project's stated operational objective:

> **Keep false positives low while retaining sufficient recall for known scam workflows.**

Because the golden test set is held out, threshold selection must occur using the validation set rather than repeatedly tuning against final-test results.

Any future change to signal weights or policy thresholds should be:
1. Documented.
2. Tuned on the validation set.
3. Evaluated once on the frozen golden test set.
4. Reported as a new measured result.

---

## 18. Score Integrity Requirements

The implementation should enforce the following invariants:

- Final risk score remains within **[0, 1]**.
- Signal values entering the weighted combination use a documented normalization.
- The eight weights sum to **1.00**.
- Template matches below **0.60** contribute zero.
- Policy thresholds map deterministically to the four specified actions.
- `BLOCK` is unavailable to the scoring engine.
- The scoring engine has no direct transaction-gateway control.
- Golden-test data is not used during threshold tuning.

These invariants are more important than adding model complexity to the MVP.

---

## 19. Implementation Boundary

The core MVP scoring interface is:

```python
def score_sequence(events: list[dict]) -> dict:
    # returns: risk_score, action, signals, template, evidence
```

The API wrapper is specified as:

```text
POST /score
```

The scoring layer should remain independently replayable so that the canonical T1 sequence can be evaluated without requiring live transaction integration.

---

## 20. Non-Claims

The scoring framework does **not** establish:
- Production fraud-detection performance.
- A calibrated probability of fraud.
- Coverage of all UPI scam types.
- Real-world precision, recall, F1, or false-positive rate.
- Automatic transaction blocking.

Those claims require measured implementation results and, for production claims, institution-specific validation.

---

## 21. Summary

VYŪH uses a normalized 0–1 risk score built from eight weighted signals and temporal scam-template evidence.

The critical design choices are:

1. **Multiple signals instead of isolated alerts.**
2. **Temporal context over 10-minute and 60-minute windows.**
3. **Known-workflow template matching.**
4. **Explicit risk-action thresholds.**
5. **No automatic BLOCK in the scoring engine.**
6. **Validation and calibration separated from the frozen golden test set.**
7. **Explainable evidence accompanying the score.**

The result is a conservative, auditable scoring layer designed for workflow-level scam detection rather than an unconstrained transaction-blocking model.