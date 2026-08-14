# Data Model

This document defines the public conceptual model for Book of Mormon Open Data. The exact JSON schemas will live in `schema/` and may evolve before the first stable release.

## Core principle

The dataset separates source material, atomic claims, accepted facts, and editorial prose.

```text
source → evidence → claim → review decision → published fact → editorial prose
```

A consumer should be able to inspect the public files and determine both **what is asserted** and **why it was accepted**.

## Entities

Entities are app-independent canonical records with stable project-owned identifiers.

Initial entity types:

- `person`
- later: `place`, `group`, `book`, `event`

External identifiers such as Wikidata QIDs are attributes, never primary keys.

Expected person fields include:

- stable project identifier
- slug
- canonical display name
- disambiguator
- aliases
- external identifiers
- publication status

## Claims

Claims are atomic factual propositions. Examples:

```text
nephi-son-of-lehi -- father --> lehi-prophet
moroni-son-of-mormon -- father --> mormon
```

Claims should carry:

- stable claim identifier
- subject entity
- predicate
- object entity or literal value
- claim status
- confidence/evidence grade
- provenance
- supporting evidence identifiers
- review metadata

Symmetric relationships such as sibling/spouse should have a canonical storage direction to prevent duplicates.

## Evidence

Evidence records explain why a claim is supportable.

Evidence may include:

- scripture references
- speaker attribution
- short evidence excerpts where legally appropriate
- Wikidata statement identifiers
- deterministic rule output
- review notes

Canonical scripture references should be stored as book/chapter/verse coordinates. Database row IDs are implementation details and should not appear in public source records.

## Sources

Source records identify external inputs and their licensing/provenance.

At minimum, source records should include:

- source identifier
- title/name
- creator/author when applicable
- source URL or permanent identifier
- license
- retrieval/version information when relevant
- how the source was used
- transformations made by this project

## Editorial content

Summaries and biographies are derivative editorial outputs, not primary evidence.

Published editorial prose should record:

- text
- entity identifier
- content type
- claim identifiers supporting each factual sentence or clause
- author/generator provenance where retained
- review status
- review metadata

The target standard is zero unsupported factual sentences in released editorial prose.

## Review states

The final vocabulary will be fixed before the first stable release. The intended distinction is between states such as:

- candidate
- scripture-verified
- externally corroborated
- model-reviewed
- human-reviewed
- production-approved
- rejected
- unresolved

A model generating or reviewing a record must never be represented as equivalent to independent human approval.
