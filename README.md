# Book of Mormon Open Data

A high-quality, citation-first structured dataset about people in the Book of Mormon.

The project is designed to make every published factual claim traceable. Relationships, identities, summaries, biographies, and other derived content should be understandable without trusting the software or model that produced them.

> **Status:** Early development. The repository structure is public, but the first validated dataset release has not been published yet.

## Goals

Book of Mormon Open Data aims to produce a dataset that is:

- **Cited** — factual claims include machine-readable evidence and source provenance.
- **Auditable** — users can trace published facts back to scripture passages and external structured sources.
- **Conservative** — uncertain, ambiguous, or weakly supported claims are kept out of the canonical release.
- **Reusable** — the public data is independent of any one application and uses stable identifiers and documented schemas.
- **Transparent about editorial content** — summaries and biographies are treated as derived prose, not primary-source facts, and must be linked back to accepted claims.
- **Open-source ready** — releases are intended to be useful to developers, researchers, educators, and scripture-study projects.

## What this repository contains

This is the **clean public dataset repository**. It contains released or release-candidate data, schemas, methodology, provenance, and review records.

It intentionally does **not** contain the private extraction, model orchestration, experimentation, or generation pipeline used to produce candidate data.

```text
book-of-mormon-open-data/
├── README.md
├── manifest.json
├── docs/
│   ├── DATA_MODEL.md
│   ├── METHODOLOGY.md
│   ├── REVIEW_POLICY.md
│   └── RELEASE_POLICY.md
├── schema/
├── sources/
├── entities/
├── claims/
├── evidence/
├── editorial/
├── review/
└── releases/
```

## Data model

The project separates four concepts that are easy to accidentally blur together:

1. **Sources** — scripture passages, Wikidata statements, licensed speaker-attribution data, and other explicitly documented inputs.
2. **Claims** — atomic factual propositions such as `Nephi -- father --> Lehi`.
3. **Accepted facts** — claims that satisfy the project's verification and review requirements.
4. **Editorial content** — summaries and biographies written from accepted facts and accompanied by claim-level provenance.

The intended trace is:

```text
published sentence
    ↓
approved claim(s)
    ↓
evidence
    ↓
source
```

See [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) for the evolving specification.

## Source policy

Initial source classes include:

- **Book of Mormon scripture text** for primary evidence. Exact edition/provenance will be documented before the first public data release.
- **Book of Mormon With Voices Identified** by John Hilton III and Shon D. Hopkin for speaker attribution, distributed through BYU ScholarsArchive under CC BY 4.0.
- **Wikidata structured data** as an external candidate/corroboration source under CC0. Wikidata descriptions and other prose are not used as biographies.
- **Original editorial content** such as normalized identities, review decisions, summaries, and biographies. Generated prose is not considered validated merely because it was produced by a model.

A Wikidata reference to another website or publication does not grant permission to reproduce that referenced source's wording.

See [`sources/README.md`](sources/README.md) and [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Publication standard

The project follows a simple rule:

> **No factual statement belongs in the canonical public dataset without machine-readable provenance explaining where it came from and why it was accepted.**

For generated or editorial prose:

> **Every factual sentence in a published summary or biography should resolve to already accepted claims.**

Unresolved, rejected, or weakly supported candidates are kept separate from canonical release data.

## Generation pipeline

The production pipeline is maintained privately. It may use deterministic parsing, local compute, language models, external APIs, automated cross-checks, and human review.

Only the resulting release data, provenance, methodology, schemas, and appropriate review records are published here. This keeps the public repository focused on the dataset rather than on internal experimentation.

## Versioning

Stable releases will be versioned and accompanied by a release manifest describing:

- schema version
- dataset version
- source snapshot/version information
- entity and claim counts
- validation results
- known limitations
- changes from the previous release

No current data should be treated as a stable research release until a versioned release is published.

## Licensing

A repository-level data license will be finalized before the first stable release. Upstream source licenses and attribution requirements are tracked independently in `sources/` and must be preserved regardless of the final repository-level license.

The expected project license is **Creative Commons Attribution 4.0 International (CC BY 4.0)**, subject to final source/provenance review.

## Contributing and corrections

The correction workflow will be documented before the first stable release. The intended model is evidence-first: proposed corrections should identify the entity or claim, explain the issue, and provide supporting primary or appropriately licensed source evidence.

## Project scope

The first major dataset focuses on **people in the Book of Mormon**, including identities, aliases, speaker mappings, family relationships, scripture evidence, summaries, and biographies.

The schema is designed to expand later to places, groups, books, events, and other structured entities without replacing the person identifiers used by early releases.
