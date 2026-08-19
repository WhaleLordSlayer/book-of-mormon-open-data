"""Configuration for EVID-001A dossier generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DataPaths:
    """Expected source data locations (cultivate-data-forge layout)."""

    project_root: Path
    production_dir: Path
    people_registry: Path
    groups_registry: Path
    places_registry: Path
    events_registry: Path
    relationships_registry: Path
    mentions_table: Path
    annotations_table: Path
    chronology_artifacts: Path
    scripture_corpus: Path
    reynolds_corpus: Path
    proposals_005c: Path
    findings_005d: Path
    forensic_reports_dir: Path
    group_occurrences: Path
    evidence_provenance: Path

    @classmethod
    def from_project_root(cls, project_root: Path) -> DataPaths:
        production = project_root / "production"
        workspace = project_root / "workspace"
        return cls(
            project_root=project_root,
            production_dir=production,
            people_registry=production / "entities" / "people.json",
            groups_registry=production / "entities" / "groups.json",
            places_registry=production / "entities" / "places.json",
            events_registry=production / "entities" / "events.json",
            relationships_registry=production / "relationships" / "canonical.json",
            mentions_table=production / "evidence" / "exact-mentions.json",
            annotations_table=production / "evidence" / "annotations.json",
            chronology_artifacts=workspace / "intermediate" / "chronology" / "artifacts.json",
            scripture_corpus=production / "sources" / "scripture-corpus.json",
            reynolds_corpus=production / "sources" / "reynolds-corpus.json",
            proposals_005c=workspace / "intermediate" / "005c-relationship-candidates" / "proposals.json",
            findings_005d=workspace / "intermediate" / "005d-semantic-audit" / "findings.json",
            forensic_reports_dir=workspace / "reports" / "forensic",
            group_occurrences=production / "evidence" / "group-occurrences.json",
            evidence_provenance=production / "evidence" / "provenance.json",
        )


@dataclass(frozen=True)
class OutputPaths:
    """Dossier output locations."""

    dossier_dir: Path
    index_json: Path
    summary_md: Path
    deferred_candidates: Path

    @classmethod
    def from_project_root(cls, project_root: Path) -> OutputPaths:
        base = project_root / "workspace" / "intermediate" / "evid-001a-priority-dossiers"
        return cls(
            dossier_dir=base / "dossiers",
            index_json=base / "index.json",
            summary_md=project_root / "workspace" / "reports" / "evid-001a-priority-dossiers-summary.md",
            deferred_candidates=base / "deferred-edge-case-candidates.json",
        )


@dataclass
class DossierSpec:
    """Specification for one evidence dossier."""

    case_id: str
    title: str
    release_goals: list[str] = field(default_factory=list)
    person_ids: list[str] = field(default_factory=list)
    group_ids: list[str] = field(default_factory=list)
    place_ids: list[str] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)
    person_name_patterns: list[str] = field(default_factory=list)
    group_name_patterns: list[str] = field(default_factory=list)
    scripture_ranges: list[str] = field(default_factory=list)
    pm_questions: list[str] = field(default_factory=list)
    notes: str = ""


DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[2]
