# VYŪH Team Responsibilities

## Team

| Member | Primary area |
|---|---|
| Nachiketa Jha | System architecture, detection logic, research engineering, integration |
| Krishna Rustagi | Frontend and analyst-facing interface |
| Ananya Singh | Backend and service integration |
| Ishika | Communication, presentation, and project documentation |

This is the four-member VYŪH team. Responsibilities describe primary ownership, not exclusive contribution.

## Responsibility areas

### System architecture
Primary owner: **Nachiketa Jha**

- Maintain system-level architecture and boundaries.
- Maintain architecture documentation and diagrams.
- Review changes that alter system behaviour or component boundaries.

### Detection and risk intelligence
Primary owner: **Nachiketa Jha**

- Maintain the eight-signal detection model.
- Maintain scam-workflow template definitions.
- Maintain risk-score construction and policy thresholds.
- Define detection experiments and evaluation criteria.

### Backend and service layer
Primary owner: **Ananya Singh**

- Implement backend service boundaries.
- Integrate the detection engine with service interfaces.
- Maintain request/response handling, validation, and backend tests.
- Document implementation decisions affecting public system contracts.

### Frontend and analyst interface
Primary owner: **Krishna Rustagi**

- Build the analyst-facing interface.
- Represent risk scores, evidence, workflow context, and policy actions clearly.
- Preserve the distinction between automated assessment and human review.

### Research, documentation, and communication
Primary owners: **Nachiketa Jha, Ishika**

- Maintain research notes and source references.
- Document assumptions and evidence boundaries.
- Keep project documentation synchronized with implementation.
- Maintain presentation materials and explanatory visuals.
- Ensure public-facing claims match project documentation.

Presentation materials are downstream artifacts and must not become the source of truth for system behaviour.

## Shared responsibilities

All team members are responsible for reviewing significant changes affecting their area, reporting inconsistencies between documentation and implementation, avoiding unsupported performance or production-readiness claims, protecting synthetic and sensitive project data, and keeping changes traceable through Git history.

## Decision ownership

| Decision type | Primary owner | Reviewers |
|---|---|---|
| Architecture | Nachiketa | Relevant technical owners |
| Detection logic | Nachiketa | Backend + research contributors |
| Risk scoring/policy | Nachiketa | Backend + research contributors |
| Backend contract | Ananya Singh | Nachiketa |
| Frontend behaviour | Krishna Rustagi | Backend + architecture owner |
| Research claims | Nachiketa / Ishika | Relevant technical owners |
| Presentation claims | Ishika | Relevant technical owners |

## Documentation ownership

| Area | Primary owner |
|---|---|
| docs/ technical specifications | Nachiketa |
| architecture/ | Nachiketa |
| research/ | Nachiketa + Ishika |
| data/ contracts and generator specifications | Nachiketa |
| Backend implementation | Ananya Singh |
| Frontend implementation | Krishna Rustagi |
| presentation/ | Ishika |
| submission/ | Team, with technical review by relevant owners |

## Current project stage

The project is currently prioritizing documentation, architecture, research definitions, data contracts, and reproducible specifications.

Implementation responsibilities become active as the corresponding engineering components are introduced.

Documentation remains the primary source of truth for intended system behaviour.