# Contributing to VYŪH

VYŪH is maintained as a research and engineering project. Contributions should preserve the distinction between documented evidence, system specification, implementation, and experimental results.

## Before making a change

1. Identify the document or contract that currently defines the behaviour.
2. Check related documents for dependencies.
3. Determine whether the change affects architecture, schemas, detection logic, risk scoring, privacy, or evaluation.
4. Update relevant documentation together with the change.
5. Do not introduce unspecified behaviour without documenting it as a proposal or implementation decision.

## Source-of-truth hierarchy

When project materials overlap:

1. Current project specification and approved decisions
2. Architecture and technical contracts
3. Research documentation and references
4. Implementation documentation
5. Presentation and submission artifacts

Presentation material must not silently redefine the technical system.

## Documentation standards

Documentation should:

- use precise technical terminology
- distinguish requirements from assumptions
- distinguish observed evidence from inference
- identify open questions instead of inventing answers
- link related project documents
- avoid unsupported production or performance claims
- preserve version information where contracts change

Research material should use the project's evidence categories:

- Observed
- Specified
- Hypothesis
- Inference
- Implementation decision
- Open question

## Changing technical contracts

Technical contracts include event schemas, dataset manifests, signal definitions, scoring equations, policy thresholds, API contracts, and architecture boundaries.

A contract change should document:

1. The reason for the change.
2. The affected files.
3. Compatibility implications.
4. Migration or fixture changes.
5. Updated validation or test requirements.

Do not modify a versioned schema solely to make an implementation convenient.

## Research contributions

External sources should be recorded in `research/references.md` with the claim or workflow they support.

Do not treat a source as evidence for claims it does not establish. Clearly distinguish source-derived facts from VYŪH design decisions.

## Data contributions

VYŪH currently uses synthetic-first data.

Do not add real customer payment information, bank-account information, UPI IDs, phone numbers, email addresses, authentication secrets, or unnecessary sensitive personal information to the repository.

Synthetic fixtures must follow the canonical event schema and remain clearly identified as synthetic.

## Detection and scoring changes

Changes to detection logic or risk scoring should document effects on:

- signal definitions
- signal weights
- template matching
- risk thresholds
- false positives
- false negatives
- validation methodology
- explainability

Do not report an improvement as a measured result until it has been evaluated using the defined validation procedure.

## Architecture changes

Architecture changes should update `architecture/README.md` and affected diagrams or technical documents.

Changes crossing component boundaries should be reviewed by the owners identified in `team/responsibilities.md`.

## Implementation status

Do not document planned functionality as implemented functionality.

Use explicit status language:

- **Specified** — defined by the project design.
- **Planned** — intended future work.
- **Implemented** — present in the repository.
- **Validated** — evaluated using a documented procedure.
- **Measured** — supported by recorded experimental results.

## Commit conventions

Prefer small, focused commits with descriptive messages.

Examples:

```text
docs: clarify temporal session model
docs: add threat workflow reference
schema: define event validation contract
test: add template matching cases
feat: implement sequence scoring
fix: correct risk threshold handling
```

Avoid combining unrelated documentation, implementation, and generated artifacts in one commit when they can be separated cleanly.

## Review checklist

- [ ] The change has a clear purpose.
- [ ] Related documentation has been updated.
- [ ] Terminology matches existing VYŪH definitions.
- [ ] No unsupported claims were introduced.
- [ ] Schema or contract changes are versioned when required.
- [ ] Synthetic data contains no unnecessary real personal information.
- [ ] Tests or validation requirements are updated where applicable.
- [ ] Links to affected documentation still resolve.
- [ ] The commit represents a coherent change.

## Current development boundary

The current project phase prioritizes documentation, architecture, research definitions, data contracts, and reproducible specifications.

Implementation should follow the documented contracts rather than becoming an alternative source of truth.