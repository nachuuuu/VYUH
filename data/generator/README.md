# VYŪH Synthetic Data Generator

**Status:** Planned implementation  
**Specification:** `data/generator-spec.md`  
**Schema:** `data/schemas/event.schema.json`  
**Manifest schema:** `data/schemas/dataset-manifest.schema.json`

---

## 1. Purpose

This directory will contain the implementation of the VYŪH synthetic event and workflow generator.

The generator converts explicit configuration and a reproducible random seed into:

- synthetic account profiles
- benign workflows
- hard-negative workflows
- scam workflows
- controlled scam variations/noise
- schema-valid event records
- dataset splits
- dataset manifests
- generation-quality reports

The generator is a research and engineering component. It does not perform fraud detection itself.

---

## 2. Design Boundary

```text
Generator
   ↓
Synthetic Events
   ↓
Schema Validation
   ↓
Dataset + Manifest
   ↓
Detection Engine
```

The generator must not:

- calculate the final VYŪH risk score
- decide ALLOW/SOFT_PROMPT/STEP_UP_VERIFY/HOLD_FOR_REVIEW
- tune detector thresholds using the golden set
- embed ground-truth labels into detector input events
- introduce unsupported event types silently

---

## 3. Planned Module Responsibilities

Implementation modules should remain separated by responsibility.

| Module | Responsibility |
|---|---|
| `config` | Generation parameters and versioning |
| `profiles` | Synthetic account behavior profiles |
| `benign` | Benign workflow generation |
| `scam` | Scam-template workflow generation |
| `noise` | Controlled scam variation and noise |
| `splits` | Leakage-safe dataset splitting |
| `schema` | Event-schema validation |
| `manifest` | Dataset provenance and manifest creation |
| `quality` | Generation-level quality checks |
| `cli` | Command-line generation entry point |

Exact module names may change during implementation if the same separation of concerns is preserved.

---

## 4. Inputs

The implementation should accept explicit:

- generation configuration
- random seed
- schema version
- generator version
- dataset version
- output location

Configuration should control generation parameters rather than burying them as unexplained constants in the implementation.

---

## 5. Outputs

A successful generation run should produce, at minimum:

```text
dataset/
├── events.jsonl
├── manifest.json
└── quality-report.json
```

The exact artifact layout can evolve during implementation.

`manifest.json` must conform to:

`data/schemas/dataset-manifest.schema.json`

Every event in `events.jsonl` must conform to:

`data/schemas/event.schema.json`

---

## 6. Reproducibility

Given identical:

- generator version
- schema version
- configuration
- random seed

the generator should produce the same logical dataset.

If environmental or implementation details prevent byte-for-byte reproduction, the limitation must be documented rather than hidden.

---

## 7. Generation Order

The intended implementation flow is:

```text
Load configuration
      ↓
Initialize deterministic RNG
      ↓
Create account profiles
      ↓
Generate benign workflows
      ↓
Generate scam workflows
      ↓
Apply controlled variation/noise
      ↓
Construct hard negatives
      ↓
Assign leakage-safe splits
      ↓
Validate events
      ↓
Run quality checks
      ↓
Write JSONL + manifest
      ↓
Freeze golden set when requested
```

---

## 8. Template Boundary

The generator must implement the five project templates:

- T1 — SIM/Device Takeover + Rapid Transfer
- T2 — Remote-Access App + Unauthorized Transfer
- T3 — Phishing/Smishing + Credential Compromise
- T4 — Vishing/Fake Support + Collect Request
- T5 — Mule Account + Rapid Dispersal

T2–T4 contain threat-model steps that are not currently explicit event types in schema v0.1.

The implementation must therefore distinguish conceptual workflow state from emitted normalized events and must not fabricate unsupported event types.

---

## 9. Validation Boundary

Schema validation is mandatory before generated events enter a dataset.

Quality validation is separate from schema validation.

### Schema validation

Answers:

> Is this event structurally valid?

### Quality validation

Answers:

> Is this generated dataset internally consistent and suitable for evaluation?

Neither validation layer replaces detector evaluation.

---

## 10. Testing Strategy

The generator should eventually include tests for:

- deterministic generation from a fixed seed
- event-schema compliance
- required dataset counts
- template allocation
- strong/moderate/noisy distribution
- hard-negative generation
- temporal constraints
- split leakage
- duplicate identifiers
- manifest validity
- golden-set freezing

Tests should include both normal and intentionally invalid configurations.

---

## 11. Current Implementation Status

At this stage the repository contains the generator specification and machine-readable contracts, but not the generator implementation.

Implementation should begin only after the interfaces defined by these documents are stable enough to test.

---

## 12. Related Files

- `data/generator-spec.md` — generator requirements
- `data/synthetic-data-manifest.md` — manifest contract
- `data/schemas/event-schema.md` — event semantics
- `data/schemas/event.schema.json` — event validation
- `data/schemas/dataset-manifest.schema.json` — manifest validation
- `data/examples/README.md` — fixture documentation

---

## 13. Principle

> **Generation is an experiment input pipeline, not the detector.**