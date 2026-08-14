# Review Policy

The project distinguishes automated generation, automated verification, model review, and human review. These are different kinds of evidence and must not be conflated.

## Review principles

1. **Generation is not verification.** A model or script that proposes a fact does not approve that fact.
2. **A source citation must support the actual claim.** Nearby or topically related scripture is not sufficient.
3. **Ambiguity is explicit.** Same-name people, uncertain chronology, figurative kinship, and inferred relationships should be marked unresolved rather than silently normalized.
4. **Independent review matters.** Where a model writes a summary or biography, the same generation event must not count as independent approval.
5. **Missing data is preferable to undocumented certainty.**

## Intended claim statuses

The exact machine-readable enum will be frozen with the schema, but the public semantics should distinguish:

- `candidate` — proposed but not accepted
- `scripture_verified` — directly supported by deterministic or reviewed scripture evidence
- `corroborated` — supported by independent external structured evidence in addition to primary evidence
- `model_reviewed` — reviewed by a separate model pass, but not human approved
- `human_reviewed` — reviewed by a person
- `production_approved` — eligible for canonical release
- `rejected` — reviewed and not accepted
- `unresolved` — insufficient evidence or unresolved ambiguity

## Editorial prose

Summaries and biographies require a stricter review than simple structured relationships because prose can introduce unsupported implications.

Before release, editorial content should pass:

- sentence/claim citation coverage check
- unsupported factual clause audit
- identity/disambiguation audit
- chronology audit where dates are used
- source-license/provenance check
- independent review appropriate to the release tier

## Corrections

Corrections should preserve an auditable history in versioned releases. A correction should identify:

- affected entity/claim/editorial record
- previous value
- corrected value
- supporting evidence
- reason for change
- release in which the correction appeared
