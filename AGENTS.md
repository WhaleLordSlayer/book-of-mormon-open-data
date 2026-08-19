# AGENTS.md

## Cursor Cloud specific instructions

### What this repository is

Book of Mormon Open Data is a **citation-first dataset + documentation repository**, not a
runnable application. It currently contains only Markdown docs and one JSON file
(`manifest.json`). The extraction/generation pipeline is intentionally kept private and is
**not** in this repo (see `README.md` and `docs/METHODOLOGY.md`).

There is deliberately **no application server, no build system, no test suite, no linter
config, and no CI**. Do not add speculative tooling (bundlers, frameworks, schema
validators) unless a task explicitly calls for it — the whole point is that the public data
is independent of any one application.

### Toolchain (already present, nothing to install)

The base image already provides everything needed to work on this repo: `python3`,
`node`/`npm`, `jq`, and `git`. The environment update script is intentionally a no-op
because there are no dependency manifests (`package.json`, `requirements.txt`, etc.) to
install. If a future change introduces a real manifest, add its install command to the
update script then.

### How to "lint / test / build / run"

Because there is no code, the meaningful checks are on the data itself:

- Validate all tracked JSON is well-formed:
  `for f in $(git ls-files '*.json'); do python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" && echo "ok $f"; done`
- Inspect a JSON file: `jq . manifest.json`

### Data model (for authoring records)

The intended provenance trace, documented in `docs/DATA_MODEL.md`, is:

```
source -> evidence -> claim -> review decision -> published fact -> editorial prose
```

Canonical records for each stage live in the correspondingly named top-level directories
(`sources/`, `evidence/`, `claims/`, `entities/`, `editorial/`, `review/`, `releases/`),
which currently hold only placeholder `README.md` files. Machine-readable JSON Schemas are
planned for `schema/` but do not exist yet, so validate records structurally by hand /
against `docs/DATA_MODEL.md` until schemas land. When authoring or validating data, ensure
every editorial factual sentence resolves to an accepted claim, every claim resolves to
evidence + entities, and every evidence record resolves to a licensed source.
