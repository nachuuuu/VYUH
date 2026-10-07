# VYŪH Threat Model

**Status:** Round 1 Submission Locked  
**Scope:** AI-driven scam pattern recognition for UPI transaction workflows

This document defines the threat model used by VYŪH: the scam workflows it is designed to recognize, the observable signals used to reconstruct those workflows, the principal assets and attack surfaces, and the controls that constrain the MVP.

> **Scope discipline:** This document describes the threat model defined in the VYŪH specification. It does not claim that the MVP detects every form of UPI fraud or that its synthetic evaluation represents production performance.

---

## 1. Security Objective

VYŪH is designed to identify **coordinated scam workflows** by correlating events over time rather than evaluating every transaction independently.

The core threat-model assumption is that several individually unusual events can become materially more suspicious when they occur in a characteristic sequence within a short time window.

The primary detection objective is:

> **Detect and explain suspicious temporal sequences associated with known scam workflows before the sequence results in an unresolved high-risk transfer.**

VYŪH produces a workflow-level risk assessment and routes the result through a policy layer. The MVP does **not** independently block transactions.

## 2. Threat Actors

### 2.1 Fraudster / Social Engineer

The primary adversary is a fraudster who manipulates a legitimate account holder into performing, authorizing, or enabling a fraudulent payment.

Relevant capabilities represented in the templates include:
- Social engineering
- Phishing or smishing
- Vishing and fake-support impersonation
- Inducing installation of a remote-access or screen-sharing application
- Obtaining or compromising credentials
- Causing a victim to approve a collect request
- Using a compromised device/session to initiate transfers

### 2.2 Account / Device Compromise Actor

The adversary may gain effective control over an account, device, authentication session, or payment workflow.

The threat model therefore considers observable changes such as:
- New device login
- Unusual authentication method
- Authentication failures
- New or rare beneficiary
- Unusual transaction amount
- Rapid transaction velocity
- Unusual session context

### 2.3 Mule Account Operator

A mule account is represented as a destination through which fraud proceeds are received and rapidly dispersed onward.

The relevant workflow is:

**Fraud proceeds received → rapid onward transfers**

VYŪH treats this as a sequence-level destination/network risk rather than as proof that an account is fraudulent.

## 3. Protected Assets

| Asset | Security objective |
|---|---|
| Customer account and payment activity | Detect suspicious activity without unnecessarily disrupting legitimate activity |
| Transaction workflow integrity | Identify coordinated attack sequences in time |
| Authentication/device context | Detect suspicious changes associated with compromise |
| Beneficiary context | Identify unusual or newly introduced payment destinations |
| Risk decisions | Produce consistent, reproducible policy outcomes |
| Evidence timeline | Give analysts an explainable sequence rather than an isolated alert |
| Analyst capacity | Reduce duplicate/coincidental alerts through sequence-level correlation |
| Feedback labels | Preserve analyst decisions for offline calibration and error analysis |

## 4. In-Scope Scam Workflows

VYŪH defines five scam templates.

### T1 — SIM/Device Takeover + Rapid Transfer

**Threat chain:**

SIM swap → new device login → new beneficiary → rapid high-value transfer

The workflow is characterized by a rapid progression from a device/authentication change to beneficiary novelty and high-value transfers.

### T2 — Remote-Access App + Unauthorized Transfer

**Threat chain:**

Social engineering → victim installs screen-sharing app → attacker gains control → transfer

The threat relies on social engineering followed by remote control of the victim's environment and an unauthorized payment.

### T3 — Phishing/Smishing + Credential Compromise

**Threat chain:**

Fraudulent link → credentials stolen → new login/session → transfer

The workflow connects a credential-compromise event to a subsequent suspicious login/session and payment.

### T4 — Vishing/Fake Support + Collect Request

**Threat chain:**

Fraudster impersonates bank → victim approves collect request → payment to attacker

The workflow models impersonation of a bank or support function followed by victim approval of a collect request.

### T5 — Mule Account + Rapid Dispersal

**Threat chain:**

Fraud proceeds enter mule account → rapidly transferred onward

The workflow models rapid movement of received proceeds through a mule destination.

## 5. Observable Attack Signals

VYŪH uses eight signals to evaluate a sequence:

| ID | Signal | Threat relevance |
|---|---|---|
| S1 | Behavioral deviation | Detects deviation from the account's rolling 90-day behavioral baseline |
| S2 | Device/authentication change | Captures new devices and unusual authentication methods |
| S3 | Amount anomaly | Measures transaction amount deviation |
| S4 | Beneficiary novelty | Captures new or rarely used beneficiaries |
| S5 | Velocity | Measures transaction activity over 10-minute and 60-minute windows |
| S6 | Session/context risk | Considers unusual hour, IP/geo context, and authentication failures |
| S7 | Template match | Measures correspondence with a known scam workflow |
| S8 | Destination/network risk | Captures high-risk payment-network context |

These signals are combined into a single weighted risk score. A single signal is not intended to independently determine the highest-risk action.

## 6. Temporal Threat Model

The central temporal assumption is that **ordering and timing matter**.

### Detection windows

| Window | Purpose |
|---|---|
| **10 minutes** | Primary scam-sequence reconstruction |
| **60 minutes** | Velocity and contextual analysis |
| **90 days** | Rolling behavioral baseline |

The 10-minute window is the primary boundary for distinguishing a coordinated sequence from unrelated unusual events spread over a longer period.

For example, a new device, a new beneficiary, and a high-value payment occurring within minutes can represent a materially different threat pattern from the same events occurring independently over several days.

## 7. Template Matching

Each known scam workflow is evaluated using:

TemplateMatch = 0.70 × event_coverage + 0.20 × temporal_consistency + 0.10 × contextual_consistency

### Threshold behavior

| Template match | Contribution |
|---|---|
| **< 0.60** | Contributes 0 to final risk score |
| **0.60–0.79** | Moderate contribution |
| **0.80–1.00** | Strong contribution |

This mechanism is important for false-positive control: an isolated anomaly should not automatically be interpreted as evidence of a complete scam workflow.

## 8. Threat-to-Signal Mapping

| Threat behavior | Primary signals |
|---|---|
| Device/account takeover | S2, S6 |
| Credential compromise | S2, S6 |
| New beneficiary after compromise | S4 |
| High-value unauthorized transfer | S3 |
| Rapid successive transfers | S5 |
| Unusual activity relative to customer history | S1 |
| Known scam workflow progression | S7 |
| Suspicious payment destination/network | S8 |

The mapping is intentionally many-to-many. A workflow can activate several signals, while a signal can be relevant to more than one workflow.

## 9. Risk Decision Boundary

The weighted signal score is mapped to four MVP actions:

| Risk score | MVP action |
|---:|---|
| **0.00–0.29** | ALLOW |
| **0.30–0.59** | SOFT_PROMPT |
| **0.60–0.79** | STEP_UP_VERIFY |
| **0.80–1.00** | HOLD_FOR_REVIEW |

### Critical safety constraint

**BLOCK does not exist in the MVP action set.**

The architecture explicitly separates signal extraction, risk scoring, policy mapping, and human review.

The scoring engine cannot directly call the transaction gateway. This prevents the risk model from independently seizing control of a customer's transaction.

## 10. False-Positive Threat Model

A legitimate customer can produce events that superficially resemble fraud.

Examples explicitly considered by the specification include:
- Legitimate device changes
- High-value family payments
- Short legitimate transaction bursts
- A customer changing phones and making a large payment to a family member
- A salary credit occurring in the same period as an otherwise unusual transaction

VYŪH therefore relies on sequence context rather than a simple OR rule.

### Hard-negative principle

A sequence such as:

**new device + ₹50K family payment + ₹80K salary credit**

should not automatically become a high-risk case merely because several individual rules fire.

The intended VYŪH behavior is to evaluate sequence timing, salary/payment context, beneficiary context, velocity, template strength, and combined risk.

A weak template match and benign contextual evidence can keep the final action below HOLD_FOR_REVIEW.

## 11. Synthetic Threat Representation

The MVP threat model is evaluated with synthetic sequences.

### Dataset composition

| Dataset | Composition |
|---|---|
| Development generation | 5,000 benign + 1,000 scam |
| Scam templates | 200 sequences per template |
| Validation | 3,000 benign + 500 scam |
| Golden test | 2,000 benign + 500 scam |
| Format | JSONL |

Scam sequences are distributed approximately as:
- **60% strong matches** — template match ≥ 0.80
- **30% moderate matches** — template match 0.60–0.79
- **10% noisy matches** — template match < 0.60

Benign data includes approximately **5–10% hard negatives** to represent legitimate behavior that may contain individual anomalies.

## 12. Adversarial Noise

Scam sequences are not assumed to be perfectly clean.

The synthetic generation plan introduces:
- Missing events
- Delayed events
- Amounts closer to the customer's normal behavior
- Additional benign transactions
- Timing jitter
- Different event ordering

These mechanisms test whether the detector depends on a rigid, idealized sequence or can tolerate incomplete/noisy evidence.

## 13. Trust Boundaries and Assumptions

The MVP treats normalized event data as the input to detection.

Architecture boundary:

Raw Events → Event Normalization → Session Construction → Signal Extraction → Template Matching → Risk Scoring → Policy Mapping → Action → Evidence Card → Human Review

Important architectural assumptions:
- Event normalization occurs before detection.
- The primary sequence is constructed over a 10-minute window.
- Historical behavior is available for accounts with sufficient history.
- New accounts do not receive a blanket suspiciousness score solely because history is missing.
- The golden test set is held out before threshold tuning.
- Test data is not used for model development.
- Analyst decisions are logged for offline calibration and error analysis.
- The MVP does not perform online retraining.

## 14. Human Review Boundary

A high-risk score is **not equivalent to an accusation of fraud**.

For HOLD_FOR_REVIEW cases:
1. The case enters a review queue.
2. The analyst receives an evidence timeline.
3. The analyst can release or escalate the case.
4. Customer-facing messaging is framed as a security verification request rather than a fraud accusation.

The feedback record includes:
- case_id
- decision
- risk_score
- template
- signal_scores
- analyst_id
- timestamp
- reason

These records are intended for offline threshold calibration, error analysis, and future model updates.

## 15. Threats Outside the MVP Claim

The five templates define the explicit scam scope of the current specification. The MVP should **not** be represented as a universal UPI fraud detector.

This document does not establish coverage for:
- Scam workflows not represented by the five templates
- Production-scale UPI telemetry
- Real-world fraud prevalence
- Real-world detection performance
- Automatic transaction blocking

Any future extension to additional fraud classes should add new threat templates, event requirements, synthetic generation rules, and validation cases rather than silently expanding the current claims.

## 16. Threat Model Summary

VYŪH's security model can be summarized as:

> **Known scam behavior + suspicious signals + temporal consistency + contextual evidence → explainable risk score → bounded policy action → human review.**

The principal design objective is not to label every unusual transaction as fraud. It is to distinguish **coordinated attack sequences** from **legitimate activity containing isolated anomalies**, while keeping the automated decision boundary conservative.

## 17. Source Basis

The five scam templates in the locked VYŪH specification are identified as being sourced from:
- RBI Master Direction on Digital Payment Security Controls
- RBI 2020 fraud awareness notification
- RBI consumer fraud materials
- RBI money-mule guidance
- NPCI fraud awareness
- IEEE paper on UPI fraud detection

The threat model should be updated when the project adds new templates or changes the evidence and action boundaries defined by the specification.