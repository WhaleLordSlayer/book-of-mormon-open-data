"""Load project source data for dossier assembly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.evid_001a.config import DataPaths


def _load_json(path: Path) -> tuple[Any | None, str | None]:
    if not path.exists():
        return None, f"file_not_found:{path}"
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh), None
    except json.JSONDecodeError as exc:
        return None, f"json_decode_error:{path}:{exc}"


class DataStore:
    """Lazy loader for all permitted evidence sources."""

    def __init__(self, paths: DataPaths) -> None:
        self.paths = paths
        self._cache: dict[str, Any] = {}
        self._load_errors: dict[str, str] = {}

    def _get(self, key: str, path: Path) -> Any:
        if key not in self._cache:
            data, err = _load_json(path)
            self._cache[key] = data if data is not None else []
            if err:
                self._load_errors[key] = err
        return self._cache[key]

    @property
    def load_errors(self) -> dict[str, str]:
        return dict(self._load_errors)

    @property
    def people(self) -> list[dict[str, Any]]:
        return self._get("people", self.paths.people_registry)

    @property
    def groups(self) -> list[dict[str, Any]]:
        return self._get("groups", self.paths.groups_registry)

    @property
    def places(self) -> list[dict[str, Any]]:
        return self._get("places", self.paths.places_registry)

    @property
    def events(self) -> list[dict[str, Any]]:
        return self._get("events", self.paths.events_registry)

    @property
    def relationships(self) -> list[dict[str, Any]]:
        return self._get("relationships", self.paths.relationships_registry)

    @property
    def mentions(self) -> list[dict[str, Any]]:
        return self._get("mentions", self.paths.mentions_table)

    @property
    def annotations(self) -> list[dict[str, Any]]:
        return self._get("annotations", self.paths.annotations_table)

    @property
    def chronology(self) -> list[dict[str, Any]]:
        return self._get("chronology", self.paths.chronology_artifacts)

    @property
    def scripture_corpus(self) -> dict[str, Any]:
        return self._get("scripture", self.paths.scripture_corpus)

    @property
    def reynolds_corpus(self) -> dict[str, Any]:
        return self._get("reynolds", self.paths.reynolds_corpus)

    @property
    def proposals_005c(self) -> list[dict[str, Any]]:
        return self._get("005c", self.paths.proposals_005c)

    @property
    def findings_005d(self) -> list[dict[str, Any]]:
        return self._get("005d", self.paths.findings_005d)

    @property
    def group_occurrences(self) -> list[dict[str, Any]]:
        return self._get("group_occurrences", self.paths.group_occurrences)

    @property
    def evidence_provenance(self) -> list[dict[str, Any]]:
        return self._get("provenance", self.paths.evidence_provenance)

    def forensic_reports(self) -> list[dict[str, Any]]:
        reports: list[dict[str, Any]] = []
        report_dir = self.paths.forensic_reports_dir
        if not report_dir.exists():
            self._load_errors["forensic_reports"] = f"dir_not_found:{report_dir}"
            return reports
        for path in sorted(report_dir.glob("*.json")):
            data, err = _load_json(path)
            if data is not None:
                reports.append({"report_path": str(path), "content": data})
            elif err:
                self._load_errors[f"forensic:{path.name}"] = err
        return reports
