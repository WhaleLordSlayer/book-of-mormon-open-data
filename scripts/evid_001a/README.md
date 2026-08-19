# EVID-001A — Priority Evidence Dossiers

Deterministic evidence dossier generation for PM-ready semantic edge-case review.

## Usage

```bash
PYTHONPATH=. python3 scripts/evid_001a/generate_dossiers.py --project-root .
```

When run inside `cultivate-data-forge` at `projects/book-of-mormon-open-data` with production
sources present, the generator resolves canonical IDs, scripture ranges, Reynolds passages,
005C proposals, and 005D advisory findings into paired JSON + Markdown dossiers.

## Outputs

- `workspace/intermediate/evid-001a-priority-dossiers/index.json`
- `workspace/intermediate/evid-001a-priority-dossiers/dossiers/<case-id>.json`
- `workspace/intermediate/evid-001a-priority-dossiers/dossiers/<case-id>.md`
- `workspace/intermediate/evid-001a-priority-dossiers/deferred-edge-case-candidates.json`
- `workspace/reports/evid-001a-priority-dossiers-summary.md`

## Tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=. python3 -m pytest tests/test_evid_001a.py -v
python3 -m ruff check scripts tests
```

## Expected source layout

The generator reads from (does not write):

- `production/entities/*.json`
- `production/evidence/*.json`
- `production/sources/scripture-corpus.json`
- `production/sources/reynolds-corpus.json`
- `workspace/intermediate/005c-relationship-candidates/proposals.json`
- `workspace/intermediate/005d-semantic-audit/findings.json`

## Data access note

This public repository skeleton does not include cultivate-data-forge production data.
Regenerate against the private pipeline checkout (base branch `feature/005d-overnight-semantic-audit`,
commit `deadb35244776d4ded4f72be1a997660429a4fe4`) to populate evidence fields.
