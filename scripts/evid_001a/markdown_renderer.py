"""Render dossier Markdown from JSON structure."""

from __future__ import annotations

from typing import Any


def render_dossier_markdown(dossier: dict[str, Any]) -> str:
    lines: list[str] = [
        f"# {dossier['title']}",
        "",
        f"**Dossier ID:** `{dossier['dossier_id']}`",
        "",
        "> Evidence preparation only. No semantic adjudication performed.",
        "",
    ]

    if dossier.get("generation_notes"):
        lines.extend(["## Generation notes", "", dossier["generation_notes"], ""])

    lines.extend(["## Affected release goals", ""])
    for goal in dossier.get("affected_release_goals", []):
        lines.append(f"- {goal}")
    lines.append("")

    lines.extend(["## Canonical entity IDs", ""])
    for kind, ids in dossier.get("canonical_entity_ids", {}).items():
        if ids:
            lines.append(f"### {kind.title()}")
            for eid in ids:
                lines.append(f"- `{eid}`")
            lines.append("")

    lines.extend(["## Canonical display names", ""])
    for kind, names in dossier.get("canonical_display_names", {}).items():
        if names:
            lines.append(f"- **{kind}:** {', '.join(names)}")
    lines.append("")

    _section_entities(lines, "Current canonical state", dossier.get("current_canonical_state", {}))
    _section_list(lines, "Scripture locators requested", dossier.get("scripture_locators_requested", []))
    _section_evidence(lines, "Scripture evidence", dossier.get("scripture_evidence", []))
    _section_evidence(lines, "Reynolds evidence", dossier.get("reynolds_evidence", []), title_key="title")
    _section_json_block(lines, "Chronology facts", dossier.get("chronology_facts", []))
    _section_json_block(lines, "Current relationships", dossier.get("current_relationships", []))
    _section_json_block(lines, "005C proposals", dossier.get("005c_proposals", []))
    _section_json_block(lines, "005D findings (advisory)", dossier.get("005d_findings_advisory", []))
    _section_json_block(lines, "Earlier forensic findings", dossier.get("earlier_forensic_findings", []))
    _section_json_block(lines, "Exact mentions", dossier.get("exact_mentions", []))
    _section_json_block(lines, "Annotations", dossier.get("annotations", []))
    _section_json_block(lines, "Group occurrences", dossier.get("group_occurrences", []))

    if dossier.get("evidence_separation"):
        lines.extend(["## Evidence separation (Mormon)", ""])
        for key, items in dossier["evidence_separation"].items():
            lines.append(f"### {key.replace('_', ' ').title()} ({len(items)})")
            lines.append("")
        lines.append("")

    if dossier.get("event_place_clusters"):
        lines.extend(["## Event→Place high-impact clusters", ""])
        for cluster in dossier["event_place_clusters"]:
            lines.append(
                f"- Event `{cluster.get('event_id')}` → Place `{cluster.get('place_id')}` "
                f"({cluster.get('predicate')}) — {len(cluster.get('proposals', []))} proposals"
            )
        lines.append("")

    if dossier.get("contradictions_and_tensions"):
        lines.extend(["## Contradictions / tensions (mechanical)", ""])
        for t in dossier["contradictions_and_tensions"]:
            lines.append(f"- **{t.get('tension_id')}:** {t.get('description')}")
        lines.append("")

    if dossier.get("unresolved_evidence_references"):
        lines.extend(["## Unresolved evidence references", ""])
        for ref in dossier["unresolved_evidence_references"]:
            lines.append(f"- `{ref.get('type')}` `{ref.get('reference')}` — {ref.get('reason')}")
        lines.append("")

    lines.extend(["## PM questions", ""])
    for q in dossier.get("pm_questions", []):
        lines.append(f"- {q}")
    lines.append("")

    resolution = dossier.get("evidence_resolution", {})
    lines.extend(
        [
            "## Evidence resolution summary",
            "",
            f"- Total references tracked: {resolution.get('total_references', 0)}",
            f"- Unresolved: {resolution.get('unresolved', 0)}",
            "",
        ]
    )
    return "\n".join(lines)


def _section_list(lines: list[str], title: str, items: list[str]) -> None:
    if not items:
        return
    lines.extend([f"## {title}", ""])
    for item in items:
        lines.append(f"- `{item}`")
    lines.append("")


def _section_evidence(
    lines: list[str],
    title: str,
    items: list[dict[str, Any]],
    title_key: str = "locator",
) -> None:
    if not items:
        return
    lines.extend([f"## {title}", ""])
    for item in items:
        label = item.get(title_key, item.get("source_id", "entry"))
        text = item.get("text", "")
        lines.append(f"### {label}")
        if text:
            lines.append("")
            lines.append(f"> {text}")
        lines.append("")


def _section_entities(lines: list[str], title: str, state: dict[str, Any]) -> None:
    if not any(state.values()):
        return
    lines.extend([f"## {title}", ""])
    for kind, records in state.items():
        if not records:
            continue
        lines.append(f"### {kind.title()}")
        for rec in records:
            lines.append(f"- `{rec.get('id')}` — {rec.get('display_name')} (status: {rec.get('status')})")
        lines.append("")


def _section_json_block(lines: list[str], title: str, items: list[Any]) -> None:
    if not items:
        return
    summary = f"*{len(items)} record(s) — see JSON dossier for full machine-readable content.*"
    lines.extend([f"## {title}", "", summary, ""])
