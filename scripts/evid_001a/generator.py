"""Generate evidence dossiers from project sources."""

from __future__ import annotations

import json
from typing import Any

from scripts.evid_001a.config import DataPaths, DossierSpec, OutputPaths
from scripts.evid_001a.dossier_specs import DEFERRED_EDGE_CASE_CANDIDATES, all_dossier_specs
from scripts.evid_001a.loaders import DataStore
from scripts.evid_001a.markdown_renderer import render_dossier_markdown
from scripts.evid_001a.resolver import (
    collect_entity_ids,
    filter_005c_proposals,
    filter_005d_findings,
    filter_annotations,
    filter_chronology,
    filter_forensic_findings,
    filter_group_occurrences,
    filter_mentions,
    filter_relationships,
    resolve_entity_ids,
    retrieve_reynolds,
    retrieve_scripture_ranges,
    select_event_place_clusters,
    summarize_resolution,
)


def _display_names(resolved_entities: dict[str, list[dict[str, Any]]]) -> dict[str, list[str]]:
    names: dict[str, list[str]] = {}
    for kind, records in resolved_entities.items():
        kind_names: list[str] = []
        for record in records:
            for key in ("display_name", "name", "canonical_name", "label"):
                if record.get(key):
                    kind_names.append(str(record[key]))
                    break
        names[kind] = sorted(set(kind_names))
    return names


def _canonical_state(resolved_entities: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for kind, records in resolved_entities.items():
        state[kind] = [
            {
                "id": r.get("id", r.get(f"{kind[:-1]}_id", "")),
                "display_name": r.get("display_name", r.get("name", "")),
                "status": r.get("status", r.get("canonical_status", "unknown")),
                "notes": r.get("notes", ""),
            }
            for r in records
        ]
    return state


def _split_mormon_evidence(
    mentions: list[dict[str, Any]],
    annotations: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Mechanically separate narrator/editor vs historical buckets when kinds exist."""

    narrator_kinds = {"narrator", "editor", "compiler", "abridger", "speaker_narrator"}
    historical_kinds = {"historical_actor", "participant", "speaker", "commander", "prophet"}

    narrator_mentions: list[dict[str, Any]] = []
    historical_mentions: list[dict[str, Any]] = []
    unclassified_mentions: list[dict[str, Any]] = []

    for m in mentions:
        kind = str(m.get("mention_kind", m.get("role", ""))).lower()
        if kind in narrator_kinds or "narrat" in kind or "editor" in kind or "abridg" in kind:
            narrator_mentions.append(m)
        elif kind in historical_kinds or "histor" in kind:
            historical_mentions.append(m)
        else:
            unclassified_mentions.append(m)

    narrator_annotations = [
        a
        for a in annotations
        if str(a.get("kind", a.get("annotation_kind", ""))).lower()
        in narrator_kinds | {"narrator", "editor", "abridger", "compiler"}
    ]
    historical_annotations = [
        a
        for a in annotations
        if str(a.get("kind", a.get("annotation_kind", ""))).lower() in historical_kinds
    ]

    return {
        "narrator_editor_mentions": narrator_mentions,
        "historical_actor_mentions": historical_mentions,
        "unclassified_mentions": unclassified_mentions,
        "narrator_editor_annotations": narrator_annotations,
        "historical_actor_annotations": historical_annotations,
    }


def build_dossier(store: DataStore, spec: DossierSpec) -> dict[str, Any]:
    """Assemble one dossier without making semantic adjudication decisions."""

    resolution = resolve_entity_ids(
        store,
        person_ids=spec.person_ids,
        group_ids=spec.group_ids,
        place_ids=spec.place_ids,
        event_ids=spec.event_ids,
        person_patterns=spec.person_name_patterns,
        group_patterns=spec.group_name_patterns,
    )
    entity_ids = collect_entity_ids(resolution["resolved_entities"])
    keywords = spec.person_name_patterns + spec.group_name_patterns

    mentions = filter_mentions(store, entity_ids, spec.person_name_patterns + spec.group_name_patterns)
    annotations = filter_annotations(store, entity_ids)
    relationships = filter_relationships(store, entity_ids)
    proposals_005c = filter_005c_proposals(store, entity_ids)
    findings_005d = filter_005d_findings(store, entity_ids, keywords)
    chronology = filter_chronology(store, entity_ids)
    group_occurrences = filter_group_occurrences(store, entity_ids)
    forensic = filter_forensic_findings(store, keywords)

    mention_locators = [str(m.get("locator", "")) for m in mentions if m.get("locator")]
    scripture, scripture_unresolved = retrieve_scripture_ranges(
        store, spec.scripture_ranges + mention_locators, spec.scripture_ranges
    )
    reynolds, reynolds_unresolved = retrieve_reynolds(
        store, keywords, _display_names(resolution["resolved_entities"]).get("people", [])
    )

    all_unresolved: list[dict[str, str]] = list(resolution["unresolved_entity_references"])
    all_unresolved.extend(scripture_unresolved)
    all_unresolved.extend(reynolds_unresolved)

    if not store.people and spec.person_name_patterns:
        all_unresolved.append(
            {
                "type": "people_registry",
                "reference": str(store.paths.people_registry),
                "reason": "registry_unavailable",
            }
        )
    if not store.groups and spec.group_name_patterns:
        all_unresolved.append(
            {
                "type": "groups_registry",
                "reference": str(store.paths.groups_registry),
                "reason": "registry_unavailable",
            }
        )

    resolved_count = (
        len(mentions)
        + len(annotations)
        + len(relationships)
        + len(proposals_005c)
        + len(scripture)
        + len(reynolds)
        + sum(len(v) for v in resolution["resolved_entities"].values())
    )

    dossier: dict[str, Any] = {
        "dossier_id": spec.case_id,
        "title": spec.title,
        "affected_release_goals": spec.release_goals,
        "canonical_entity_ids": {
            "people": [r.get("id", r.get("person_id", "")) for r in resolution["resolved_entities"]["people"]],
            "groups": [r.get("id", r.get("group_id", "")) for r in resolution["resolved_entities"]["groups"]],
            "places": [r.get("id", r.get("place_id", "")) for r in resolution["resolved_entities"]["places"]],
            "events": [r.get("id", r.get("event_id", "")) for r in resolution["resolved_entities"]["events"]],
        },
        "canonical_display_names": _display_names(resolution["resolved_entities"]),
        "current_canonical_state": _canonical_state(resolution["resolved_entities"]),
        "scripture_evidence": scripture,
        "scripture_locators_requested": spec.scripture_ranges,
        "reynolds_evidence": reynolds,
        "chronology_facts": chronology,
        "current_relationships": relationships,
        "005c_proposals": proposals_005c,
        "005d_findings_advisory": findings_005d,
        "earlier_forensic_findings": forensic,
        "exact_mentions": mentions,
        "annotations": annotations,
        "group_occurrences": group_occurrences,
        "unresolved_evidence_references": sorted(
            all_unresolved, key=lambda x: (x.get("type", ""), x.get("reference", ""))
        ),
        "contradictions_and_tensions": _mechanical_tensions(spec, mentions, proposals_005c, scripture),
        "pm_questions": spec.pm_questions,
        "generation_notes": spec.notes,
        "evidence_resolution": summarize_resolution(resolved_count, all_unresolved),
    }

    if spec.case_id == "mormon-narrator-vs-historical-actor":
        dossier["evidence_separation"] = _split_mormon_evidence(mentions, annotations)

    if spec.case_id == "event-place-high-impact":
        clusters = select_event_place_clusters(store, limit=10)
        dossier["event_place_clusters"] = clusters
        dossier["005c_proposals"] = [
            p for cluster in clusters for p in cluster.get("proposals", [])
        ]
        if not clusters:
            all_unresolved.append(
                {
                    "type": "005c_proposals",
                    "reference": str(store.paths.proposals_005c),
                    "reason": "no_event_place_clusters_available",
                }
            )
            dossier["unresolved_evidence_references"] = sorted(
                all_unresolved, key=lambda x: (x.get("type", ""), x.get("reference", ""))
            )

    return dossier


def _mechanical_tensions(
    spec: DossierSpec,
    mentions: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
    scripture: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Surface mechanical tensions without semantic adjudication."""

    tensions: list[dict[str, str]] = []
    if spec.case_id == "stripling-warriors-count":
        count_tokens = ("2000", "2,000", "2060", "2,060")
        counts = [
            m
            for m in mentions
            if any(x in str(m.get("surface_text", m.get("text", ""))) for x in count_tokens)
        ]
        if len({str(c.get("locator", "")) for c in counts}) > 1:
            tensions.append(
                {
                    "tension_id": "membership-count-multiple-passages",
                    "description": (
                        "Multiple membership-count mentions present; "
                        "human judgment required on Group continuity."
                    ),
                }
            )
    if not scripture and spec.scripture_ranges:
        tensions.append(
            {
                "tension_id": "scripture-corpus-gap",
                "description": "Requested scripture ranges not available in frozen corpus loader.",
            }
        )
    if proposals and not mentions:
        tensions.append(
            {
                "tension_id": "proposals-without-mentions",
                "description": "005C proposals exist in spec scope but no exact mentions resolved.",
            }
        )
    return tensions


def generate_all(
    data_paths: DataPaths,
    output_paths: OutputPaths,
) -> dict[str, Any]:
    """Generate all dossiers, index, summary inputs, and deferred candidates."""

    store = DataStore(data_paths)
    output_paths.dossier_dir.mkdir(parents=True, exist_ok=True)
    output_paths.summary_md.parent.mkdir(parents=True, exist_ok=True)

    dossiers: list[dict[str, Any]] = []
    for spec in all_dossier_specs():
        dossier = build_dossier(store, spec)
        dossiers.append(dossier)

        json_path = output_paths.dossier_dir / f"{spec.case_id}.json"
        md_path = output_paths.dossier_dir / f"{spec.case_id}.md"
        with json_path.open("w", encoding="utf-8") as fh:
            json.dump(dossier, fh, indent=2, sort_keys=True)
            fh.write("\n")
        md_path.write_text(render_dossier_markdown(dossier), encoding="utf-8")

    index = _build_index(dossiers, store)
    with output_paths.index_json.open("w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with output_paths.deferred_candidates.open("w", encoding="utf-8") as fh:
        json.dump(
            {"deferred_edge_case_candidates": DEFERRED_EDGE_CASE_CANDIDATES},
            fh,
            indent=2,
            sort_keys=True,
        )
        fh.write("\n")

    summary = _build_summary_md(dossiers, index, output_paths, store)
    output_paths.summary_md.write_text(summary, encoding="utf-8")

    return {
        "dossier_count": len(dossiers),
        "index_path": str(output_paths.index_json),
        "summary_path": str(output_paths.summary_md),
        "load_errors": store.load_errors,
    }


def _build_index(dossiers: list[dict[str, Any]], store: DataStore) -> dict[str, Any]:
    total_scripture = sum(len(d.get("scripture_evidence", [])) for d in dossiers)
    total_reynolds = sum(len(d.get("reynolds_evidence", [])) for d in dossiers)
    total_005c = sum(len(d.get("005c_proposals", [])) for d in dossiers)
    total_unresolved = sum(len(d.get("unresolved_evidence_references", [])) for d in dossiers)

    coverage = []
    for d in dossiers:
        score = (
            len(d.get("scripture_evidence", []))
            + len(d.get("reynolds_evidence", []))
            + len(d.get("005c_proposals", []))
            + len(d.get("exact_mentions", []))
        )
        coverage.append(
            {
                "dossier_id": d["dossier_id"],
                "title": d["title"],
                "evidence_items": score,
                "unresolved_count": len(d.get("unresolved_evidence_references", [])),
                "json_path": f"workspace/intermediate/evid-001a-priority-dossiers/dossiers/{d['dossier_id']}.json",
                "md_path": f"workspace/intermediate/evid-001a-priority-dossiers/dossiers/{d['dossier_id']}.md",
            }
        )

    strong = sorted(
        [c for c in coverage if c["evidence_items"] >= 3 and c["unresolved_count"] <= 2],
        key=lambda x: x["dossier_id"],
    )
    missing = sorted(
        [c for c in coverage if c["evidence_items"] == 0],
        key=lambda x: x["dossier_id"],
    )

    return {
        "task_id": "EVID-001A",
        "dossiers_completed": len(dossiers),
        "entities_covered": {
            "people": sorted({pid for d in dossiers for pid in d["canonical_entity_ids"]["people"] if pid}),
            "groups": sorted({gid for d in dossiers for gid in d["canonical_entity_ids"]["groups"] if gid}),
            "places": sorted({pid for d in dossiers for pid in d["canonical_entity_ids"]["places"] if pid}),
            "events": sorted({eid for d in dossiers for eid in d["canonical_entity_ids"]["events"] if eid}),
        },
        "scripture_evidence_count": total_scripture,
        "reynolds_evidence_count": total_reynolds,
        "005c_proposals_represented": total_005c,
        "unresolved_references_total": total_unresolved,
        "dossiers": coverage,
        "strong_evidence_coverage": strong,
        "missing_evidence_dossiers": missing,
        "source_load_errors": store.load_errors,
        "base_data_availability": {
            "note": (
                "Generation run against configured project root; unresolved counts reflect "
                "missing cultivate-data-forge production sources when unavailable."
            ),
            "people_registry_loaded": bool(store.people),
            "groups_registry_loaded": bool(store.groups),
            "scripture_corpus_loaded": bool(store.scripture_corpus),
            "reynolds_corpus_loaded": bool(store.reynolds_corpus),
            "005c_proposals_loaded": bool(store.proposals_005c),
            "005d_findings_loaded": bool(store.findings_005d),
        },
    }


def _build_summary_md(
    dossiers: list[dict[str, Any]],
    index: dict[str, Any],
    output_paths: OutputPaths,
    store: DataStore,
) -> str:
    lines = [
        "# EVID-001A Priority Evidence Dossiers — Summary",
        "",
        "## Overview",
        "",
        f"- Dossiers completed: **{index['dossiers_completed']}**",
        f"- Scripture evidence items: **{index['scripture_evidence_count']}**",
        f"- Reynolds evidence items: **{index['reynolds_evidence_count']}**",
        f"- 005C proposals represented: **{index['005c_proposals_represented']}**",
        f"- Unresolved references: **{index['unresolved_references_total']}**",
        "",
        "## Entities covered",
        "",
        f"- People IDs resolved: {len(index['entities_covered']['people'])}",
        f"- Group IDs resolved: {len(index['entities_covered']['groups'])}",
        f"- Place IDs resolved: {len(index['entities_covered']['places'])}",
        f"- Event IDs resolved: {len(index['entities_covered']['events'])}",
        "",
        "## Source availability",
        "",
    ]
    for key, val in index["base_data_availability"].items():
        if key != "note":
            lines.append(f"- {key}: `{val}`")
    lines.extend(["", index["base_data_availability"]["note"], ""])
    if store.load_errors:
        lines.extend(["## Source load errors", ""])
        for src, err in sorted(store.load_errors.items()):
            lines.append(f"- `{src}`: {err}")
        lines.append("")

    lines.extend(["## Dossiers with strong evidence coverage", ""])
    if index["strong_evidence_coverage"]:
        for item in index["strong_evidence_coverage"]:
            lines.append(f"- `{item['dossier_id']}` ({item['evidence_items']} items)")
    else:
        lines.append("- None at current source availability (all dossiers await production source data).")
    lines.extend(["", "## Dossiers with missing evidence", ""])
    if index["missing_evidence_dossiers"]:
        for item in index["missing_evidence_dossiers"]:
            lines.append(f"- `{item['dossier_id']}`")
    else:
        lines.append("- None fully empty; see per-dossier unresolved reference lists.")

    lines.extend(
        [
            "",
            "## Exact paths",
            "",
            f"- Index: `{output_paths.index_json}`",
            f"- Dossier directory: `{output_paths.dossier_dir}`",
            f"- Summary: `{output_paths.summary_md}`",
            f"- Deferred candidates: `{output_paths.deferred_candidates}`",
            "",
            "## Per-dossier index",
            "",
        ]
    )
    for item in index["dossiers"]:
        lines.append(
            f"- `{item['dossier_id']}` — unresolved: {item['unresolved_count']}, "
            f"[json]({item['json_path']}), [md]({item['md_path']})"
        )
    lines.append("")
    return "\n".join(lines)
