# VYŪH Team Responsibilities

## Purpose

This document defines ownership boundaries for the VYŪH project. Responsibilities are organized around the actual research and engineering work rather than a single event or submission.

Ownership may evolve as the project moves from specification to implementation and validation.

## Team

| Member | Primary area |
|---|---|
| Nachiketa Jha | System architecture, detection logic, research engineering, integration |
| Krishna Rustagi | Frontend and analyst-facing interface |
| Ananya Singh | Backend and service integration |
| Ishika | Communication, presentation, and project documentation |
| Ananya | Communication, presentation, and project documentation |

These areas describe primary ownership, not exclusive contribution. Technical decisions should remain visible to the full team where they affect system behaviour.

## Responsibility areas

### System architecture

Primary owner: **Nachiketa Jha**

- Maintain the system-level architecture.
- Maintain boundaries between normalization, session construction, detection, scoring, policy, evidence, and review.
- Keep architectural decisions consistent with the project specification.
- Review changes that alter system behaviour or component boundaries.
- Maintain architecture documentation and diagrams.

### Detection and risk intelligence

Primary owner: **Nachiketa Jha**

- Maintain the eight-signal detection model.
- Maintain scam-workflow template definitions.
- Maintain risk-score construction and policy thresholds.
- Define detection experiments and evaluation criteria.
- Review changes that affect false-positive or false-negative behaviour.

Relevant documentation:

- [`docs/detection-logic.md`](../docs/detection-logic.md)
- [`docs/risk-scoring.md`](../docs/risk-scoring.md)
- [`docs/threat-model.md`](../docs/threat-model.md)
- [`research/scam-workflows.md`](../research/scam-workflows.md)

### Backend and service layer

Primary owner: **Ananya Singh**

- Implement backend service boundaries once implementation begins.
- Integrate the detection engine with service interfaces.
- Maintain request/response handling and validation.
- Maintain backend tests and integration tests.
- Document implementation decisions that affect the public system contract.

Backend implementation must follow the documented event schema and detection contract rather than silently redefining them.

### Frontend and analyst interface

Primary owner: **Krishna Rustagi**

- Build the analyst-facing interface once implementation begins.
- Represent risk scores, evidence, workflow context, and policy actions clearly.
- Preserve the distinction between automated assessment and human review.
- Maintain frontend tests and interface documentation where required.

The interface should not imply capabilities that the backend does not provide.

### Research and documentation

Primary owners: **Nachiketa Jha, Ishika, Ananya**

- Maintain research notes and source references.
- Document assumptions and evidence boundaries.
- Keep project documentation synchronized with the implemented system.
- Distinguish observed evidence, specified behaviour, hypotheses, inferences, and implementation decisions.
- Review public-facing claims for accuracy and support.

The research layer should not introduce unsupported claims into technical documentation.

### Communication and presentation

Primary owners: **Ishika, Ananya**

- Translate documented technical work into clear project communication.
- Maintain presentation materials and explanatory visuals.
- Ensure claims in presentations match the project documentation.
- Coordinate narrative consistency across project materials.

Presentation materials are downstream artifacts. They should not become the source of truth for system behaviour.

## Shared responsibilities

All team members are responsible for:

- Reviewing significant changes affecting their area.
- Reporting inconsistencies between documentation and implementation.
- Avoiding unsupported performance or production-readiness claims.
- Protecting synthetic and sensitive project data.
- Keeping changes traceable through Git history.

## Decision ownership

| Decision type | Primary owner | Reviewers |
|---|---|---|
| Architecture | Nachiketa | Relevant technical owners |
| Detection logic | Nachiketa | Backend + research contributors |
| Risk scoring/policy | Nachiketa | Backend + research contributors |
| Backend contract | Ananya Singh | Nachiketa |
| Frontend behaviour | Krishna Rustagi | Backend + architecture owner |
| Research claims | Research owners | Relevant technical owners |
| Presentation claims | Ishika / Ananya | Relevant technical owners |

## Documentation ownership

| Area | Primary owner |
|---|---|
| `docs/` technical specifications | Nachiketa |
| `architecture/` | Nachiketa |
| `research/` | Nachiketa + research contributors |
| `data/` contracts and generator specifications | Nachiketa |
| Backend implementation | Ananya Singh |
| Frontend implementation | Krishna Rustagi |
| `presentation/` | Ishika + Ananya |
| `submission/` | Team, with technical review by relevant owners |

Ownership does not grant unilateral authority to change another component's contract. Cross-boundary changes should be reviewed by the affected owners.

## Current project stage

The project is currently prioritizing documentation, architecture, research definitions, data contracts, and reproducible specifications.

Implementation responsibilities become active as the corresponding engineering components are introduced.

Until then, documentation should remain the primary source of truth for intended system behaviour.