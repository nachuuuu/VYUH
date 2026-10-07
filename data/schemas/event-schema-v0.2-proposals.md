# VYŪH Event Schema v0.2 — Proposal Notes

**Status:** Proposal  
**Current schema:** v0.1  
**Purpose:** Document event semantics that may be required by the VYŪH threat model but are not representable by the current normalized event contract.

---

## 1. Why This Proposal Exists

The v0.1 event schema represents the core normalized events required by the current detection pipeline:

- authentication activity
- device changes
- beneficiary activity
- payment and transfer activity
- session/context information
- destination/network context

The threat model contains five scam templates. Some templates include precursor states that are not currently represented as explicit event types.

This document records those gaps before any change is made to `event.schema.json`.

**Principle:** Do not add an event type merely because a threat narrative mentions it. Add it only when the event is observable, useful to detection logic, and sufficiently well-defined for synthetic generation and validation.

---

## 2. Current v0.1 Event Types

The current schema defines:

| Event type | Purpose |
|---|---|
| `LOGIN` | Account login/session establishment |
| `AUTH_CHANGE` | Authentication-state or authentication-method change |
| `AUTH_FAILURE` | Failed authentication activity |
| `DEVICE_CHANGE` | Device change activity |
| `BENEFICIARY_CREATE` | New beneficiary creation |
| `BENEFICIARY_INTERACTION` | Interaction with an existing beneficiary |
| `PAYMENT_INITIATED` | Payment initiation |
| `TRANSFER` | Transfer event |

These remain the baseline contract until a proposal is accepted.

---

## 3. Gaps Identified From the Threat Model

### 3.1 Remote-Access Application Activity

**Relevant template:** T2 — Remote-Access App + Unauthorized Transfer

Threat chain:

`Social engineering → victim installs screen-sharing app → attacker gains control → transfer`

The current event schema cannot explicitly represent:

- remote-access application installation
- remote-access application activation
- remote-control session establishment

### Proposal

Potential event type:

`REMOTE_ACCESS_ACTIVITY`

Potential normalized fields:

- application/category identifier
- activity status
- session linkage
- device context

**Status:** Open proposal.

**Reason:** The specification defines the threat chain but does not define a normalized event contract for remote-access applications.

---

### 3.2 Credential-Compromise Indicators

**Relevant template:** T3 — Phishing/Smishing + Credential Compromise

Threat chain:

`Fraudulent link → credentials stolen → new login/session → transfer`

The current schema can represent the later `LOGIN` and `TRANSFER`, but not an explicit credential-compromise precursor.

### Proposal

Potential event type:

`CREDENTIAL_COMPROMISE_INDICATOR`

Potential normalized fields would need to distinguish an observable security signal from an asserted conclusion of compromise.

**Status:** Open proposal.

**Reason:** A detection system should not treat an unverified credential-compromised label as ground truth merely because a synthetic scenario describes it.

---

### 3.3 Collect-Request Activity

**Relevant template:** T4 — Vishing/Fake Support + Collect Request

Threat chain:

`Fraudster impersonates bank → victim approves collect request → payment to attacker`

The current schema has payment/transfer events but no explicit collect-request event.

### Proposal

Potential event type:

`COLLECT_REQUEST`

Potential normalized fields:

- request identifier
- requester/destination identifier
- amount
- status
- approval state

**Status:** Open proposal.

**Reason:** Collect-request approval is materially different from a conventional outgoing transfer and may be useful for temporal template matching.

---

### 3.4 Incoming Proceeds and Rapid Dispersal

**Relevant template:** T5 — Mule Account + Rapid Dispersal

Threat chain:

`Fraud proceeds enter mule account → rapidly transferred onward`

The current `TRANSFER` event already supports `direction`, including `INCOMING` and `OUTGOING`.

Therefore, T5 does **not automatically require a new event type**.

A T5 workflow can potentially be represented as:

`TRANSFER(INCOMING) → TRANSFER(OUTGOING) → TRANSFER(OUTGOING) ...`

**Status:** No new event type proposed at this stage.

**Reason:** The existing event model already contains the core semantic distinction required to represent incoming proceeds followed by onward transfers.

---

## 4. Schema Design Rule

Before adding any new event type, VYŪH should establish:

1. **Observability** — Can the event be generated or observed from an input event stream?
2. **Semantic stability** — Is its meaning sufficiently precise?
3. **Detection value** — Does it materially improve one or more signals/templates?
4. **Synthetic reproducibility** — Can it be generated consistently without relying on real customer data?
5. **Validation value** — Can its effect be measured independently?
6. **Privacy compatibility** — Can it be represented without unnecessary sensitive information?
7. **Backward compatibility** — Can v0.1 events continue to validate unchanged?

---

## 5. Important Boundary

The threat model describes **attack workflows**.

The event schema describes **observable normalized events**.

These are not the same abstraction.

For example:

`victim installs remote-access application`

is a threat-model step.

It does not automatically follow that:

`REMOTE_ACCESS_ACTIVITY`

must exist in the normalized event stream.

The event must represent something the detection system can actually observe or receive as an input.

---

## 6. Current Recommendation

Do not modify `event.schema.json` yet.

Proceed with the existing v0.1 schema while the following questions are resolved:

- What source would produce remote-access activity?
- Is credential compromise directly observable or only inferred?
- What exact collect-request fields are available?
- Which of these events are required for MVP detection versus useful future enrichment?
- Which new events can be represented without introducing unsupported assumptions?

T5 can already be represented using the existing `TRANSFER` event and its `direction` field.

---

## 7. Decision Record

| Item | Decision |
|---|---|
| Change v0.1 schema immediately | No |
| Add T2 remote-access event | Open |
| Add T3 credential-compromise event | Open |
| Add T4 collect-request event | Open |
| Add T5 mule/dispersal event | No new type required yet |
| Preserve v0.1 compatibility | Yes |
| Invent unsupported event semantics | No |

---

## 8. Next Step

The next implementation step should be to create **T3–T5 reference fixtures only where the current v0.1 schema can represent the workflow without inventing unsupported event types**.

Any schema extension should be proposed and reviewed separately before implementation.