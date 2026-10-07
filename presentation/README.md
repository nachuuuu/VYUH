# VYŪH Presentation

## Purpose

This directory contains presentation materials used to explain VYŪH to technical, research, evaluation, or external audiences.

Presentation artifacts are derived communication layers. They summarize the project; they do not redefine its technical behaviour.

## What belongs here

Examples include:

- presentation source material
- slide decks
- presentation-specific diagrams
- speaker notes
- supporting visual assets
- exported presentation files

Final exported decks may also be copied into `submission/` when they form part of a formal submission package.

## Source of truth

Technical content should be derived from the core project documentation:

- `docs/` — specifications and technical decisions
- `architecture/` — system architecture
- `research/` — research evidence and workflow definitions
- `data/` — data and schema contracts

The presentation should not introduce a new signal, threshold, workflow, architectural component, dataset result, or performance claim without a corresponding project-level definition or documented evidence.

## Presentation structure

A presentation may organize the project around:

1. Problem and motivation
2. Threat and scam workflows
3. VYŪH approach
4. Temporal detection architecture
5. Signals and workflow matching
6. Risk scoring and policy
7. Evidence and human review
8. Data and validation methodology
9. Current status and limitations
10. Future roadmap

The exact structure should be adapted to the audience and purpose.

## Claims discipline

Presentations must clearly distinguish:

- specified system behaviour
- implemented functionality
- measured experimental results
- illustrative examples
- planned future work

Illustrative scenarios must not be presented as measured operational outcomes.

In particular, do not present the illustrative analyst-hours reduction scenario as a measured VYŪH result.

Do not imply production deployment, real-world UPI validation, automatic transaction blocking, or production-scale performance unless those claims are supported by project evidence.

## Visual consistency

Diagrams should match the architecture documentation.

When a diagram simplifies the system for presentation, the simplification should preserve the meaning of the underlying architecture.

Recommended visual assets should have stable names and, where practical, source files should be retained alongside exports.

## Versioning

Final presentation artifacts should be identifiable by:

- purpose or audience
- version or date
- relationship to the relevant project state

Example:

```text
presentation/
├── README.md
├── source/
│   └── vyuh-overview.md
├── decks/
│   └── vyuh-overview-v1.pdf
└── assets/
    └── architecture/
```

The exact structure may evolve as presentation tooling is introduced.

## Relationship to submissions

A presentation can be reused for a hackathon, research discussion, demo, internal review, or external briefing.

When a presentation is adapted for a specific submission, the submission-specific copy belongs in `submission/`.

The reusable project presentation remains here.

## Current status

Presentation materials are maintained separately from the core technical documentation so that communication requirements do not distort the underlying VYŪH specification.