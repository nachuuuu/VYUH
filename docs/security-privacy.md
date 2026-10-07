# VYŪH — Security & Privacy

> **Purpose:** Document the security, privacy, and safety boundaries of the VYŪH prototype.
>
> **Source of truth:** `docs/VYUH_Complete_Specification.md`
>
> **Status:** Round 1 MVP specification

---

## 1. Security and Privacy Objective

VYŪH is designed as a **contextual risk-assessment layer** rather than an autonomous transaction-control system.

The central safety principle is:

> **VYŪH scores risk. Analyst decides. Gateway executes.**

The prototype should minimize unnecessary exposure of customer information, isolate risk scoring from transaction execution, provide explainable evidence for analyst review, and preserve reproducibility during development.

---

## 2. Security Boundaries

The MVP architecture separates the following responsibilities:

```text
Raw Events
    ↓
Event Normalization
    ↓
Session Construction
    ↓
Signal Extraction
    ↓
Risk Scoring
    ↓
Policy Mapper
    ↓
Evidence Card
    ↓
Human Reviewer
    ↓
Transaction Gateway
```

### Critical boundary

The **scoring engine cannot call the transaction gateway directly**.

This prevents a model or scoring failure from independently executing a transaction-control action.

The policy mapper is also kept separate from scoring logic so that risk estimation and action selection remain distinct concerns.

---

## 3. Automated Action Limits

The MVP action enum is:

```text
ALLOW
SOFT_PROMPT
STEP_UP_VERIFY
HOLD_FOR_REVIEW
```

There is **no BLOCK action in the scoring engine**.

The highest automated action is:

```text
HOLD_FOR_REVIEW
```

A high risk score therefore routes the case to review rather than independently seizing control of the customer's transaction.

Unit tests should validate the boundaries between policy actions.

---

## 4. Human Review

High-risk cases produce an evidence-backed review workflow.

The analyst receives:

- case ID;
- risk score;
- signal contributions;
- matched template;
- event timeline; and
- supporting evidence.

The analyst can record:

- **RELEASE**
- **ESCALATE**
- **FALSE_POSITIVE**

The VYŪH specification distinguishes this analyst decision from actual gateway execution.

> **High-risk score ≠ accusation of fraud.**

For customer-facing verification, the intended language is a security verification request rather than an accusation of fraudulent behavior.

---

## 5. Explainability

VYŪH is designed to produce an explainable workflow-level risk assessment.

The evidence representation should allow an analyst to understand:

1. which events formed the relevant sequence;
2. which of the eight signals contributed to the score;
3. which scam template matched, if any;
4. how the sequence evolved over time; and
5. why the resulting policy action was selected.

The system should expose evidence rather than presenting an unexplained binary fraud label.

---

## 6. Data Minimization

The MVP should process only information required for:

- event normalization;
- temporal/session construction;
- signal extraction;
- template matching;
- risk scoring;
- evidence generation; and
- offline evaluation.

The synthetic-data implementation should avoid introducing real customer identifiers or unnecessary personal information.

Where identifiers are needed for demonstration, use synthetic or pseudonymous identifiers such as:

```text
ACC-DEMO-001
DEV-NEW-3B81E0
VPA-NEW-8842
```

These identifiers are illustrative and do not represent real customers.

---

## 7. Pseudonymization

The prototype should use pseudonymous identifiers rather than exposing direct customer identity wherever possible.

Examples include:

- account IDs;
- device IDs;
- beneficiary IDs;
- case IDs.

Pseudonymization does not make data inherently anonymous. If real institutional data is introduced later, appropriate access controls and governance remain necessary.

---

## 8. Access Control and Least Privilege

The architecture should follow least-privilege principles.

In particular:

- the scoring engine should not have transaction-gateway credentials;
- scoring components should receive only the data required for their task;
- analyst actions should be represented through the review layer;
- sensitive production integrations should remain outside the prototype scoring boundary.

The MVP is a research/prototype system and should not be presented as having production-grade institutional access controls.

---

## 9. Storage and Feedback

The MVP specification uses **SQLite** for feedback and case information.

The feedback record contains:

| Field | Purpose |
|---|---|
| `case_id` | Identify the review case |
| `decision` | RELEASE / ESCALATE / FALSE_POSITIVE |
| `risk_score` | Preserve the scored outcome |
| `template` | Record matched template |
| `signal_scores` | Preserve signal-level evidence |
| `analyst_id` | Associate the review decision |
| `timestamp` | Record review timing |
| `reason` | Capture analyst rationale |

The feedback is intended for:

- offline threshold calibration;
- error analysis; and
- future model updates.

### No online retraining

The MVP deliberately does **not** perform online retraining.

This preserves reproducibility and prevents a live feedback loop from unexpectedly changing scoring behavior during the prototype.

---

## 10. Retention and Dataset Separation

Synthetic datasets should remain separated between development/tuning and final evaluation.

The golden set is:

- held out;
- frozen before threshold tuning; and
- evaluated once.

The system should not use golden-set results to tune thresholds or signal weights.

For any future real-data deployment, retention periods, deletion procedures, audit requirements, and institutional data-governance controls must be defined by the deploying organization. These production policies are outside the locked MVP specification.

---

## 11. Temporal and Behavioral Privacy Considerations

VYŪH uses temporal and behavioral information:

- 10-minute primary sequence window;
- 60-minute velocity/context window;
- rolling 90-day behavioral baseline.

These features can be sensitive even when direct identity is removed.

Therefore, the prototype should:

- use only the temporal/context information required by the detector;
- avoid unnecessary exposure of historical events in analyst views;
- use pseudonymous identifiers in demonstrations; and
- distinguish prototype evidence requirements from production data-governance requirements.

---

## 12. False-Positive Safety

VYŪH is explicitly designed to avoid treating isolated anomalies as proof of fraud.

Safety mechanisms include:

1. **Sequence awareness** — distinguishes coordinated events from unrelated events spread over time.
2. **Weighted combination** — one signal alone should not determine the highest-risk action.
3. **Template matching** — weak workflow matches reduce the likelihood that individual anomalies are interpreted as a coordinated scam.
4. **Human review** — high-risk cases enter a review workflow.
5. **No automatic BLOCK** — the scoring engine cannot independently block a transaction.

A legitimate transaction can therefore be released by the analyst when the evidence indicates a false positive.

---

## 13. Feedback Governance

Analyst feedback is recorded for offline analysis and calibration.

The feedback loop is:

```text
Scored Case
    ↓
Analyst Review
    ↓
RELEASE / ESCALATE / FALSE_POSITIVE
    ↓
Logged Feedback
    ↓
Offline Calibration / Error Analysis
    ↓
Future Model Updates
```

The MVP does not perform online retraining.

This creates a controlled boundary between production-like review decisions and future model development.

---

## 14. Security Testing Boundaries

The MVP should test the safety-critical boundaries explicitly.

At minimum:

- verify that the scoring engine cannot issue a BLOCK action;
- verify that policy boundaries map scores to the intended actions;
- verify that the scoring engine has no direct gateway integration;
- verify that evidence contains the relevant signal and timeline information;
- verify that ground-truth labels are not passed as model features;
- verify that the golden set is not used during tuning;
- verify that synthetic identifiers are used in demonstrations.

These tests validate architecture and behavior; they do not constitute a production security audit.

---

## 15. Production Security Boundary

VYŪH is **not** a production-grade fraud system in its MVP form.

Production deployment would require additional controls, including institution-specific:

- identity and access management;
- encryption and key management;
- audit logging;
- network segmentation;
- secrets management;
- data-retention governance;
- incident response;
- privacy review;
- model-risk governance;
- monitoring and adversarial testing.

These are deployment requirements, not claims about the current prototype.

---

## 16. Non-Claims

VYŪH must not claim:

- production-grade security;
- validated performance on real UPI or bank data;
- automatic blocking;
- direct transaction-gateway control;
- complete privacy compliance for a real institution; or
- immunity to adversarial adaptation.

Synthetic validation demonstrates prototype behavior. Real deployment requires institution-specific security, privacy, operational, and governance validation.

---

## 17. Security & Privacy Acceptance Checklist

Before submission or demonstration:

- [ ] No BLOCK action exists in the scoring engine.
- [ ] Highest automated action is HOLD_FOR_REVIEW.
- [ ] Scoring engine has no direct transaction-gateway access.
- [ ] Policy mapping is separated from scoring logic.
- [ ] Analyst review actions are RELEASE / ESCALATE / FALSE_POSITIVE.
- [ ] Evidence exposes score, signals, template, and timeline.
- [ ] Synthetic/pseudonymous identifiers are used for demonstrations.
- [ ] Ground-truth labels are not scoring inputs.
- [ ] Golden evaluation data remains isolated from tuning.
- [ ] Online retraining is disabled for the MVP.
- [ ] SQLite feedback fields follow the specified case structure.
- [ ] Production security and privacy requirements are clearly distinguished from prototype behavior.
- [ ] No unsupported production-security claims appear in the submission.

---

## 18. Canonical Principle

> **VYŪH can recommend and escalate risk; it does not independently seize control of the customer's transaction.**

This boundary is central to the MVP's safety model and should remain consistent across the architecture, implementation, dashboard, and submission materials.
