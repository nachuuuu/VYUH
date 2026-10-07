# VYŪH References

**Status:** Initial reference ledger

## Purpose

This file records external sources that support the research context, threat assumptions, terminology, and future validation work for VYŪH.

A reference is not automatically evidence for a specific VYŪH detection rule. Each source is mapped to what it actually supports.

---

## Primary Institutional Sources

### 1. Reserve Bank of India — Annual Report 2024–25

**Source:** RBI, Annual Report 2024–25, Chapter VI: Regulation, Supervision and Financial Stability.

**Supports:**
- The importance of strengthening fraud detection and consumer protection.
- The prevalence of digital-payment frauds by number within the reported fraud categories.
- RBI's continued focus on cyber security and fraud detection.
- The need for resilience and stronger controls around digital financial services.

**VYŪH relevance:** Establishes institutional context for fraud-detection research and the importance of controls around digital payments.

**Source:** https://www.rbi.org.in/scripts/AnnualReportPublications.aspx?Id=1436

---

### 2. Reserve Bank of India — Annual Report 2023–24

**Source:** RBI, Annual Report 2023–24.

**Supports:**
- Digital-payment frauds being a major category by number.
- The reported time lag between occurrence and detection of frauds.
- The importance of improving fraud detection and payment-system integrity.

**VYŪH relevance:** Supports research interest in earlier detection and temporal fraud analysis. It does **not** establish that VYŪH itself reduces detection latency.

**Source:** https://www.rbi.org.in/scripts/AnnualReportPublications.aspx?Id=1406

---

### 3. NPCI — UPI Frequently Asked Questions

**Source:** National Payments Corporation of India, UPI FAQs.

**Supports:**
- UPI registration and device/SIM-change behaviour.
- UPI collect-request mechanics.
- The role of the UPI PIN in transaction authorization.
- The fact that UPI transactions operate continuously rather than only during banking hours.

**VYŪH relevance:** Provides authoritative UPI-system context relevant to T1, T4, device changes, authentication, and transaction events.

**Source:** https://www.npci.org.in/what-we-do/upi/faqs

---

### 4. NPCI — Fraud Awareness

**Source:** National Payments Corporation of India, Fraud Awareness.

**Supports:**
- Social-engineering as a relevant fraud mechanism.
- Fraud patterns involving unknown links, QR codes, unknown applications, messages, and online scams.
- User-facing security guidance around digital payments.

**VYŪH relevance:** Provides institutional context for threat patterns related to social engineering, malicious links, and unknown applications.

**Source:** https://www.npci.org.in/fraud-awareness

---

### 5. NPCI — UPI Ecosystem Statistics

**Source:** National Payments Corporation of India, UPI Ecosystem Statistics.

**Supports:**
- UPI ecosystem terminology.
- Definitions associated with payer/payee PSPs, device binding, transaction processing, and collect requests.
- Official UPI ecosystem statistics when quantitative context is required.

**VYŪH relevance:** Provides authoritative terminology and a source for future project-level quantitative context.

**Source:** https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics

---

### 6. NPCI — UPI Fraud-Risk Mitigation Circular

**Source:** NPCI, UPI/OC No.57/2018-19, “Changes in PSP & Customer communication to prevent fraudulent transactions,” 25 July 2018.

**Supports:**
- Historical UPI fraud-risk mitigation measures.
- Standardized customer communication for collect requests.
- Account-number masking as a security measure.

**VYŪH relevance:** Useful background for the evolution of UPI fraud controls and customer-facing safeguards.

**Source:** https://www.npci.org.in/PDF/npci/upi/circular/2018/Circular%2057.pdf

---

## Project Specification Sources

### 7. VYŪH Complete Specification

**Source:** `docs/VYUH_Complete_Specification.md`

**Supports:**
- The five canonical scam templates.
- Eight detection signals.
- Temporal windows.
- Template-matching formula.
- Risk weights and policy thresholds.
- Synthetic-data design.
- Validation targets.
- Security and privacy boundaries.

**VYŪH relevance:** This is the project's primary internal source of truth for the current architecture and specified behaviour.

---

### 8. VYŪH Threat Model

**Source:** `docs/threat-model.md`

**Supports:**
- Threat actors and protected assets.
- Threat-to-signal mapping.
- Temporal threat assumptions.
- False-positive and hard-negative considerations.
- Trust boundaries.

---

### 9. VYŪH Detection Logic

**Source:** `docs/detection-logic.md`

**Supports:**
- Event normalization.
- Session construction.
- Signal extraction.
- Template matching.
- Risk-scoring pipeline.
- Policy mapping.
- Evidence generation.

---

### 10. VYŪH Synthetic Data Specification

**Source:** `docs/synthetic-data.md`

**Supports:**
- Dataset composition.
- Benign and scam sequence generation.
- Hard-negative generation.
- Noise mechanisms.
- Evaluation split design.
- Leakage prevention.

---

## Evidence Discipline

References in this file should be used according to the following rules:

1. **Do not cite a source for a claim it does not support.**
2. **Separate institutional facts from VYŪH design decisions.**
3. **Do not present synthetic-data targets as measured results.**
4. **Do not infer real-world scam prevalence from the existence of a threat pattern alone.**
5. **Record new quantitative claims with their exact source.**
6. **Prefer primary institutional sources for UPI-system and regulatory claims.**
7. **Update this ledger when a new external source materially changes a threat assumption or design decision.**

---

## Source-to-Workflow Mapping

| Source | T1 | T2 | T3 | T4 | T5 |
|---|:---:|:---:|:---:|:---:|:---:|
| RBI Annual Report 2024–25 | Context | Context | Context | Context | Context |
| RBI Annual Report 2023–24 | Context | Context | Context | Context | Context |
| NPCI UPI FAQs | ✓ | ✓ | — | ✓ | — |
| NPCI Fraud Awareness | ✓ | ✓ | ✓ | ✓ | — |
| NPCI UPI Ecosystem Statistics | ✓ | — | — | ✓ | ✓ |
| NPCI Fraud-Risk Mitigation Circular | — | — | — | ✓ | — |

The checkmarks indicate relevance to research context, not empirical validation of the workflow.

---

## Future References

The following categories should be added as VYŪH research develops:

- peer-reviewed research on fraud and anomaly detection
- temporal and sequential pattern-mining literature
- behavioural anomaly-detection literature
- adversarial machine-learning research
- explainable fraud-detection research
- privacy-preserving financial analytics
- official Indian cyber-fraud advisories
- relevant regulatory and payment-system guidance
- institutionally governed datasets, where access is lawful and appropriate

New sources should be added with a short note explaining exactly what they contribute.

---

## Important Distinction

This reference ledger contains **supporting evidence**, not a bibliography of everything related to fraud.

A source should be added because it contributes to a VYŪH research question, assumption, implementation decision, or validation plan.

> **References should make project claims traceable. They should not be used to manufacture authority for unsupported claims.**