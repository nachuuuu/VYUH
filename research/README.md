# VYŪH Research

This directory contains the research foundation behind VYŪH.

The purpose of the research layer is to connect the system's threat model, scam workflows, detection assumptions, and evaluation methodology to documented evidence and reproducible reasoning.

VYŪH is intended to be developed as a research and engineering project. Research therefore remains part of the system's lifecycle rather than being limited to a single submission or demonstration.

---

## Research Areas

### 1. Threat Research

Documents the threat environment relevant to VYŪH, including:

- scam mechanisms
- attacker behaviour
- account and device compromise patterns
- payment-flow abuse
- mule-account behaviour
- operational assumptions
- known limitations in available evidence

See [threat-research.md](./threat-research.md).

### 2. Scam Workflow Analysis

Documents the temporal workflows that VYŪH is designed to recognize.

The current system specification defines five canonical templates:

- **T1** — SIM/Device Takeover + Rapid Transfer
- **T2** — Remote-Access App + Unauthorized Transfer
- **T3** — Phishing/Smishing + Credential Compromise
- **T4** — Vishing/Fake Support + Collect Request
- **T5** — Mule Account + Rapid Dispersal

The objective is to represent scams as sequences of related events rather than isolated suspicious transactions.

See [scam-workflows.md](./scam-workflows.md).

### 3. Detection-Pattern Research

Research findings should inform, but not silently modify, the documented detection architecture.

The current VYŪH detection model uses:

- behavioural deviation
- device/authentication changes
- amount anomalies
- beneficiary novelty
- transaction velocity
- session/context risk
- temporal template matching
- destination/network risk

The implementation specification for these signals belongs in [../docs/detection-logic.md](../docs/detection-logic.md) and [../docs/risk-scoring.md](../docs/risk-scoring.md).

Research may propose changes to these mechanisms, but proposed changes should be explicitly identified as proposals until they are incorporated into the project specification.

---

## Evidence and References

Research claims should be traceable to an identifiable source wherever practical.

[references.md](./references.md) is intended to maintain the project's external references and source notes.

For important findings, the research record should distinguish between:

| Classification | Meaning |
|---|---|
| **Observed** | Directly supported by a source or measured experiment |
| **Specified** | Defined by the VYŪH project specification |
| **Hypothesis** | A proposition that requires validation |
| **Inference** | A conclusion derived from available evidence |
| **Implementation decision** | A deliberate engineering choice |
| **Open question** | An issue requiring further investigation |

This prevents assumptions from being presented as measured facts.

---

## Research → Engineering Flow

Research should feed the engineering process through an explicit chain:

```text
External Evidence
       ↓
Threat / Workflow Finding
       ↓
VYŪH Hypothesis or Assumption
       ↓
Detection Design
       ↓
Implementation
       ↓
Controlled Evaluation
       ↓
Result
       ↓
Specification / Roadmap Update
```

A research finding should not automatically become a production rule.

It should first be translated into a testable detection hypothesis, implemented where appropriate, and evaluated against benign and malicious behaviour.

---

## Relationship to the Rest of the Repository

| Area | Role |
|---|---|
| `docs/` | Formal system specification and engineering decisions |
| `research/` | Evidence, threat research, workflow analysis, and hypotheses |
| `data/` | Dataset definitions, schemas, and example data |
| `architecture/` | System architecture and diagrams |
| `presentation/` | Project communication and presentation material |
| `submission/` | Submission-specific artifacts |
| `team/` | Ownership and contribution information |

The separation is intentional.

**Research explains why. Documentation defines what. Engineering implements how. Evaluation determines whether it works.**

---

## Research Standards

Research added to this repository should:

1. Identify the source or evidence basis.
2. Separate facts from inference.
3. Avoid unsupported quantitative claims.
4. State important assumptions.
5. Record uncertainty where evidence is incomplete.
6. Avoid treating synthetic-data results as real-world validation.
7. Preserve reproducibility where experiments are involved.
8. Record material changes to detection assumptions.
9. Avoid exposing unnecessary sensitive or personally identifiable information.
10. Link research findings to the relevant VYŪH component when applicable.

---

## Current Research Scope

The initial research scope follows the project's defined threat model and detection architecture.

It includes:

- UPI scam workflows relevant to the five canonical templates
- temporal relationships between payment and account events
- behavioural and transactional anomalies
- device and authentication changes
- beneficiary and destination risk
- velocity and session context
- false-positive and hard-negative behaviour
- synthetic workflow generation
- explainable risk evidence
- security and privacy implications

This scope can expand as VYŪH develops, but new research areas should be documented explicitly rather than implicitly changing the project's boundaries.

---

## Research Status

Research maturity should be treated independently from implementation maturity.

A topic can be:

- researched but not implemented
- implemented but not sufficiently validated
- validated synthetically but not validated on real-world data
- experimentally promising but not yet part of the VYŪH specification

The repository should preserve these distinctions.

---

## Current Research Files

| File | Purpose | Status |
|---|---|---|
| [threat-research.md](./threat-research.md) | Threat landscape and supporting evidence | Planned |
| [scam-workflows.md](./scam-workflows.md) | T1–T5 workflow analysis | Planned |
| [references.md](./references.md) | External sources and research references | Planned |

---

## Principle

> **Research should make VYŪH more defensible, not merely more complicated.**

Every new detection feature should ultimately answer three questions:

1. **What evidence motivates it?**
2. **What behaviour is it intended to distinguish?**
3. **How will we determine whether it actually improves detection without creating unacceptable false positives?**