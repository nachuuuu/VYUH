# VYŪH Scam Workflows

**Status:** Canonical workflow reference

## Purpose

This document defines the five canonical scam workflows currently represented in VYŪH.

The workflows describe **temporal patterns of related events**, not fixed transaction rules. They provide the conceptual basis for template matching and synthetic-data generation.

A workflow is evidence for risk only when the observed sequence, timing, and context are sufficiently consistent with the corresponding template. VYŪH does not treat the presence of one isolated event as proof of a scam.

---

## Workflow Overview

| ID | Workflow | Primary pattern |
|---|---|---|
| **T1** | SIM/Device Takeover + Rapid Transfer | Device/account state changes followed by rapid beneficiary and transfer activity |
| **T2** | Remote-Access App + Unauthorized Transfer | Suspicious device/session context followed by unauthorized payment activity |
| **T3** | Phishing/Smishing + Credential Compromise | Compromise indicators followed by account access and payment activity |
| **T4** | Vishing/Fake Support + Collect Request | Social-engineering context followed by a collect-request payment flow |
| **T5** | Mule Account + Rapid Dispersal | Funds received into an account followed by rapid onward movement |

The five templates are the current VYŪH threat-model boundary.

---

# T1 — SIM/Device Takeover + Rapid Transfer

## Objective

Represent a sequence in which a change in device or account-access context is followed by rapid payment activity involving a new beneficiary and anomalous amounts.

## Canonical sequence

The specification defines the following illustrative T1 sequence:

| Time | Event |
|---|---|
| 10:00 | Normal transaction: ₹1,200 using an old device and existing beneficiary |
| 10:02 | Login from a new device |
| 10:05 | New beneficiary introduced |
| 10:06 | ₹48,000 transfer |
| 10:08 | ₹15,000 rapid additional transfer |

The expected demonstration risk is approximately 0.87, with **HOLD_FOR_REVIEW** and **T1** as the expected interpretation.

The value 0.87 is a demonstration target, not a hardcoded score. The actual implementation must calculate the score from the event sequence.

## Key temporal relationships

- Device change precedes suspicious payment activity.
- New beneficiary appears shortly after the device change.
- Transfer occurs shortly after beneficiary creation.
- A second transfer follows rapidly.

## Relevant signals

Primary signals include:

- S1 — Behavioral deviation
- S2 — Device/authentication change
- S3 — Amount anomaly
- S4 — Beneficiary novelty
- S5 — Velocity
- S6 — Session/context risk
- S7 — Template match

## Defined parameter ranges for synthetic generation

The synthetic-data specification defines:

| Parameter | Range |
|---|---:|
| Account age | 30–1000 days |
| Device change → login | 0–2 minutes |
| Login → beneficiary | 1–5 minutes |
| Beneficiary → transfer | 1–5 minutes |
| Amount multiplier | 1.5–4.0× baseline |
| Rapid transfers | 1–2 |

These ranges are generation parameters, not claims about real-world scam behaviour.

## Benign lookalikes

Potential legitimate sequences include:

- a customer replacing or upgrading a phone
- legitimate login from a new device
- adding a beneficiary for a planned purchase
- a genuine large transfer
- multiple legitimate transfers made close together

The detector therefore relies on the combined sequence rather than any single event.

---

# T2 — Remote-Access App + Unauthorized Transfer

## Objective

Represent a workflow in which a suspicious session or device context is followed by unauthorized payment activity.

## Conceptual sequence

    Suspicious session/device context
                ↓
    Account interaction
                ↓
    Payment initiation
                ↓
    Unauthorized transfer

## Relevant signals

The threat-model mapping identifies:

- S2 — Device/authentication change
- S3 — Amount anomaly
- S5 — Velocity
- S6 — Session/context risk
- S7 — Template match

## Important detection context

Session and authentication context are important because the payment itself may not be anomalous enough to identify the workflow in isolation.

## Benign lookalikes

Potential legitimate sequences include:

- remote technical support that does not involve payment authorization
- legitimate device-access or account-recovery activity
- a user making a normal transaction during an unusual session context

VYŪH should distinguish the payment workflow from the mere presence of unusual session activity.

## Research limitation

The current specification defines the workflow concept and relevant signals but does not define a dedicated raw event proving that a remote-access application was installed or used. Such an event schema requires further implementation and validation.

---

# T3 — Phishing/Smishing + Credential Compromise

## Objective

Represent a compromise workflow in which a phishing or smishing interaction is followed by account access and subsequent payment activity.

## Conceptual sequence

    Phishing / smishing interaction
                ↓
    Credential compromise
                ↓
    Account access
                ↓
    Payment activity

## Relevant signals

The current threat-to-signal mapping identifies:

- S2 — Device/authentication change
- S3 — Amount anomaly
- S4 — Beneficiary novelty
- S5 — Velocity
- S6 — Session/context risk
- S7 — Template match

## Detection consideration

The external social-engineering event may not be directly visible to a payment-risk engine.

VYŪH therefore should not assume that an observed payment sequence proves a phishing event occurred. Instead, the engine can use payment/account events as observable consequences where the required signals are available.

## Benign lookalikes

Potential legitimate sequences include:

- normal credential recovery
- routine authentication changes
- new-device login followed by normal payments
- legitimate beneficiary creation after account access

---

# T4 — Vishing/Fake Support + Collect Request

## Objective

Represent a social-engineering workflow in which a victim is induced to interact with a fraudulent support actor and subsequently approves or receives a collect-request payment flow.

## Conceptual sequence

    Fake support / vishing interaction
                ↓
    Social-engineering instruction
                ↓
    Collect request
                ↓
    Payment approval / resulting transaction

## Relevant signals

The current mapping identifies:

- S3 — Amount anomaly
- S4 — Beneficiary novelty
- S6 — Session/context risk
- S7 — Template match
- S8 — Destination/network risk

## Detection consideration

A voice call or social-engineering conversation is not necessarily observable in the transaction event stream.

The workflow should therefore be interpreted from the payment-side evidence available to VYŪH rather than assuming direct visibility into the conversation.

## Benign lookalikes

Potential legitimate activity includes:

- legitimate collect requests
- payments initiated after a genuine support interaction
- expected payments to newly encountered counterparties

The distinction depends on the combined payment context and sequence.

---

# T5 — Mule Account + Rapid Dispersal

## Objective

Represent an account receiving funds and rapidly moving them onward, potentially across multiple destinations.

## Conceptual sequence

    Incoming funds
          ↓
    Short holding period
          ↓
    Rapid onward transfer
          ↓
    Additional dispersal

## Relevant signals

The current mapping identifies:

- S1 — Behavioral deviation
- S3 — Amount anomaly
- S4 — Beneficiary novelty
- S5 — Velocity
- S7 — Template match
- S8 — Destination/network risk

## Detection consideration

Rapid onward movement can be legitimate.

Examples include:

- businesses receiving and redistributing funds
- individuals transferring money between their own accounts
- scheduled or operational payments
- legitimate high-frequency payment activity

Therefore, rapid dispersal should be interpreted in account context rather than treated as inherently fraudulent.

---

# Template Matching

The current VYŪH specification defines the template score as:

    T = 0.70 × event_coverage
      + 0.20 × temporal_consistency
      + 0.10 × contextual_consistency

Where:

- **event coverage** measures how much of the expected workflow is observed
- **temporal consistency** measures how closely event timing follows the workflow
- **contextual consistency** measures compatibility with relevant account/session/payment context

The specification defines:

| Template score | Interpretation |
|---|---|
| < 0.60 | Template does not contribute to risk score |
| 0.60–0.79 | Moderate template contribution |
| 0.80–1.00 | Strong template contribution |

The exact raw-feature extraction and normalization required to calculate these components is an implementation detail unless separately specified.

---

# Noise and Workflow Variation

Synthetic scam sequences should not all appear as idealized canonical examples.

The project specification permits:

- missing events
- delayed events
- timing jitter
- amounts closer to normal
- benign transactions mixed into scam sequences
- different event ordering

This is important because a detector that only recognizes perfect sequences would have limited robustness.

---

# Benign Counterexamples

Every workflow should be evaluated against legitimate sequences that share some of its characteristics.

| Workflow | Example benign similarity |
|---|---|
| T1 | New phone + new beneficiary + legitimate large payment |
| T2 | Unusual session context + legitimate payment |
| T3 | Credential recovery + normal payment |
| T4 | Legitimate collect request |
| T5 | Legitimate account receiving and redistributing funds |

These counterexamples should inform hard-negative generation and false-positive analysis.

---

# Workflow Evidence Boundaries

VYŪH must distinguish between:

1. **Observed event**
2. **Inferred workflow**
3. **Risk score**
4. **Policy action**

For example, a high T1 template score means that observed events resemble the T1 workflow. It does not establish that a SIM takeover actually occurred.

This distinction is important for explainability, human review, and safe deployment.

---

# Research Questions

The workflow definitions leave several questions for future empirical research:

- Which observable event combinations most reliably distinguish each workflow?
- How often do benign customers produce similar sequences?
- Which workflow steps are commonly missing from available telemetry?
- How much temporal variation can template matching tolerate?
- Which signals are redundant across templates?
- Which templates are most difficult to distinguish from legitimate activity?
- How should workflows evolve when new scam mechanisms appear?

These questions should be answered through controlled experiments and appropriately governed data rather than assumptions.

---

# Non-Claims

The workflow definitions do **not** establish:

- that these five workflows represent all UPI scam types
- that every workflow is directly observable from payment data
- that a template match proves fraud
- that any individual signal is sufficient for a fraud decision
- that synthetic workflow performance transfers directly to production
- that VYŪH can identify the social-engineering interaction itself when that event is outside its telemetry

---

## Principle

> **VYŪH recognizes patterns in observable event sequences; it does not claim to observe every event in the real-world scam narrative.**
