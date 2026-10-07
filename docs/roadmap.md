# VYŪH Roadmap

## Purpose

This roadmap describes the planned evolution of VYŪH from a research-defined detection system into a validated, deployable risk-intelligence platform.

It is a project roadmap, not a competition or submission timeline. Each stage separates work that is already specified from work that requires implementation, empirical validation, or access to real institutional data.

---

## Current State

VYŪH currently has a defined:

- threat model covering five canonical UPI scam workflows
- temporal detection architecture
- eight-signal risk model
- five template-matching framework
- risk-scoring and policy boundaries
- synthetic-data specification
- security and privacy principles
- validation methodology and acceptance targets

The next major step is implementation and measurement.

---

## Phase 1 — Research and Specification

**Status:** Defined

Establish the conceptual and technical foundation of VYŪH.

### Work

- Research scam and fraud workflows
- Define threat actors, assets, and trust boundaries
- Formalize T1–T5 scam templates
- Define event normalization and session construction
- Define the eight detection signals
- Define temporal windows
- Define template matching
- Define risk scoring and policy mapping
- Document security and privacy constraints

### Exit condition

The detection architecture and its assumptions are sufficiently specified to support reproducible implementation.

---

## Phase 2 — Synthetic Data Generation

**Status:** Specified; implementation pending

Build a controlled dataset for development and evaluation.

### Work

- Generate 5,000 benign sequences
- Generate 1,000 scam sequences
- Generate 200 scam sequences per template
- Represent events as JSONL
- Generate account-specific benign behaviour
- Introduce 5–10% hard negatives
- Generate strong, moderate, and noisy scam sequences
- Add realistic temporal and behavioural noise
- Preserve ground-truth labels
- Prevent train/validation leakage

### Exit condition

A reproducible dataset exists that can exercise both normal behaviour and the five defined scam workflows without relying on real customer data.

---

## Phase 3 — Detection Engine

**Status:** Architecture defined; implementation pending

Implement the deterministic VYŪH scoring pipeline.

### Work

1. Event normalization
2. Session construction
3. Signal extraction
4. Temporal template matching
5. Weighted risk scoring
6. Policy mapping
7. Evidence generation

### Core interface

The initial implementation should expose:

`score_sequence(events: list[dict]) -> dict`

and a service endpoint:

`POST /score`

### Exit condition

The engine produces a reproducible risk score, matched template information, policy action, and supporting evidence for a supplied event sequence.

---

## Phase 4 — Evaluation and Calibration

**Status:** Defined; implementation pending

Measure whether VYŪH actually performs as intended.

### Work

- Evaluate precision
- Evaluate recall
- Evaluate F1
- Measure false-positive rate
- Measure false positives per 1,000 benign sequences
- Measure detection latency
- Compare against the baseline detector
- Perform threshold analysis
- Perform signal ablation analysis
- Inspect hard-negative failures
- Review false-positive and false-negative cases

### Target metrics

The current specification defines the following targets:

| Metric | Target |
|---|---:|
| Precision | ≥ 80% |
| Recall | ≥ 80% |
| F1 | ≥ 80% |
| False-positive rate | < 1% |
| False positives / 1,000 benign | < 10 |

The primary operational metric is **false positives per 1,000 benign sequences**.

These are validation targets, not measured results.

### Exit condition

Performance is measured on held-out data and the causes of important errors are documented.

---

## Phase 5 — Analyst-Facing MVP

**Status:** Planned

Expose the detection engine through a usable workflow for investigation and review.

### Work

- FastAPI service
- Evidence dashboard
- Case identifiers
- Risk score display
- Eight signal contributions
- Event timeline
- Template match explanation
- RELEASE / ESCALATE / FALSE_POSITIVE review actions
- SQLite-backed feedback
- Deterministic replay for demonstrations and regression testing

### Design boundary

The scoring engine remains separate from transaction execution. The current system does not automatically block transactions.

### Exit condition

An analyst can submit or replay a sequence, inspect why it was scored as risky, and record a review outcome.

---

## Phase 6 — Robustness and Research

**Status:** Future research

Test whether the approach remains useful when scam workflows are incomplete, noisy, or deliberately altered.

### Work

- Adversarial sequence variation
- Missing-event testing
- Timing jitter
- Benign-event interleaving
- Event-order variation
- Amount variation
- Template mutation
- Hard-negative expansion
- Signal ablation
- Threshold sensitivity analysis
- Robustness evaluation across account profiles

### Exit condition

Failure modes are characterized and the limits of temporal template matching are documented.

---

## Phase 7 — Real-World Validation

**Status:** Requires institutional data and partnerships

Move beyond synthetic evaluation without treating synthetic performance as evidence of production effectiveness.

### Work

- Define institution-specific event schemas
- Establish lawful data-access mechanisms
- Validate feature availability
- Evaluate on representative historical data
- Recalibrate thresholds using appropriate validation procedures
- Measure operational false-positive burden
- Study analyst-review outcomes
- Assess drift across customer populations and time

### Exit condition

The system has evidence from appropriately governed real-world data demonstrating where the approach works, where it fails, and what calibration is required.

---

## Phase 8 — Production Hardening

**Status:** Future

Address the engineering and governance requirements of an operational deployment.

### Work

- Service reliability and scaling
- Authentication and authorization
- Secrets management
- Audit logging
- Monitoring and alerting
- Data-retention controls
- Model and rule versioning
- Change management
- Incident response
- Access governance
- Performance testing
- Resilience testing
- Integration with institutional fraud-review systems

### Exit condition

VYŪH has documented operational controls and measurable reliability appropriate to its deployment environment.

---

## Cross-Cutting Principles

These principles apply across every phase.

### 1. Sequence over isolation

VYŪH evaluates relationships between events over time rather than treating a single transaction as sufficient evidence of fraud.

### 2. Explainability over opaque decisions

Every risk decision should expose the signals, temporal evidence, and template contribution that influenced it.

### 3. Human review over irreversible automation

The current policy boundary does not include automatic transaction blocking. High-risk cases are escalated for review.

### 4. Validation over assumption

Synthetic performance is useful for development, but it does not establish production effectiveness.

### 5. Privacy by design

Development should minimize sensitive data, use pseudonymous identifiers where possible, and maintain clear separation between data required for detection and data required for investigation.

### 6. Reproducibility

Datasets, scoring logic, evaluation procedures, and configuration changes should be versioned so that results can be reproduced and compared.

---

## What VYŪH Does Not Claim

The roadmap does not imply that VYŪH currently:

- detects every UPI scam
- has been validated on real banking or UPI transaction data
- provides production-grade fraud detection
- automatically blocks transactions
- guarantees a specific reduction in fraud losses
- replaces institutional fraud teams
- satisfies regulatory or banking deployment requirements

Those claims require evidence beyond the current project specification.

---

## Definition of Progress

VYŪH should advance from one phase to the next based on evidence, not simply completion of implementation tasks.

A completed component is considered mature only when its:

- behaviour is documented
- assumptions are explicit
- tests exist where applicable
- evaluation results are measurable
- limitations are recorded

The long-term objective is not merely to produce a fraud score. It is to develop a reproducible, explainable temporal risk-intelligence system that can be evaluated rigorously and integrated responsibly.
