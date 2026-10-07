# VYŪH Example Event Fixtures

**Schema version:** 0.1  
**Purpose:** Reference index for the synthetic event sequences stored in this directory.

---

## 1. Purpose

This directory contains small, deterministic event sequences used to exercise the VYŪH event schema and threat-model workflows.

These fixtures are **not** the full synthetic dataset. They are compact examples intended for schema validation, detection-engine development, unit tests, demonstrations, and documentation.

---

## 2. Fixture Index

| File | Template | Status | What it represents |
|---|---|---|---|
| `t1-canonical.json` | T1 — SIM/Device Takeover + Rapid Transfer | Canonical | Full T1 sequence defined in the project specification |
| `t2-reference.json` | T2 — Remote-Access App + Unauthorized Transfer | Reference | Observable login/transfer portion representable by schema v0.1 |
| `t3-reference.json` | T3 — Phishing/Smishing + Credential Compromise | Reference | Observable login/transfer portion representable by schema v0.1 |
| `t4-reference.json` | T4 — Vishing/Fake Support + Collect Request | Reference | Payment/transfer portion representable by schema v0.1 |
| `t5-reference.json` | T5 — Mule Account + Rapid Dispersal | Reference | Incoming transfer followed by rapid outgoing transfers |

---

## 3. Canonical vs Reference

### Canonical

A canonical fixture is directly defined by the current VYŪH specification with an explicit event sequence.

Currently:

- `t1-canonical.json`

### Reference

A reference fixture demonstrates a threat-template pattern using only event semantics currently supported by the v0.1 schema.

Reference fixtures must not be interpreted as complete representations of the underlying real-world scam workflow when the schema lacks the relevant precursor events.

Currently:

- `t2-reference.json`
- `t3-reference.json`
- `t4-reference.json`
- `t5-reference.json`

---

## 4. Schema Contract

Every fixture in this directory is intended to validate against:

`data/schemas/event.schema.json`

The fixtures use the v0.1 normalized event contract.

Core required fields:

- `event_id`
- `timestamp`
- `event_type`
- `account_id`

Transaction events additionally require:

- `transaction.amount`
- `transaction.currency`
- `transaction.direction`

---

## 5. Temporal Semantics

VYŪH uses three temporal scopes:

| Window | Purpose |
|---|---|
| 10 minutes | Primary sequence construction |
| 60 minutes | Velocity and contextual analysis |
| Rolling 90 days | Behavioral baseline |

The example fixtures primarily demonstrate short workflow sequences. They do not contain the historical 90-day event history required to calculate a real behavioral baseline.

---

## 6. Synthetic Data Boundary

These examples use synthetic identifiers and values.

They must not contain:

- real bank-account numbers
- real UPI IDs
- real phone numbers
- real email addresses
- customer names
- authentication secrets
- unnecessary precise location information

Fixture values are illustrative and are not claims about real customer behavior.

---

## 7. Expected Use

These fixtures may be used for:

1. JSON Schema validation
2. Parser and normalization tests
3. `score_sequence(events)` development
4. Template-matching tests
5. Evidence-card examples
6. Regression tests
7. Documentation and demonstrations

They should not be treated as statistically representative data.

---

## 8. Relationship to the Synthetic Dataset

The project specification defines the larger synthetic dataset as:

- 5,000 benign workflows
- 1,000 scam workflows
- 200 scam cases per template
- approximately 60% strong scam cases
- approximately 30% moderate scam cases
- approximately 10% noisy scam cases

The workflows are serialized as multiple event records in the JSONL data layer. These small fixtures demonstrate event-level representations and are not statistically representative of the full dataset.

---

## 9. Current Limitations

Schema v0.1 does not explicitly model:

- remote-access application activity
- credential-compromise indicators
- collect-request activity

Consequently, T2–T4 reference fixtures represent only the portions of those workflows that can be expressed by the current normalized event contract.

These limitations are tracked in:

`data/schemas/event-schema-v0.2-proposals.md`

---

## 10. Principle

> **Fixtures demonstrate the event contract; they do not redefine the threat model.**
