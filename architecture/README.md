# VYŪH Architecture

## Purpose

This directory documents the architecture of VYŪH as a research and engineering system for temporal risk intelligence in digital payments.

VYŪH identifies suspicious payment workflows by evaluating related events over time rather than treating each transaction as an isolated decision.

The architecture separates event normalization, temporal session construction, signal extraction, scam-workflow matching, risk scoring, policy mapping, evidence generation, and human review.

## System flow

```text
Raw Events → Event Normalization → Session Construction
          → 8 Signal Extractors → 5 Template Matchers
          → Weighted Risk Score → Policy Mapper
          → Evidence Card → Human Review → Label + Reason
```

The scoring engine and policy layer are intentionally separate. The scoring engine produces a risk assessment; the policy layer maps that assessment to an action.

VYŪH does not automatically issue a transaction BLOCK decision in the current architecture.

## Architecture layers

### 1. Event ingestion and normalization

The input boundary accepts normalized payment-related events represented by the VYŪH event schema.

The current schema represents login/authentication events, device changes, beneficiary activity, payment initiation, transfers, transaction context, beneficiary context, authentication state, and destination/network-risk context.

Normalization provides a consistent representation to downstream detection components. VYŪH does not claim that this schema is a universal production UPI event standard.

See [`data/schemas/event-schema.md`](../data/schemas/event-schema.md).

### 2. Session construction

VYŪH groups related events into temporal sequences.

- **10 minutes** — primary sequence window
- **60 minutes** — broader velocity and contextual analysis
- **90 days** — rolling behavioural baseline

Session construction is an analytical boundary. It does not imply a particular production banking session implementation.

### 3. Signal extraction

The detection layer extracts eight normalized signals:

| Signal | Purpose | Weight |
|---|---|---:|
| S1 | Behavioural deviation | 20% |
| S2 | Device/authentication change | 20% |
| S3 | Amount anomaly | 15% |
| S4 | Beneficiary novelty | 15% |
| S5 | Transaction velocity | 10% |
| S6 | Session/context risk | 10% |
| S7 | Scam-workflow template match | 5% |
| S8 | Destination/network risk | 5% |

See [`docs/detection-logic.md`](../docs/detection-logic.md) for signal definitions and implementation boundaries.

### 4. Scam-workflow matching

The current research model defines five workflow templates:

1. T1 — SIM/Device Takeover + Rapid Transfer
2. T2 — Remote-Access App + Unauthorized Transfer
3. T3 — Phishing/Smishing + Credential Compromise
4. T4 — Vishing/Fake Support + Collect Request
5. T5 — Mule Account + Rapid Dispersal

A template score combines event coverage, temporal consistency, and contextual consistency:

```text
T = 0.70 × event_coverage
  + 0.20 × temporal_consistency
  + 0.10 × contextual_consistency
```

Template matches below 0.60 do not contribute as positive template evidence.

The distinction between a real-world scam workflow and the events currently observable in the normalized schema is documented in [`research/scam-workflows.md`](../research/scam-workflows.md).

### 5. Risk scoring

The eight signals are combined using the specified weighted model:

```text
Risk Score = 0.20*S1 + 0.20*S2 + 0.15*S3 + 0.15*S4
           + 0.10*S5 + 0.10*S6 + 0.05*S7 + 0.05*S8
```

The resulting score is normalized to the 0–1 range.

See [`docs/risk-scoring.md`](../docs/risk-scoring.md).

### 6. Policy mapping

| Risk score | Action |
|---:|---|
| 0.00–0.29 | ALLOW |
| 0.30–0.59 | SOFT_PROMPT |
| 0.60–0.79 | STEP_UP_VERIFY |
| 0.80–1.00 | HOLD_FOR_REVIEW |

There is no automatic BLOCK action in the current VYŪH architecture.

Keeping policy separate from scoring prevents the risk engine from directly controlling a transaction gateway.

### 7. Evidence and human review

A high-risk result is accompanied by an evidence representation explaining the contributing signals, relevant temporal sequence, template evidence, score, and resulting policy action.

The architecture includes a human-review boundary after policy mapping. A reviewer can associate a label and reason with the reviewed sequence.

Feedback is treated as controlled evaluation and future calibration data; it is not used for unrestricted online model retraining.

## Trust boundaries

```text
External / source events
        ↓
Normalization boundary
        ↓
Detection boundary
        ↓
Policy boundary
        ↓
Evidence + human-review boundary
```

Each boundary should validate the assumptions of the component receiving its output.

Security, privacy, access control, data minimization, and review safeguards are documented in [`docs/security-privacy.md`](../docs/security-privacy.md).

## Data architecture

VYŪH currently follows a synthetic-first development model.

```text
Generation configuration
        ↓
Synthetic workflow generation
        ↓
Schema validation
        ↓
Quality checks
        ↓
Development / validation data
        ↓
Detection and calibration

Frozen golden set
        ↓
One-time evaluation
```

The synthetic dataset specification defines 5,000 benign workflows and 1,000 scam workflows, with 200 scam workflows per template.

The dataset is intended to represent workflows rather than isolated suspicious transactions.

See [`data/README.md`](../data/README.md) and [`data/generator-spec.md`](../data/generator-spec.md).

## Current architectural constraints

The current architecture does not define:

- a production UPI gateway integration
- a universal UPI event standard
- a production destination-risk provider
- final production database/storage architecture
- regulatory retention requirements
- automatic transaction blocking
- production-scale performance guarantees

These are future engineering and validation questions, not assumptions of the current research system.

## Architecture maturity

The current architecture is a documented research and prototype design.

The project roadmap separates specification and research, synthetic-data development, detection implementation, evaluation and calibration, an analyst-facing MVP, robustness research, real-world validation, and production hardening.

See [`docs/roadmap.md`](../docs/roadmap.md).

## Diagrams

Finalized architecture diagrams belong in `architecture/diagrams/`.

Recommended naming:

- `01-system-architecture.png`
- `02-event-processing-pipeline.png`
- `03-session-construction.png`
- `04-signal-extraction.png`
- `05-template-matching.png`
- `06-risk-scoring.png`
- `07-policy-decision.png`
- `08-human-escalation.png`

Diagrams should reflect the written architecture rather than introduce undocumented system behaviour.

## Related documentation

- [`docs/VYUH_Complete_Specification.md`](../docs/VYUH_Complete_Specification.md) — complete system specification
- [`docs/threat-model.md`](../docs/threat-model.md) — threat and attack model
- [`docs/detection-logic.md`](../docs/detection-logic.md) — signal and detection logic
- [`docs/risk-scoring.md`](../docs/risk-scoring.md) — scoring and policy thresholds
- [`docs/security-privacy.md`](../docs/security-privacy.md) — security and privacy boundaries
- [`data/schemas/event-schema.md`](../data/schemas/event-schema.md) — canonical event contract
- [`research/scam-workflows.md`](../research/scam-workflows.md) — workflow/template reference
- [`docs/roadmap.md`](../docs/roadmap.md) — project evolution path