# Release Policy

A public release is a reviewed dataset artifact, not a dump of internal pipeline output.

## Release requirements

Before a stable release is published:

- schemas are versioned and documented
- all canonical entities have stable project-owned identifiers
- public claims satisfy the configured evidence/review threshold
- unresolved and rejected claims are excluded from canonical data
- source records include license and provenance metadata
- editorial prose satisfies citation-coverage requirements
- validation checks pass
- known limitations are documented
- the release manifest records counts and source versions/snapshots

## Release manifest

Each stable release should record at least:

- dataset version
- schema version
- release date
- entity counts by type/status
- claim counts by predicate/status/evidence grade
- editorial record counts
- unresolved/rejected counts where published for transparency
- source snapshot/version identifiers
- validation summary
- known limitations
- previous release identifier

## Canonical vs review data

Canonical release files contain only records eligible for public consumption.

The `review/` directory may contain deliberately published review metadata, unresolved cases, or correction records when doing so improves transparency, but it must be clearly separated from canonical data.

## Stability

Once a stable entity identifier or claim identifier has been published, it should not be casually reassigned. Corrections should update or supersede records while preserving release history.

## Pre-release data

Until a versioned release explicitly declares itself stable, repository contents should be treated as development/release-candidate material rather than a finalized research dataset.
