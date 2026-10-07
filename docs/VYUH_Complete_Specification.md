# VYŪH — Complete Specification & Pitch Deck Design Brief

**Date:** October 4, 2026  
**Project:** VYŪH (Track 02: AI-Driven Scam Pattern Recognition)  
**Status:** Round 1 Submission Locked  

---

## TABLE OF CONTENTS

1. [Product Overview](#product-overview)
2. [Threat Model](#threat-model)
3. [Detection Architecture](#detection-architecture)
4. [Synthetic Data Specification](#synthetic-data-specification)
5. [Validation Metrics](#validation-metrics)
6. [User & Problem](#user--problem)
7. [Differentiation](#differentiation)
8. [Safety & Human Review](#safety--human-review)
9. [48-Hour MVP Plan](#48-hour-mvp-plan)
10. [Pitch Deck Outline](#pitch-deck-outline)
11. [Complete Slide-by-Slide Design Brief](#complete-slide-by-slide-design-brief)
12. [Claims Discipline](#claims-discipline)

---

## PRODUCT OVERVIEW

**Name:** VYŪH  
**Tagline:** "From event flagging to sequence scoring."  
**One-liner:** "VYŪH detects suspicious payment workflows by connecting device, behaviour, beneficiary, velocity, and transaction context over time — not by judging transactions in isolation."

**Core Claim:**  
VYŪH detects AI-enabled financial scam workflows by connecting behavioral, temporal, and transactional signals into explainable risk assessments — instead of judging transactions in isolation.

**Why it matters:**  
Current fraud systems flag individual anomalies (new device, unusual amount, new beneficiary) independently. When these happen in rapid sequence (within 5 minutes), they appear as 3 separate alerts instead of one coordinated attack. By the time an analyst reviews the first alert, funds have moved to a mule account. VYŪH reconstructs the attack sequence and produces one explainable workflow-level risk assessment before the suspicious transfer completes.

---

## THREAT MODEL — 5 SCAM TEMPLATES

All templates sourced from RBI/NPCI documentation.

| ID | Template | Threat Chain |
|---|---|---|
| **T1** | SIM/Device Takeover + Rapid Transfer | SIM swap → new device login → new beneficiary → rapid high-value transfer |
| **T2** | Remote-Access App + Unauthorized Transfer | Social engineering → victim installs screen-sharing app → attacker gains control → transfer |
| **T3** | Phishing/Smishing + Credential Compromise | Fraudulent link → credentials stolen → new login/session → transfer |
| **T4** | Vishing/Fake Support + Collect Request | Fraudster impersonates bank → victim approves collect request → payment to attacker |
| **T5** | Mule Account + Rapid Dispersal | Fraud proceeds enter mule account → rapidly transferred onward |

**Sources:**  
- RBI Master Direction on Digital Payment Security Controls
- RBI 2020 fraud awareness notification
- RBI consumer fraud materials
- RBI money-mule guidance
- NPCI fraud awareness
- IEEE paper on UPI fraud detection

---

## DETECTION ARCHITECTURE

### Pipeline Flow

```
Raw Events 
  ↓
Event Normalization 
  ↓
Session Construction (10 min window) 
  ↓
8 Signal Extractors 
  ↓
5 Template Matchers 
  ↓
Weighted Risk Score 
  ↓
Policy Mapper 
  ↓
Actions (ALLOW / SOFT_PROMPT / STEP_UP_VERIFY / HOLD_FOR_REVIEW)
  ↓
Evidence Card 
  ↓
Human Reviewer 
  ↓
Label + Reason (for future calibration)
```

### 8 Signals & Final Weights

| Signal | Weight | Description |
|---|---:|---|
| S1 | Behavioral deviation | rolling 90-day MAD baseline |
| S2 | Device/authentication change | new device, unusual auth method |
| S3 | Amount anomaly | transaction amount deviation |
| S4 | Beneficiary novelty | new/rare beneficiary |
| S5 | Velocity | 10 min + 60 min transaction windows |
| S6 | Session/context risk | unusual hour, IP/geo, auth failures |
| S7 | Template match | ≥0.60 threshold to contribute |
| S8 | Destination/network risk | high-risk payment network |

**Total: 100% (all signals weighted and combined into single risk score)**

### Template Match Formula

```
TemplateMatch = 0.70 × event_coverage 
                + 0.20 × temporal_consistency 
                + 0.10 × contextual_consistency
```

**Threshold behavior:**
- < 0.60: Contributes 0 to final score
- 0.60–0.79: Moderate contribution
- 0.80–1.00: Strong contribution

### Risk Thresholds → Actions

| Risk Score | Action |
|---|---|
| 0.00–0.29 | ALLOW |
| 0.30–0.59 | SOFT_PROMPT |
| 0.60–0.79 | STEP_UP_VERIFY |
| 0.80–1.00 | HOLD_FOR_REVIEW |

**CRITICAL:** No BLOCK in MVP. Highest automated action = HOLD_FOR_REVIEW.

### Detection Windows

- **Primary sequence window:** 10 minutes
- **Velocity/context window:** 60 minutes
- **Behavioral baseline:** rolling 90 days

### New Account Defaults (< 7 days history)

Signal-specific defaults, not blanket 0.5. Lack of history ≠ suspicious.

---

## SYNTHETIC DATA SPECIFICATION

### Composition

| Parameter | Value |
|---|---|
| Benign sequences | 5,000 |
| Scam sequences | 1,000 (200/template) |
| Scam distribution | ~60% strong match (≥0.80), ~30% moderate (0.60–0.79), ~10% noisy (<0.60) |
| Validation set | 3,000 benign + 500 scam (for threshold tuning) |
| Golden test set | 2,000 benign + 500 scam (held out, evaluated once only) |
| Format | JSONL (one event per line) |

### Benign Sequence Generation

- Account-specific behavioral profiles (typical amounts, hours, devices, beneficiaries)
- ~5–10% hard negatives: legitimate device changes, high-value family payments, short legitimate bursts
- Template match must be < 0.60
- Generated from account history, not rules

### T1 (SIM Takeover) Generation Parameters

- Account age: 30–1000 days
- Device change → login: 0–2 min
- Login → beneficiary: 1–5 min
- Beneficiary → transfer: 1–5 min
- Amount multiplier: 1.5–4.0×
- Transfer count: 1–2

### Noise Mechanisms for Scams

- Missing events
- Delayed events
- Amounts closer to normal
- Additional benign transactions mixed in
- Timing jitter
- Different event ordering

### Data Split Enforcement

- Generation and evaluation sets separated to prevent leakage
- Golden test set frozen before threshold tuning
- No test data used for model development

---

## VALIDATION METRICS

### Baseline Detector (Transparent, Reproducible)

```
IF (amount > 3× account baseline) 
   OR (new device) 
   OR (new beneficiary) 
   OR (>3 transactions in 10 min) 
   OR (unusual hour AND amount z-score > 2.5)
THEN FLAG
ELSE ALLOW
```

### VYŪH Targets (on synthetic test set)

- **Precision:** ≥ 80%
- **Recall:** ≥ 80%
- **F1:** ≥ 80%
- **FP rate:** < 1% (< 10 FP per 1,000 benign sequences)

### Primary Operational Metric

**FP per 1,000 benign sequences** (most intuitive for alert fatigue story)

Report alongside:
- Precision
- Recall
- F1
- Confusion matrix
- Actual measured results (not targets)

---

## USER & PROBLEM

### Primary User

**Title:** Fraud Risk Analyst  
**Organization:** Large Indian bank (modeled at ICICI Bank scale; generic, not named)  
**Department:** Fraud Risk Operations  
**Team size:** ~40–50 analysts (24/7 operations)  
**Authority:** Analysts decide RELEASE / ESCALATE / FALSE_POSITIVE. Actual BLOCK/ALLOW executed by transaction gateway, not VYŪH.

### Daily Workflow

- **Morning:** Review overnight alert backlog, prioritize high-risk cases
- **Throughout day:** Review flagged transactions, decide action
- **Weekly:** Tune thresholds based on feedback

### Scenario (Illustrative Assumptions)

- Daily transactions: 100M
- Alert rate: 0.3% → 300K alerts/day
- Analyst capacity: 40 analysts × 8hr × 60min ÷ 3min per alert = 6,400 alerts/day reviewed
- Benign-alert rate: 40% → 120K benign alerts/day = 6,000 analyst-hours/day on noise
- **With VYŪH (target):** 40% → 15% benign alerts = 45K benign alerts/day = 2,250 analyst-hours/day
- **Result:** 3,750 hours freed per day (62.5% reduction)

**⚠️ Disclaimer:** 62.5% is ILLUSTRATIVE SCENARIO, not measured prototype performance.

### Intervention Point

**When:** Immediately before suspicious transfer executes, after precursor events accumulated  
**Target window:** 1–2 minutes before funds move (architectural target, not guaranteed SLA)

### Concrete Failure Example (Account B)

```
23:30 — Attacker logs in from new device (unusual hour)
23:33 — Attacker adds new beneficiary
23:35 — Attacker transfers ₹30,000 (4× normal)

Current system: 3 separate alerts evaluated in isolation
By time analyst reviews alert #1, transfer is complete.
```

**Root cause:** System doesn't recognize 5-minute SEQUENCE as one coordinated attack.

### Problem Statement for Deck

"Fraud systems can detect individual anomalies such as a new device, unusual amount, or new beneficiary. The operational problem VYŪH targets is that related anomalies can occur as a short, coordinated sequence, creating either fragmented alerts or insufficient context for rapid review. VYŪH reconstructs that sequence and produces one explainable workflow-level risk assessment before the suspicious transfer completes."

---

## DIFFERENTIATION

### Baseline Approach

- **Method:** Flags if ANY single rule triggers (OR logic)
- **Evaluation:** Each transaction independently
- **Context:** No temporal awareness

### VYŪH Approach

- **Method:** Combines 8 signals + sequence timing into weighted risk score
- **Evaluation:** Distinguishes "coincidental unusual events spread over days" from "coordinated attack within 10 minutes"
- **Context:** Full sequence and temporal awareness

### FP Reduction Mechanisms

1. **Sequence awareness:** "Customer did 3 unusual things on different days" ≠ "Attacker did 3 things in 10 minutes"
2. **Weighted combination:** One signal alone cannot push score above 0.80 threshold
3. **Template matching:** Benign sequences produce weak template matches even with individual anomalies

### Hard-Negative Example

**Scenario:** Customer changes phones, pays sister ₹50K, gets salary ₹80K (all same day)

**Baseline behavior:**
- Flags (new device) + Flags (amount > 3×) + Flags (new beneficiary) = 3 separate alerts

**VYŪH behavior:**
- Scores the sequence
- Salary credit provides context
- Transfer to sister with limited velocity
- Weak template match
- Combined risk = below HOLD_FOR_REVIEW threshold
- Result: ALLOW or SOFT_PROMPT

---

## SAFETY & HUMAN REVIEW

### No BLOCK in MVP Code

**Action enum:** {ALLOW, SOFT_PROMPT, STEP_UP_VERIFY, HOLD_FOR_REVIEW}  
**No BLOCK option exists in scoring engine**  
**Scoring engine cannot call transaction gateway directly**  
**Policy mapper separated from scoring logic**  
**Unit tests validate action boundaries**

### False Positive Handling

- High-risk score ≠ accusation of fraud
- Case enters HOLD_FOR_REVIEW queue
- Analyst sees evidence timeline and can RELEASE
- Customer receives: "For your security, please verify this transaction" — not a fraud accusation

### Feedback Loop

**Logged to SQLite:**
- case_id
- decision (RELEASE / ESCALATE / FALSE_POSITIVE)
- risk_score
- template
- signal_scores
- analyst_id
- timestamp
- reason

**Use:**
- Offline threshold calibration
- Error analysis
- Future model updates

**Note:** No online retraining during MVP (deliberate for reproducibility).

### Design Principle

"VYŪH can recommend and escalate risk; it does not independently seize control of the customer's transaction."

---

## 48-HOUR MVP PLAN

### Canonical Demo — T1 SIM/Device Takeover

```
Account: ACC-DEMO-001
Old device: DEV-OLD-A7F291
New device: DEV-NEW-3B81E0

10:00 - Normal transaction (₹1,200, old device, existing beneficiary)
10:02 - New device login
10:05 - New beneficiary added (VPA-NEW-8842)
10:06 - ₹48,000 transfer to new beneficiary
10:08 - ₹15,000 rapid transfer

VYŪH output:
Risk ≈ 0.87
Action: HOLD_FOR_REVIEW
Template: T1
```

**Actual score must come from scoring engine, not hardcoded.**

### By Hour 48, Reviewers See

1. **Working scoring API**
   - POST /score → returns risk_score, action, signals, template, evidence

2. **Analyst evidence dashboard**
   - Case ID
   - Risk score
   - 8 signal contributions
   - Event timeline
   - RELEASE/ESCALATE/FALSE_POSITIVE buttons

3. **Canonical T1 demo end-to-end**
   - Full attack sequence processed
   - Risk score computed
   - Evidence card generated

4. **Measured validation results**
   - Actual precision/recall/F1/FP rate
   - Vs. baseline comparison

### Fallback (Hour 40)

If integration fails:
- `demo_replay.py` feeds canonical event sequence directly into `score_sequence()` function
- Dashboard connects to replay output
- Scoring engine decoupled from live integration
- Full analyst workflow demonstrable without live backend

### Delivery Format

**Core function (Python):**
```python
def score_sequence(events: list[dict]) -> dict:
    # returns: risk_score, action, signals, template, evidence
```

**API wrapper:** FastAPI  
**Database:** SQLite (not PostgreSQL for MVP)  
**ML:** scikit-learn/XGBoost  
**Frontend:** React/Vite/Tailwind  
**Infra:** Docker

**GPU not required** — CPU laptop sufficient.

---

## PITCH DECK OUTLINE

### 10 Slides — Complete Structure

| Slide | Title | Key Message |
|---|---|---|
| 1 | The Problem | Systems see signals. Attackers see windows. |
| 2 | The User | Fraud analyst drowning in 6,000 analyst-hours/day of noise. |
| 3 | VYŪH Intervention | Detect workflow before funds move. Analyst decides. |
| 4 | From Events to Workflows | 8 signals + sequence = one explainable score. |
| 5 | How It Works | Sequence awareness + weighted combination + template matching. |
| 6 | Impact (Scenario) | 62.5% reduction in false-positive burden (illustrative). |
| 7 | Safety First | No auto-block. Analyst always decides. Code-level guardrails. |
| 8 | 48-Hour MVP | API + dashboard + demo + validation results. |
| 9 | Validation on Synthetic Data | Precision ≥80%, Recall ≥80%, FP <1%. Honest caveats. |
| 10 | From MVP to Production | Real-data validation, operating model, success metrics. |

---

## COMPLETE SLIDE-BY-SLIDE DESIGN BRIEF

### SLIDE 1: THE PROBLEM

```
HEADLINE (60-80pt, bold):
Fraud Systems See Signals. Attackers See Windows.

VISUAL LAYOUT: Two-column split-screen

LEFT COLUMN — Individual Alerts (BROKEN):
- Three stacked red alert boxes, disconnected from each other
- Label: "Individual Alerts"
- Alert 1: New device login → Alert #1
- Alert 2: New beneficiary added → Alert #2
- Alert 3: Large transfer → Alert #3
- Bottom text (small, red): By alert review #1, funds are gone

RIGHT COLUMN — Coordinated Attack (DANGER):
- Clock/timeline showing 5-minute window with red X
- Label: "Coordinated Attack"
- 23:30 — Device login
- 23:33 — Beneficiary added
- 23:35 — ₹30,000 transferred
- 23:37 — Funds dispersed
- Bottom text (bold, red): All within 5 minutes

DESIGN NOTES:
- Dark background (charcoal #2C2C2C or navy #1A1A2E)
- Red accent color (#FF4444)
- Sans-serif font (Inter, Montserrat, Helvetica)
- Plenty of whitespace between sections
- No decorative graphics
```

---

### SLIDE 2: THE USER

```
HEADLINE (60-80pt, bold):
Meet the User: Fraud Risk Analyst

CENTER: Simple icon or silhouette (professional, analytical)

THREE STAT BLOCKS (bold numbers with supporting text below):

BLOCK 1:
100M
Transactions Per Day

BLOCK 2:
300K
Alerts Per Day

BLOCK 3:
6,000
Analyst-Hours Wasted on Noise

SUPPORTING TEXT (below stats, left-aligned, 14-16pt):
Fraud Risk Operations team at major Indian bank (₹100B+ AUM)

PROBLEM STATEMENT (emphasized box, 18-20pt, italicized):
40% of flagged alerts are benign. Alert fatigue is real.

PAIN POINTS (bullet list, right side or below, 14pt):
- Missing coordinated attack patterns
- Delayed response (manual correlation)
- False-positive burden
- Analyst burnout

DESIGN NOTES:
- Use data-forward color palette (blue primary, green positive, orange/red problems)
- Stat blocks with generous padding
- Quote/problem statement in subtle background box (light gray, 20% opacity)
- No images of people — keep abstract and professional
```

---

### SLIDE 3: VYŪH INTERVENTION

```
HEADLINE (60-80pt, bold):
Intervene Before Funds Move

TIMELINE/ATTACK-CHAIN DIAGRAM (horizontal, left to right):

T=0min | New Device Login | [Icon]
T=3min | New Beneficiary | [Icon]
T=6min | High-Value Transfer | [Icon]
T=7min | ⚠️ DETECTION WINDOW (1-2 min) | [Checkmark Icon]
T=8min | Analyst Review HOLD_FOR_REVIEW | [Person Icon]
T=9min | Outcome | [Lock/Release Icon]

KEY INSIGHT (bold, 20-24pt, centered):
VYŪH detects at stage 4. Analyst decides before stage 5.

RIGHT SIDE: Three decision options (equal boxes, 14pt):
- ✓ RELEASE (green)
- ⚠️ ESCALATE (orange)
- ✗ BLOCK (red)

BOTTOM TEXT (14pt, italicized):
Analyst always decides. No auto-block.

DESIGN NOTES:
- Timeline with clean, minimal lines
- Simple stroke-based icons
- Color coding for outcomes consistent throughout
- Central message dominates
```

---

### SLIDE 4: FROM EVENTS TO WORKFLOWS

```
HEADLINE (60-80pt, bold):
Workflow-Aware Detection

LEFT SIDE (50% width):

SUBHEADING (18pt, bold):
Traditional: OR Logic

FORMULA (monospace, 16pt):
IF (amount > 3x)
   OR (new_device)
   OR (new_beneficiary)
THEN FLAG

RESULT (14pt, red):
Result: 3 separate alerts per scam

---

RIGHT SIDE (50% width):

SUBHEADING (18pt, bold):
Sequence-Aware: Weighted Scoring

8 SIGNALS WITH WEIGHTS (bar chart or percentage list):

Behavioral Deviation ████████░░ 20%
Device/Auth Change ████████░░ 20%
Amount Anomaly ███████░░░ 15%
Beneficiary Novelty ███████░░░ 15%
Velocity (10min/60min) █████░░░░░ 10%
Session Context █████░░░░░ 10%
Template Match ██░░░░░░░░ 5%
Network/Destination ██░░░░░░░░ 5%
───────────────────────────────
Single Risk Score: 0.87

RESULT (14pt, green):
Result: One explainable workflow-level score

DESIGN NOTES:
- 50/50 split left-right
- Use actual bar chart for 8 signals
- Monospace for code/formulas
- Final score in large text
- Green accent for VYŪH vs. red for baseline
```

---

### SLIDE 5: HOW IT WORKS

```
HEADLINE (60-80pt, bold):
Three Mechanisms

THREE EQUAL COLUMNS:

---

COLUMN 1 — SEQUENCE AWARENESS

SUBHEADING (18pt, bold):
Sequence Awareness

ICON: Clock or timeline

KEY QUESTION (16pt, italicized):
Is this coordinated or coincidental?

EXAMPLE 1 (12pt):
Device change day 1 + salary day 3 = Not suspicious

EXAMPLE 2 (12pt):
Device change + beneficiary + transfer within 10 min = Attack

---

COLUMN 2 — WEIGHTED COMBINATION

SUBHEADING (18pt, bold):
Weighted Combination

ICON: Network/nodes connected

KEY POINT (16pt, italicized):
One signal does not equal alert

EXAMPLE 1 (12pt):
New device alone: 0.2/1.0

EXAMPLE 2 (12pt):
New device + new beneficiary + velocity: 0.7/1.0

---

COLUMN 3 — TEMPLATE MATCHING

SUBHEADING (18pt, bold):
Template Matching

ICON: Pattern/puzzle piece

KEY POINT (16pt, italicized):
Recognize attack workflows

WORKFLOWS (12pt, bullet list):
- SIM takeover
- Phishing/credential theft
- Remote-access fraud

CLOSING (12pt):
Weak match = lower risk even with anomalies

DESIGN NOTES:
- Three equal-width columns with thin vertical separators (20% opacity)
- Symbolic icons, not literal
- Consistent visual weight per column
- Example text in light gray or secondary color
```

---

### SLIDE 6: EXPECTED IMPACT (SCENARIO)

```
HEADLINE (60-80pt, bold):
Impact: Analyst Hours Freed

LARGE NUMBER VISUAL (centered, 120pt+, bold):
62.5%
Reduction in False-Positive Burden
(Illustrative Scenario)

---

TWO-COLUMN BREAKDOWN (below):

LEFT COLUMN — CURRENT STATE:
100M transactions/day
0.3% flagged = 300K alerts/day
40% benign = 120K false alerts
Analyst capacity: 6,400 alerts/day reviewed
Result: 6,000 analyst-hours/day wasted

RIGHT COLUMN — WITH VYŪH:
100M transactions/day
0.3% flagged = 300K alerts/day
15% benign = 45K false alerts
Analyst capacity: 6,400 alerts/day reviewed
Result: 2,250 analyst-hours/day on noise

---

LARGE CALLOUT (center, 24pt, bold, green):
3,750 hours freed per day
→ Better fraud catch rate
→ Faster analyst response
→ Reduced customer friction

DISCLAIMER (10pt, italicized, gray, bottom):
⚠️ Illustrative scenario, not measured prototype performance

DESIGN NOTES:
- 62.5% should be HUGE (100+ pt)
- Two-column comparison with clear visual distinction
- Callout box with green accent color
- Disclaimer clearly visible but not prominent
```

---

### SLIDE 7: SAFETY & HUMAN REVIEW

```
HEADLINE (60-80pt, bold):
Safety First: Always Human

CENTRAL PRINCIPLE (24pt, bold, italicized):
VYŪH scores risk. Analyst decides. Gateway executes.

---

LEFT SIDE (40% width) — FLOW DIAGRAM:

Scoring Engine
     ↓
HOLD_FOR_REVIEW (max action)
     ↓
Analyst Reviews Evidence
     ↓
Analyst Decision:
├─ RELEASE ✓
├─ ESCALATE ⚠️
└─ BLOCK ✗
     ↓
Transaction Gateway Executes

---

RIGHT SIDE (60% width) — SAFETY GUARDRAILS:

SUBHEADING (18pt, bold):
Code-Level Protections

GUARDRAIL 1 (16pt):
✓ No BLOCK in scoring engine — max action is HOLD_FOR_REVIEW

GUARDRAIL 2 (16pt):
✓ No direct gateway access — scoring engine cannot call transaction gateway

GUARDRAIL 3 (16pt):
✓ Policy mapper isolated — separated from scoring logic

GUARDRAIL 4 (16pt):
✓ Unit tests — action boundaries validated

---

FALSE POSITIVES:

SUBHEADING (18pt, bold):
Handling Legitimate Transactions

- Analyst can release legitimate transactions
- Feedback logged (case ID, decision, score, signals)
- Monthly threshold calibration
- No online retraining (deliberate for reproducibility)

DESIGN NOTES:
- Left: flow diagram, clean boxes with arrows
- Right: checkmark bullets with light background boxes
- Central principle prominent
- Green for safety, neutral for process flow
```

---

### SLIDE 8: 48-HOUR MVP

```
HEADLINE (60-80pt, bold):
What Reviewers See in 48 Hours

FOUR DELIVERABLE BOXES (2x2 grid):

---

BOX 1 (top-left):

TITLE (18pt, bold):
Scoring API

ICON: Code brackets or API endpoint

CONTENT (14pt, monospace):
POST /score
↓
risk_score (0.87)
action (HOLD_FOR_REVIEW)
signals (8 scores)
template_match (T1)
evidence (timeline)

---

BOX 2 (top-right):

TITLE (18pt, bold):
Evidence Dashboard

ICON: Dashboard/monitor

CONTENT (14pt):
- Case ID
- Risk score & visualization
- 8 signal contributions
- Event timeline
- Analyst action buttons

---

BOX 3 (bottom-left):

TITLE (18pt, bold):
T1 Canonical Demo

ICON: Checkmark or success

CONTENT (14pt):
- Device takeover flow
- 5 events, 10-min window
- Risk score: 0.87
- Correct detection: ✓

---

BOX 4 (bottom-right):

TITLE (18pt, bold):
Validation Results

ICON: Chart or metrics

CONTENT (14pt):
- Precision, Recall, F1
- FP rate
- Baseline vs. VYŪH comparison
- Actual measured numbers

---

BOTTOM SECTION (18pt, bold, italicized):
Fallback if integration fails (hour 40): Deterministic replay engine + sandbox dashboard. Full analyst workflow demonstrable.

DESIGN NOTES:
- Four equal boxes with subtle borders or background
- Icons consistent with previous slides
- Monospace for code
- Fallback less prominent but visible
```

---

### SLIDE 9: VALIDATION ON SYNTHETIC DATA

```
HEADLINE (60-80pt, bold):
Measured on Synthetic Data

LEFT SIDE (30% width):

SUBHEADING (16pt, bold):
Test Set Composition

Benign: 5,000 sequences
Scams: 1,000 sequences
        (200 per template)

Total: 6,000 sequences

Golden set: 2,000 benign + 500 scam
            (held out, evaluated once)

---

RIGHT SIDE (70% width):

METRICS COMPARISON TABLE (16pt):

Metric          | Baseline | VYŪH    | Target
Precision       | ~60%     | [val]   | ≥80%
Recall          | ~75%     | [val]   | ≥80%
F1 Score        | ~67%     | [val]   | ≥80%
FP Rate         | ~40%     | [val]   | <1%
FP per 1K benign| ~400     | [val]   | <10

---

HONEST CAVEATS (below table, 12pt, italicized, gray):
- Synthetic, not real UPI transaction data
- Real-world performance requires institution-specific calibration
- Adversarial adaptation: fraudsters will evolve; VYŪH requires updates
- Results = prototype validation, not production claims

DESIGN NOTES:
- Left: clean data boxes, monospace font
- Right: metrics table with color distinction baseline vs. VYŪH
- Table easy to scan
- Caveats clearly visible
```

---

### SLIDE 10: FROM MVP TO PRODUCTION

```
HEADLINE (60-80pt, bold):
Path to Production

THREE VERTICAL SECTIONS (33% width each):

---

SECTION 1:

SUBHEADING (18pt, bold):
Real-Data Validation

✓ Run on anonymized UPI transactions
✓ Calibrate thresholds to actual distribution
✓ Measure false-positive impact on customers
✓ Tune recall vs. analyst capacity

---

SECTION 2:

SUBHEADING (18pt, bold):
Operating Model

- Fraud Risk team reviews HOLD_FOR_REVIEW cases
- Target review time: <2 minutes per case
- Monthly threshold tuning (based on feedback)
- Quarterly model updates (new attack patterns)
- Continuous adversarial monitoring

---

SECTION 3:

SUBHEADING (18pt, bold):
Success Metrics

₹ Fraud loss prevented (per month)
⏱ Analyst efficiency (alerts reviewed/day)
🔴 False-positive rate (customer friction)
🎯 Fraud recall (% of scams caught)
⚡ System latency (<2 min to detection)

---

BOTTOM — INTEGRATION PATHWAY (16pt, italicized, centered):
VYŪH is a contextual risk-assessment layer for India's digital-payment infrastructure.

DESIGN NOTES:
- Three vertical columns with vertical dividers
- Consistent visual structure per section
- KPIs use icons and large numbers
- Bottom statement is mission/vision closing
```

---

## DESIGN SYSTEM SPECIFICATIONS

### Typography

- **Headline:** 60-80pt, bold, sans-serif (Inter, Montserrat, Helvetica)
- **Subheading:** 16-20pt, bold
- **Body:** 14-16pt, regular
- **Small text:** 12-14pt, secondary color
- **Monospace for code:** 14-16pt

### Color Palette

- **Background:** Dark charcoal #2C2C2C or navy #1A1A2E
- **Primary text:** White #FFFFFF
- **Accent positive/solution:** Green #00D084 or #2ECC71
- **Accent problem/danger:** Red #FF4444 or #E74C3C
- **Accent warning:** Orange #F39C12 or #FFA500
- **Secondary text:** Light gray #AAAAAA
- **Borders/dividers:** Gray 20% opacity

### Layout

- **Aspect ratio:** 16:9 (standard presentation)
- **Margins:** 80px on all sides
- **Whitespace:** 40%+ empty space per slide (crucial)
- **Grid alignment:** 8px or 16px multiples
- **Padding consistency:** All boxes and containers
- **No decorative graphics or animations**

### Icons

- Simple stroke-based (not filled)
- Consistent across all slides
- Symbolic, not literal
- Single color (white or accent)
- Minimal complexity

### Data Visualization

- Bar charts for comparisons (8 signals, metrics)
- Timelines for attack flows
- Simple boxes/containers for grouped info
- Color-coded for decision states (green/orange/red)
- Clean, minimal style (no shadows, gradients, or effects)

### Tone & Content

- **Professional, direct, no fluff**
- Numbers dominate text
- Minimal narrative (let data tell story)
- Honest about limitations (synthetic, illustrative, caveats)
- Avoid jargon; use plain language

---

## CLAIMS DISCIPLINE

### NEVER Claim

- Production-grade fraud detection
- Validated performance on real UPI/bank data
- 62.5% FP reduction as a measured result
- Automatic blocking
- "98% of alerts never reviewed" without source
- Specific real-world fraud-loss numbers

### ALWAYS Label

- 100M txns/day → "Scenario assumption"
- 0.3% alert rate → "Scenario assumption"
- 40% benign-alert rate → "Scenario assumption"
- 62.5% reduction → "Illustrative scenario calculation"
- <1% FP → "Synthetic validation target"
- 0.87 risk score → "Demo target; actual output from engine"

### Synthetic Data Caveat (for deck)

"VYŪH is validated on generated transaction/event sequences designed to represent documented fraud workflows. Synthetic distributions cannot fully reproduce real UPI behaviour, customer heterogeneity, operational fraud labels, or adversarial adaptation. Results demonstrate prototype performance, not production effectiveness."

---

## PENDING ACTIONS

- [ ] Finalize 10-slide deck copy (currently in design brief)
- [ ] Write 3-page architecture section
- [ ] Create system diagram (architecture flow)
- [ ] Combine into one PDF submission
- [ ] Disclose AI-generated content in appendix
- [ ] Name team members and assign workstreams
- [ ] Replace metric placeholders with actual test results (after 48-hour build)

---

## REFERENCE

**Transcript:** `/mnt/transcripts/2026-10-03-20-14-51-vyuh-hackathon-round1-prep.txt`  
**Status:** Round 1 Submission Ready  
**Last Updated:** October 4, 2026  
**Next Steps:** Build MVP, measure validation results, finalize PDF submission