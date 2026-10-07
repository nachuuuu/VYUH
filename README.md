# VYŪH

### Temporal Risk Intelligence for UPI Fraud

VYŪH is a proposed transaction-risk engine designed to detect AI-enabled and socially engineered UPI fraud by identifying suspicious temporal sequences of events rather than evaluating transactions only in isolation.

## Project Status

**Current phase:** Architecture, research, and MVP specification

The repository contains the system specification, threat model, architecture, research material, data design, and submission structure. Implementation code will be added as the MVP is built.

## Repository Structure

- `docs/` — Core technical specifications and design decisions
- `architecture/` — System architecture and flow diagrams
- `research/` — Threat research, scam workflows, and references
- `data/` — Data schemas and synthetic-data documentation
- `submission/` — Submission-specific artifacts
- `presentation/` — Presentation-related materials
- `team/` — Team responsibilities and project ownership
- `assets/` — Logos, screenshots, and other project visuals

## Core Idea

```text
Transaction / Behavioral Events
            ↓
      Event Normalization
            ↓
       Sessionization
            ↓
       Signal Extraction
            ↓
   Temporal Pattern Matching
            ↓
         Risk Score
            ↓
       Policy Mapper
            ↓
ALLOW / SOFT_PROMPT / STEP_UP_VERIFY / HOLD_FOR_REVIEW
            ↓
      Evidence + Human Review
```

The scoring engine does not automatically block transactions. High-risk cases are routed to the review boundary rather than directly controlling a transaction gateway.

## Disclaimer

VYŪH is a research and prototype project. The designs in this repository represent the proposed MVP architecture and are not a production UPI fraud-detection system.
