# VYŪH — Security & Privacy

> **Purpose:** Document the security, privacy, and safety boundaries of the VYŪH system.
>
> **Source of truth:** `docs/VYUH_Complete_Specification.md`
>
> **Scope:** Project architecture and prototype implementation

---

## 1. Security and Privacy Objective

VYŪH is designed as a **contextual risk-assessment layer** rather than an autonomous transaction-control system.

The central safety principle is:

> **VYŪH scores risk. Analyst decides. Gateway executes.**

The system should minimize unnecessary exposure of customer information, isolate risk scoring from transaction execution, provide explainable evidence for analyst review, and maintain controlled model behavior.

---

## 2. Security Boundaries

The architecture separates the following responsibilities:

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

This prevents a scoring or model failure from independently executing a transaction-control action.

The policy mapper is also separated from scoring logic so that risk estimation and action selection remain distinct concerns.

---

## 3. Automated Action Limits

The current VYŪH action enum is:

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

The VYŪH architecture distinguishes analyst decisions from actual gateway execution.

> **High-risk score ≠ accusation of fraud.**

Where customer-facing verification is required, the intended interaction should request security verification rather than accuse the customer of fraud.

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

VYŪH should process only information required for:

- event normalization;
- temporal/session construction;
- signal extraction;
- template matching;
- risk scoring;
- evidence generation; and
- evaluation.

The synthetic implementation should not introduce real customer identifiers or unnecessary personal information.

Where identifiers are needed for development or demonstration, use synthetic or pseudonymous identifiers such as:

```text
ACC-DEMO-001
DEV-NEW-3B81E0
VPA-NEW-8842
```

These identifiers are illustrative and do not represent real customers.

---

## 7. Pseudonymization

The system should use pseudonymous identifiers rather than exposing direct customer identity wherever possible.

Relevant identifiers may include:

- account IDs;
- device IDs;
- beneficiary IDs; and
- case IDs.

Pseudonymization does not make data inherently anonymous. If real institutional data is introduced later, appropriate access controls and governance remain necessary.

---

## 8. Access Control and Least Privilege

The architecture should follow least-privilege principles.

In particular:

- the scoring engine should not have transaction-gateway credentials;
- scoring components should receive only the data required for their task;
- analyst actions should be represented through the review layer; and
- sensitive external integrations should remain outside the scoring boundary unless explicitly required.

The current project implementation should not be presented as having production-grade institutional access controls unless those controls have actually been implemented and tested.

---

## 9. Storage and Feedback

The current implementation specification uses **SQLite** for feedback and case information.

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

The current system deliberately does **not** perform online retraining.

This preserves reproducibility and prevents a live feedback loop from unexpectedly changing scoring behavior.

---

## 10. Dataset Separation and Evaluation Integrity

Synthetic datasets should remain separated between development/tuning and final evaluation.

The golden set is:

- held out;
- frozen before threshold tuning; and
- evaluated once.

Golden-set results must not be used to tune thresholds or signal weights.

For any future real-data deployment, retention periods, deletion procedures, audit requirements, and institutional data-governance controls must be defined by the deploying organization.

---

## 11. Temporal and Behavioral Privacy Considerations

VYŪH uses temporal and behavioral information:

- 10-minute primary sequence window;
- 60-minute velocity/context window; and
- rolling 90-day behavioral baseline.

These features can be sensitive even when direct identity is removed.

Therefore, the system should:

- use only temporal/context information required by the detector;
- avoid unnecessary exposure of historical events in analyst views;
- use pseudonymous identifiers where appropriate; and
- distinguish project-level evidence requirements from deployment-specific data-governance requirements.

---

## 12. False-Positive Safety

VYŪH is explicitly designed to avoid treating isolated anomalies as proof of fraud.

Safety mechanisms include:

1. **Sequence awareness** — distinguishes coordinated events from unrelated events spread over time.
2. **Weighted combination** — combines multiple signals rather than relying on a single anomaly.
3. **Template matching** — weak workflow matches reduce the likelihood that individual anomalies are interpreted as a coordinated scam.
4. **Human review** — high-risk cases enter a review workflow.
5. **No automatic BLOCK** — the scoring engine cannot independently block a transaction.

A legitimate transaction can therefore be released by the analyst when the evidence indicates a false positive.

---

## 13. Feedback Governance

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

Online retraining is intentionally excluded from the current implementation.

This creates a controlled boundary between review decisions and future model development.

---

## 14. Security Testing Boundaries

The project should explicitly test the safety-critical boundaries.

At minimum:

- verify that the scoring engine cannot issue a BLOCK action;
- verify that policy boundaries map scores to the intended actions;
- verify that the scoring engine has no direct gateway integration;
- verify that evidence contains relevant signal and timeline information;
- verify that ground-truth labels are not passed as model features;
- verify that the golden set is not used during tuning; and
- verify that synthetic identifiers are used for demonstrations.

These tests validate architecture and behavior; they do not constitute a production security audit.

---

## 15. Deployment Security Boundary

The current project is not a claim of production-grade fraud infrastructure.

A production deployment would require additional controls appropriate to the deploying institution, including:

- identity and access management;
- encryption and key management;
- audit logging;
- network segmentation;
- secrets management;
- data-retention governance;
- incident response;
- privacy review;
- model-risk governance; and
- monitoring and adversarial testing.

These requirements should be addressed when VYŪH moves from prototype to institutional deployment.

---

## 16. Non-Claims

VYŪH should not claim:

- production-grade security without corresponding implementation and testing;
- validated performance on real UPI or bank data without such evaluation;
- automatic blocking;
- direct transaction-gateway control;
- complete privacy compliance for a real institution; or
- immunity to adversarial adaptation.

Synthetic validation demonstrates project behavior under controlled conditions. Real deployment requires institution-specific security, privacy, operational, and governance validation.

---

## 17. Security & Privacy Acceptance Checklist

Before a release or demonstration:

- [ ] No BLOCK action exists in the scoring engine.
- [ ] Highest automated action is HOLD_FOR_REVIEW.
- [ ] Scoring engine has no direct transaction-gateway access.
- [ ] Policy mapping is separated from scoring logic.
- [ ] Analyst review actions are RELEASE / ESCALATE / FALSE_POSITIVE.
- [ ] Evidence exposes score, signals, template, and timeline.
- [ ] Synthetic/pseudonymous identifiers are used where appropriate.
- [ ] Ground-truth labels are not scoring inputs.
- [ ] Golden evaluation data remains isolated from tuning.
- [ ] Online retraining is disabled.
- [ ] SQLite feedback fields follow the defined case structure.
- [ ] Deployment-specific security and privacy requirements are distinguished from current project behavior.
- [ ] Unsupported production-security claims are not made.

---

## 18. Canonical Principle

> **VYŪH can recommend and escalate risk; it does not independently seize control of the customer's transaction.**

This boundary should remain consistent across the architecture, scoring engine, dashboard, integrations, and future deployment design.
