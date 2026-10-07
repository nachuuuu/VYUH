# VYŪH Synthetic Data Generator Specification

**Status:** Specification  
**Schema version:** 0.1  
**Purpose:** Define the deterministic and reproducible rules for generating VYŪH's synthetic training, validation, and golden datasets.

---

## 1. Objective

VYŪH uses synthetic data to develop and evaluate sequence-aware scam detection before real-world validation.

The generator must create **workflows, not isolated suspicious transactions**.

Generated data must support:

- sequence construction
- eight-signal extraction
- five-template matching
- weighted risk scoring
- false-positive analysis
- hard-negative testing
- reproducible evaluation
- schema validation

All generated records must conform to `data/schemas/event.schema.json`.

---

## 2. Dataset Composition

The locked project specification defines the following primary synthetic dataset:

| Class | Count | Purpose |
|---|---:|---|
| Benign | 5,000 | Normal customer workflows and hard negatives |
| Scam | 1,000 | Five scam templates |
| **Total** | **6,000** | Development dataset |

Scam allocation:

- 200 cases per template
- T1: 200
- T2: 200
- T3: 200
- T4: 200
- T5: 200

Scam-strength distribution:

- approximately 60% strong cases (`≥ 0.80`)
- approximately 30% moderate cases (`0.60–0.79`)
- approximately 10% noisy cases (`< 0.60`)

These are generation targets, not measured detector performance.

---

## 3. Output Format

The synthetic event layer uses JSONL:

- one event object per line
- UTF-8 encoded JSON
- timestamps in ISO 8601 format with timezone
- synthetic or pseudonymous identifiers only

A workflow consists of multiple event records associated with the same synthetic account and temporal context.

The generator must produce deterministic metadata sufficient to reproduce a dataset version, including the random seed and generator/schema version.

---

## 4. Generation Pipeline

```text
Seed + Configuration
        ↓
Account Profiles
        ↓
Benign Workflow Generation
        ↓
Scam Workflow Generation
        ↓
Scam Noise / Variation
        ↓
Hard-Negative Construction
        ↓
Dataset Split
        ↓
Schema Validation
        ↓
Quality Checks
        ↓
JSONL Dataset
```

Generation and evaluation must remain separate stages.

---

## 5. Synthetic Account Profiles

Benign workflows should be generated from account-specific behavioral profiles rather than from one global distribution.

A profile may capture:

- account age
- normal transaction amounts
- usual transaction frequency
- usual beneficiary behavior
- normal device behavior
- normal session timing
- normal context patterns

The project specification does not prescribe exact probability distributions for every profile feature. Those parameters should therefore remain explicit generator configuration rather than undocumented assumptions.

---

## 6. Benign Workflow Generation

Benign data should represent ordinary activity across diverse account profiles.

Examples include:

- routine outgoing payments
- repeated payments to established beneficiaries
- normal transaction amounts
- normal device usage
- ordinary changes in transaction frequency
- legitimate contextual variation

Benign workflows must not be constructed simply by setting every risk signal to zero.

The generator should contain approximately **5–10% hard negatives** within the benign population.

Hard negatives intentionally contain individually unusual events while remaining benign at the workflow level.

Examples from the project specification include:

- customer changes phones
- customer pays a family member a large amount
- customer receives a salary credit
- multiple unusual events occur on the same day

The sequence should remain distinguishable from a coordinated scam workflow through timing, context, velocity, and template-match behavior.

---

## 7. Scam Workflow Generation

Each scam case begins from one of the five threat templates:

| ID | Template |
|---|---|
| T1 | SIM/Device Takeover + Rapid Transfer |
| T2 | Remote-Access App + Unauthorized Transfer |
| T3 | Phishing/Smishing + Credential Compromise |
| T4 | Vishing/Fake Support + Collect Request |
| T5 | Mule Account + Rapid Dispersal |

The generator should preserve the causal ordering of the selected workflow while allowing controlled variation.

Because the current v0.1 event schema does not explicitly represent remote-access activity, credential compromise, or collect requests, T2–T4 generation must distinguish between:

1. the conceptual threat workflow, and
2. the normalized events actually emitted into the current dataset.

No unsupported event types should be silently invented.

---

## 8. T1 Generation Parameters

The specification provides explicit T1 synthetic parameters:

| Parameter | Range / rule |
|---|---|
| Account age | 30–1000 days |
| Device change → login | 0–2 minutes |
| Login → beneficiary | 1–5 minutes |
| Beneficiary → transfer | 1–5 minutes |
| Amount multiplier | 1.5–4.0× normal |
| Transfers | 1–2 |

These parameters should remain configurable rather than hard-coded into the generator implementation.

---

## 9. Scam Noise and Variation

Not every scam case should be a perfect template match.

Controlled noise may include:

- missing precursor events
- delayed events
- amounts closer to the account's normal range
- benign transactions mixed into the sequence
- timing jitter
- different event ordering where the workflow remains plausible

Noise must not destroy the ground-truth label.

The approximately 10% noisy scam population is intended to create weak-template and boundary cases rather than obvious clean positives.

---

## 10. Temporal Windows

Generated workflows must respect VYŪH's temporal model:

| Window | Use |
|---|---|
| 10 minutes | Primary sequence detection |
| 60 minutes | Velocity/context analysis |
| Rolling 90 days | Behavioral baseline |

Events outside the primary 10-minute sequence may still be relevant to the 60-minute context or 90-day account baseline.

The generator must therefore be capable of producing both local workflow events and historical account activity.

---

## 11. Template Matching

The generator should preserve enough structure for the detector to calculate:

```text
TemplateMatch =
0.70 × event_coverage
+ 0.20 × temporal_consistency
+ 0.10 × contextual_consistency
```

Threshold behavior:

- `< 0.60` → contributes 0
- `0.60–0.79` → moderate contribution
- `0.80–1.00` → strong contribution

The generator must not directly write a template score into the event records.

The detector calculates the score from generated events.

---

## 12. Ground Truth

Ground truth belongs to the generated case/workflow metadata or dataset manifest, not to individual event fields unless explicitly required by the event schema.

At minimum, the generation process must preserve:

- benign/scam class
- scam template where applicable
- generation configuration/version
- random seed or reproducibility identifier
- dataset split

Ground truth must remain available for evaluation while avoiding leakage into detector input features.

---

## 13. Dataset Splits

The specification defines:

- **Development/validation:** 3,000 benign + 500 scam
- **Golden evaluation:** 2,000 benign + 500 scam

The golden set must be held out and evaluated once.

Golden data must be frozen before threshold tuning or final detector calibration.

---

## 14. Leakage Prevention

The generator and split process must prevent information leakage across evaluation boundaries.

Controls include:

1. Split accounts or account identities before deriving account-specific histories.
2. Do not copy or mutate the same workflow into multiple splits.
3. Do not use golden-set outcomes to tune thresholds.
4. Freeze golden data before final calibration.
5. Keep ground-truth labels outside detector input fields.
6. Ensure historical events for an account do not cross split boundaries in a way that leaks target information.

Exact implementation details should be defined when the generator is implemented.

---

## 15. New Accounts

Accounts with less than seven days of history require signal-specific defaults.

Do not use a blanket `0.5` value for all signals.

Lack of history must not itself be interpreted as suspicious behavior.

The generator should include new-account cases so this behavior can be tested explicitly.

---

## 16. Schema Validation

Every generated event must validate against:

`data/schemas/event.schema.json`

Invalid events should be rejected or quarantined rather than silently repaired.

Validation should check:

- required fields
- event type
- timestamp format
- transaction structure
- identifier presence
- numeric types
- prohibited real-world customer information

---

## 17. Quality Checks

Every generated dataset version should report at least:

- total event count
- total workflow/case count
- benign count
- scam count
- scam count by template
- strong/moderate/noisy distribution
- hard-negative count
- schema validation failures
- duplicate identifiers
- temporal ordering violations
- split leakage checks

Quality checks are generation safeguards, not model evaluation metrics.

---

## 18. Evaluation Metrics

The detector is evaluated separately from generation.

Required validation metrics:

- precision
- recall
- F1
- false-positive rate
- false positives per 1,000 benign cases
- confusion matrix

Project targets:

- precision ≥ 80%
- recall ≥ 80%
- F1 ≥ 80%
- false-positive rate < 1%
- false positives per 1,000 benign < 10

These are target thresholds, not achieved results.

---

## 19. Reproducibility

A dataset must be reproducible from:

- generator version
- schema version
- configuration version
- random seed
- dataset split definition

Changing any generation parameter should produce a new dataset version.

Generated datasets should not silently change after evaluation.

---

## 20. Privacy Boundary

The synthetic generator must never require real customer data.

It must not generate realistic personal identifiers merely for appearance.

Do not generate or store:

- real bank-account numbers
- real UPI IDs
- real phone numbers
- real email addresses
- customer names
- authentication secrets
- unnecessary precise location information

Identifiers should be synthetic and non-resolving.

---

## 21. Implementation Boundary

This document specifies **what the generator must do**, not how the generator must be implemented.

The implementation may use Python or another suitable toolchain, provided that it preserves:

- the event schema
- dataset composition
- threat-template semantics
- temporal constraints
- ground-truth integrity
- leakage controls
- reproducibility
- validation requirements

---

## 22. Acceptance Criteria

The generator specification is considered satisfied when an implementation can:

- generate the required 6,000-case development population
- produce 200 scam cases per template
- generate benign workflows with hard negatives
- generate strong, moderate, and noisy scam cases
- preserve temporal constraints
- validate every emitted event against the schema
- produce deterministic output from a fixed seed
- create leakage-safe development and golden splits
- freeze and reproduce the golden set
- report generation-quality checks
- keep ground truth separate from detector inputs

---

## 23. Core Principle

> **Generate workflows, not isolated suspicious transactions.**

The generator exists to test whether VYŪH can distinguish coordinated scam sequences from legitimate behavior that merely contains individual anomalies.