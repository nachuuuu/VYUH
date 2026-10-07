# VYŪH Detection Logic

**Status:** Round 1 Submission Locked  
**Scope:** Sequence-level detection of known UPI scam workflows

This document defines the detection path from normalized events to signal extraction, temporal template matching, weighted risk scoring, policy mapping, and evidence generation.

> **Implementation discipline:** Where the locked specification gives an exact formula, threshold, window, or boundary, this document preserves it. Where the specification does not define an implementation-level formula, the implementation should not invent one without updating the specification.

---

## 1. Detection Objective

VYŪH does not treat every transaction as an independent classification problem.

The detector is designed to answer:

> **Do the observed events form a coordinated sequence that is consistent with a known scam workflow?**

The system combines:
- Behavioral context
- Device and authentication changes
- Transaction amount behavior
- Beneficiary novelty
- Transaction velocity
- Session/context information
- Known scam-template correspondence
- Destination/network risk

The output is a single explainable risk assessment with a bounded policy action.

---

## 2. End-to-End Detection Pipeline

```text
Raw Events
    ↓
Event Normalization
    ↓
Session Construction — 10 min
    ↓
8 Signal Extractors
    ↓
5 Template Matchers
    ↓
Weighted Risk Score
    ↓
Policy Mapper
    ↓
ALLOW / SOFT_PROMPT / STEP_UP_VERIFY / HOLD_FOR_REVIEW
    ↓
Evidence Card
    ↓
Human Reviewer
    ↓
Label + Reason
```

Each stage has a distinct responsibility. In particular, scoring and policy mapping remain separate so that the scoring engine does not directly control the transaction gateway.

---

## 3. Event Normalization

Raw payment, authentication, device, beneficiary, and contextual events must first be normalized into a common event representation.

The purpose of normalization is to make heterogeneous events comparable before session construction and signal extraction.

At this stage, the detector should preserve the event information required to evaluate:
- Event type
- Event timestamp
- Account/session relationship
- Device/authentication context
- Transaction information
- Beneficiary information
- Session/context information
- Destination/network context

The locked specification does not prescribe a final production event schema. The schema should therefore remain an implementation artifact until formally defined.

---

## 4. Session Construction

### Primary sequence window: 10 minutes

VYŪH constructs a primary session/sequence over a **10-minute window**.

This is the principal temporal boundary used to distinguish a coordinated attack sequence from unrelated unusual events.

### Supporting windows

| Window | Purpose |
|---|---|
| **10 minutes** | Primary sequence reconstruction and velocity |
| **60 minutes** | Extended velocity and contextual analysis |
| **90 days** | Rolling behavioral baseline |

### Why the temporal layer matters

Consider the difference between:

```text
Device change → beneficiary change → high-value transfer
within minutes
```

and:

```text
Device change on one day
Beneficiary change several days later
Large payment later
```

The first pattern has substantially stronger workflow-level evidence because the events form a temporally coherent sequence.

---

## 5. Signal Extraction

VYŪH extracts eight signals.

| ID | Signal | Definition in specification |
|---|---|---|
| **S1** | Behavioral deviation | Deviation from a rolling 90-day MAD baseline |
| **S2** | Device/authentication change | New device or unusual authentication method |
| **S3** | Amount anomaly | Transaction amount deviation |
| **S4** | Beneficiary novelty | New or rare beneficiary |
| **S5** | Velocity | Activity across 10-minute and 60-minute windows |
| **S6** | Session/context risk | Unusual hour, IP/geo context, and authentication failures |
| **S7** | Template match | Correspondence with a known scam workflow; contributes at ≥0.60 |
| **S8** | Destination/network risk | High-risk payment-network context |

These signals are combined rather than treated as independent binary alerts.

---

## 6. Signal Weighting

The locked specification states that all eight signals are weighted and combined into a single risk score.

The slide design in the same locked specification defines the following weighting presentation:

| Signal | Weight |
|---|---:|
| Behavioral deviation | 20% |
| Device/authentication change | 20% |
| Amount anomaly | 15% |
| Beneficiary novelty | 15% |
| Velocity | 10% |
| Session/context risk | 10% |
| Template match | 5% |
| Destination/network risk | 5% |
| **Total** | **100%** |

Conceptually:

```text
Risk Score = weighted combination of S1 ... S8
```

The exact normalization formula for each individual signal is not specified in the locked document. Implementations should therefore define and document those transformations separately rather than presenting an invented formula as part of the locked architecture.

---

## 7. Template Matching

VYŪH evaluates five known scam workflows:

| ID | Template |
|---|---|
| **T1** | SIM/Device Takeover + Rapid Transfer |
| **T2** | Remote-Access App + Unauthorized Transfer |
| **T3** | Phishing/Smishing + Credential Compromise |
| **T4** | Vishing/Fake Support + Collect Request |
| **T5** | Mule Account + Rapid Dispersal |

Each template is evaluated using:

```text
TemplateMatch =
    0.70 × event_coverage
  + 0.20 × temporal_consistency
  + 0.10 × contextual_consistency
```

### 7.1 Event coverage

Measures how much of the expected workflow is represented by the observed events.

### 7.2 Temporal consistency

Measures whether the observed events occur in the expected temporal relationship.

### 7.3 Contextual consistency

Measures whether the surrounding context is compatible with the workflow.

The locked specification gives the formula and weighting but does not prescribe a more granular implementation formula for each component.

---

## 8. Template Contribution Thresholds

Template matches are interpreted using three bands:

| Match score | Treatment |
|---:|---|
| **< 0.60** | Contributes 0 to final risk score |
| **0.60–0.79** | Moderate contribution |
| **0.80–1.00** | Strong contribution |

This prevents weak correspondence with a scam workflow from automatically becoming strong evidence.

A benign sequence can contain one or more unusual events while still producing a weak template match.

---

## 9. False-Positive Control Through Sequence Logic

The primary false-positive defense is contextual correlation.

### Traditional baseline

The specification defines a transparent baseline using OR logic:

```text
IF (amount > 3× account baseline)
   OR (new device)
   OR (new beneficiary)
   OR (>3 transactions in 10 min)
   OR (unusual hour AND amount z-score > 2.5)
THEN FLAG
ELSE ALLOW
```

This baseline treats individual anomalies as sufficient to generate an alert.

### VYŪH

VYŪH instead asks whether the anomalies form a coherent sequence.

Example hard negative:

```text
Customer changes phones
        +
Pays sister ₹50K
        +
Receives ₹80K salary
```

These events can individually appear unusual. VYŪH evaluates their sequence, context, velocity, and template match before determining the risk action.

The intended result is that legitimate sequences with weak template correspondence remain below the highest-risk threshold.

---

## 10. New-Account Handling

For accounts with **less than seven days of history**, the specification explicitly rejects a blanket default of 0.5.

Instead:

> **Use signal-specific defaults; lack of history does not itself imply suspiciousness.**

The locked specification does not define the exact numeric default for each signal. Those values should therefore be treated as an implementation decision requiring explicit documentation and validation.

---

## 11. Risk Score → Policy Mapping

After signal extraction and template matching, the weighted risk score is passed to a separate policy mapper.

| Risk score | Action |
|---:|---|
| **0.00–0.29** | `ALLOW` |
| **0.30–0.59** | `SOFT_PROMPT` |
| **0.60–0.79** | `STEP_UP_VERIFY` |
| **0.80–1.00** | `HOLD_FOR_REVIEW` |

### MVP safety boundary

**There is no `BLOCK` action in the scoring engine.**

The highest automated action is `HOLD_FOR_REVIEW`.

The architecture separates:

```text
Signal Extraction
       ↓
Risk Scoring
       ↓
Policy Mapping
       ↓
HOLD_FOR_REVIEW
       ↓
Human Review
```

The scoring engine cannot directly call the transaction gateway.

---

## 12. Evidence Generation

Every scored sequence should produce an evidence representation that allows the analyst to understand why the sequence received its risk score.

The MVP specification expects the evidence output to contain the information necessary to review:
- Case ID
- Risk score
- Signal contributions
- Event timeline
- Template match
- Resulting policy action

The evidence card is an explanation layer; it is not itself the decision engine.

---

## 13. Human Feedback

After review, analyst outcomes are recorded for future calibration and error analysis.

The specified feedback fields are:
- `case_id`
- `decision`
- `risk_score`
- `template`
- `signal_scores`
- `analyst_id`
- `timestamp`
- `reason`

Supported analyst decisions include:
- `RELEASE`
- `ESCALATE`
- `FALSE_POSITIVE`

These labels are intended for offline threshold calibration, error analysis, and future model updates.

**Online retraining is explicitly out of scope for the MVP.**

---

## 14. Canonical T1 Detection Example

The locked specification defines a canonical SIM/device takeover sequence:

| Time | Event |
|---|---|
| 10:00 | Normal transaction — ₹1,200, old device, existing beneficiary |
| 10:02 | New device login |
| 10:05 | New beneficiary added |
| 10:06 | ₹48,000 transfer to new beneficiary |
| 10:08 | ₹15,000 rapid transfer |

Expected demonstration output:

```text
Template: T1
Risk: approximately 0.87
Action: HOLD_FOR_REVIEW
```

**Important:** the specification explicitly requires the actual score to be produced by the scoring engine rather than hardcoded.

---

## 15. Detection Output Contract

The intended scoring interface is:

```python
def score_sequence(events: list[dict]) -> dict:
    # returns: risk_score, action, signals, template, evidence
```

The MVP API is expected to expose this scoring capability through:

```text
POST /score
```

The response is expected to expose:
- `risk_score`
- `action`
- `signals`
- `template`
- `evidence`

This is the documented MVP contract; exact request/response schemas should be defined when implementation begins.

---

## 16. Validation Requirements

Detection logic is intended to be evaluated against the synthetic datasets defined in the project specification.

Target metrics are:

| Metric | Target |
|---|---:|
| Precision | ≥ 80% |
| Recall | ≥ 80% |
| F1 | ≥ 80% |
| False-positive rate | < 1% |

The primary operational metric is:

**False positives per 1,000 benign sequences.**

Results must be reported as measured values after implementation. Targets must not be presented as achieved performance.

---

## 17. Unit-Test Boundaries

The specification requires unit tests to validate policy-action boundaries.

At minimum, implementation tests should verify that scores at and around each threshold map to the intended action:

```text
0.29 → ALLOW
0.30 → SOFT_PROMPT
0.59 → SOFT_PROMPT
0.60 → STEP_UP_VERIFY
0.79 → STEP_UP_VERIFY
0.80 → HOLD_FOR_REVIEW
```

The test suite should also verify that:
- `BLOCK` is not an available scoring-engine action.
- The scoring engine does not directly call the transaction gateway.
- Weak template matches below 0.60 contribute zero.
- The golden test set is not used for threshold tuning.

---

## 18. Implementation Boundary

The 48-hour MVP stack specified by the project is:

| Layer | MVP technology |
|---|---|
| Core scoring | Python |
| API | FastAPI |
| Database | SQLite |
| ML | scikit-learn / XGBoost |
| Frontend | React / Vite / Tailwind |
| Infrastructure | Docker |

GPU acceleration is not required for the MVP.

The detector should remain modular enough that the scoring function can be replayed directly against the canonical T1 sequence if live integration fails.

---

## 19. Non-Claims

The detection logic document must not be interpreted as evidence that:
- VYŪH has production UPI access.
- The synthetic targets are measured real-world performance.
- The system can detect every scam class.
- The system automatically blocks transactions.
- The illustrative canonical score is guaranteed for every implementation.

Those claims require implementation evidence, measured validation, or additional production integration.

---

## 20. Summary

VYŪH's detection logic is built around one central distinction:

> **An isolated anomaly is not the same thing as a coordinated attack sequence.**

The detector therefore combines temporal reconstruction, behavioral/contextual signals, scam-template matching, weighted scoring, and conservative policy boundaries.

The resulting system is intended to produce **one explainable workflow-level assessment** instead of a collection of disconnected transaction alerts, while preserving human authority over high-risk cases.