# Submission Artifacts

## Purpose

This directory contains artifacts prepared for external evaluations, competitions, demonstrations, or other formal submissions involving VYŪH.

Submission materials are downstream representations of the project. They are not the source of truth for VYŪH's architecture, detection logic, research claims, or data contracts.

## What belongs here

Examples include:

- architectural overviews prepared for a submission
- pitch decks
- combined submission PDFs
- submission-specific forms or supporting documents
- final, versioned submission packages

Store only final or clearly versioned artifacts. Working drafts should remain outside this directory unless they are necessary for reproducibility.

## Relationship to the project

The relationship is:

```text
VYŪH research + specification + engineering
                    ↓
        Project architecture and evidence
                    ↓
          Submission-specific packaging
                    ↓
             External evaluation
```

A submission may simplify, reorder, or selectively present project material to satisfy an external format. Such presentation constraints must not be treated as changes to the underlying VYŪH system.

## Source of truth

For technical definitions, use the project documentation under:

- `docs/` — specifications and technical decisions
- `architecture/` — system architecture
- `research/` — research evidence and workflow definitions
- `data/` — data and schema contracts

If a submission artifact conflicts with the current project documentation, the discrepancy should be resolved explicitly rather than silently propagating the submission wording into the core project.

## Claims discipline

Submission materials must distinguish between:

- specified behaviour
- implemented behaviour
- measured results
- illustrative scenarios
- future plans

Do not present an illustrative number as a measured result or a planned component as an implemented component.

The submission should not claim production readiness, real-world validation, automatic transaction blocking, or measured operational impact unless the project has actually established those claims through documented evidence.

## Versioning

When a submission artifact is finalized, record enough information to identify:

- submission or evaluation context
- artifact type
- version or date
- relationship to the VYŪH project version, where applicable

For example:

```text
submission/
├── round-1/
│   ├── architectural-overview.pdf
│   ├── pitch-deck.pdf
│   └── README.md
└── README.md
```

The exact directory structure may evolve with future submission requirements.

## Reproducibility

Where practical, a submission should be reproducible from project documentation and referenced source artifacts.

Generated PDFs, decks, diagrams, and other derived artifacts should not become the only record of the technical decisions they contain.

## Current status

Submission materials are maintained separately from the core VYŪH research and engineering documentation.

The project may participate in external evaluations, but the repository is intended to remain useful beyond any individual submission.