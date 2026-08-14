# Methodology

Book of Mormon Open Data is produced with a citation-first workflow. The internal generation pipeline is private; this document describes the public methodology and quality expectations rather than implementation details.

## 1. Candidate discovery

Potential entities and facts may be proposed from permitted structured sources, deterministic extraction, or editorial research.

A candidate is not a published fact.

## 2. Identity resolution

People with shared or ambiguous names are assigned project-owned canonical identities. External IDs such as Wikidata QIDs are pinned only after identity review and are stored as external identifiers.

Name-only matching is insufficient for ambiguous figures such as multiple people named Nephi, Helaman, Ammon, Alma, or Moroni.

## 3. Atomic claims

Facts are normalized into atomic claims so each assertion can be independently cited, accepted, rejected, or corrected.

## 4. Primary-source verification

Where practical, claims are checked against the Book of Mormon scripture corpus. Evidence is stored as canonical scripture references and linked to the claim.

The methodology must distinguish literal genealogy from forms of address, ancestral language, figurative kinship, titles, quoted speech, and same-name collisions.

## 5. External corroboration

Wikidata structured statements may be used to propose or corroborate claims. Wikidata alone does not automatically make a claim canonical.

The project preserves enough Wikidata provenance to identify the originating entity/property/statement and retrieval snapshot. Wikidata prose descriptions are not used as biographies.

## 6. Review

Automated and model-based review can reduce the number of cases requiring manual attention, but model agreement is not treated as human approval.

Ambiguous or weakly supported claims remain unresolved or rejected until they satisfy release policy.

## 7. Editorial prose

Summaries and biographies are written from accepted claims rather than copied from source prose.

The target release standard requires factual sentences to identify the accepted claims that support them. Generated prose receives an additional factual-support audit before production approval.

## 8. Release build

Only records that satisfy the release policy are copied into the clean public dataset. Internal model logs, caches, experiments, extraction scripts, rejected intermediate files, and private orchestration code are not part of this repository.

## 9. Reproducibility and transparency

The generation code is private, but the public release should preserve enough provenance to independently evaluate the factual content:

- stable entity and claim identifiers
- source records and licenses
- scripture evidence
- external statement identifiers
- review status
- release manifest and validation counts
- known limitations

The public dataset should never require trust in an undocumented black-box decision.
