"""Reference resolution and evidence retrieval helpers."""

from __future__ import annotations

import re
from typing import Any

from scripts.evid_001a.loaders import DataStore

LOCATOR_RE = re.compile(r"^([1-4]\s)?[A-Za-z]+\s+\d+:\d+(-\d+)?$")


def _entity_id(record: dict[str, Any]) -> str | None:
    for key in ("id", "person_id", "group_id", "place_id", "event_id", "entity_id"):
        if key in record and record[key]:
            return str(record[key])
    return None


def _entity_name(record: dict[str, Any]) -> str:
    for key in ("display_name", "name", "canonical_name", "label"):
        if key in record and record[key]:
            return str(record[key])
    return ""


def _matches_pattern(name: str, patterns: list[str]) -> bool:
    lower = name.lower()
    return any(p.lower() in lower for p in patterns)


def resolve_entity_ids(
    store: DataStore,
    *,
    person_ids: list[str],
    group_ids: list[str],
    place_ids: list[str],
    event_ids: list[str],
    person_patterns: list[str],
    group_patterns: list[str],
) -> dict[str, Any]:
    """Resolve canonical IDs and collect unresolved references."""

    resolved: dict[str, list[dict[str, Any]]] = {
        "people": [],
        "groups": [],
        "places": [],
        "events": [],
    }
    unresolved: list[dict[str, str]] = []

    id_sets = {
        "people": (store.people, person_ids, person_patterns, "person_id"),
        "groups": (store.groups, group_ids, group_patterns, "group_id"),
        "places": (store.places, place_ids, [], "place_id"),
        "events": (store.events, event_ids, [], "event_id"),
    }

    for kind, (records, explicit_ids, patterns, id_key) in id_sets.items():
        by_id = {str(_entity_id(r)): r for r in records if _entity_id(r)}
        seen: set[str] = set()

        for eid in explicit_ids:
            if eid in by_id:
                resolved[kind].append(by_id[eid])
                seen.add(eid)
            else:
                unresolved.append({"type": id_key, "reference": eid, "reason": "not_in_registry"})

        if patterns and records:
            for record in records:
                eid = _entity_id(record)
                name = _entity_name(record)
                if eid and eid not in seen and _matches_pattern(name, patterns):
                    resolved[kind].append(record)
                    seen.add(eid)

    return {"resolved_entities": resolved, "unresolved_entity_references": unresolved}


def filter_mentions(
    store: DataStore,
    entity_ids: set[str],
    name_patterns: list[str] | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for mention in store.mentions:
        mid = str(mention.get("entity_id", mention.get("person_id", mention.get("group_id", ""))))
        text = str(mention.get("surface_text", mention.get("text", "")))
        if mid in entity_ids:
            results.append(mention)
        elif name_patterns and _matches_pattern(text, name_patterns):
            results.append(mention)
    return sorted(results, key=lambda m: (m.get("locator", ""), m.get("evidence_id", "")))


def filter_annotations(
    store: DataStore,
    entity_ids: set[str],
    kinds: list[str] | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for ann in store.annotations:
        eid = str(ann.get("entity_id", ann.get("person_id", "")))
        kind = str(ann.get("kind", ann.get("annotation_kind", "")))
        if eid not in entity_ids:
            continue
        if kinds and kind not in kinds:
            continue
        results.append(ann)
    return sorted(results, key=lambda a: (a.get("locator", ""), a.get("evidence_id", "")))


def filter_relationships(
    store: DataStore,
    entity_ids: set[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for rel in store.relationships:
        subj = str(rel.get("subject_id", rel.get("from_id", "")))
        obj = str(rel.get("object_id", rel.get("to_id", "")))
        if subj in entity_ids or obj in entity_ids:
            results.append(rel)
    return sorted(results, key=lambda r: (r.get("predicate", ""), r.get("subject_id", "")))


def filter_005c_proposals(
    store: DataStore,
    entity_ids: set[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for prop in store.proposals_005c:
        subj = str(prop.get("subject_id", prop.get("from_id", "")))
        obj = str(prop.get("object_id", prop.get("to_id", "")))
        if subj in entity_ids or obj in entity_ids:
            results.append(prop)
    return sorted(results, key=lambda p: (p.get("proposal_id", ""), p.get("predicate", "")))


def filter_005d_findings(
    store: DataStore,
    entity_ids: set[str],
    case_keywords: list[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for finding in store.findings_005d:
        text = json_dumps_safe(finding).lower()
        entity_hit = any(eid.lower() in text for eid in entity_ids)
        keyword_hit = any(kw.lower() in text for kw in case_keywords)
        if entity_hit or keyword_hit:
            tagged = dict(finding)
            tagged["_advisory_label"] = "005D advisory finding"
            results.append(tagged)
    return sorted(results, key=lambda f: f.get("finding_id", ""))


def filter_chronology(
    store: DataStore,
    entity_ids: set[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for entry in store.chronology:
        text = json_dumps_safe(entry)
        if any(eid in text for eid in entity_ids):
            results.append(entry)
    return sorted(results, key=lambda c: c.get("chronology_id", c.get("locator", "")))


def filter_group_occurrences(
    store: DataStore,
    group_ids: set[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for occ in store.group_occurrences:
        gid = str(occ.get("group_id", ""))
        if gid in group_ids:
            results.append(occ)
    return sorted(results, key=lambda o: (o.get("locator", ""), o.get("group_id", "")))


def retrieve_scripture_ranges(
    store: DataStore,
    locators: list[str],
    context_ranges: list[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Retrieve scripture text for locators from frozen corpus."""

    corpus = store.scripture_corpus
    verses: dict[str, str] = {}
    if isinstance(corpus, dict):
        verses = corpus.get("verses", corpus.get("passages", {}))

    all_locators = sorted(set(locators + (context_ranges or [])))
    evidence: list[dict[str, Any]] = []
    unresolved: list[dict[str, str]] = []

    for locator in all_locators:
        text = verses.get(locator)
        if text:
            evidence.append({"locator": locator, "text": text, "source": "scripture-corpus"})
        else:
            unresolved.append({"type": "verse_locator", "reference": locator, "reason": "not_in_corpus"})

    return evidence, unresolved


def retrieve_reynolds(
    store: DataStore,
    keywords: list[str],
    entity_names: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    corpus = store.reynolds_corpus
    passages: list[dict[str, Any]] = []
    if isinstance(corpus, dict):
        for entry in corpus.get("passages", corpus.get("entries", [])):
            text = str(entry.get("text", ""))
            title = str(entry.get("title", entry.get("section", "")))
            combined = f"{title} {text}".lower()
            if any(kw.lower() in combined for kw in keywords + entity_names):
                passages.append(entry)

    passages.sort(key=lambda p: (p.get("source_id", ""), p.get("locator", "")))

    unresolved: list[dict[str, str]] = []
    if not passages and keywords:
        unresolved.append(
            {
                "type": "reynolds_corpus",
                "reference": "|".join(keywords[:5]),
                "reason": "no_matching_passages_or_corpus_missing",
            }
        )
    return passages, unresolved


def filter_forensic_findings(
    store: DataStore,
    keywords: list[str],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for report in store.forensic_reports():
        content = report.get("content", {})
        text = json_dumps_safe(content).lower()
        if any(kw.lower() in text for kw in keywords):
            results.append(report)
    return sorted(results, key=lambda r: r.get("report_path", ""))


def select_event_place_clusters(
    store: DataStore,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Select highest-impact Event→Place proposal clusters by proposal count."""

    place_predicates = {"at", "located_at", "event_at", "took_place_at", "place"}
    proposals = [
        p for p in store.proposals_005c if str(p.get("predicate", "")).lower() in place_predicates
    ]
    clusters: dict[str, dict[str, Any]] = {}
    for prop in proposals:
        event_id = str(prop.get("subject_id", prop.get("event_id", "")))
        place_id = str(prop.get("object_id", prop.get("place_id", "")))
        key = f"{event_id}|{place_id}|{prop.get('predicate', '')}"
        if key not in clusters:
            clusters[key] = {
                "event_id": event_id,
                "place_id": place_id,
                "predicate": prop.get("predicate", ""),
                "proposals": [],
            }
        clusters[key]["proposals"].append(prop)

    ranked = sorted(clusters.values(), key=lambda c: len(c["proposals"]), reverse=True)
    return ranked[:limit]


def json_dumps_safe(obj: Any) -> str:
    import json

    return json.dumps(obj, sort_keys=True, default=str)


def collect_entity_ids(resolved_entities: dict[str, list[dict[str, Any]]]) -> set[str]:
    ids: set[str] = set()
    for records in resolved_entities.values():
        for record in records:
            eid = _entity_id(record)
            if eid:
                ids.add(eid)
    return ids


def summarize_resolution(
    resolved_count: int,
    all_unresolved: list[dict[str, str]],
) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    for ref in all_unresolved:
        by_type[ref.get("type", "unknown")] = by_type.get(ref.get("type", "unknown"), 0) + 1
    total = resolved_count + len(all_unresolved)
    return {
        "total_references": total,
        "resolved": resolved_count,
        "unresolved": len(all_unresolved),
        "unresolved_by_type": dict(sorted(by_type.items())),
    }
