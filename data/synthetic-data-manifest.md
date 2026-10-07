# VYŪH Synthetic Dataset Manifest

**Status:** Specification  
**Purpose:** Define the metadata contract for every generated VYŪH synthetic dataset version.

---

## 1. Purpose

The dataset manifest records how a synthetic dataset was produced and how it should be interpreted.

It exists separately from the event records so that:

- detector inputs remain free of generation metadata
- datasets can be reproduced
- dataset versions can be compared
- evaluation splits remain explicit
- quality checks are auditable
- the golden set can be frozen and identified

---

## 2. Manifest Identity

Every dataset version should have a unique manifest containing:

| Field | Purpose |
|---|---|
| `dataset_id` | Human-readable dataset identifier |
| `dataset_version` | Immutable dataset version |
| `generator_version` | Generator implementation/specification version |
| `schema_version` | Event schema version used for validation |
| `config_version` | Generation configuration version |
| `random_seed` | Seed required for deterministic reproduction |
| `created_at` | Dataset creation timestamp |
| `status` | Dataset lifecycle state |

Recommended lifecycle states:

- `DRAFT`
- `VALIDATED`
- `FROZEN`
- `RETIRED`

---

## 3. Dataset Composition

The manifest must record the actual generated counts rather than assuming the target counts were achieved.

Required composition metadata:

- total workflows/cases
- total events
- benign workflows
- scam workflows
- T1 workflows
- T2 workflows
- T3 workflows
- T4 workflows
- T5 workflows
- hard-negative count
- strong scam count
- moderate scam count
- noisy scam count

The locked project targets are:

- 5,000 benign
- 1,000 scam
- 200 scam cases per template
- approximately 60% strong
- approximately 30% moderate
- approximately 10% noisy

Targets must not be recorded as achieved results unless the generated dataset actually satisfies them.

---

## 4. Dataset Splits

The manifest must identify every split included in the dataset version.

Current project split specification:

| Split | Benign | Scam | Purpose |
|---|---:|---:|---|
| Development/validation | 3,000 | 500 | Development and validation |
| Golden | 2,000 | 500 | Frozen final evaluation |

The manifest should record the actual counts and split identifiers.

Each workflow/case must belong to exactly one evaluation split.

---

## 5. Golden Dataset State

The golden set has a special lifecycle requirement.

Before threshold tuning or final detector calibration:

1. Generate the golden set.
2. Validate the golden set.
3. Freeze the golden set.
4. Record its manifest/version identity.
5. Do not use golden outcomes to tune the detector.

A frozen golden manifest should include a stable dataset fingerprint or equivalent immutable identifier.

---

## 6. Reproducibility Metadata

A dataset should be reproducible from its recorded generation inputs.

At minimum, preserve:

- generator version
- schema version
- configuration version
- random seed
- split definition
- template allocation
- generation timestamp

Where practical, also record cryptographic fingerprints for generated dataset artifacts.

---

## 7. Schema Validation Results

The manifest must record schema-validation outcomes.

Recommended fields:

- events generated
- events validated
- validation failures
- quarantined events
- validation status

Expected invariant:

`validated_events + quarantined_events = generated_events`

unless the generator explicitly records another disposition.

Invalid events must not silently enter the evaluation dataset.

---

## 8. Quality-Control Results

The manifest should record generation-level quality checks, including:

- duplicate event identifiers
- duplicate workflow identifiers
- temporal ordering violations
- invalid event types
- missing required fields
- split leakage checks
- prohibited real-world identifiers
- unexpected class counts
- unexpected template counts

Each check should have an explicit result such as:

- `PASS`
- `FAIL`
- `NOT_RUN`

---

## 9. Ground-Truth Metadata

Ground truth is required for evaluation but must not be exposed as an input feature to the detector.

The manifest should record the labeling scheme used by the dataset.

At workflow/case level, ground truth may identify:

- `BENIGN`
- `SCAM`
- scam template for scam cases

The event schema itself should not be modified merely to carry evaluation labels.

---

## 10. Generator Configuration

The manifest should identify the configuration used for generation.

Configuration may control:

- account-profile distributions
- transaction amount distributions
- workflow timing ranges
- beneficiary behavior
- device behavior
- scam-template parameters
- noise parameters
- hard-negative rate
- split allocation

Configuration changes must result in a new dataset version.

---

## 11. Privacy and Synthetic-Data Declaration

Every dataset manifest should explicitly declare that the dataset is synthetic.

Recommended declaration:

> This dataset contains synthetic event data generated for VYŪH research and engineering. It must not contain real customer identifiers, payment credentials, or authentication secrets.

The manifest should also record whether privacy validation was executed.

---

## 12. Evaluation Boundary

The manifest describes the dataset.

It does not contain detector performance results unless those results are stored as a separate evaluation artifact referencing this exact dataset version.

This separation prevents dataset metadata from being confused with model performance.

Performance reports should reference:

- dataset ID
- dataset version
- split
- detector version
- configuration/calibration version

---

## 13. Example Manifest Shape

The following is illustrative metadata structure, not the final machine-readable manifest schema:

```json
{
  "dataset_id": "vyuh-synthetic",
  "dataset_version": "0.1.0",
  "generator_version": "0.1.0",
  "schema_version": "0.1",
  "config_version": "0.1.0",
  "random_seed": 42,
  "status": "VALIDATED",
  "composition": {
    "benign": 5000,
    "scam": 1000,
    "T1": 200,
    "T2": 200,
    "T3": 200,
    "T4": 200,
    "T5": 200
  },
  "splits": {
    "development": {
      "benign": 3000,
      "scam": 500
    },
    "golden": {
      "benign": 2000,
      "scam": 500
    }
  }
}
```

The actual machine-readable manifest format should be finalized when dataset generation is implemented.

---

## 14. Versioning Rules

A new dataset version is required when any of the following changes:

- generator logic
- generator configuration
- event schema
- template parameters
- class allocation
- split allocation
- noise rules
- hard-negative generation

Re-running the same generator, configuration, schema, and seed should reproduce the same dataset contents, subject to explicitly documented environmental constraints.

---

## 15. Acceptance Criteria

A dataset manifest implementation is acceptable when it can answer:

1. What dataset is this?
2. Which generator produced it?
3. Which event schema validated it?
4. Which configuration produced it?
5. Which random seed was used?
6. How many benign and scam workflows exist?
7. How are scams distributed across T1–T5?
8. Which workflows belong to the golden set?
9. Was the golden set frozen before tuning?
10. Did schema and leakage checks pass?
11. Can the dataset be reproduced?

---

## 16. Core Principle

> **A dataset without provenance is not a reproducible experiment.**