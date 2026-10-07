# VYŪH Data

This directory defines the data layer used by VYŪH.

The current project is **synthetic-data first**. No production banking or UPI customer dataset is assumed to be available. Data structures are therefore designed to support deterministic development, controlled evaluation, reproducibility, and eventual integration with appropriately governed institutional data.

---

## Data Architecture

VYŪH operates on sequences of normalized events rather than isolated transaction records.

The conceptual flow is:

```text
Raw / Synthetic Events
        ↓
Event Normalization
        ↓
Session Construction
        ↓
Signal Extraction
        ↓
Template Matching
        ↓
Risk Scoring
        ↓
Policy + Evidence
```

The canonical event representation should contain only information required by the detection and evaluation pipeline.

---

## Current Dataset Design

The project specification defines an initial synthetic dataset of:

| Dataset | Count | Purpose |
|---|---:|---|
| Benign sequences | 5,000 | Represent legitimate behavioural variation |
| Scam sequences | 1,000 | Represent T1–T5 workflows |
| Scam sequences / template | 200 | Balanced representation across T1–T5 |

The scam dataset is distributed approximately as:

- 60% strong sequences
- 30% moderate sequences
- 10% noisy sequences

The dataset should contain realistic variation rather than repeating one canonical sequence.

---

## Sequence Representation

Synthetic data is represented as **JSONL**, with one event per line.

A sequence therefore consists of multiple temporally ordered events associated with the same logical account/session context.

A future implementation should preserve:

- event ordering
- timestamps
- event type
- account-level context
- device/authentication context where available
- transaction context where applicable
- beneficiary/destination context where applicable
- ground-truth labels
- scenario/template metadata where appropriate

The exact schema belongs in the schemas directory.

---

## Event Categories

The current VYŪH threat model requires event information capable of representing categories such as:

### Account and authentication

- login
- authentication change
- authentication failure
- device change

### Beneficiary

- beneficiary creation
- beneficiary interaction
- beneficiary novelty

### Transaction

- payment initiation
- transfer
- transaction amount
- transaction direction
- transaction timestamp

### Session and context

- session identifier
- device context
- IP/geo context
- unusual-hour context

### Destination

- destination identifier
- destination/network risk context

Not every event will contain every field.

The schema should use explicit event types and optional fields rather than filling unavailable information with fabricated values.

---

## Temporal Windows

The data layer must support the three temporal horizons used by VYŪH:

| Window | Purpose |
|---|---|
| **10 minutes** | Primary sequence construction and rapid workflow detection |
| **60 minutes** | Supporting velocity and contextual analysis |
| **90 days** | Account-specific behavioural baseline |

Synthetic sequences should therefore contain enough historical context to evaluate behavioural deviation where required.

---

## Labels and Ground Truth

Ground truth should describe what the synthetic generator intended to represent, not what the detector predicted.

At minimum, evaluation data should distinguish:

- benign
- T1
- T2
- T3
- T4
- T5

Additional metadata may describe:

- workflow strength
- noise level
- injected variation
- hard-negative status
- generation seed/version

Predicted risk scores, template matches, and policy actions must remain separate from ground-truth labels.

This separation is necessary to avoid evaluation leakage.

---

## Hard Negatives

Approximately 5–10% of benign data should be designed as hard negatives.

Hard negatives are legitimate sequences that contain one or more characteristics associated with scam workflows, such as:

- new-device activity
- new beneficiary creation
- unusually large legitimate payment
- rapid legitimate transfers
- unusual session or network context

Their purpose is to test whether VYŪH can distinguish a suspicious-looking sequence from an actually malicious workflow.

---

## Scam Sequence Variation

Scam sequences should include controlled variation.

The current specification permits:

- missing events
- delayed events
- timing jitter
- amounts closer to normal
- benign events mixed into scam sequences
- altered event ordering

This prevents the detector from learning or encoding only a single idealized sequence.

---

## Benign Data Generation

Benign sequences should be generated from account-specific behavioural profiles rather than from a single global distribution.

A benign account may have its own:

- normal transaction amounts
- transaction frequency
- active hours
- beneficiary patterns
- device patterns
- session characteristics

This is important because behavioural deviation is account-relative.

A behaviour can be unusual for one account and completely normal for another.

---

## Synthetic Data and Privacy

Synthetic data should not contain real customer identifiers.

Where identifiers are needed for relationships within a synthetic sequence, use generated or pseudonymous identifiers such as:

- synthetic account IDs
- synthetic device IDs
- synthetic beneficiary IDs
- synthetic session IDs

Do not place real:

- account numbers
- UPI IDs
- phone numbers
- email addresses
- IP addresses
- personally identifiable information

into the repository unless there is an explicit, documented reason and appropriate authorization.

---

## Evaluation Splits

The project specification defines:

### Validation set

- 3,000 benign sequences
- 500 scam sequences

Used during development and calibration.

### Golden set

- 2,000 benign sequences
- 500 scam sequences

Held out from tuning and evaluated as a final validation set.

The golden set should be frozen before final evaluation.

No thresholds, weights, feature transformations, or rules should be tuned against golden-set results.

---

## Leakage Prevention

Data generation and evaluation must avoid leakage through:

- duplicated sequences
- near-duplicate sequences across splits
- shared scenario instances
- shared generation artefacts that reveal labels
- tuning against the golden set
- using detector predictions as ground truth
- copying template-specific examples directly into evaluation data

When data generation changes materially, the dataset version should change as well.

---

## Reproducibility

Synthetic generation should be deterministic when provided with the same:

- generator version
- configuration
- random seed
- dataset version

A generated dataset should therefore be traceable to the configuration that produced it.

Future generators should record sufficient metadata to reproduce or audit a dataset without storing unnecessary sensitive information.

---

## Schema Evolution

The data schema will evolve as VYŪH moves from synthetic events toward more realistic integration requirements.

Schema changes should:

1. preserve backwards compatibility where practical
2. document breaking changes
3. update affected examples
4. update detection logic when required
5. update evaluation procedures
6. increment the schema version

The repository should not silently change the meaning of an existing field.

---

## Directory Structure

```text
data/
├── README.md
├── schemas/
│   └── ...
└── examples/
    └── ...
```

The schemas directory defines machine-readable data structures.

The examples directory contains small, human-readable synthetic scenarios used for documentation, development, testing, and deterministic demonstrations.

Large generated datasets should not be committed to the repository by default.

---

## Data Quality Requirements

Before data is used for evaluation, verify:

- timestamps are valid and ordered where required
- required event fields are present
- event types are valid
- identifiers are internally consistent
- labels match generator intent
- template metadata is valid
- no evaluation leakage is present
- no real customer data is included
- dataset version and generation configuration are recorded

---

## Current Boundaries

The current data layer does **not** claim:

- access to real UPI transaction streams
- representative production fraud prevalence
- that synthetic distributions match real customer populations
- that synthetic detection results transfer directly to production
- that all relevant UPI event types are currently represented

These require appropriately governed real-world data and further research.

---

## Principle

> **Generate workflows, not isolated suspicious transactions.**

The data layer exists to preserve the temporal relationships that make VYŪH a sequence-oriented risk engine rather than a collection of independent transaction rules.