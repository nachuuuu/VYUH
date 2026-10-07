# VYŪH Event Schema

**Status:** Canonical schema specification  
**Schema version:** 0.1

## Purpose

This document defines the canonical normalized event representation consumed by the VYŪH detection pipeline.

VYŪH evaluates sequences of related events. The event schema therefore provides a consistent representation for authentication, device, beneficiary, transaction, session, and destination context.

This is a **project schema specification**, not a claim that every field is available in a real UPI integration.

---

## Design Principles

The event schema must:

- represent one observable event at a time
- preserve event ordering through timestamps
- support multiple event types
- permit optional context where telemetry exists
- avoid fabricated values for unavailable fields
- use stable identifiers for relationships within a sequence
- remain suitable for synthetic-data generation
- support deterministic replay and evaluation

The machine-readable contract in `event.schema.json` is normative for structural validation. The constraints documented below are therefore part of schema v0.1 unless explicitly marked as implementation-dependent.

---

## Canonical Event Object

A normalized event has the following conceptual structure:

```json
{
  "event_id": "evt_000001",
  "timestamp": "2026-10-04T10:02:00Z",
  "event_type": "LOGIN",
  "account_id": "acct_001",
  "session_id": "sess_001",
  "device_id": "dev_002",
  "authentication": {},
  "transaction": {},
  "beneficiary": {},
  "context": {},
  "destination": {}
}
```

The example is illustrative. Optional objects should be omitted when the corresponding context is not part of the event.

---

## Core Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `event_id` | string | Yes | Unique identifier for the event within the dataset |
| `timestamp` | ISO 8601 datetime | Yes | Event occurrence time |
| `event_type` | enum | Yes | Canonical event category |
| `account_id` | string | Yes | Synthetic/pseudonymous account identifier |
| `session_id` | string | No | Session identifier when applicable |
| `device_id` | string | No | Device identifier when applicable |
| `authentication` | object | No | Authentication-related context |
| `transaction` | object | No | Payment/transfer context |
| `beneficiary` | object | No | Beneficiary context |
| `context` | object | No | Session, network, geographic, or behavioural context |
| `destination` | object | No | Destination/network context |

---

## Event Types

The initial schema supports event categories required by the current VYŪH threat model.

### Authentication and Account

| Event type | Purpose |
|---|---|
| `LOGIN` | Account login/access event |
| `AUTH_CHANGE` | Authentication method or state change |
| `AUTH_FAILURE` | Failed authentication attempt |
| `DEVICE_CHANGE` | New or changed device context |

### Beneficiary

| Event type | Purpose |
|---|---|
| `BENEFICIARY_CREATE` | New beneficiary introduced |
| `BENEFICIARY_INTERACTION` | Interaction with an existing or new beneficiary |

### Transaction

| Event type | Purpose |
|---|---|
| `PAYMENT_INITIATED` | Payment initiation event |
| `TRANSFER` | Transfer/payment event |

The list may expand as VYŪH gains additional telemetry requirements. New event types should be documented rather than silently reusing an unrelated type.

---

## Timestamp Semantics

`timestamp` represents the time at which the event occurred according to the event source or synthetic generator.

Requirements:

- Use ISO 8601 representation.
- Include timezone information.
- Preserve event timestamps rather than replacing them with ingestion time.
- Do not fabricate precise timestamps when only coarse timing is available in a future integration.
- Sequence construction should use normalized event time consistently.

The detection model depends on temporal relationships, so timestamp integrity is security- and evaluation-relevant.

---

## Identifier Semantics

Identifiers establish relationships between events.

### `account_id`

Identifies the logical account associated with the event.

For synthetic data, it must be generated and must not contain a real account number.

### `session_id`

Groups events belonging to the same logical interaction/session where session information exists.

### `device_id`

Identifies the device context associated with an event.

For synthetic data, device identifiers should be generated consistently so device changes can be represented.

### `event_id`

Uniquely identifies the event record.

Identifiers should be stable during deterministic replay.

---

## Authentication Object

The authentication object may contain fields required to represent authentication context.

Example:

```json
{
  "method": "UPI_PIN",
  "status": "SUCCESS",
  "attempt_count": 1
}
```

Schema v0.1 constrains:

- `status` to `SUCCESS` or `FAILURE`
- `attempt_count` to an integer of at least 1
- `method` to a non-empty string when present

The exact allowed authentication methods are implementation-dependent unless defined by an upstream data source.

VYŪH should not infer an authentication method that is not present in the event data.

---

## Transaction Object

A transaction event may contain:

```json
{
  "amount": 48000,
  "currency": "INR",
  "direction": "OUTGOING",
  "status": "SUCCESS"
}
```

| Field | Type | Required for transaction events | v0.1 constraint |
|---|---|---:|---|
| `amount` | number | Yes | Must be greater than 0 |
| `currency` | string | Yes | `INR` in the current project scope |
| `direction` | enum | Yes | `INCOMING` or `OUTGOING` |
| `status` | enum | No | `SUCCESS`, `FAILED`, or `PENDING` |

For `PAYMENT_INITIATED` and `TRANSFER` events, the `transaction` object is required by schema v0.1.

The current VYŪH specification is focused on behavioural and temporal detection. It does not define a complete production transaction schema.

---

## Beneficiary Object

A beneficiary object represents counterpart information relevant to novelty and transaction context.

Example:

```json
{
  "beneficiary_id": "ben_004",
  "is_new": true
}
```

Schema v0.1 constrains:

- `beneficiary_id` to a non-empty string when present
- `is_new` to a boolean when present

The `is_new` value should represent the event's normalized novelty state, not a detector prediction.

If beneficiary history is unavailable, the implementation should not invent novelty.

---

## Context Object

Context may contain information relevant to session and environmental risk.

Potential fields include:

```json
{
  "ip_context": "new",
  "geo_context": "unusual",
  "hour_context": "unusual"
}
```

Schema v0.1 constrains:

- `ip_context` to `normal`, `new`, or `unusual`
- `geo_context` to `normal`, `new`, or `unusual`
- `hour_context` to `normal` or `unusual`

These are normalized context values, not raw IP, geographic, or timestamp data.

The exact raw representation and normalization of these features remains an implementation decision.

---

## Destination Object

Destination context supports S8 — Destination/network risk.

Example:

```json
{
  "destination_id": "dest_021",
  "network_risk": 0.72
}
```

Schema v0.1 constrains:

- `destination_id` to a non-empty string when present
- `network_risk` to the inclusive range 0–1 when present

A production implementation must define the authoritative source and semantics of destination/network risk.

The current project specification does not establish a real-world risk provider or production network-risk feed.

---

## Event-to-Signal Mapping

| Signal | Relevant event/schema information |
|---|---|
| **S1 — Behavioral deviation** | Historical transaction, timing, beneficiary, device, and account behaviour |
| **S2 — Device/authentication change** | `device_id`, authentication events, authentication context |
| **S3 — Amount anomaly** | `transaction.amount` and account baseline |
| **S4 — Beneficiary novelty** | Beneficiary identity/history and `is_new` state |
| **S5 — Velocity** | Transaction timestamps and event ordering |
| **S6 — Session/context risk** | Session, authentication, time, IP/geo context |
| **S7 — Template match** | Ordered events and their temporal/contextual relationships |
| **S8 — Destination/network risk** | Destination and network-risk context |

This mapping describes required information, not the exact signal-calculation formulas.

---

## Sequence Requirements

A sequence supplied to the scoring engine should:

1. contain events associated with the same logical account context
2. contain valid timestamps
3. preserve event ordering
4. use stable identifiers
5. contain only available/known fields
6. be suitable for the configured temporal windows

The canonical scoring interface is:

```text
score_sequence(events: list[dict]) -> dict
```

The schema is designed to support that interface but does not prescribe the internal implementation.

---

## Validation Rules

A normalized event should be rejected or quarantined when:

- `event_id` is missing
- `timestamp` is invalid
- `event_type` is unknown
- `account_id` is missing
- a required transaction field is absent from a transaction event
- numeric values violate the v0.1 type/range constraints
- identifiers violate the configured format
- event data contains prohibited real customer information in synthetic datasets

Validation behaviour should be deterministic.

The machine-readable JSON Schema is the structural validation authority for v0.1.

---

## Privacy Requirements

The repository's synthetic examples must use generated identifiers.

Do not store:

- real bank-account numbers
- real UPI IDs
- real phone numbers
- real email addresses
- real customer names
- unnecessary precise location data
- production authentication secrets

The schema itself should support data minimization: an event should contain only the fields required for its purpose.

---

## Versioning

The current schema version is **0.1**.

Schema changes should document:

- changed fields
- added/removed event types
- required/optional changes
- compatibility impact
- migration requirements

A breaking change should increment the major schema version once formal versioning reaches a stable release model.

---

## What This Schema Does Not Define

This document intentionally does not define:

- production UPI gateway integration
- a universal UPI event standard
- exact raw-feature normalization formulas
- production destination-risk providers
- institutional retention requirements
- regulatory compliance requirements
- final database storage structures
- detector output schema

Those belong to later implementation and integration work.

---

## Example: Canonical T1 Sequence

The following synthetic sequence matches the canonical T1 fixture in `data/examples/t1-canonical.json`:

```json
[
  {
    "event_id": "evt_t1_001",
    "timestamp": "2026-10-04T10:00:00Z",
    "event_type": "TRANSFER",
    "account_id": "acct_001",
    "device_id": "dev_old",
    "transaction": {
      "amount": 1200,
      "currency": "INR",
      "direction": "OUTGOING",
      "status": "SUCCESS"
    },
    "beneficiary": {
      "beneficiary_id": "ben_existing",
      "is_new": false
    }
  },
  {
    "event_id": "evt_t1_002",
    "timestamp": "2026-10-04T10:02:00Z",
    "event_type": "LOGIN",
    "account_id": "acct_001",
    "device_id": "dev_new"
  },
  {
    "event_id": "evt_t1_003",
    "timestamp": "2026-10-04T10:05:00Z",
    "event_type": "BENEFICIARY_CREATE",
    "account_id": "acct_001",
    "beneficiary": {
      "beneficiary_id": "ben_new",
      "is_new": true
    }
  },
  {
    "event_id": "evt_t1_004",
    "timestamp": "2026-10-04T10:06:00Z",
    "event_type": "TRANSFER",
    "account_id": "acct_001",
    "device_id": "dev_new",
    "transaction": {
      "amount": 48000,
      "currency": "INR",
      "direction": "OUTGOING",
      "status": "SUCCESS"
    },
    "beneficiary": {
      "beneficiary_id": "ben_new",
      "is_new": true
    }
  },
  {
    "event_id": "evt_t1_005",
    "timestamp": "2026-10-04T10:08:00Z",
    "event_type": "TRANSFER",
    "account_id": "acct_001",
    "device_id": "dev_new",
    "transaction": {
      "amount": 15000,
      "currency": "INR",
      "direction": "OUTGOING",
      "status": "SUCCESS"
    },
    "beneficiary": {
      "beneficiary_id": "ben_new",
      "is_new": false
    }
  }
]
```

This is a synthetic documentation example. It is not a production UPI payload.

---

## Principle

> **The event schema is the contract between raw event generation, normalization, detection, and evaluation.**

If the event representation changes, the affected detection logic and evaluation assumptions must be reviewed explicitly.
